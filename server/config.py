from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = ""
    database_test_hostname: str = ""
    database_port: str = ""
    database_name: str = ""
    database_password: str = ""
    database_username: str = ""
    server_address: str = ""
    server_port: int = 8000
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 60

    base_url_dev: str = ""
    base_url_prod: str = ""
    base_url_test: str = ""

    # Get the Environment variables from the .env file
    class Config:
        env_file = ".env"


settings = Settings()
