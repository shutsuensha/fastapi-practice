from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import uuid
import jwt
from src.config import Config
import logging
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


passwd_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict , expiry:timedelta =None, refresh: bool= False) -> str:
    payload = {
        'user':user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        'jti': str(uuid.uuid4()),
        'refresh' : refresh
    }


    token = jwt.encode(
        payload=payload,
        key= Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as jwte:
        logging.exception(jwte)
        return None

    except Exception as e:
        logging.exception(e)
        return None
    
salt="email-configuration"
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt=salt
)

def create_url_safe_token(data: dict, expiration=3600):
    """Serialize a dict into a URLSafe token"""

    return serializer.dumps(data, salt=salt)


def decode_url_safe_token(token: str, max_age=3600):
    """Deserialize a URLSafe token to get data"""
    try:
        token_data = serializer.loads(token, salt=salt, max_age=max_age)

        return token_data

    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")