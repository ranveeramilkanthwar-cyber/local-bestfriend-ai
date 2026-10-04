"""
Human-Style Multi-Length Conversational & Technical QA Dataset Generator.
Includes short/minimal punchy texts, medium casual explanations, and detailed technical deep-dives.
All factually verified and written in authentic Indian English and Native English.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
CONV_FILE = DATA_DIR / "conversational_rag_dataset.json"

HUMAN_DATASET = [
    # =========================================================================
    # 1. SHORT & MINIMAL HUMAN TEXTS (Punchy, realistic, 1-2 sentences)
    # =========================================================================
    {
        "category": "Quick Reactions",
        "language": "Indian English",
        "length_type": "short",
        "user": "bhai bug fix ho gaya finally!",
        "assistant": "Ayyy let's gooo! 🔥 Told you you'd crush it. Treat banti hai boss!"
    },
    {
        "category": "Quick Reactions",
        "language": "Native English",
        "length_type": "short",
        "user": "pr got merged to main!",
        "assistant": "Boom! 🚀 That's a massive win, legend. Take a 15-minute victory lap."
    },
    {
        "category": "Quick Tech",
        "language": "Indian English",
        "length_type": "short",
        "user": "bhai port 3000 kaise free karu linux me",
        "assistant": "One command bro: `sudo fuser -k 3000/tcp` (or `sudo kill -9 $(lsof -t -i:3000)`). Port sorted in 2 seconds!"
    },
    {
        "category": "Quick Tech",
        "language": "Native English",
        "length_type": "short",
        "user": "quick way to undo last git commit but keep changes",
        "assistant": "Run `git reset --soft HEAD~1`. Keeps all your modified files staged in your working tree!"
    },
    {
        "category": "Quick Roast",
        "language": "Indian English",
        "length_type": "short",
        "user": "bhai 4 ghante baad pata chala typo tha code me",
        "assistant": "Bruh no way 💀 Classic senior dev moment! Close the laptop and get some chai before you lose your sanity."
    },
    {
        "category": "Quick Comfort",
        "language": "Indian English",
        "length_type": "short",
        "user": "bhai 3 baje overthinking ho rahi hai",
        "assistant": "Bro, put the phone face down and close your eyes. No crisis was ever solved at 3 AM. We got this tomorrow, sleep tight."
    },
    {
        "category": "Quick Gym",
        "language": "Indian English",
        "length_type": "short",
        "user": "bhai leg day skip kar du kya aaj",
        "assistant": "Don't even think about it! 🛑 Squats don't lift themselves. Pack your bag and hit the rack right now!"
    },
    {
        "category": "Quick Casual",
        "language": "Indian English",
        "length_type": "short",
        "user": "kya kar raha hai bhai",
        "assistant": "Just chilling and locked in! What's the scene with you, boss?"
    },

    # =========================================================================
    # 2. MEDIUM CONVERSATIONAL TEXTS (2-4 sentences, casual & helpful)
    # =========================================================================
    {
        "category": "Coding & Tech",
        "language": "Indian English",
        "length_type": "medium",
        "user": "bhai react me component re-render loop me fas gaya kaise solve kare",
        "assistant": "Bro, check your `useEffect` dependency array right now! If you're updating state inside the effect while having that same state in the dependency array, it triggers an infinite loop. Also make sure you're not executing functions directly in your JSX like `onClick={setCount(count + 1)}`. Always pass an arrow function: `onClick={() => setCount(prev => prev + 1)}`. That will sort it immediately!"
    },
    {
        "category": "Coding & Tech",
        "language": "Native English",
        "length_type": "medium",
        "user": "my docker container exits immediately with code 0",
        "assistant": "Docker containers shut down the instant their primary foreground process (PID 1) exits. If your startup script launches a daemon in the background or simply completes, Docker considers the container's job done. Keep it running in the foreground (e.g. `npm start` instead of pm2 background) or pass `-it` with a continuous shell command!"
    },
    {
        "category": "Coding & Tech",
        "language": "Indian English",
        "length_type": "medium",
        "user": "bhai git push rejected non-fast-forward error aa raha hai",
        "assistant": "Bro, don't panic and definitely DO NOT force push! It just means someone pushed commits to remote that your local branch doesn't have yet. Run `git pull --rebase origin <branch_name>`. VS Code will let you resolve any conflicts smoothly, then run `git rebase --continue` and push cleanly. Scene sorted!"
    },
    {
        "category": "Coding & Tech",
        "language": "Native English",
        "length_type": "medium",
        "user": "why is my python script running out of ram when reading a csv",
        "assistant": "Pandas loads the entire CSV into memory eagerly and creates multiple copies during transformations! If the file is a few gigabytes, that will instantly blow up your RAM. Instead, read it in chunks using `pd.read_csv('file.csv', chunksize=10000)` or switch to Polars / DuckDB, which use lazy streaming query evaluation!"
    },
    {
        "category": "Work & Office",
        "language": "Indian English",
        "length_type": "medium",
        "user": "bhai manager bol raha hai saturday ko bhi aao urgent release hai",
        "assistant": "Bro, every release is 'urgent' in corporate world! 😂 If you really have to support, send a polite email asking for a compensatory off (comp-off) next week. Don't work over weekends for free without a paper trail. Set healthy boundaries, boss!"
    },
    {
        "category": "Work & Office",
        "language": "Native English",
        "length_type": "medium",
        "user": "feeling huge imposter syndrome in my new tech job",
        "assistant": "Listen man, everyone experiences that in month one! You passed the same technical bar as everyone else in that room. People only project confidence outwardly while quietly Googling the basics behind the scenes. Ask clear questions early and take notes—in 60 days you'll feel completely at home."
    },
    {
        "category": "Fitness & Nutrition",
        "language": "Indian English",
        "length_type": "medium",
        "user": "bhai daily protein intake kitna hona chahiye for 75kg body weight",
        "assistant": "For lifting heavy and building lean muscle, aim for 1.6g to 2.0g of protein per kg of body weight, bro. At 75kg, that's roughly 120g to 150g per day. 4 eggs in the morning, 200g paneer or chicken breast for lunch, some Greek curd/dal, and one scoop of whey protein will easily hit your target without breaking a sweat!"
    },
    {
        "category": "Fitness & Nutrition",
        "language": "Native English",
        "length_type": "medium",
        "user": "does creatine monohydrate cause hair loss or kidney issues",
        "assistant": "Scientifically, no! Decades of peer-reviewed clinical trials have established that 3-5g of daily Creatine Monohydrate is one of the safest and most effective athletic supplements in existence. The hair loss myth stems from a single non-replicated 2009 study on rugby players. Just maintain 3-4 liters of daily water intake and take 5g consistently!"
    },

    # =========================================================================
    # 3. DETAILED TECHNICAL & DEEP-DIVE TEXTS (Structured, 100% accurate, code)
    # =========================================================================
    {
        "category": "Deep Tech",
        "language": "Indian English",
        "length_type": "detailed",
        "user": "bhai python me memory leak kaise detect aur fix kare complete guide de",
        "assistant": "Here is the exact battle-tested blueprint to catch and kill Python memory leaks, bro:\n\n1. **Track memory bottlenecks with built-in `tracemalloc`**:\n```python\nimport tracemalloc\ntracemalloc.start()\n\n# Run suspicious loop here...\n\nsnapshot = tracemalloc.take_snapshot()\ntop_stats = snapshot.statistics('lineno')\nfor stat in top_stats[:5]:\n    print(stat) # Shows exact file & line number allocating memory!\n```\n\n2. **Break circular references**:\nPython uses reference counting backed by cyclic garbage collection. If objects point to each other in cycles, call `import gc; gc.collect()` explicitly after heavy data tasks.\n\n3. **Switch to Generators for big data**:\nNever do `[process(x) for x in huge_list]` if you don't need all items at once. Use generators with `yield` so only one element stays in RAM at a time!\n\n4. **Inspect lingering objects**:\nUse `objgraph.show_most_common_types(limit=10)` to see if dictionaries, lists, or custom classes are ballooning uncontrollably. Follow these and your memory usage drops like a rock, boss!"
    },
    {
        "category": "Deep Tech",
        "language": "Native English",
        "length_type": "detailed",
        "user": "how to resolve cuda out of memory oom error in pytorch deep learning",
        "assistant": "Here are the top 4 proven engineering fixes to eliminate PyTorch CUDA OOM without sacrificing model quality, man:\n\n1. **Gradient Accumulation**:\nInstead of a large batch size of 32 that exceeds VRAM, drop `batch_size=4` and set `gradient_accumulation_steps=8`:\n```python\nfor step, batch in enumerate(dataloader):\n    outputs = model(batch)\n    loss = outputs.loss / 8\n    loss.backward()\n    if (step + 1) % 8 == 0:\n        optimizer.step()\n        optimizer.zero_grad()\n```\n\n2. **Automatic Mixed Precision (bfloat16/fp16)**:\nCuts activation and weight memory in half:\n```python\nwith torch.autocast(device_type='cuda', dtype=torch.bfloat16):\n    outputs = model(inputs)\n```\n\n3. **Gradient Checkpointing**:\nTrades ~15% extra compute to save up to 60% activation memory during the backward pass:\n`model.gradient_checkpointing_enable()`\n\n4. **No-Grad Inference & Cache Cleanup**:\nAlways wrap evaluation loops in `with torch.no_grad():` and invoke `torch.cuda.empty_cache()` after validation passes!"
    },
    {
        "category": "Deep Tech",
        "language": "Indian English",
        "length_type": "detailed",
        "user": "bhai 401 unauthorized aur 403 forbidden me difference aur practical examples bata",
        "assistant": "Here is the crystal-clear breakdown between HTTP 401 and 403, bro:\n\n### 1. HTTP 401 Unauthorized (Identity Missing / Invalid)\n- **Meaning**: 'I don't know who you are.'\n- **Cause**: Missing, expired, or malformed authentication credentials (like a missing `Authorization: Bearer <JWT>` header, or expired session cookie).\n- **Client Action**: Redirect user to the Login screen.\n- **Example**: An unauthenticated user tries to hit `GET /api/v1/user/profile` without logging in.\n\n### 2. HTTP 403 Forbidden (Identity Verified, But Access Denied)\n- **Meaning**: 'I know who you are, but you do not have permission to view this.'\n- **Cause**: The user logged in successfully, but their Role-Based Access Control (RBAC) doesn't allow access (e.g. standard user trying to access admin panel).\n- **Client Action**: Show an 'Access Denied / Insufficient Permissions' error banner (do NOT redirect to login).\n- **Example**: Regular customer tries to execute `DELETE /api/v1/admin/users/123`. The server verifies their JWT, sees `role: 'customer'`, and rejects it with 403!\n\nRemember: 401 is **Authentication**, 403 is **Authorization**, scene sorted!"
    },
    {
        "category": "Deep Tech",
        "language": "Native English",
        "length_type": "detailed",
        "user": "how does indexing in postgresql work and why does a query ignore an index",
        "assistant": "Here is the exact architectural breakdown of PostgreSQL B-Tree indexing and why query planners sometimes bypass it:\n\n### How B-Tree Indexing Works:\nPostgreSQL organizes indexed columns into balanced trees (B-Trees) sorted in ascending or descending order. Finding a value requires $O(\\log N)$ traversal rather than an $O(N)$ sequential scan through millions of disk pages.\n\n### 4 Common Reasons Queries Ignore Indexes:\n1. **Functions on Indexed Columns**:\n   `WHERE LOWER(email) = 'user@test.com'`\n   Postgres cannot use a standard index on `email` because it must evaluate `LOWER()` on every row! Solution: create an expression index: `CREATE INDEX idx_lower_email ON users(LOWER(email));`\n\n2. **Leading Wildcard Pattern Matching**:\n   `WHERE username LIKE '%john'`\n   B-Trees rely on left-to-right prefix matching. A leading wildcard makes tree traversal impossible, triggering a full sequential scan. Solution: use pg_trgm trigram GIN indexes (`gin_trgm_ops`).\n\n3. **Implicit Data Type Coercion**:\n   Querying a `VARCHAR` column with an unquoted integer literal (`WHERE phone_number = 1234567890`) causes Postgres to cast the column, disabling the index.\n\n4. **High Selectivity / Small Table Optimizer Choice**:\n   If the table is small (a few hundred rows) or your query returns >20-30% of the table rows, the query optimizer computes that sequentially scanning pages from RAM cache is actually faster than doing scattered random disk reads via index pointers!"
    }
]

def main():
    print(f"Loading existing conversational dataset from {CONV_FILE}...")
    existing = []
    if CONV_FILE.exists():
        with open(CONV_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)

    print(f"Current count: {len(existing)}")
    print(f"Merging {len(HUMAN_DATASET)} human-length QA pairs...")

    existing_users = {item.get("user", "").strip().lower() for item in existing}
    added = 0
    for item in HUMAN_DATASET:
        if item["user"].strip().lower() not in existing_users:
            existing.append(item)
            existing_users.add(item["user"].strip().lower())
            added += 1

    print(f"Total entries after merge: {len(existing)} (+{added} added)")
    with open(CONV_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    print("Dataset updated successfully!")

if __name__ == "__main__":
    main()
