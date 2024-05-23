from pydantic import BaseModel, Field

from .training import UserTrain

class User(BaseModel):
    """Объект пользователя
    """
    card_id: int
    password: str
    trainings: list[UserTrain] = Field(default_factory=list)
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, BaseModel):
            return self.model_dump() == value.model_dump()
        else:
            return self == value