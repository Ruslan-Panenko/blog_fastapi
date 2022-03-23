from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from users.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'AdasdaQWDdqw55dSDqwd06as7D6a7sd72asd0'
ALGORYTHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORYTHM])
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORYTHM)
        id: str = payload.get('user_id')

        if id in None:
            raise credentials_exception
        token_date = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_date



def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f'Could not validate credentials',
                                          headers={'WWW-Authenticate': 'Bearer'})
    return verify_access_token(token, credentials_exception)
