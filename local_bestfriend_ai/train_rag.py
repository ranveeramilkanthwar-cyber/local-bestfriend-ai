"""
RAG Training & Vector Indexing Script
Embeds all documents in data/rag_corpus.json, data/personal_notes.txt,
and data/conversational_rag_dataset.json into high-speed 384-d dense vector stores.
"""
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from pathlib import Path
from core.rag_engine import LocalRAGEngine

def main():
    print("=" * 70)
    print(" 🚀 Local Best Friend AI: Training & Indexing Conversational RAG")
    print("=" * 70)

    start_time = time.time()
    rag = LocalRAGEngine()

    print(f"📊 Knowledge Corpus Facts & Notes: {len(rag.knowledge_docs)}")
    print(f"💬 Conversational Message-Response Pairs: {len(rag.dialogues)}")
    print(f"📚 Total Combined RAG Documents: {len(rag.documents)}")
    
    print("\n[RAG Training] Building dense semantic vector embeddings...")
    rag.build_and_save_index()
    build_time = time.time() - start_time
    print(f"⚡ Indexing completed in {build_time:.2f} seconds!")

    # 1. Benchmark Factual Knowledge Retrieval
    print("\n" + "-" * 70)
    print(" 🔍 Benchmarking Factual Knowledge Retrieval:")
    print("-" * 70)
    fact_queries = [
        "gym bench press routine",
        "Goa trip plans",
        "what is my core tech stack",
        "creatine supplement benefits"
    ]
    for q in fact_queries:
        t0 = time.time()
        res = rag.retrieve(q, top_k=1)
        latency_ms = (time.time() - t0) * 1000
        print(f"\n[Query]: '{q}' ({latency_ms:.1f}ms)")
        if res:
            print(f"  {res.replace(chr(10), ' ')}")
        else:
            print("  (No match above threshold)")

    # 2. Benchmark Conversational Dialect Exemplar Retrieval
    print("\n" + "-" * 70)
    print(" 🗣️ Benchmarking Conversational Slang & Exemplar Retrieval:")
    print("-" * 70)
    dialogue_test_cases = [
        ("bhava nodejs backend crash hotay unhandled promise rejection mule", "Marathish"),
        ("manager bol raha hai saturday ko bhi aao urgent release hai", "Hinglish"),
        ("भाई पायथन में मेमोरी लीक हो रही है, रैम फुल हो गया", "Devanagari Hindi"),
        ("भावा गिट पुश रिजेक्ट झाला नॉन-फास्ट-फॉरवर्ड एररमुळे", "Devanagari Marathi"),
        ("feeling huge imposter syndrome in this new team", "English")
    ]

    for q, lang in dialogue_test_cases:
        t0 = time.time()
        exemplar = rag.retrieve_dialogue_exemplar(q, lang=lang)
        latency_ms = (time.time() - t0) * 1000
        print(f"\n[User ({lang})]: '{q}' ({latency_ms:.1f}ms)")
        if exemplar:
            for line in exemplar.split("\n"):
                print(f"  {line}")
        else:
            print("  (No exemplar found)")

    print("\n" + "=" * 70)
    print("🎉 RAG Training & Indexing 100% Complete! Ready for authentic chatting.")
    print("=" * 70)

if __name__ == "__main__":
    main()
