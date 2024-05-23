from typing import Literal

from pydantic import BaseModel

class Training(BaseModel):
    """Класс тренировок"""
    title: str
    time: list[str]
    location: Literal['Зал 1', 'Зал 2', 'Зал 3']
    trainer: Literal['Анна', 'Мария', 'Захар']
    capacity: int
    age_limit: int
    class_type: Literal['Групповое', 'Индивидуальное']
    
class UserTrain(Training):
    """Класс тренировок пользователя"""
    date: str
    time: str