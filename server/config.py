from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str
    server_address: str
    server_port: int

    # Get the Environment variables from the .env file
    class Config:
        env_file = ".env"


settings = Settings()
