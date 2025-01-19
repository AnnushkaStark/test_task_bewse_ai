# test_task_bewse_ai

## Задание

Разработайте сервис для обработки заявок пользователей. Сервис должен:

1. Принимать заявки через REST API (FastAPI).
2. Обрабатывать и записывать заявки в PostgreSQL.
3. Публиковать информацию о новых заявках в Kafka
4. Обеспечивать эндпоинт для получения списка   заявок с фильтрацией и пагинацией.
5. Включать Docker-файл для развертывания приложения.

## Детали реализации

1. REST API:

    * Создайте эндпоинт
    ```
    POST /applications
    ```
    для создания новой заявки. Заявка содержит следующие поля:

        id  - (генерируется автоматически)

        username -  (имя пользователя)

        description -  (описание заявки)


        created_at  - (дата и время создания, устанавливается автоматически)

    * Создайте эндпоинт

    ```
    GET /applications
    ```
    для получения списка заявок:

     - Поддержка фильтрации по имени пользователя (user_name)

     - Поддержка пагинации (параметры page и size).

2. PostgreSQL:

    - Спроектируйте таблицу для хранения заявок.
    - Используйте SQLAlchemy для работы с базой данных.

3. Kafka:

     - Настройте публикацию данных о новых заявках в топик Kafka.

     - В сообщении должно содержаться:

     ```
     id заявки
     user_name
     description
     created_at
     ```
4. Асинхронность:
    - Убедитесь, что все взаимодействия с Kafka и PostgreSQL реализованы асинхронно.

5. Docker:

    - Подготовьте Dockerfile и docker-compose.yml для локального запуска:

    ```
    Приложение (FastAPI)
    PostgreSQL
    Kafka
    ```

6. Документация:

    - Опишите инструкцию по запуску проекта.
    - Добавьте пример запроса и ответа для  эндпоинтов.

7. Дополнительно
     - Реализованные дополнительные функции будут преимуществом:

     - Валидация входящих данных с использованием Pydantic.

     - Логирование ошибок и событий в приложении.

     - Подготовка unit-тестов для ключевых компонентов.


## Реализация
В качетсве дополнительного функционала добавила
 - регистрацию и аутентификацию пользователя
 - поиск заявки по username автора
 - вывод заявок с возможностью фильтрации по дате создание (от-до)
 - получение одной заявки по uid
 - тестирование всех энпойтнов pytest_asyncio

## Доступные энпойнты

1. User
- Регистрация (создание ) пользоватлея

POST http://127.0.0.1:8000/application_service/api/v1/user/

REQUEST:
```
{
  "username": "Test",
  "email": "psk221221@gmail.com",
  "password": "12345678",
  "password_confirm": "12345678"
}
```
RESPONSE
```
{
  "username": "Test",
  "password": "$2b$12$c5s/Gs1P25P33ckKRS2yvuK8hU6pCmC.idYhH.AsGwFEbXig2F/1C",
  "uid": "6393ce73-7779-432c-85f7-20f9fb6f9768",
  "id": 3,
  "email": "psk221221@gmail.com"
}
```
- Аутентификация пользователя (Login)

POST http://127.0.0.1:8000/application_service/api/v1/user/login/

