"""
CWM (Chat With MES) - Demo Runner
==================================
Run:  python run_demo.py

Prerequisites:
  1. python setup_db.py          (create SQLite DB - run only once)
  2. .env file with OPENAI_API_KEY

Sample questions to try:
  - What are the orders for PolyU?
  - Show all customers.
  - What products are in the PolyU_Tshirt order?
  - Which cutting tasks are still in progress?
  - What is the progress of sewing tasks for Michael's SweaterAndShorts order?
  - Show me all working groups.
"""

import os
import sys
import json

# Fix Windows console encoding for emoji/unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── path setup ────────────────────────────────────────────────────────────────
SRC_DIR = os.path.join(os.path.dirname(__file__), "src", "chatDB")
sys.path.insert(0, SRC_DIR)

# ── check .env ────────────────────────────────────────────────────────────────
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(ENV_PATH):
    print("[ERROR] .env 파일이 없습니다.")
    print("  1) .env.example 파일을 복사하세요:")
    print("       copy .env.example .env")
    print("  2) .env 파일 안에 OPENAI_API_KEY 를 입력하세요.")
    sys.exit(1)

# ── check DB ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "fashion.db")
if not os.path.exists(DB_PATH):
    print("[ERROR] fashion.db 파일이 없습니다.")
    print("  다음 명령어로 DB를 먼저 생성하세요:")
    print("       python setup_db.py")
    sys.exit(1)

# ── import chatdb ─────────────────────────────────────────────────────────────
try:
    from chatdb import generate_chat_responses, init_database
except ImportError as e:
    print(f"[ERROR] Import 실패: {e}")
    print("  pip install -r requirements.txt 를 먼저 실행하세요.")
    sys.exit(1)

# ── main ──────────────────────────────────────────────────────────────────────
def print_divider(char="─", width=60):
    print(char * width)

def print_steps(steps):
    if not steps:
        return
    print("\n[Steps]")
    for i, step in enumerate(steps, 1):
        step_type = step.get("type", "SQL")
        print(f"  Step {i} [{step_type}]: {step.get('description', '')}")
        if step_type == "SQL":
            print(f"    SQL: {step.get('sql', '')}")
            results = step.get("results", [])
            if results and isinstance(results, list):
                print(f"    결과: {json.dumps(results[:3], ensure_ascii=False)}"
                      + (" ..." if len(results) > 3 else ""))

def main():
    print_divider("=")
    print("  CWM - Chat With MES  (SQLite + OpenAI)")
    print("  AI-powered natural language interface for Manufacturing MES")
    print_divider("=")
    print("  Type 'quit' or 'exit' to stop")
    print("  샘플 질문:")
    print("    - What are the orders for PolyU?")
    print("    - Show all customers.")
    print("    - Which cutting tasks are still in progress?")
    print_divider()

    mysql_db = init_database()
    historical_message = []
    context_abstract = ""

    while True:
        try:
            user_input = input("\nUSER > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        print_divider()
        print("Processing...")
        try:
            sql_results, sql_commands, err, response, context_abstract = generate_chat_responses(
                user_inp=user_input,
                mysql_db=mysql_db,
                historical_message=historical_message,
                context_abstract=context_abstract,
            )
            historical_message = historical_message[-10:]  # keep last 10

            print_steps(sql_results)

            print_divider()
            print("[Response]")
            print(response)
            print_divider()

        except Exception as e:
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
