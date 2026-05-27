from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import math
import re

import pandas as pd


REQUIRED_COLUMNS = [
    "year",
    "round",
    "institute",
    "academic_program_name",
    "quota",
    "seat_type",
    "gender",
    "opening_rank",
    "closing_rank",
]


@dataclass
class JosaaQuery:
    rank: int
    year: int
    round_number: int | None = None
    quota: str | None = None
    gender: str | None = None
    preferred_branches: list[str] | None = None
    preferred_institutes: list[str] | None = None
    mode: str = "basic"  # basic | strict
    branch_weight: float = 0.15
    institute_weight: float = 0.10


class JosaaService:
    def __init__(self, csv_path: str | Path):
        self.csv_path = Path(csv_path)
        self._df: pd.DataFrame | None = None

    def _ensure_loaded(self) -> pd.DataFrame:
        if self._df is not None:
            return self._df

        if not self.csv_path.exists():
            raise FileNotFoundError(f"JoSAA dataset not found at: {self.csv_path}")

        df = pd.read_csv(self.csv_path, usecols=lambda c: c in REQUIRED_COLUMNS, low_memory=False)

        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"Dataset missing required columns: {missing}")

        df = df.dropna(subset=["year", "round", "institute", "academic_program_name", "opening_rank", "closing_rank"])
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
        df["round"] = pd.to_numeric(df["round"], errors="coerce").astype("Int64")
        df["opening_rank"] = pd.to_numeric(df["opening_rank"], errors="coerce")
        df["closing_rank"] = pd.to_numeric(df["closing_rank"], errors="coerce")
        df = df.dropna(subset=["year", "round", "opening_rank", "closing_rank"])

        for col in ["institute", "academic_program_name", "quota", "seat_type", "gender"]:
            df[col] = df[col].astype(str).str.strip()

        # Repair weird rows where opening > closing.
        swap_mask = df["opening_rank"] > df["closing_rank"]
        if swap_mask.any():
            tmp = df.loc[swap_mask, "opening_rank"].copy()
            df.loc[swap_mask, "opening_rank"] = df.loc[swap_mask, "closing_rank"]
            df.loc[swap_mask, "closing_rank"] = tmp

        self._df = df
        return self._df

    def get_years(self) -> list[int]:
        df = self._ensure_loaded()
        return sorted(df["year"].astype(int).unique().tolist())

    def get_rounds_for_year(self, year: int) -> list[int]:
        df = self._ensure_loaded()
        subset = df[df["year"] == year]
        return sorted(subset["round"].astype(int).unique().tolist())

    def get_quotas(self) -> list[str]:
        df = self._ensure_loaded()
        values = sorted(v for v in df["quota"].dropna().unique().tolist() if v)
        return values

    def get_genders(self) -> list[str]:
        df = self._ensure_loaded()
        values = sorted(v for v in df["gender"].dropna().unique().tolist() if v)
        return values

    @staticmethod
    def _normalize_terms(values: list[str] | None) -> list[str]:
        if not values:
            return []
        cleaned = []
        for value in values:
            for part in re.split(r"[,\n]", value):
                p = part.strip().lower()
                if p:
                    cleaned.append(p)
        return list(dict.fromkeys(cleaned))

    @staticmethod
    def _probability(rank: int, opening: float, closing: float) -> float:
        if rank <= opening:
            return 0.99

        band = max(1.0, closing - opening)
        if rank <= closing:
            # Linear decay inside the opening-closing window.
            return max(0.05, 1.0 - ((rank - opening) / band))

        # Exponential tail beyond closing so “stretch” options can still appear.
        tail_scale = max(500.0, band * 0.6)
        p = math.exp(-((rank - closing) / tail_scale))
        return max(0.001, min(0.25, p))

    @staticmethod
    def _band(probability: float) -> str:
        if probability >= 0.75:
            return "Safe"
        if probability >= 0.40:
            return "Target"
        return "Aspirational"

    @staticmethod
    def _strict_row_ok(row: pd.Series) -> bool:
        # Light-weight rule-aware checks based on common JoSAA data integrity assumptions.
        if row.get("opening_rank") is None or row.get("closing_rank") is None:
            return False
        if float(row["opening_rank"]) <= 0 or float(row["closing_rank"]) <= 0:
            return False
        if str(row.get("quota", "")).strip() == "":
            return False
        if str(row.get("seat_type", "")).strip() == "":
            return False
        if str(row.get("gender", "")).strip() == "":
            return False
        return True

    def add_compare_rank(self, rows: list[dict], compare_rank: int) -> list[dict]:
        enriched = []
        for row in rows:
            p2 = self._probability(compare_rank, row["opening_rank"], row["closing_rank"])
            row2 = dict(row)
            row2["compare_rank"] = compare_rank
            row2["compare_probability"] = float(p2)
            row2["compare_probability_pct"] = round(p2 * 100, 1)
            row2["compare_band"] = self._band(p2)
            enriched.append(row2)
        return enriched

    def round_delta_insights(self, base_rows: list[dict], query: JosaaQuery) -> list[dict]:
        if query.round_number is not None or not base_rows:
            return []

        df = self._ensure_loaded().copy()
        df = df[df["year"] == query.year]

        if query.quota:
            df = df[df["quota"].str.lower() == query.quota.strip().lower()]
        if query.gender:
            df = df[df["gender"].str.lower() == query.gender.strip().lower()]

        insights = []
        for row in base_rows[:10]:
            opt = df[
                (df["institute"] == row["institute"])
                & (df["academic_program_name"] == row["program"])
                & (df["quota"] == row["quota"])
                & (df["seat_type"] == row["seat_type"])
                & (df["gender"] == row["gender"])
            ].sort_values("round")

            if opt.empty or len(opt) < 2:
                continue

            first = int(opt.iloc[0]["closing_rank"])
            last = int(opt.iloc[-1]["closing_rank"])
            delta = last - first
            direction = "eased" if delta > 0 else ("tightened" if delta < 0 else "flat")

            rounds = [int(x) for x in opt["round"].tolist()]
            closes = [int(x) for x in opt["closing_rank"].tolist()]

            # Tiny ASCII trendline: ▁▂▃▄▅▆▇█
            blocks = "▁▂▃▄▅▆▇█"
            mn, mx = min(closes), max(closes)
            if mx == mn:
                trend = blocks[0] * len(closes)
            else:
                trend = "".join(blocks[int((c - mn) * (len(blocks) - 1) / (mx - mn))] for c in closes)

            insights.append(
                {
                    "institute": row["institute"],
                    "program": row["program"],
                    "quota": row["quota"],
                    "seat_type": row["seat_type"],
                    "gender": row["gender"],
                    "first_round": int(opt.iloc[0]["round"]),
                    "last_round": int(opt.iloc[-1]["round"]),
                    "closing_first": first,
                    "closing_last": last,
                    "delta_closing": delta,
                    "direction": direction,
                    "rounds": rounds,
                    "closes": closes,
                    "trend": trend,
                }
            )

        insights.sort(key=lambda x: abs(x["delta_closing"]), reverse=True)
        return insights

    def top_25(self, query: JosaaQuery) -> tuple[list[dict], dict]:
        df = self._ensure_loaded().copy()

        # Base mandatory filters.
        df = df[df["year"] == query.year]
        if query.round_number is not None:
            df = df[df["round"] == query.round_number]

        if query.quota:
            df = df[df["quota"].str.lower() == query.quota.strip().lower()]

        if query.gender:
            df = df[df["gender"].str.lower() == query.gender.strip().lower()]

        # User preference constraints (hard filters if provided).
        branch_terms = self._normalize_terms(query.preferred_branches)
        institute_terms = self._normalize_terms(query.preferred_institutes)

        branch_text = df["academic_program_name"].str.lower()
        institute_text = df["institute"].str.lower()

        branch_match = pd.Series(False, index=df.index)
        institute_match = pd.Series(False, index=df.index)

        if branch_terms:
            for term in branch_terms:
                branch_match = branch_match | branch_text.str.contains(re.escape(term), regex=True)
            df = df[branch_match]
        else:
            branch_match = pd.Series(True, index=df.index)

        if institute_terms:
            for term in institute_terms:
                institute_match = institute_match | institute_text.str.contains(re.escape(term), regex=True)
            df = df[institute_match]
        else:
            institute_match = pd.Series(True, index=df.index)

        if query.mode == "strict":
            df = df[df.apply(self._strict_row_ok, axis=1)]

        if df.empty:
            return [], {
                "total_candidates": 0,
                "filters_applied": {
                    "year": query.year,
                    "round": query.round_number,
                    "quota": query.quota,
                    "gender": query.gender,
                    "branch_terms": branch_terms,
                    "institute_terms": institute_terms,
                },
            }

        probs = [self._probability(query.rank, o, c) for o, c in zip(df["opening_rank"], df["closing_rank"])]
        df["probability"] = probs

        # Preference boosts influence ordering, but probability remains visible as primary signal.
        b_weight = max(0.0, min(0.5, query.branch_weight))
        i_weight = max(0.0, min(0.5, query.institute_weight))
        df["branch_boost"] = branch_match.loc[df.index].astype(float) if branch_terms else 0.0
        df["institute_boost"] = institute_match.loc[df.index].astype(float) if institute_terms else 0.0
        df["score"] = df["probability"] + (df["branch_boost"] * b_weight) + (df["institute_boost"] * i_weight)

        df["probability_pct"] = (df["probability"] * 100).round(1)
        df["band"] = df["probability"].apply(self._band)

        # If round is not constrained, same program can appear multiple times across rounds.
        # Keep the strongest row per option so users get cleaner Top 25 suggestions.
        if query.round_number is None:
            df = df.sort_values(by=["probability", "round", "closing_rank"], ascending=[False, False, True])
            df = df.drop_duplicates(
                subset=["institute", "academic_program_name", "quota", "seat_type", "gender"],
                keep="first",
            )

        df = df.sort_values(
            by=["score", "probability", "closing_rank"],
            ascending=[False, False, True],
        )

        top = df.head(25).copy()

        records = []
        for _, row in top.iterrows():
            rank_gap_to_close = int(query.rank - row["closing_rank"])
            records.append(
                {
                    "year": int(row["year"]),
                    "round": int(row["round"]),
                    "institute": row["institute"],
                    "program": row["academic_program_name"],
                    "quota": row["quota"],
                    "seat_type": row["seat_type"],
                    "gender": row["gender"],
                    "opening_rank": int(row["opening_rank"]),
                    "closing_rank": int(row["closing_rank"]),
                    "rank_gap_to_close": rank_gap_to_close,
                    "probability": float(row["probability"]),
                    "probability_pct": float(row["probability_pct"]),
                    "score": float(row["score"]),
                    "band": row["band"],
                }
            )

        meta = {
            "total_candidates": int(len(df)),
            "filters_applied": {
                "year": query.year,
                "round": query.round_number,
                "quota": query.quota,
                "gender": query.gender,
                "branch_terms": branch_terms,
                "institute_terms": institute_terms,
                "mode": query.mode,
                "branch_weight": b_weight,
                "institute_weight": i_weight,
            },
        }
        return records, meta


@lru_cache(maxsize=1)
def get_josaa_service(csv_path: str) -> JosaaService:
    return JosaaService(csv_path)
