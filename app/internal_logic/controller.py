from cryptography import fernet
import json

from .training import UserTrain
from .user import User


class Controller:
    def __init__(self, users: list[User] = []) -> None:
        """Ядро приложения, контролирует все действия над пользователем

        :param users: Список юзеров
        """
        self.users = {user.card_id: user for user in users}
        key = fernet.Fernet.generate_key()
        self.crypter = fernet.Fernet(key)
        
    def decrypt_auth_cookie(self, auth: str):
        """Расшифровывает данные из куки, возвращает user_id

        :param auth: куки
        """
        res = self.crypter.decrypt(auth.encode('utf-8'))
        data = json.loads(res.decode('utf-8'))
        return data['user_id']
    
    def create_auth_cookie(self, user: User):
        """Генерирует шифрованную строку для куки

        :param user: объект юзера
        :return: куки в байтах
        """
        res = self.crypter.encrypt(json.dumps({'user_id': user.card_id}).encode('utf-8'))
        return res
    
    def get_user(self, card_id: int):
        """Получает пользователя по id

        :param card_id: номер карточки пользователя
        """
        return self.users[card_id]

    def check_password(self, user: User, password: str):
        """Проверяет пароль пользователя

        :param user: объект юзера
        :param password: пароль для проверки
        :return: булево значение
        """
        return user.password == password

    def add_training(self, user: User, training: UserTrain):
        """Добавляет запись на тренировку пользователю

        :param user: объект пользователя
        :param training: запись на тренировку
        """
        user.trainings.append(training)
        
    def delete_training(self, user: User, train_id: int):
        """Удаляет запись у пользователя

        :param user: объект пользователя
        :param train_id: id тренировки
        """
        del user.trainings[train_id]