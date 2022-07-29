from fastapi.responses import RedirectResponse
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserOut, UserAuth, TokenSchema, SystemUser
from uuid import uuid4
from config import *
from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
import SQL_CRUD
from app.deps import get_current_user

app = FastAPI()


@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    table = SQL_CRUD.SQL_CRUD(user=user,
                              password=password,
                              host=host,
                              port=port,
                              dbname=database,
                              table=users_table)

    table.connect()
    temp_user = table.get_with_email(data.email)
    if len(temp_user) != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    print("It's got till here")
    my_user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }

    # Insert into user database
    table.insert(
        user_id=my_user['id'],
        password=my_user['password'],
        email=data.email
    )
    table.commit()
    table.close()

    return my_user


@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = db.get(form_data.username, None)
    # querying database to check if user already exist
    table = SQL_CRUD.SQL_CRUD(user=user,
                              password=password,
                              host=host,
                              port=port,
                              dbname=database,
                              table=users_table)

    table.connect()
    temp_user = table.get_with_email(form_data.username)

    if len(temp_user) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    # print(type(temp_user))
    # print(temp_user)

    hashed_pass = temp_user[0][1]  # password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    table.commit()
    table.close()
    email = temp_user[0][2]
    return {
        "access_token": create_access_token(email),
        "refresh_token": create_refresh_token(email),
    }


@app.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(my_user: SystemUser = Depends(get_current_user)):
    print("called app.get_me")
    return my_user


# @app.get("/alert/create", tags=['ROOT'], response_model=dict)
# async def create_alert(my_user=Depends(get_current_user)) -> dict:
#     # print(my_user)
#     return {"Ping": "Surya"}

@app.get("/alert/create", tags=['ROOT'], response_model=dict)
async def create_alert(my_user=Depends(get_current_user)) -> dict:
    # print(my_user)
    return {"Ping": "Surya"}