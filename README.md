# Regarding AI Response - RAG 기반 광고 추천 시스템

사용자의 취미(hobby)와 읽고 있는 신문 제목(newspaper_title)을 입력하면, MongoDB Atlas Vector Search를 통해 관련 문서를 검색하고 GPT-4o가 맞춤 광고 문구를 생성하는 RAG(Retrieval-Augmented Generation) 시스템입니다.

## 동작 흐름

1. 사용자가 `hobby`와 `newspaper_title`을 쿼리 파라미터로 전달
2. Redis 캐시에 동일한 요청이 있으면 캐시된 결과 반환
3. 캐시가 없으면:
   - MongoDB Atlas Vector Search로 신문 제목과 관련된 **취미** 검색 (`RAG.embedding`)
   - 관련된 **신문 기사** 검색 (`newspaperTitle.title`)
   - GPT-4o로 취미와 신문에 맞는 **광고 문구** 생성
4. 결과를 Redis에 캐시하고 JSON으로 반환

## 기술 스택

- **FastAPI** + **Uvicorn** - 웹 서버
- **OpenAI API** - 임베딩(text-embedding-ada-002) 및 광고 생성(GPT-4o)
- **MongoDB Atlas** - 벡터 검색 (Vector Search)
- **LangChain** - LLM 체인 및 벡터 스토어 연동
- **Redis** - 응답 캐싱

## 프로젝트 구조

```
.
├── app/
│   └── main.py                # FastAPI 엔트리포인트, /fetch 엔드포인트
├── embedding.py               # OpenAI 임베딩 API 호출
├── fetch_relevant.py          # MongoDB Atlas Vector Search로 유사 문서 검색
├── prompt.py                  # 관련 신문 검색 및 GPT-4o 광고 문구 생성
├── generate_random_hobby_and_newspaper_title.py  # 테스트용 취미/신문제목 생성
├── generate_data.py           # 취미 데이터 임베딩 후 MongoDB에 저장
├── save_title_embedding_to_db.py  # 신문 제목 임베딩 후 MongoDB에 저장
├── key.py                     # API 키 및 DB 비밀번호 (git에 포함하지 말 것)
├── requirements.txt           # Python 의존성
├── Dockerfile                 # Docker 빌드 설정
└── Jenkinsfile                # CI/CD 파이프라인
```

## 환경 설정

### 1. Conda 환경 생성 및 패키지 설치

```bash
conda create -n rag_server python=3.11 -y
conda activate rag_server
pip install uvicorn fastapi openai pymongo certifi redis langchain langchain-openai langchain-mongodb
```

### 2. 환경변수 설정

서버 실행 시 아래 환경변수가 필요합니다:

| 환경변수 | 설명 |
|---------|------|
| `openai_key` | OpenAI API 키 |
| `mongodb_password` | MongoDB Atlas 비밀번호 |

### 3. Redis 설치 및 실행

```bash
# macOS
brew install redis
redis-server
```

### 4. MongoDB Atlas 설정

- [MongoDB Atlas](https://cloud.mongodb.com)에서 클러스터 생성
- **Network Access**에서 현재 IP 주소 허용
- **Database Access**에서 사용자 생성
- 아래 두 컬렉션에 Vector Search 인덱스 생성 필요:

**`RAG.embedding`** 컬렉션 - 인덱스명: `hobby_index`
```json
{
  "type": "vectorSearch",
  "fields": [
    {
      "path": "hobby_embedding",
      "type": "vector",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}
```

**`newspaperTitle.title`** 컬렉션 - 인덱스명: `title_vector_index`
```json
{
  "type": "vectorSearch",
  "fields": [
    {
      "path": "hobby_embedding",
      "type": "vector",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}
```

## 서버 실행

### 로컬 실행

```bash
openai_key="YOUR_KEY" mongodb_password="YOUR_PASSWORD" uvicorn app.main:app --reload
```

### Docker 실행

```bash
docker build -t rag .
docker run --env-file .env -p 8000:8000 rag
```

## API 사용법

### GET /fetch

취미와 신문 제목을 기반으로 관련 문서 검색 및 광고 문구를 생성합니다.

**요청:**
```
GET http://127.0.0.1:8000/fetch?hobby=sports&newspaper_title=World%20Cup%20Finals
```

**응답 예시:**
```json
{
  "relevent hobby": ["테니스"],
  "relevent newspapers": [
    "광주시청 근대5종 전웅태, 소피아 월드컵 2차 대회 우승",
    "동신고 소프트테니스, 종별선수권대회 금빛 스트로크",
    "모든 시민이 테니스로 행복할 수 있도록 최선",
    "광주 근대5종 선수단, 전국 선수권대회 선전",
    "광양여고 축구부 춘계연맹전 우승"
  ],
  "recommended_advertise": "월드컵 결승전, 나이키 축구화로 당신의 경기를 빛내세요!"
}
```

## 벡터 검색 방식 비교 (ANN vs Exact Search)

`fetch_relevant.py`를 직접 실행하면 두 검색 방식의 결과와 소요 시간을 비교할 수 있습니다.

```bash
/opt/miniconda3/envs/rag_server/bin/python fetch_relevant.py
```

### 검색 방식

| 방식 | 설명 |
|------|------|
| **ANN** (Approximate Nearest Neighbor) | HNSW 인덱스를 활용한 근사 검색. 결과가 완전히 정확하지 않을 수 있으나 대규모 데이터에서 빠름 |
| **Exact Search** | `$vectorSearch`의 `exact: true` 옵션으로 전체 벡터를 직접 비교. 결과가 정확하나 데이터가 많을수록 느려짐 |

### 실측 결과 (현재 데이터셋 기준)

```
============================================================
  검색 방식 비교  |  query: 'User's hobby is travel ...'
============================================================

[ANN Search]  소요 시간: 1.2784s
[Full Scan]   소요 시간: 0.1161s

  → Full Scan이 11.0배 더 빠름
============================================================
```

> **결과 해석:** 현재 데이터셋은 규모가 작아 ANN 인덱스 탐색 오버헤드가 Exact Search보다 크게 나타남.
> 데이터가 수십만 건 이상으로 늘어나면 ANN이 압도적으로 빨라짐.

## 데이터 출처

신문 기사 제목: [AIHub - 신문기사 기계독해 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=577)
