# Task Manager API

![FastAPI](https://img.shields.io/badge/FastAPI-000000?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

Task Manager — это асинхронное RESTful API для управления задачами, построенное на FastAPI и PostgreSQL с использованием Docker.

## 🚀 Возможности

- CRUD операции для задач (создание, чтение, обновление, удаление)
- Поддержка enum-статусов задач (`CREATED`, `IN_PROGRESS`, `DONE`)
- Асинхронная работа с базой данных через SQLAlchemy + asyncpg
- Swagger документация `/docs` и OpenAPI `/openapi.json`
- Docker для лёгкой установки и запуска

## 📦 Технологии

- Python 3.10+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Docker & Docker Compose
- Pydantic

## ⚡ Быстрый старт

1. Клонируем репозиторий:

```bash
git clone <your-repo-url>
cd task_manager
```
2. Создаём .env (пример):

```bash
# db
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/mycooldb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mycooldb
POSTGRES_HOST=5432
POSTGRES_PORT=5432

# pgadmin
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin

# ports
APP_PORT=8000
PGADMIN_PORT=5050
HOST_PORT_DB=5432
POSTGRES_PORT=5432
```

3. Сборка и запуск через Docker Compose:

```bash
docker compose up --build
```

4. Перейти в Swagger UI:

```bash
http://localhost:8000/docs
```

## 🧪 Тесты
Запуск тестов с pytest:

```bash
pytest
```

## 📂 Структура проекта

```bash
taskmanager/
├── src/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── README
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── routers/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── tasks.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── task.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── task_repository.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── task.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── task_service.py
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── gauge/
│   │   ├── main.py
│   │   └── __init__.py
│   ├── Dockerfile
│   ├── alembic.ini
│   └── __init__.py
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
├── .dockerignore
└── README.md
```


