# Django + Elasticsearch 문서 검색 시스템 구성 가이드

Elasticsearch와 Django를 이용하여 다국어 문서를 색인하고, 웹 UI를 통해 검색하는 시스템입니다.  
CSV 문서 파일을 자동으로 색인하며, 실시간 검색 및 하이라이팅을 지원합니다.

---

## 📁 디렉터리 구조

```plaintext
.
├── Dockerfile                     # Django 앱 빌드용 Docker 설정
├── docker-compose.yaml            # 전체 서비스 도커 컴포지션 정의
├── manage.py                      # Django 명령줄 관리 도구
├── requirements.txt               # 프로젝트 의존 패키지 목록
├── README.md                      # 프로젝트 설명서
├── db.sqlite3                     # SQLite DB (테스트용)
├── wait-for-it.sh                 # DB 컨테이너 대기 스크립트

├── data/
│   ├── output_KCS/*.csv           # KCS 문서 데이터
│   └── output_KDS/*.csv           # KDS 문서 데이터

├── search_app/
│   ├── documents.py               # Elasticsearch 문서 정의
│   ├── management/commands/load_csv.py  # CSV 자동 색인 스크립트
│   ├── migrations/
│   ├── models.py                  # StandardDoc 모델 정의
│   ├── templates/search_app/search.html # 검색 결과 UI 템플릿
│   ├── urls.py                    # URL 라우팅
│   └── views.py                   # 검색 뷰 로직

├── search_project/
│   ├── settings.py 등             # Django 프로젝트 설정

├── static/
│   └── 로고.png     # 삽입된 로고 이미지
```

---

## 🧬 모델 필드 구성

| 필드명        | 설명                    |
| ------------- | ----------------------- |
| `code_type`   | 문서 분류 (KCS, KDS 등) |
| `code`        | 고유 문서 코드          |
| `name`        | 문서 제목 (국문)        |
| `contents`    | 문서 본문 내용 (국문)   |
| `name_en`     | 문서 제목 (영문)        |
| `contents_en` | 문서 본문 내용 (영문)   |

---

## 📥 CSV 자동 색인 방식

`load_csv.py`는 다음 경로의 모든 `.csv` 파일을 자동 탐색합니다:

- `data/output_KCS/*.csv` → `code_type = KCS`
- `data/output_KDS/*.csv` → `code_type = KDS`

> ⚠️ `code` 값이 숫자가 아닌 경우 해당 행은 색인되지 않습니다.

---

## 🛠️ 명령어 정리

```bash
# 컨테이너 실행
docker compose up -d

# Django 컨테이너 접속
docker exec -it django_elasticsearch-web-1 bash

# 마이그레이션 (DB 테이블 생성)
python manage.py makemigrations search_app
python manage.py migrate

# CSV → DB 삽입
python manage.py load_csv

# Elasticsearch 인덱스 색인
python manage.py search_index --rebuild
```

| 명령어                   | 설명                                      |
| ------------------------ | ----------------------------------------- |
| `makemigrations`         | 모델 변경사항 추적                        |
| `migrate`                | DB 테이블 생성                            |
| `load_csv`               | 다중 CSV 파일 데이터를 DB에 삽입          |
| `search_index --rebuild` | Elasticsearch 인덱스를 새로 생성하고 색인 |

---

## ✅ 색인 상태 및 초기화

### 색인 상태 확인

```bash
curl -X GET http://localhost:9200/_cat/indices?v
```

### 인덱스 초기화 (삭제)

```bash
curl -X DELETE "http://localhost:9200/standard_docs"
```

---

## 🔍 검색 페이지 접속

- [http://localhost:9100](http://localhost:9100) 에 접속하면 검색 UI 제공
- `/admin` 경로로 슈퍼유저 접속 가능 (`createsuperuser`로 생성)

---

## 🔎 검색 기능 (모드 및 출력)

### 검색 모드

| 모드       | 설명                                        |
| ---------- | ------------------------------------------- |
| `fulltext` | `multi_match` 기반 유사도 검색              |
| `like`     | `wildcard` 기반 부분 문자열 검색 (`*문자*`) |

### 출력 모드

| 출력 옵션   | 설명                                      |
| ----------- | ----------------------------------------- |
| `highlight` | 검색어가 포함된 문장만 표시 (노란색 강조) |
| `full`      | 문서 전체 내용 출력                       |

사용자는 검색창 아래 드롭다운을 통해 모드를 선택할 수 있습니다.

---

## 🎨 UI 기능 요약 (`search.html`)

| 기능              | 설명                                                     |
| ----------------- | -------------------------------------------------------- |
| ✅ 실시간 검색    | 입력 시 자동으로 결과 업데이트 (JS `fetch`)              |
| ✅ 하이라이팅     | 검색어 포함 문장 노란색 강조 (`highlight`)               |
| ✅ 전체 보기 전환 | 문서 전체 내용 출력 모드 제공                            |
| ✅ 페이지네이션   | 결과가 많을 경우 페이지 이동 지원                        |
| ✅ 로고 삽입      | 상단에 회사 로고 표시 (`/static/한맥기술_좌우_국문.png`) |

---

## 📦 Elasticsearch 직접 쿼리 예시

```bash
curl -X POST "http://localhost:9200/standard_docs/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "multi_match": {
        "query": "건축",
        "fields": ["name", "contents"]
      }
    }
  }'
```

---

## ✅ 관리자 계정 생성

```bash
docker exec -it django_elasticsearch-web-1 python manage.py createsuperuser
```

관리자 페이지 접속: [http://localhost:9100/admin](http://localhost:9100/admin)

---

## ✨ 실행 흐름 요약

```bash
docker compose up -d
docker exec -it django_elasticsearch-web-1 bash
python manage.py migrate
python manage.py load_csv
python manage.py search_index --rebuild
python manage.py runserver 0.0.0.0:9100
```

→ [http://localhost:9100](http://localhost:9100) 접속 후 검색 실행
