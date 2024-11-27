from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com", "127.0.0.1"]
)


@app.get("/")
async def main():
    return {"message": "Hello World"}