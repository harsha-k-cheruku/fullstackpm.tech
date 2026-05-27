from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen

from app.config import settings


def ensure_josaa_dataset() -> str:
    """Ensure JoSAA CSV exists locally.

    Priority:
    1) If JOSAA_DATA_PATH already exists -> use it.
    2) Else if JOSAA_CSV_URL provided -> download to JOSAA_DOWNLOAD_PATH.
    3) Else keep existing path (caller/tool will raise clear file-not-found later).
    """
    current = Path(settings.josaa_data_path)
    if current.exists():
        print(f"[josaa-bootstrap] Using existing dataset: {current}")
        return str(current)

    if not settings.josaa_csv_url:
        print(
            "[josaa-bootstrap] Dataset missing and JOSAA_CSV_URL not set. "
            f"Current path: {current}"
        )
        return str(current)

    target = Path(settings.josaa_download_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    print(f"[josaa-bootstrap] Downloading dataset from URL to {target}")
    with urlopen(settings.josaa_csv_url, timeout=60) as resp:
        data = resp.read()
    target.write_bytes(data)

    settings.josaa_data_path = str(target)
    print(f"[josaa-bootstrap] Dataset ready: {target} ({target.stat().st_size} bytes)")
    return str(target)
