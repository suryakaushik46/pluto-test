from pydantic import BaseSettings

class Settings(BaseSettings):
    """_summary_:
        mapper to .env file variables
     
    Args:
        BaseSettings (_type_): _description_
    """
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    database_schema_name:str
    class Config:
        env_file=".env"

settings=Settings()
