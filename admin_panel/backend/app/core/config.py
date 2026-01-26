from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "Baraka Admin Panel"
    debug: bool = False
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # Database
    database_url: str
    
    # Admin Init (for first run)
    first_admin_email: str = "admin@baraka.ai"
    first_admin_password: str = "change_me_immediately"

    model_config = {
        "env_file": ".env",
        "extra": "ignore" 
    }

@lru_cache()
def get_settings():
    return Settings()
