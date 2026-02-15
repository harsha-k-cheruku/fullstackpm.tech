from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fullstackpm.tech"
    debug: bool = False
    base_dir: Path = Path(__file__).resolve().parent.parent
    content_dir: Path = base_dir / "content"
    templates_dir: Path = base_dir / "app" / "templates"
    static_dir: Path = base_dir / "app" / "static"

    # Database
    database_url: str = "sqlite:///./fullstackpm.db"

    # OpenAI API (for interview coach)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 2000

    # Multi-provider LLM settings
    google_api_key: str = ""  # For Gemini free tier
    anthropic_api_key: str = ""  # For fallback
    secret_key: str = ""  # Required for session encryption (min 32 chars)

    # Session security
    session_cookie_secure: bool = True  # HTTPS-only
    session_cookie_httponly: bool = True  # Prevent JS access
    session_cookie_samesite: str = "lax"  # CSRF protection
    session_max_age: int = 1800  # 30 minutes in seconds

    # Rate limiting
    free_tier_rate_limit: int = 50  # requests per hour
    byok_rate_limit: int = 1000  # requests per hour

    # Site metadata
    site_title: str = "fullstackpm.tech"
    site_description: str = "Portfolio of Harsha Cheruku — Full Stack AI Product Manager"
    site_author: str = "Harsha Cheruku"
    site_url: str = "https://fullstackpm.tech"

    # Social links
    github_url: str = "https://github.com/harsha-k-cheruku"
    linkedin_url: str = "https://linkedin.com/in/harshacheruku"
    rss_url: str = "/feed.xml"

    class Config:
        env_file = ".env"


settings = Settings()
