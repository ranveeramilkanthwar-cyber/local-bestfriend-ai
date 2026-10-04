"""
Fine-Tuning Script for Local Best Friend AI Companion
Utilizes Unsloth for ultra-efficient 4-bit QLoRA fine-tuning of Phi-3-mini-4k-instruct.
Automatically exports the fine-tuned model into quantized GGUF format (q4_k_m) for Ollama.
"""

import os
import json
import torch
from pathlib import Path

# Blackwell / RTX 50-series CUDA forward compatibility
os.environ["CUDA_MODULE_LOADING"] = "LAZY"
if "TORCH_CUDA_ARCH_LIST" not in os.environ:
    os.environ["TORCH_CUDA_ARCH_LIST"] = "12.0;9.0;8.9"

def format_prompts(batch, tokenizer):
    """Formats multi-turn conversations into the Phi-3 ChatML template."""
    formatted_texts = []
    for conv_item in batch["conversations"]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are the user's ultimate ride-or-die best friend. You think in English "
                    "using <thought>...</thought> tags, and then speak back in the user's exact "
                    "language and script (Hinglish, Marathish, Hindi, Marathi, or English). "
                    "Zero corporate speak, always authentic, loyal, witty, and supportive."
                )
            }
        ]
        for turn in conv_item:
            messages.append({"role": turn["role"], "content": turn["content"]})
        
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        formatted_texts.append(text)
    return {"text": formatted_texts}

def main():
    print("=" * 65)
    print(" Local Best Friend AI: 4-bit QLoRA Fine-Tuning Pipeline")
    print("=" * 65)

    base_dir = Path(__file__).resolve().parent
    dataset_file = base_dir / "dataset.json"

    if not dataset_file.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_file}")

    print(f"Loading dataset from: {dataset_file}")
    with open(dataset_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    print(f"Total multi-turn conversations: {len(raw_data)}")

    # Dual-Engine: Attempt Unsloth first; fallback to standard PEFT BitsAndBytes 4-bit
    use_unsloth = False
    try:
        from unsloth import FastLanguageModel, is_bfloat16_supported
        print("\n[Engine]: Unsloth detected, attempting FastLanguageModel initialization...")
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name="unsloth/Phi-3-mini-4k-instruct-bnb-4bit",
            max_seq_length=2048,
            load_in_4bit=True,
            dtype=None
        )
        model = FastLanguageModel.get_peft_model(
            model,
            r=16,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_alpha=16,
            lora_dropout=0,
            bias="none",
            use_gradient_checkpointing="unsloth",
            random_state=3407
        )
        use_unsloth = True
        print("[Engine]: Successfully initialized Unsloth 4-bit QLoRA engine!")
    except Exception as e:
        print(f"\n[Engine Notice]: Unsloth initialization encountered: {e}")
        print("[Engine]: Switching to Native HuggingFace + BitsAndBytes 4-bit QLoRA...")

        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

        model_id = "microsoft/Phi-3-mini-4k-instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        model = prepare_model_for_kbit_training(model)

        peft_config = LoraConfig(
            r=16,
            lora_alpha=16,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        model = get_peft_model(model, peft_config)
        print("[Engine]: Successfully initialized Native 4-bit QLoRA engine!")

    # Format training dataset
    formatted_texts = []
    for item in raw_data:
        res = format_prompts({"conversations": [item["conversations"]]}, tokenizer)
        formatted_texts.append(res["text"][0])

    print(f"\n[Dataset]: Formatted {len(formatted_texts)} conversations with Phi-3 ChatML template.")

    # 3. Setup Trainer
    print("\n[3/4] Configuring SFTTrainer & Optimizer...")
    from trl import SFTTrainer
    from transformers import TrainingArguments

    class SimpleDataset(torch.utils.data.Dataset):
        def __init__(self, texts):
            self.texts = texts
        def __len__(self):
            return len(self.texts)
        def __getitem__(self, idx):
            return {"text": self.texts[idx]}

    train_dataset = SimpleDataset(formatted_texts)

    training_args = TrainingArguments(
        output_dir="./lora_checkpoints",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,
        learning_rate=2e-4,
        fp16=True,
        bf16=False,
        logging_steps=1,
        optim="paged_adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="cosine",
        seed=3407,
        report_to="none"
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        dataset_text_field="text",
        max_seq_length=2048,
        packing=False,
        args=training_args
    )

    print("\nStarting QLoRA Fine-Tuning on RTX 5050...")
    trainer_stats = trainer.train()
    print(f"Training completed! Final Loss: {trainer_stats.training_loss:.4f}")

    # 4. Save & Automated GGUF Export
    print("\n[4/4] Saving fine-tuned LoRA adapters & exporting...")
    export_dir = base_dir / "Phi-3-BestFriend"
    export_dir.mkdir(parents=True, exist_ok=True)

    if use_unsloth:
        try:
            model.save_pretrained_gguf(
                str(export_dir),
                tokenizer,
                quantization_method="q4_k_m"
            )
            print(f"\nSUCCESS: GGUF model exported to: {export_dir}")
        except Exception as e:
            print(f"[Export Notice]: Direct GGUF export returned: {e}")
            model.save_pretrained_merged(str(base_dir / "Phi-3-BestFriend-Merged"), tokenizer, save_method="merged_16bit")
    else:
        model.save_pretrained(str(export_dir))
        tokenizer.save_pretrained(str(export_dir))
        print(f"\nSUCCESS: LoRA adapters saved to: {export_dir}")
        print("Ready for Ollama conversion or direct serving.")

    print("\n" + "=" * 65)
    print("Fine-tuning pipeline execution finished.")
    print("=" * 65)

if __name__ == "__main__":
    main()

