import sys
import shutil
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    print("=" * 60)
    print(" Local Best Friend AI: Environment & GPU Diagnostics")
    print("=" * 60)
    
    # 1. Python info
    print(f"Python Version : {sys.version.split()[0]} ({sys.executable})")
    
    # 2. PyTorch & CUDA Verification
    try:
        import torch
        print(f"PyTorch Version: {torch.__version__}")
        cuda_avail = torch.cuda.is_available()
        print(f"CUDA Available : {cuda_avail}")
        
        if cuda_avail:
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0)
            capability = torch.cuda.get_device_capability(0)
            total_vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            free_vram, _ = torch.cuda.mem_get_info(0)
            free_vram_gb = free_vram / (1024 ** 3)
            
            print(f"Device Count   : {device_count}", flush=True)
            print(f"GPU Name       : {device_name}", flush=True)
            print(f"Compute Cap.   : {capability[0]}.{capability[1]}", flush=True)
            print(f"Total VRAM     : {total_vram:.2f} GB", flush=True)
            print(f"Free VRAM      : {free_vram_gb:.2f} GB", flush=True)
        else:
            print("[WARNING] CUDA is not available. GPU acceleration will not function.", flush=True)
    except ImportError:
        print("[ERROR] PyTorch is not installed.", flush=True)
        return

    # 3. Fine-tuning Libraries Check
    print("-" * 60, flush=True)
    for pkg in ["transformers", "datasets", "trl", "peft", "accelerate", "bitsandbytes", "unsloth", "sentence_transformers"]:
        print(f"Checking {pkg}...", end=" ", flush=True)
        try:
            m = __import__(pkg)
            version = getattr(m, "__version__", "installed")
            print(f"OK (v{version})", flush=True)
        except Exception as e:
            print(f"ERROR ({e})", flush=True)

    # 4. Ollama CLI Check
    print("-" * 60)
    ollama_path = shutil.which("ollama")
    if ollama_path:
        print(f"Ollama CLI Found      : {ollama_path}")
        try:
            res = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=5)
            print(f"Ollama Version        : {res.stdout.strip() or res.stderr.strip()}")
        except Exception as e:
            print(f"Ollama Version Check  : Failed ({e})")
    else:
        print("Ollama CLI Found      : NOT FOUND in PATH")
        
    print("=" * 60)
    print("Diagnostics complete! Ready for QLoRA fine-tuning & Ollama deployment.")
    print("=" * 60)

if __name__ == "__main__":
    main()
