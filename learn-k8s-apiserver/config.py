from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    db_host: str = "db.local.testapp.private"
    db_port: int = 3306
    db_driver: str = "mysql+pymysql"
    db_username: str = "badmin"
    db_password: str = "vagrant"
    db_database: str = "appdb"
    db_echo : bool = True

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()