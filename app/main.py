from pathlib import Path

import uvicorn
from fastapi import FastAPI, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from dependencies import get_user_from_header

from internal_logic import User, UserTrain
from models import Credentials, TrainsData
from dependencies import CONTROLLER, credentials_exception, TRAINS

users = [
    User(card_id=123, password='test')
]

for user in users:
    CONTROLLER.users[user.card_id] = user

currnet_path = Path(__file__).absolute().parent
app = FastAPI()
path = currnet_path / Path('static')
app.mount('/static', StaticFiles(directory=str(path)), name="static")

TRAINS_DATA = TrainsData(headers=[
    'Номер',
    'Занятие',
    'Время',
    'Помещение',
    'Тренер',
    'Свободные места',
    'Возрастное ограничение',
    'Тип'
    ],
    rows=[
    [i.title, i.time, i.location, i.trainer, i.capacity, i.age_limit, i.class_type] for i in TRAINS
])

with open(currnet_path / Path('pages/auth.html')) as f:
    AUTH_PAGE = HTMLResponse(f.read())
    
with open(currnet_path / Path('pages/trains.html')) as f:
    TRAINS_PAGE = HTMLResponse(f.read())
    
with open(currnet_path / Path('pages/my_trains.html')) as f:
    MY_TRAINS_PAGE = HTMLResponse(f.read())

@app.get("/")
async def login():
    return AUTH_PAGE

@app.post("/api/login")
async def auth(credentials: Credentials):
    try:
        user = CONTROLLER.get_user(credentials.user_id)
    except KeyError:
        raise credentials_exception
    if user.password != credentials.password:
        raise credentials_exception
    cookie = CONTROLLER.create_auth_cookie(user).decode()
    response = Response()
    response.set_cookie(key='authorization', value=cookie, httponly=True, samesite="none")
    return response


@app.get("/api/trains_page")
async def all_trains(user: User = Depends(get_user_from_header)):
    return TRAINS_PAGE

@app.get("/api/trains")
async def get_train_data(user: User = Depends(get_user_from_header)) -> TrainsData:
    return TRAINS_DATA


@app.get("/api/my_trains_page")
async def my_trains(user: User = Depends(get_user_from_header)):
    return MY_TRAINS_PAGE

@app.get("/api/my_trains")
async def get_my_trains(user: User = Depends(get_user_from_header)) -> TrainsData:
    data = TrainsData(headers=[
        'Номер',
        'Занятие',
        'Время',
        'Помещение',
        'Тренер',
        'Свободные места',
        'Возрастное ограничение',
        'Тип',
        'Дата'
    ], rows=[])
    for i in user.trainings:
        row = [i.title, i.time, i.location, i.trainer, i.capacity, i.age_limit, i.class_type, i.date]
        data.rows.append(row)
    return data

@app.post("/api/create_train")
async def create_train(train_id: int, date: str, time: str, user: User = Depends(get_user_from_header)):
    train = TRAINS[train_id]
    train = train.model_dump()
    train['time'] = time
    train['date'] = date
    train = UserTrain.model_validate(train)
    CONTROLLER.add_training(user, train)
    return Response(status_code=201)

@app.delete("/api/delete_train")
async def delete_train(train_id: int, user: User = Depends(get_user_from_header)):
    CONTROLLER.delete_training(user, train_id)
    return Response()

if __name__=='__main__':
    uvicorn.run(app, port=1337)