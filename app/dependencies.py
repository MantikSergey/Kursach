from cryptography import fernet
from fastapi import Cookie, HTTPException, status

try:
    from internal_logic import Controller, User, Training
except ImportError:
    from .internal_logic import Controller, User, Training

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

CONTROLLER = Controller()
key = fernet.Fernet.generate_key()
CRYPTER = fernet.Fernet(key)

TRAINS = [
    Training(title='Йога', time=["10:00", "11:00", "12:00"], location='Зал 1', trainer='Анна', capacity=20, age_limit=16, class_type='Групповое'),
    Training(title='Бокс', time=["18:00", "20:00"], location='Зал 2', trainer='Захар', capacity=1, age_limit=18, class_type="Индивидуальное"),
    Training(title='Пилатес', time=["13:00", "14:00", "15:00"], location='Зал 3', trainer='Мария', capacity=10, age_limit=16, class_type='Групповое')
]

def get_user_from_header(*, authorization: str = Cookie(None)) -> User:
    try:
        user_id = CONTROLLER.decrypt_auth_cookie(authorization)
        return CONTROLLER.get_user(user_id)
    except Exception as e:
        print(e)
        raise credentials_exception
