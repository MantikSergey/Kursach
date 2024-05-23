import json
import pytest
import datetime

from app.internal_logic import Controller, User, UserTrain
from app.dependencies import TRAINS

@pytest.fixture
def prepare_data(request):
    user = User(card_id=1, password='test', trainings=[])
    controller = Controller([user])
    return user, controller

@pytest.fixture
def train(request):
    return UserTrain(title='Бокс', 
                     time='10:00', 
                     location='Зал 1', 
                     trainer='Анна', 
                     capacity=10, 
                     age_limit=10, 
                     class_type='Групповое',
                     date=str(datetime.datetime.now().date()))

@pytest.fixture
def controller_cookie(request):
    controller = Controller()
    data = json.dumps({'user_id': 1}).encode()
    cookie = controller.crypter.encrypt(data).decode()
    return controller, cookie

class TestController:
    
    def test_get_user(self, prepare_data):
        user: User = prepare_data[0]
        controller: Controller = prepare_data[1]
        user_in_bd = controller.get_user(user.card_id)
        assert user_in_bd == user

    def test_add_train(self, prepare_data, train):
        
        user: User = prepare_data[0]
        controller: Controller = prepare_data[1]
        assert train not in user.trainings # проверям, что такой записи вообще нет
        controller.add_training(user, train)
        user = controller.get_user(user.card_id) # обновляем инстанс юзера
        assert train in user.trainings
        
    def test_delete_train(self, prepare_data, train):
        
        user: User = prepare_data[0]
        controller: Controller = prepare_data[1]
        user.trainings = [train]
        controller.delete_training(user, 0)
        user = controller.get_user(user.card_id) # обновляем инстанс юзера
        assert train not in user.trainings
        
    def test_create_cookie(self, prepare_data):
        
        user: User = prepare_data[0]
        controller: Controller = prepare_data[1]
        cookie = controller.create_auth_cookie(user)
        assert isinstance(cookie, bytes) # просто проверяем, что функция вызывается и возвращает результат, тк для расшифровки есть другой тест

    def test_decrypt_cookie(self, controller_cookie):
        
        controller: Controller = controller_cookie[0]
        cookie: str = controller_cookie[1]
        assert controller.decrypt_auth_cookie(cookie)