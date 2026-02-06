from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    redis_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_expires_min: int = 15
    jwt_refresh_expires_days: int = 7

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
