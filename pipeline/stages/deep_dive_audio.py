"""Stage 7: synthesize audio for a deep_dive transcript via Edge TTS.

Voice mapping comes from Narada's config/voices.yaml (top 3 by rating + contrast):
  Believer → en-US-AndrewNeural  (m_andrew, good+, US male)
  Skeptic  → en-GB-RyanNeural    (gb_ryan, good, UK male)
  Realist  → en-US-AvaNeural     (f_ava, good, US female)

Outputs per episode:
  pipeline/data/deep_dives/episode-{id}/
    ├── segments/{NN-persona}.mp3   ← per-turn TTS files
    └── episode.mp3                  ← ffmpeg-concatenated final
"""
from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
from pathlib import Path
from typing import List

from pipeline import config

from app.database import SessionLocal
from app.models.pipeline_models import DeepDive


VOICE_MAP = {
    "believer": {"voice": "en-US-AndrewNeural", "label": "m_andrew (US M, good+)"},
    "skeptic":  {"voice": "en-GB-RyanNeural",   "label": "gb_ryan (UK M, good)"},
    "realist":  {"voice": "en-US-AvaNeural",    "label": "f_ava (US F, good)"},
}


async def _synth_turn(text: str, voice: str, out_path: Path) -> None:
    import edge_tts
    comm = edge_tts.Communicate(text, voice)
    await comm.save(str(out_path))


def _ffmpeg_concat(segments: List[Path], out_path: Path) -> None:
    """Concatenate mp3 segments. Re-encodes (not stream copy) so different
    voices/bitrates concat cleanly."""
    list_file = out_path.parent / "_concat.txt"
    # ffmpeg concat needs paths quoted only if they contain spaces; using -safe 0 + absolute paths
    list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in segments))
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-acodec", "libmp3lame", "-b:a", "128k",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    list_file.unlink(missing_ok=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr[-500:]}")


def run(deep_dive_id: int) -> dict:
    if not shutil.which("ffmpeg"):
        return {"stage": "deep_dive_audio", "error": "ffmpeg not on PATH — `brew install ffmpeg`"}

    db = SessionLocal()
    try:
        dd = db.query(DeepDive).filter(DeepDive.id == deep_dive_id).first()
        if not dd:
            return {"stage": "deep_dive_audio", "error": f"no deep_dive id={deep_dive_id}"}
        transcript = json.loads(dd.transcript_json)
        topic = dd.topic
    finally:
        db.close()

    out_dir = config.PIPELINE_ROOT / "data" / "deep_dives" / f"episode-{deep_dive_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    seg_dir = out_dir / "segments"
    seg_dir.mkdir(exist_ok=True)

    print(f"\n══ AUDIO: deep_dive {deep_dive_id} ══")
    print(f"  Topic: {topic}")
    for k, v in VOICE_MAP.items():
        print(f"  {k:<10} → {v['label']}")

    segment_paths: List[Path] = []
    for i, turn in enumerate(transcript):
        persona = turn["persona"]
        text = (turn.get("text") or "").strip()
        if not text or text.startswith("["):
            print(f"  [{i+1:02d}] {persona}: SKIP (empty/error)")
            continue
        cfg = VOICE_MAP.get(persona)
        if not cfg:
            print(f"  [{i+1:02d}] {persona}: SKIP (no voice mapped)")
            continue
        seg_path = seg_dir / f"{i:02d}-{persona}.mp3"
        preview = text[:60] + ("…" if len(text) > 60 else "")
        print(f"  [{i+1:02d}] {turn['name']:<14} ({cfg['voice']:<22}) — {preview}")
        try:
            asyncio.run(_synth_turn(text, cfg["voice"], seg_path))
            segment_paths.append(seg_path)
        except Exception as exc:
            print(f"      ! TTS failed: {exc}")

    if not segment_paths:
        return {"stage": "deep_dive_audio", "error": "no segments synthesized"}

    final_path = out_dir / "episode.mp3"
    print(f"\n  Mixing {len(segment_paths)} segments → {final_path.name}")
    try:
        _ffmpeg_concat(segment_paths, final_path)
    except Exception as exc:
        return {"stage": "deep_dive_audio", "error": str(exc)}

    print(f"  ✓ {final_path}")
    return {
        "stage": "deep_dive_audio",
        "deep_dive_id": deep_dive_id,
        "episode_path": str(final_path),
        "segment_count": len(segment_paths),
        "voice_map": {k: v["voice"] for k, v in VOICE_MAP.items()},
    }
