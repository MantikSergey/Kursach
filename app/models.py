from pydantic import BaseModel


class Credentials(BaseModel):
    
    user_id: int
    password: str
    
class TrainsData(BaseModel):
    
    headers: list[str]
    rows: list[list]
