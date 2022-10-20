from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str

    # Get the Environment variables from the .env file
    class Config:
        env_file = ".env"


settings = Settings()
