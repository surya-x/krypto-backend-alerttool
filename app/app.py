from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserOut, UserAuth, TokenSchema, SystemUser, Alert
from uuid import uuid4
import test_websocket
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

@app.post('/alert/create', tags=['ROOT'], summary="Create new alert", response_model=dict)
async def create_alert(alert_info: Alert, my_user=Depends(get_current_user)) -> dict:
    # print(my_user)
    # print(alert_info)
    table = SQL_CRUD.SQL_CRUD(user=user,
                              password=password,
                              host=host,
                              port=port,
                              dbname=database,
                              table=alerts_table)
    table.connect()
    print(str(my_user.id))

    table.insert(
        user_id=str(my_user.id),
        crypto_code=alert_info.crypto_code,
        trigger_value=alert_info.trigger_price,
        status='CREATED'
    )

    last_alert_id = table.get_last_id()[0][0]

    table.commit()
    table.close()

    test_websocket.push_to_lc(sym=alert_info.crypto_code, trigger=float(alert_info.trigger_price), alert_id=last_alert_id)

    return {"status": "created", "crypto_code": str(alert_info.crypto_code),
            "trigger_price": str(alert_info.trigger_price)}


@app.get('/alert', tags=['ROOT'], summary='Get details of all alerts with filters', response_model=dict)
async def fetch_all_alerts(status: str = "", my_user: SystemUser = Depends(get_current_user)) -> dict:
    table = SQL_CRUD.SQL_CRUD(user=user,
                              password=password,
                              host=host,
                              port=port,
                              dbname=database,
                              table=alerts_table)
    table.connect()

    if status == 'CREATED' or status == 'DELETED' or status == 'TRIGGERED':
        selected = table.get_all_alerts_with_status_and_user(user_id=str(my_user.id), status=status)
    else:
        selected = table.get_all_alerts_with_user(str(my_user.id))

    table.commit()

    table.close()

    my_list = []
    for each in selected:
        my_dict = {"alert_id": each[0], 'crypto_code': each[1], 'trigger_price': each[2], 'status': each[3]}
        my_list.append(my_dict)

    return {'data': my_list}


@app.put('/alert/delete', tags=['ROOT'], summary='Update status of alert', response_model=dict)
async def update_alerts(alert_id: int, my_user: SystemUser = Depends(get_current_user)) -> dict:
    table = SQL_CRUD.SQL_CRUD(user=user,
                              password=password,
                              host=host,
                              port=port,
                              dbname=database,
                              table=alerts_table)
    table.connect()

    new_status = "DELETED"
    table.update_status_of_alert(status=new_status, alert_id=alert_id)

    table.commit()

    table.close()

    return {"status": 200}
