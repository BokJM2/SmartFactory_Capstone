# PROMPTS.md — Claude Code 프롬프트 로그

> 과목: 캡스톤디자인  
> 오픈소스: CWM (Chat With MES)  
> 작성자: 복재민  
> 도구: Claude Code (claude-sonnet-4-6)

---

## 1단계: 프로젝트 파악

**Prompt 1**
```
이 프로젝트 실행하는 방법 알려줘
```

**Prompt 2**
```
MySQL 설치 없이 실행할 수 있는 방법 없어?
과제로 오픈소스 실행만 하면 되는데 MySQL 세팅이 너무 복잡함
```

**Prompt 3**
```
SQLite로 MySQL 대체해서 바로 실행되게 만들어줘.
setup_db.py랑 run_demo.py도 같이 만들어줘
```

---

## 2단계: 의존성 설치 및 오류 해결

**Prompt 4**
```
pip install 하다가 이런 오류 남

error: subprocess-exited-with-error
numpy 1.26.4 build 실패

어떻게 해?
```

**Prompt 5**
```
실행했더니 이런 오류 뜸

ModuleNotFoundError: No module named 'pymysql'

고쳐줘
```

**Prompt 6**
```
또 오류남

cannot import name 'AgentExecutor' from 'langchain.agents'

이거 왜 이러는 거야? 고쳐줘
```

**Prompt 7**
```
아직도 오류 있음

No module named 'langchain.prompts'

langchain 버전 문제인 것 같은데 전부 다 고쳐줘
```

**Prompt 8**
```
실행은 되는데 이런 오류 뜸

openai.AuthenticationError: 401 - ApiKey错误 (chatanywhere)

API 키 어떻게 써야 해?
```

---

## 3단계: 데이터베이스 및 API 연결

**Prompt 9**
```
setup_db.py 실행했는데 테이블은 만들어졌는데 데이터가 하나도 없음
customers: 0 rows
왜 그런지 찾아서 고쳐줘
```

**Prompt 10**
```
API 키 충전했어. 이제 실행하면 되는 거야?
```

**Prompt 11**
```
실행하면 이모지 출력할 때 오류남

UnicodeEncodeError: 'cp949' codec can't encode character

Windows 콘솔 문제인 것 같은데 고쳐줘
```

---

## 4단계: 코드 분석

**Prompt 12**
```
이 프로젝트 코드 분석해줘.
전체 아키텍처랑 각 파일이 무슨 역할인지 설명해줘
```

**Prompt 13**
```
chain_of_memory가 뭔지 자세히 설명해줘.
SQL placeholder 어떻게 동작하는지도 알려줘
```

---

## 5단계: GitHub 업로드

**Prompt 14**
```
이 프로젝트 github https://github.com/BokJM2/SmartFactory_Capstone.git 에 올리는 법
```

