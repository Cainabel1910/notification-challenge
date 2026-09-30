from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    password_min_length: int
    password_require_uppercase: bool
    password_require_number: bool
    password_require_symbol: bool
    
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiration_minutes: int
    
    sms_max_length: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()