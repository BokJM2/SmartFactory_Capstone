# CWM 프롬프트 로그 (Prompt Log)

> 과목: 캡스톤디자인  
> 오픈소스: CWM (Chat With MES)  
> 작성자: 복재민  

---

## 1. 환경 설정 및 오류 해결

### 1.1 LangChain 버전 호환성 문제
```
[문제] cannot import name 'AgentExecutor' from 'langchain.agents'
[원인] LangChain 1.x에서 AgentExecutor 및 create_tool_calling_agent 제거
[해결] TOOL_OPEN=False 설정 + 조건부 import 처리
```

**수정 코드 (chatdb.py)**
```python
if cfg.tool_open:
    try:
        from agents.agent_tools import tools_description_str, agent_executor
    except Exception:
        cfg.tool_open = False
        tools_description_str = ""
        agent_executor = None
else:
    tools_description_str = ""
    agent_executor = None
```

### 1.2 MySQL → SQLite 전환
```
[문제] MySQL 설치 없이 즉시 실행 불가
[해결] sqlite_db.py 작성 — 동일한 인터페이스로 SQLite 구현
```

**tables.py 수정**
```python
from sqlite_db import SQLiteDB

def init_database(database_info=None, db=None):
    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "fashion.db"
    )
    return SQLiteDB(db_path=os.path.abspath(db_path))
```

### 1.3 API 프록시 URL 제거 (chatgpt.py)
```
[문제] base_url="https://api.chatanywhere.tech/v1" 하드코딩
[오류] AuthenticationError: 401 - ApiKey 错误
[해결] base_url 파라미터 제거 → 공식 OpenAI API 사용
```

```python
# 수정 전
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.chatanywhere.tech/v1"
)

# 수정 후
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
```

### 1.4 ENABLE_REWRITE_QUERY 파싱 버그 (config.py)
```
[문제] os.getenv("ENABLE_REWRITE_QUERY", True) 에서
       "False" 문자열이 bool True로 평가됨
[해결] 다른 설정과 동일하게 == "True" 비교로 통일
```

```python
# 수정 전
self.enable_rewrite_query = os.getenv("ENABLE_REWRITE_QUERY", True)

# 수정 후
self.enable_rewrite_query = os.getenv("ENABLE_REWRITE_QUERY", "True") == "True"
```

### 1.5 recall_knowledge.py — Lazy Loading으로 변경
```
[문제] import 시점에 OpenAI 임베딩 API 호출 → 크레딧 없으면 import 자체 실패
[해결] _build_index() 함수로 감싸서 실제 사용 시점에만 호출
```

```python
_index_ready = False

def _build_index():
    global retrievers, _index_ready
    if _index_ready:
        return
    try:
        Settings.embed_model = OpenAIEmbedding(...)
        # ... 인덱스 빌드
        _index_ready = True
    except Exception as e:
        print(f"[WARNING] Vector index build failed: {e}")
```

---

## 2. 시스템 프롬프트 분석

### 2.1 SQL 계획 요청 프롬프트 (cwm_prompts.py)

```
Please tell me what basic operations, including sql, should I use 
in order to respond to the "USER INPUT".

If it needs multiple operations, please list them step by step 
concisely.

The output should be a markdown code snippet formatted in the 
following schema:
```
Step1: <Description of first step>
SQL `SQL command for step1`

Step2: <Description of first step>
SQL `SQL command for step2`
```

Backticks are important and must be added at the beginning and end 
of the command for every step!

Here are some examples:
{egs}

Here are some context abstracts:
{context_abstracts}

USER INPUT: {user_inp}
ANSWER:
```

### 2.2 최종 응답 생성 프롬프트

```
You are the chatDB intelligent assistant, capable of answering user 
questions based on the execution results of SQL queries within the 
<sql-result> XML tag.

The user question is "{user_inp}".

SQL Result
<sql-result>{sql_results}</sql-result>

Answer Requirements:
- Do not mention that the information comes from the <sql-result> tag.
- Use markdown to optimize your answer, try to organize results in a table.
- Respond in a friendly and lively tone.
```

### 2.3 시스템 역할 프롬프트 (init_system_msg)

```
You are Chat With MES, a powerful AI assistant, a variant of ChatGPT 
that can utilize the database of the Manufacturing Execution System 
as external symbolic memory.

You are an expert in databases, proficient in SQL statements and can 
use the database to help users.

The details of tables in the database are delimited by triple quotes.
"""
{table_details}
"""
```

