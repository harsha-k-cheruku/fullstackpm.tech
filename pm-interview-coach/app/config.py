"""pm-interview-coach/app/config.py
Application configuration using Pydantic Settings.
Loads from environment variables and .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # App metadata
    app_name: str = "PM Interview Coach"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./pm_interview_coach.db"

    # Anthropic API
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_max_tokens: int = 2000

    # Server
    host: str = "0.0.0.0"
    port: int = 8002
    reload: bool = True

    # CORS (for local development)
    cors_origins: list[str] = ["http://localhost:8002", "http://127.0.0.1:8002"]

    # Social links
    github_url: str = "https://github.com/harsha-k-cheruku"
    linkedin_url: str = "https://linkedin.com/in/harshacheruku"

    # Session management
    session_cookie_name: str = "pm_coach_session"
    session_max_age: int = 86400 * 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
