"""Stage 6: AI-vs-AI-vs-AI roundtable.

Three personas, three providers, N rounds. Transcript-only — voices added
later via Narada. Each turn engages the prior speaker by name; the closing
turn (Realist) synthesizes + names the PM action.

Personas:
  Believer (GPT)     — sees AI as transformative, bullish, evidence-based
  Skeptic  (Grok)    — calls out hype, demands evidence, counter-takes
  Realist  (Claude)  — synthesizes, names what a PM should actually do
"""
from __future__ import annotations

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from pipeline import config
from pipeline.llm import chat

from app.database import SessionLocal, ensure_pipeline_tables, init_db
from app.models.feed_article import FeedArticle
from app.models.pipeline_models import ArticleAnalysis, DeepDive


PERSONAS: Dict[str, dict] = {
    "believer": {
        "name": "The Believer",
        "provider": config.BELIEVER_PROVIDER,
        "model": config.BELIEVER_MODEL,
        "system": (
            "You are The Believer — a senior product manager and AI builder who sees AI as the most "
            "important technological shift of our lifetime. You're not naive about risks, but you think "
            "the upside dominates the discussion. You read every paper, run your own experiments, ship "
            "AI-native features. In conversations with skeptics and realists, you push back on doom "
            "narratives with specific evidence and recent capability gains. Persuasive, not preachy. "
            "Direct, occasionally provocative, never academic. Speak in first person — this is a "
            "podcast roundtable, not an essay. Never say 'As an AI'. Keep responses 80-150 words."
        ),
    },
    "skeptic": {
        "name": "The Skeptic",
        "provider": config.SKEPTIC_PROVIDER,
        "model": config.SKEPTIC_MODEL,
        "system": (
            "You are The Skeptic — a senior product manager with two decades of seeing tech hype "
            "cycles. VR, crypto, metaverse, now AI. You think AI is useful, but you call BS on inflated "
            "claims, missed timelines, benchmark fetishism. You demand evidence, you smell vendor "
            "incentives, you remember when previous 'breakthroughs' fizzled. Anti-hype, not anti-AI. "
            "Push back specifically — name what's wrong with the bullish take. Sharp, occasionally "
            "biting, never cynical for its own sake. Speak in first person — this is a podcast "
            "roundtable. Never say 'As an AI'. Keep responses 80-150 words."
        ),
    },
    "realist": {
        "name": "The Realist",
        "provider": config.REALIST_PROVIDER,
        "model": config.REALIST_MODEL,
        "system": (
            "You are The Realist — a senior product manager who actually ships into the real world "
            "with real customers and real budgets. You don't argue from ideology — you argue from what "
            "works in production. You take the Believer's energy and the Skeptic's pushback and find "
            "the actionable middle. You name the specific decisions a PM should make today, given the "
            "uncertainty. Not boring, not fence-sitting — you have opinions, grounded in what "
            "enterprises actually do. Speak in first person — this is a podcast roundtable. Never say "
            "'As an AI'. Keep responses 80-150 words."
        ),
    },
}

TURN_ORDER = ["believer", "skeptic", "realist"]


def _format_history(transcript: List[dict]) -> str:
    return "\n\n".join(f"{t['name']}: {t['text']}" for t in transcript)


_CLOSING_PREAMBLE = (
    "This is the CLOSING turn. You are {me}. {believer} and {skeptic} will NOT respond after you — "
    "do not leave threads dangling, do not end on a question directed at them. Acknowledge where "
    "they each had a point and where the discussion left things unresolved. End with a closing "
    "thought that signals the conversation is complete (not a cliffhanger)."
)

_CLOSING_BY_MODE = {
    "force": (
        " Synthesize what's been said. Name one specific thing a PM listening to this should do "
        "tomorrow morning. Land it sharp. 120-200 words."
    ),
    "optional": (
        " Synthesize what's been said. If a clean, non-obvious PM action actually falls out of "
        "this discussion, name it. If it doesn't, DON'T force one — it's fine to land on a sharp "
        "observation or an unresolved tension. Don't manufacture a takeaway. 120-200 words."
    ),
    "off": (
        " Synthesize what's been said. End on a sharp observation. Do NOT give PM advice or "
        "'here's what to do' takeaways — that's not this episode's frame. 120-200 words."
    ),
}

_LENGTH_INSTRUCTIONS = {
    "short":  "Interject briefly — 40-80 words. Quick and sharp, no setup.",
    "normal": "80-150 words.",
    "long":   "Develop the argument — 200-280 words. Take the time to make the case properly.",
}


