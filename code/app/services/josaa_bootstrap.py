from __future__ import annotations

from pathlib import Path
import gzip
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

    try:
        print(f"[josaa-bootstrap] Downloading dataset from URL to {target}")
        with urlopen(settings.josaa_csv_url, timeout=120) as resp:
            data = resp.read()
        target.write_bytes(data)

        final_path = target
        if str(target).endswith('.gz') or settings.josaa_csv_url.lower().endswith('.gz'):
            unzipped = target.with_suffix('')
            print(f"[josaa-bootstrap] Detected gzip. Extracting to {unzipped}")
            with gzip.open(target, 'rb') as fin, open(unzipped, 'wb') as fout:
                while True:
                    chunk = fin.read(1024 * 1024)
                    if not chunk:
                        break
                    fout.write(chunk)
            final_path = unzipped

        settings.josaa_data_path = str(final_path)
        print(f"[josaa-bootstrap] Dataset ready: {final_path} ({final_path.stat().st_size} bytes)")
        return str(final_path)
    except Exception as exc:
        print(f"[josaa-bootstrap] Download failed: {exc}")
        print(f"[josaa-bootstrap] Falling back to configured path: {current}")
        return str(current)
