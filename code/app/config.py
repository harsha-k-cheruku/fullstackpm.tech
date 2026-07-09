import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fullstackpm.tech"
    debug: bool = False
    base_dir: Path = Path(__file__).resolve().parent.parent
    content_dir: Path = base_dir / "content"
    templates_dir: Path = base_dir / "app" / "templates"
    static_dir: Path = base_dir / "app" / "static"
    data_dir: Path = base_dir / "app" / "data"

    # Database
    database_url: str = "sqlite:///./fullstackpm.db"

    # OpenAI API (for interview coach)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 2000

    # Anthropic API (for feed AI processing)
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-haiku-4-5-20251001"

    # Editorial dashboard token (set via env var EDITORIAL_TOKEN)
    editorial_token: str = "fspm-editorial-2026"

    # Options Intel webhook receiver token. Must be configured in production.
    options_intel_webhook_token: str = os.getenv("OPTIONS_INTEL_WEBHOOK_TOKEN", "")

    # Google Sheets Newsletter
    google_sheets_credentials_path: str = os.getenv(
        "GOOGLE_SHEETS_CREDENTIALS_PATH",
        str(base_dir / "secrets" / "credentials.json")  # Use absolute path
    )
    google_sheets_id: str = os.getenv("GOOGLE_SHEETS_ID", "19-FyJ8gKiqodVBGnyAYIlvJ9Tun9NYU02AdvUM12T3Q")

    # JoSAA tool dataset
    josaa_data_path: str = os.getenv(
        "JOSAA_DATA_PATH",
        "/Users/sidc/Projects/josaa-data-pipeline/data/normalized/josaa_master.csv",
    )
    josaa_csv_url: str = os.getenv("JOSAA_CSV_URL", "")
    josaa_download_path: str = os.getenv("JOSAA_DOWNLOAD_PATH", "/tmp/josaa_master.csv")
    josaa_compute_enabled: bool = os.getenv("JOSAA_COMPUTE_ENABLED", "false").lower() == "true"

    # Site metadata
    site_title: str = "fullstackpm.tech"
    site_description: str = "Portfolio of Harsha Cheruku — Full Stack AI Product Manager"
    site_author: str = "Harsha Cheruku"
    site_url: str = "https://fullstackpm.tech"

    # Social links
    github_url: str = "https://github.com/harsha-k-cheruku"
    linkedin_url: str = "https://linkedin.com/in/harshacheruku"
    rss_url: str = "/feed.xml"
    twitter_handle: str = "@fullstackpmtech"
    og_image: str = "https://fullstackpm.tech/static/img/FSPM.png"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
