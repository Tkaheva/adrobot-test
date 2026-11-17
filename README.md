# Adrobot Test Task - Keitaro Wrapper

Тестовое задание на позицию Fullstack-разработчик (Python/FastAPI). 
Сервис-обертка над рекламным трекером Keitaro для создания кампаний и управления офферами.

## Стек технологий
- **Backend:** Python 3.11, FastAPI, SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** HTML + Vanilla JavaScript (минималистичный интерфейс)
- **Инфраструктура:** Docker, Docker Compose

## Инструкция по запуску (Docker)

Самый простой способ запустить проект — использовать Docker.

1. Клонируйте репозиторий:
   git clone https://github.com/Tkaheva/adrobot-test.git
   cd adrobot-test

2. Запуск в терминале:
   docker compose up --build -d
   
3. Открытие проекта:
   Документация API (Swagger): http://localhost:8001/docs
   
   Веб-интерфейс: http://localhost:8001/

4. Структура проекта:
adrobot-test/
├── app/
│   ├── __init__.py
│   ├── main.py             # Точка входа, роуты FastAPI
│   ├── database.py         # Подключение к PostgreSQL
│   ├── models.py           # Модели SQLAlchemy (Domain, Group, Offer)
│   ├── schemas.py          # Pydantic-схемы (валидация входящих данных)
│   └── keitaro_client.py   # Обертка над API Keitaro (GET/POST запросы)
├── frontend/
│   └── index.html          # Интерфейс для работы с API
├── .env                    # (Не коммитится, добавлен в .gitignore)
├── .env.example            # Пример заполнения переменных
├── docker-compose.yml      # Конфигурация Docker
├── Dockerfile              # Инструкция сборки образа
├── requirements.txt        # Зависимости Python
└── README.md