REQUEST
```
{
  "username": "Test",
  "password": "12345678"
}
```
RESPONSE
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7InVzZXJuYW1lIjoiVGVzdCIsInBhc3N3b3JkIjoiJDJiJDEyJGhNRWppQjRYUUxRWS9ZQXZMbGpQSC4xelA4SUU5aVBKU0V3NHlERFNwdG9UaHNCelpSTHEuIn0sInR5cGUiOiJhY2Nlc3MiLCJleHAiOjE3MzcyODYzMDgsImlhdCI6MTczNzI4NDUwOCwianRpIjoiM2VhYmI0NzItMGI4My00YmY4LTkxYTYtZGRkMzk0YWE3NjA3In0.we4Dh6Md1iO-bLmtUKnvSv29d0bfslIQrSBv_91S5N4",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7InVzZXJuYW1lIjoiVGVzdCIsInBhc3N3b3JkIjoiJDJiJDEyJGhNRWppQjRYUUxRWS9ZQXZMbGpQSC4xelA4SUU5aVBKU0V3NHlERFNwdG9UaHNCelpSTHEuIn0sInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzM3ODg5MzA4LCJpYXQiOjE3MzcyODQ1MDgsImp0aSI6IjIxYWZlNGU4LWU5NzMtNDQ0Yy1hNTcwLTIyYjJhODNhNDZiMiJ9.qk7McZ5RZauMvsCpoAD1qOeGwoKyIxSaLo6pARO8-FI",
  "token_type": "bearer"
}
```

- Refresh (обновление пары токенов после исчеткания срока жизни access)
POST http://127.0.0.1:8000/application_service/api/v1/user/refresh/

RESPONSE
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7InVzZXJuYW1lIjoiTmF0YXNoYSIsInBhc3N3b3JkIjoiJDJiJDEyJEdHb2Q0dUdEaHdDMTVNbXpzWEEvRmVGUzJVb3hWd0VHQmRDc1YvUDNrczBnLmVsbGZrM3pTIn0sInR5cGUiOiJhY2Nlc3MiLCJleHAiOjE3MzcyODkxMjEsImlhdCI6MTczNzI4NzMyMSwianRpIjoiYjRlY2U0OGUtMTU3MS00ZWI3LWEyZjAtZjRlMDJlZGJiM2IzIn0.jYE9x_ka7-CEk2t0EqdpFE0eAUYUatkj06s9DuVPt3k",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7InVzZXJuYW1lIjoiTmF0YXNoYSIsInBhc3N3b3JkIjoiJDJiJDEyJEdHb2Q0dUdEaHdDMTVNbXpzWEEvRmVGUzJVb3hWd0VHQmRDc1YvUDNrczBnLmVsbGZrM3pTIn0sInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzM3ODkyMTIxLCJpYXQiOjE3MzcyODczMjEsImp0aSI6IjRmNWU4NDdlLTdmMGItNDQ0OS1iY2Y5LTcxZWQ5MmQzODg1YiJ9.MMaOXRqXrajYxJSxO4TVLdAuka2ERdvg6pQL3X6jC1c",
  "token_type": "bearer"
}
```

- Logout

POST http://127.0.0.1:8000/application_service/api/v1/user/logout/

STATUS_CODE 200_OK

2. Application:

* Создание заявки (При создании заявки она так же публикуется в Topic Kafka)

  POST http://109.71.247.92:5000/application_service/api/v1/application/

REQUEST
```
{
  "description": "Description"
}
```
поле created_at созддается автоматически

id автора заявки (так же как и юзернейм)
получаются из текущего пользователя - который создает заявку

RESPONSE

```
{
  "description": "Description",
  "id": 1,
  "uid": "c0eb9232-65f1-4149-a81a-9042e1e1492e",
  "created_at": "2025-01-19T11:58:10.926992+00:00",
  "author_id": 1
}
```
- Получение одной заявки по UID

GET http://127.0.0.1:8000/application_service/api/v1/application/application_uid/

Пареметры - application_uid: uuid  (uid заявки)

RESPONSE
```
{
  "description": "Description",
  "uid": "c0eb9232-65f1-4149-a81a-9042e1e1492e",
  "author": {
    "id": 1,
    "username": "Test"
  }
}
```
- Поиск заявок по username автора

GET http://127.0.0.1:8000/application_service/api/v1/application/

Параметры

skip: int - количество записей которое необходимо пропустить (default=0)

limit: int - количество записей которое необходимо вывести на страницу  (default=20)

query: str - строка от 2х символов (поиск не учиьтывает регистр и работает с транслитерацией)

RESPONSE:
```
{
  "limit": 20,
  "offset": 0,
  "total": 1,
  "objects": [
    {
      "description": "Description",
      "uid": "c0eb9232-65f1-4149-a81a-9042e1e1492e",
      "author": {
        "id": 1,
        "username": "Test"
      }
    }
  ]
}
```
- Получение списка заявок с возможностью фильтрации по дате создания от-до

GET  http://127.0.0.1:8000/application_service/api/v1/application/all/

Параметры

skip: int - количество записей которое необходимо пропустить (default=0)

limit: int - количество записей которое необходимо вывести на страницу  (default=20)

created_at__gte : date (от) в формате гг-мм-дд

created_at__lte : date (до) в формате гг-мм-дд

RESPONSE
```
{
  "limit": 20,
  "offset": 0,
  "total": 1,
  "objects": [
    {
      "description": "Description",
      "uid": "c0eb9232-65f1-4149-a81a-9042e1e1492e",
      "author": {
        "id": 1,
        "username": "Test"
      }
    }
  ]
}
```
