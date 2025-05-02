# FastAPI: Must-Have для собеседования

## 1. Что такое FastAPI и чем он отличается от других фреймворков, таких как Flask или Django?

**FastAPI** — это современный фреймворк для создания RESTful API с фокусом на асинхронность, высокую производительность и типизацию с использованием Python type hints.
- **Отличия**:
  - FastAPI использует Python type hints для автоматической генерации документации (OpenAPI), в отличие от Flask и Django.
  - Он поддерживает асинхронность (async/await), что позволяет обрабатывать тысячи запросов параллельно, чем Flask и Django, которые используют синхронные обработчики.
  - FastAPI генерирует документацию по умолчанию, а Flask и Django требуют дополнительной настройки или сторонних библиотек (например, Flask-RESTful).

## 2. Как работают маршруты (endpoints) в FastAPI?

Маршруты создаются с помощью декораторов, таких как `@app.get()`, `@app.post()`, `@app.put()` и других HTTP-методов. Эти декораторы привязываются к соответствующим функциям, которые обрабатывают запросы.

Пример:

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

## 3. Что такое path parameters и query parameters в FastAPI? Приведи примеры.

- **Path parameters** — параметры, указанные в URL.
  Пример:

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

- **Query parameters** — параметры, передаваемые через строку запроса.
  Пример:

@app.get("/items/")
def read_items(q: str = None):
    return {"q": q}

## 4. Как работает автоматическая генерация OpenAPI документации в FastAPI?

FastAPI автоматически генерирует документацию с использованием OpenAPI, которая доступна по адресу `/docs` или `/redoc`. Документация создается на основе аннотаций типов и схем Pydantic, которые описывают запросы и ответы.

## 5. Когда и почему ты должен использовать `async def` вместо обычных функций?

Использование `async def` необходимо для асинхронных операций, таких как запросы к базе данных, внешним API и файловым системам, которые могут занять время. Это позволяет выполнять другие задачи, пока выполняется операция ввода-вывода, улучшая производительность и отзывчивость.

Пример:

@app.get("/items/")
async def get_items():
    items = await fetch_items_from_db()
    return items

## 6. Что произойдет, если забыть использовать `await` в асинхронной функции?

Если забыть использовать `await`, асинхронная операция не будет выполнена корректно, и код будет выполняться синхронно, что может привести к блокировке и снижению производительности.

## 7. Как FastAPI работает с асинхронными базами данных (например, с PostgreSQL)?

FastAPI позволяет использовать асинхронные библиотеки для работы с базами данных, например, `asyncpg` или `databases`. Это позволяет делать запросы к базе данных без блокировки основного потока.

Пример с `asyncpg`:

import asyncpg
async def get_user(user_id: int):
    conn = await asyncpg.connect(user='user', password='password', database='test')
    row = await conn.fetchrow('SELECT * FROM users WHERE id=$1', user_id)
    await conn.close()
    return row

## 8. Что такое dependency injection в FastAPI и как работает `Depends()`?

**Dependency Injection** позволяет инжектировать зависимости в функцию обработки маршрута, например, подключение к базе данных или авторизацию. В FastAPI это делается с помощью `Depends()`.

Пример:

from fastapi import Depends

def get_db():
    db = DBConnection()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: DBConnection = Depends(get_db)):
    return db.get_items()

## 9. Как работают вложенные зависимости с `Depends()`?

Вложенные зависимости позволяют инжектировать одну зависимость внутри другой. Например, можно создать зависимость для подключения к базе данных и еще одну для выполнения транзакций.

Пример:

def get_db():
    db = DBConnection()
    try:
        yield db
    finally:
        db.close()

def get_user(db: DBConnection, user_id: int):
    return db.get_user(user_id)

@app.get("/user/{user_id}")
def read_user(user: dict = Depends(get_user)):
    return user

## 10. Как работают модели Pydantic в FastAPI для валидации данных?

**Pydantic** используется для валидации и сериализации данных, полученных от пользователя. Модели Pydantic описывают структуру данных и проверяют их типы.

Пример:

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item

## 11. Как кастомизировать валидаторы в Pydantic?

В Pydantic можно использовать `@root_validator` и `@validator` для кастомной валидации данных.

Пример:

from pydantic import BaseModel, validator

class Item(BaseModel):
    name: str
    price: float

    @validator("name")
    def name_must_be_capitalized(cls, v):
        if not v[0].isupper():
            raise ValueError("Name must be capitalized")
        return v

## 12. Какая разница между `parse_obj` и `model_validate` в Pydantic v2?

- **`parse_obj()`** — используется для преобразования данных в модель Pydantic.
- **`model_validate()`** — улучшенная версия в Pydantic v2, которая позволяет проводить валидацию и инициализацию модели, сохраняя дополнительные возможности для кастомизации и асинхронных операций.

## 13. Почему FastAPI использует типизацию Python?

**Типизация** помогает автоматически генерировать OpenAPI документацию и позволяет FastAPI проверять данные на соответствие типам до выполнения функции, улучшая читаемость и надежность кода.

## 14. Как обрабатывать ошибки в FastAPI, используя HTTPException?

**HTTPException** используется для поднятия ошибок с кастомными сообщениями и статусами.

Пример:

from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

## 15. Как ты тестируешь FastAPI приложение?

Для тестирования можно использовать `TestClient` и `pytest`.

Пример:

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": None}

## 16. Как реализовать JWT-аутентификацию в FastAPI?

Для JWT-аутентификации нужно создать и проверять токены с помощью библиотеки `pyjwt`.

Пример:

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_token(token: str):
    try:
        return jwt.decode(token, "secret_key", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

## 17. Как упаковать FastAPI приложение в Docker контейнер?

Пример `Dockerfile`:

FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