def _build_turn_prompt(
    persona_key: str,
    transcript: List[dict],
    topic_context: str,
    is_first: bool,
    is_final: bool,
    length_mode: str = "normal",
    pm_action_mode: str = "optional",
) -> str:
    me = PERSONAS[persona_key]["name"]

    if is_first:
        length = _LENGTH_INSTRUCTIONS.get(length_mode, _LENGTH_INSTRUCTIONS["normal"])
        return (
            f"{topic_context}\n\n"
            "You're opening a roundtable discussion on this topic. Lead with your strongest take. "
            "Be specific — name what's actually happening, not generalities. Don't introduce yourself "
            f"or restate the topic — just dive in. {length}"
        )

    history = _format_history(transcript)
    last = transcript[-1]
    last_name = last["name"]

    if is_final:
        preamble = _CLOSING_PREAMBLE.format(
            me=me,
            believer=PERSONAS["believer"]["name"],
            skeptic=PERSONAS["skeptic"]["name"],
        )
        closing_body = _CLOSING_BY_MODE.get(pm_action_mode, _CLOSING_BY_MODE["optional"])
        return f"{topic_context}\n\nDISCUSSION SO FAR:\n{history}\n\n{preamble}{closing_body}"

    length = _LENGTH_INSTRUCTIONS.get(length_mode, _LENGTH_INSTRUCTIONS["normal"])
    return (
        f"{topic_context}\n\n"
        f"DISCUSSION SO FAR:\n{history}\n\n"
        f"It's your turn. You are {me}. {last_name} just spoke. Engage directly — push back, build "
        f"on it, or take it somewhere new. Reference {last_name} by name. Don't just dump your own "
        f"take in a vacuum. {length}"
    )


def _pick_next_speaker(transcript: List[dict], excluded: List[str] = None) -> str:
    """Weighted random pick — biased toward whoever spoke least in last 4 turns."""
    excluded = excluded or []
    prev = transcript[-1]["persona"] if transcript else None
    candidates = [p for p in TURN_ORDER if p != prev and p not in excluded]
    counts = {p: 0 for p in candidates}
    for t in transcript[-4:]:
        if t["persona"] in counts:
            counts[t["persona"]] += 1
    weights = [1.0 / (counts[p] + 1) for p in candidates]
    return random.choices(candidates, weights=weights)[0]


def _pick_length_mode() -> str:
    r = random.random()
    if r < 0.20:
        return "short"
    if r < 0.85:
        return "normal"
    return "long"


def _resolve_personas(depth: str) -> Dict[str, dict]:
    """Apply depth profile to PERSONAS — overrides model field per tier."""
    profile = config.DEEP_DIVE_DEPTH_PROFILES.get(depth, config.DEEP_DIVE_DEPTH_PROFILES["standard"])
    resolved = {}
    for key, base in PERSONAS.items():
        resolved[key] = {**base, "model": profile[f"{key}_model"]}
    return resolved


def _context_from_article(article_id: int) -> Tuple[Optional[str], Optional[str]]:
    """Return (topic, source_context) for an analysed article."""
    db = SessionLocal()
    try:
        article = db.query(FeedArticle).filter(FeedArticle.id == article_id).first()
        if not article:
            return None, None
        analysis = (
            db.query(ArticleAnalysis)
            .filter(ArticleAnalysis.article_id == article_id)
            .filter(ArticleAnalysis.is_latest == True)
            .first()
        )
        topic = (analysis.display_title if analysis else None) or article.title

        parts = [f"Source: {article.source_name}"]
        if analysis:
            if analysis.pull_quote:
                parts.append(f'Pull quote: "{analysis.pull_quote}"')
            try:
                takeaways = json.loads(analysis.takeaways_json or "[]")
            except json.JSONDecodeError:
                takeaways = []
            if takeaways:
                parts.append("Key takeaways from the source:\n" + "\n".join(f"- {t}" for t in takeaways[:6]))
            if analysis.contrarian:
                parts.append(f"Contrarian read: {analysis.contrarian}")
        return topic, "TOPIC: " + topic + "\n\n" + "\n\n".join(parts)
    finally:
        db.close()


def _slugify(text: str) -> str:
    import re, unicodedata
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", norm).strip("-").lower()
    return s[:70] or "deep-dive"


