# OAuth2 and JWT Authorization example from FastAPI docs
## Web server
```bash
uvicorn auth:app --reload
```
## Requirements
```bash
pip install python-multipart
pip install pyjwt
pip install "passlib[bcrypt]"
```
## Secret key to sign the JWT tokens
```bash
openssl rand -hex 32
```