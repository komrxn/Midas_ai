from __future__ import annotations

import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    telegram_bot_token: str = Field(alias="TELEGRAM_BOT_TOKEN")
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    supabase_url: str = Field(alias="SUPABASE_URL")
    supabase_anon_key: str = Field(alias="SUPABASE_ANON_KEY")
    redis_url: str = Field(alias="REDIS_URL")
    default_currency: str = Field(default="uzs", alias="DEFAULT_CURRENCY")

    class Config:
        populate_by_name = True


def get_settings() -> Settings:
    return Settings(**os.environ)