---

## 3. 실제 질문-응답 로그

### Query 1: 전체 고객 목록
```
USER > Show all customers.

[LLM 계획 생성]
Step1: Retrieve all customer names from the customers table
SQL `SELECT customer_name FROM customers;`

[DB 실행 결과]
+---------------+
| customer_name |
+---------------+
|     PolyU     |
|     Alice     |
|      Bob      |
|    Michael    |
|     Sophia    |
|      Emma     |
|     James     |
+---------------+

[최종 응답]
Sure! Here's the list of all customers we have:

| Customer Name |
|---------------|
| PolyU         |
| Alice         |
| Bob           |
| Michael       |
| Sophia        |
| Emma          |
| James         |
```

### Query 2: 진행 중인 재단 작업 조회
```
USER > Which cutting tasks are still in progress?

[LLM 계획 생성]
Step1: Find cutting tasks that are not completed (status != 2)
SQL `SELECT ct.id, wg.name as group_name, ct.planned_number, 
     ct.completed_number, ct.status
     FROM cutting_tasks ct
     JOIN working_group wg ON ct.working_group_id = wg.id
     WHERE ct.status != 2;`

[최종 응답]
Here are the cutting tasks still in progress:
| Task ID | Group           | Planned | Completed |
|---------|-----------------|---------|-----------|
| 2       | Cutting Group B | 30      | 20        |
| 5       | Cutting Group B | 45      | 30        |
...
```

### Query 3: PolyU 주문 현황
```
USER > What are the orders for PolyU?

[LLM 계획 생성]
Step1: Find all orders placed by the customer named PolyU
SQL `SELECT o.id, o.order_name, o.created_at
     FROM orders o
     JOIN customers c ON o.user_id = c.id
     WHERE c.customer_name = 'PolyU';`

[최종 응답]
PolyU has placed 2 orders:
| Order ID | Order Name   | Created At          |
|----------|--------------|---------------------|
| 1        | PolyU_Tshirt | 2024-02-10 00:00:00 |
| 9        | PolyU_Skirt  | 2024-04-15 00:00:00 |
```

### Query 4: 봉제 작업 진행률
```
USER > What is the sewing progress for PolyU's orders?

[LLM 계획 생성]
Step1: Calculate sewing task completion percentage for PolyU's orders
SQL `SELECT o.order_name,
     SUM(st.completed_number) as total_completed,
     SUM(st.planned_number) as total_planned,
     ROUND(SUM(st.completed_number) * 100.0 / SUM(st.planned_number), 1) as progress_pct
     FROM sewing_tasks st
     JOIN order_product op ON st.order_product_id = op.id
     JOIN orders o ON op.order_id = o.id
     JOIN customers c ON o.user_id = c.id
     WHERE c.customer_name = 'PolyU'
     GROUP BY o.id, o.order_name;`
```

---

## 4. setup_db.py — 데이터베이스 초기화 쿼리

```sql
-- 고객 샘플 데이터
INSERT OR IGNORE INTO customers (id, customer_name) VALUES
(1, 'PolyU'), (2, 'Alice'), (3, 'Bob'),
(4, 'Michael'), (5, 'Sophia'), (6, 'Emma'), (7, 'James');

-- 주문 샘플 데이터
INSERT OR IGNORE INTO orders (id, user_id, order_name, created_at) VALUES
(1,  1, 'PolyU_Tshirt',           '2024-02-10 00:00:00'),
(2,  2, 'Alice_Jacket',            '2024-03-01 00:00:00'),
(3,  3, 'Bob_Sweater',             '2024-03-05 00:00:00'),
(4,  4, 'Michael_TshirtAndSkirt',  '2024-03-10 00:00:00'),
(6,  4, 'Michael_SweaterAndShorts','2024-04-01 00:00:00'),
(9,  1, 'PolyU_Skirt',             '2024-04-15 00:00:00');
```

---

## 5. .env 설정 파일

```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
FAST_LLM_MODEL=gpt-4o-mini
SMART_LLM_MODEL=gpt-4o-mini
ENABLE_REWRITE_QUERY=False
TOOL_OPEN=False
THOUGHT_OPEN=False
SINGLE_SQL_STEP=False
SLEEP=False
```
