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
- Dockerized для лёгкой установки и запуска

## 📦 Технологии

- Python 3.10+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic (миграции)
- Docker & Docker Compose
- Pydantic (валидация данных)

## ⚡ Быстрый старт

1. Клонируем репозиторий:

```bash
git clone <your-repo-url>
cd task_manager
