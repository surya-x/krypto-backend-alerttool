from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from config import *
from jose import jwt
from pydantic import ValidationError
from app.schemas import TokenPayload, SystemUser
import SQL_CRUD


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    try:
        print("started me")
        # reuseable_oauth.
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        # print(token_data)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # querying database to check if user already exist
    table = SQL_CRUD.SQL_CRUD(user=user,
                              password=password,
                              host=host,
                              port=port,
                              dbname=database,
                              table=users_table)

    table.connect()
    my_user = table.get_with_email(token_data.sub)
    table.commit()

    if len(my_user) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    table.close()
    print(my_user)
    user_mapping: Union[dict[str, Any], None] = {
        'email': my_user[0][2],
        'password': my_user[0][1],
        'id': my_user[0][0],
    }
    return SystemUser(**user_mapping)
    # return True