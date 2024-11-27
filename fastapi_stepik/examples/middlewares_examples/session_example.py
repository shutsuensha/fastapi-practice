from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="7UzGQS7woBazLUtVQJG39ywOP7J7lkPkB0UmDhMgBR8=")


@app.get("/create_session")
async def session_set(request: Request):
    request.session["my_session"] = "1234"
    return 'ok'


@app.get("/read_session")
async def session_info(request: Request):
    my_var = request.session.get("my_session")
    return my_var

@app.get("/delete_session")
async def session_delete(request: Request):
    my_var = request.session.pop("my_session")
    return my_var
