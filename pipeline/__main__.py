"""CLI entry: python -m pipeline <stage> [options]"""
import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(prog="pipeline", description="fullstackpm.tech editorial pipeline")
    sub = parser.add_subparsers(dest="stage", required=True)

    sub.add_parser("fetch", help="Pull RSS feeds into local DB")

    e = sub.add_parser("extract", help="Scrape full text for new articles")
    e.add_argument("--limit", type=int, default=None)
    e.add_argument("--re-extract", action="store_true")

    a = sub.add_parser("analyse", help="Claude analyses full text → structured")
    a.add_argument("--limit", type=int, default=None)
    a.add_argument("--re-analyse", action="store_true")

    r = sub.add_parser("rewrite", help="Top N articles get HC-voice editorial drafts")
    r.add_argument("--top-n", type=int, default=None)
    r.add_argument("--re-rewrite", action="store_true")

    p = sub.add_parser("publish", help="Write published articles as JSON for Render")
    p.add_argument("--include-drafts", action="store_true",
                   help="Include editorial drafts (otherwise only is_published=True)")

    sub.add_parser("daily", help="fetch → extract → analyse (no rewrite, no publish)")

    dd = sub.add_parser("deep-dive", help="Generate AI-vs-AI-vs-AI roundtable transcript")
    dd.add_argument("--topic", type=str, default=None)
    dd.add_argument("--article-id", type=int, default=None)
    dd.add_argument("--depth", choices=["light", "standard", "deep"], default=None)
    dd.add_argument("--rounds", type=int, default=None, help="Fixed override: rounds × 3 turns")
    dd.add_argument("--pm-action", choices=["force", "optional", "off"], default=None)
    dd.add_argument("--seed", type=int, default=None, help="For reproducibility")
    dd.add_argument("--with-audio", action="store_true", help="Also synthesize per-speaker audio")

    args = parser.parse_args()

    if args.stage == "fetch":
        from pipeline.stages import fetch
        result = fetch.run()
    elif args.stage == "extract":
        from pipeline.stages import extract
        result = extract.run(limit=args.limit, re_extract=args.re_extract)
    elif args.stage == "analyse":
        from pipeline.stages import analyse
        result = analyse.run(limit=args.limit, re_analyse=args.re_analyse)
    elif args.stage == "rewrite":
        from pipeline.stages import rewrite
        result = rewrite.run(top_n=args.top_n, re_rewrite=args.re_rewrite)
    elif args.stage == "publish":
        from pipeline.stages import publish
        result = publish.run(include_drafts=args.include_drafts)
    elif args.stage == "daily":
        from pipeline.stages import fetch, extract, analyse
        results = [fetch.run(), extract.run(), analyse.run()]
        result = {"stage": "daily", "steps": results}
    elif args.stage == "deep-dive":
        from pipeline.stages import deep_dive
        result = deep_dive.run(
            topic=args.topic,
            article_id=args.article_id,
            depth=args.depth,
            rounds=args.rounds,
            pm_action=args.pm_action,
            seed=args.seed,
        )
        if args.with_audio and result.get("id"):
            from pipeline.stages import deep_dive_audio
            audio_result = deep_dive_audio.run(deep_dive_id=result["id"])
            result["audio"] = audio_result
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
