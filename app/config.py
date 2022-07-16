# this class contains environment varibles like username and password to connet to DB
# we can give this varaibles default values 

from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str
    database_password: str = "password"
    database_name: str 
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    # opening the .env file to read the val for enviroment varibles
    class Config: 
        env_file = ".env"
    
    
# an objec form class Settings
settings = Settings()    