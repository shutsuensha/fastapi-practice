
# FastAPI + SQLAlchemy: Must-Have для собеседования

## 1. Как устроен database session через Depends (get_db)

FastAPI использует Depends для внедрения зависимости подключения к базе данных. Обычно создается функция `get_db`, которая инициализирует сессию, отдает её через `yield`, а затем закрывает. Это позволяет использовать одну и ту же сессию в разных обработчиках и автоматически закрывать соединение после выполнения запроса.

Пример:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```
## 2. Разница между ORM и SQLAlchemy Core

- **SQLAlchemy ORM** — объектно-реляционная модель, где таблицы отображаются как Python-классы. Операции производятся через объекты, а не SQL-запросы напрямую.
- **SQLAlchemy Core** — низкоуровневый API, предоставляющий декларативное описание таблиц и явное написание SQL-запросов, ближе к "чистому SQL".

ORM пример:
```python
user = db.query(User).filter(User.id == 1).first()
```
Core пример:
```python
stmt = select(users_table).where(users_table.c.id == 1)
result = connection.execute(stmt)
```
## 3. Lazy-loading vs eager-loading (joinedload, selectinload)

- **Lazy-loading** — связанные объекты загружаются при первом обращении к ним (по умолчанию). Может привести к множеству дополнительных запросов (N+1 проблема).
- **Eager-loading** — связанные объекты загружаются сразу, что сокращает количество запросов к базе данных.

- `joinedload` — делает SQL JOIN и сразу загружает связанные объекты.
- `selectinload` — делает отдельный SELECT-запрос, более эффективен при множестве родительских объектов.

Пример joinedload:
```python
user = db.query(User).options(joinedload(User.items)).first()
```
Пример selectinload:
```python
users = db.query(User).options(selectinload(User.items)).all()
```
## 4. Почему важно использовать scoped_session или sessionmaker в Depends

- `sessionmaker` гарантирует, что для каждого запроса создается новая, независимая сессия.
- `scoped_session` используется в многопоточном окружении (например, в старых приложениях), чтобы изолировать сессии по потоку.

Важно: никогда не использовать глобальную сессию. Она может привести к утечке памяти, гонкам данных и ошибкам транзакций.

Создание sessionmaker:
```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Используется внутри Depends:

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
## 5. Как писать CRUD-логику с separation of concerns (router → service → repo)

**Separation of concerns** — принцип разделения ответственности:
- **Router** — принимает HTTP-запросы, валидирует вход, вызывает сервис.
- **Service** — бизнес-логика, оркестрация, проверка условий.
- **Repository** — прямое взаимодействие с базой данных (CRUD).

Пример:

Router:
```python
@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)
```
Service:
```python
def get_user_by_id(db: Session, user_id: int):
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```
Repository:
```python
def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
```