def run(
    topic: Optional[str] = None,
    article_id: Optional[int] = None,
    depth: Optional[str] = None,
    rounds: Optional[int] = None,
    pm_action: Optional[str] = None,
    seed: Optional[int] = None,
) -> dict:
    if not topic and not article_id:
        return {"stage": "deep_dive", "error": "must provide --topic or --article-id"}

    if seed is not None:
        random.seed(seed)
    elif config.DEEP_DIVE_SEED:
        random.seed(int(config.DEEP_DIVE_SEED))

    init_db()
    ensure_pipeline_tables()

    source_context = None
    if article_id:
        topic, source_context = _context_from_article(article_id)
        if not topic:
            return {"stage": "deep_dive", "error": f"no article {article_id}"}
    else:
        source_context = f"TOPIC: {topic}"

    depth_key = depth or config.DEEP_DIVE_DEFAULT_DEPTH
    if depth_key not in config.DEEP_DIVE_DEPTH_PROFILES:
        depth_key = "standard"
    profile = config.DEEP_DIVE_DEPTH_PROFILES[depth_key]
    personas = _resolve_personas(depth_key)

    # Total turns — fixed override via --rounds (rounds * 3) or random within depth range
    if rounds:
        total_turns = rounds * len(TURN_ORDER)
    else:
        total_turns = random.randint(profile["min_turns"], profile["max_turns"])

    pm_mode = pm_action or config.DEEP_DIVE_PM_ACTION_MODE
    if pm_mode not in _CLOSING_BY_MODE:
        pm_mode = "optional"

    print(f"\n══════════════════════════════════════════════════")
    print(f"  DEEP DIVE: {topic}")
    print(f"  depth={depth_key}  turns={total_turns}  pm_action={pm_mode}")
    for k, p in personas.items():
        print(f"    {p['name']:<14} → {p['provider']}/{p['model']}")
    print(f"══════════════════════════════════════════════════")

    transcript: List[dict] = []

    for turn_num in range(total_turns):
        is_first = turn_num == 0
        is_final = turn_num == total_turns - 1

        if is_first:
            # Random opener — not always Believer
            persona_key = random.choice(TURN_ORDER)
        elif is_final:
            # Realist always closes (synthesis is their role)
            persona_key = "realist"
        else:
            persona_key = _pick_next_speaker(transcript)

        length_mode = "normal" if (is_first or is_final) else _pick_length_mode()
        max_tokens = {"short": 220, "normal": 500, "long": 800}[length_mode]
        if is_final:
            max_tokens = 650  # give the closing room to land

        persona = personas[persona_key]
        prompt = _build_turn_prompt(persona_key, transcript, source_context, is_first, is_final, length_mode, pm_mode)

        tag = "OPEN" if is_first else ("CLOSE" if is_final else length_mode.upper())
        print(f"\n— Turn {turn_num + 1}/{total_turns} [{tag}]: {persona['name']} ({persona['provider']}/{persona['model']}) —")
        try:
            response = chat(
                provider=persona["provider"],
                model=persona["model"],
                system=persona["system"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
        except Exception as exc:
            print(f"  ! failed: {exc}")
            response = f"[turn skipped — {persona['provider']} error]"

        transcript.append({
            "persona": persona_key,
            "name": persona["name"],
            "provider": persona["provider"],
            "model": persona["model"],
            "length_mode": length_mode,
            "text": response,
        })
        preview = response[:240] + ("…" if len(response) > 240 else "")
        print(preview)

    # Save to DB
    db = SessionLocal()
    try:
        participants = [
            {"persona": k, "name": v["name"], "provider": v["provider"], "model": v["model"]}
            for k, v in personas.items()
        ]
        dd = DeepDive(
            source_article_id=article_id,
            topic=topic,
            format="unpack",
            participants_json=json.dumps(participants),
            transcript_json=json.dumps(transcript),
            status="draft",
            generated_at=datetime.utcnow(),
        )
        db.add(dd)
        db.commit()
        dd_id = dd.id
    finally:
        db.close()

    # Dump JSON for review
    out_dir = config.PIPELINE_ROOT / "data" / "deep_dives"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    out_path = out_dir / f"{ts}-{_slugify(topic)}.json"
    out_path.write_text(json.dumps({
        "id": dd_id,
        "topic": topic,
        "source_article_id": article_id,
        "prompt_version": config.DEEP_DIVE_PROMPT_VERSION,
        "depth": depth_key,
        "total_turns": total_turns,
        "pm_action_mode": pm_mode,
        "participants": participants,
        "transcript": transcript,
        "generated_at": datetime.utcnow().isoformat(),
    }, indent=2))

    print(f"\n✓ Saved to DB (id={dd_id}) + {out_path}\n")
    return {
        "stage": "deep_dive",
        "id": dd_id,
        "topic": topic,
        "turns": len(transcript),
        "output_file": str(out_path),
    }


if __name__ == "__main__":
    print(json.dumps(run(topic="AI Systems Will Autonomously Build Their Successors By 2028"), indent=2))
