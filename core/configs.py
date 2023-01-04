from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR:str = "/api/v1"
    DB_URL:str = 'mysql+asyncmy://root:''@localhost:3306/hoteis'
    DBBaseModel = declarative_base()
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()


