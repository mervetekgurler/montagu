"""
Convert page-level OCR JSONL output to a letter-level CSV.

Each row in the output represents one complete letter with its metadata
and full body text assembled from all page fragments.

Page IDs use the convention vol1_PAGE or vol2_PAGE to disambiguate
the two volumes whose page numbering restarts at 1 in Part II.
"""

import csv
import json
import sys
from pathlib import Path

JSONL_PATH = Path(__file__).parent / "gemini_output" / "all_responses.jsonl"
CSV_PATH = Path(__file__).parent / "gemini_output" / "letters.csv"

# Roman numeral letter numbers for the two volumes:
# Part I:  PREMIERE through XXXII
# Part II: XXXIII through LII
# We determine the volume by detecting when the raw page numbering resets
# (drops sharply after having been high) within the sequential outer pages.

def parse_jsonl(path):
    """Yield dicts: outer_page, raw_page, letters (list of fragment dicts)."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            outer = row["page"]
            raw_response = row.get("raw_response", "").strip()
            if not raw_response:
                continue
            try:
                resp = json.loads(raw_response)
            except json.JSONDecodeError:
                continue
            raw_page = resp.get("page")
            language = resp.get("language", "fr")
            letters = resp.get("letters", [])
            yield outer, raw_page, language, letters


def assign_volume(raw_page, prev_raw_page, current_vol):
    """Return the current volume given a potential page-number reset.

    Only increment the volume when raw_page resets to a small value (≤ 20)
    after having been high (> 100). This catches the Part I → Part II
    transition (e.g. 227 → 1) while ignoring mid-run jumps that are
    artefacts of the OCR pipeline re-processing overlapping page ranges.
    """
    if raw_page is None or prev_raw_page is None:
        return current_vol
    try:
        rp = int(raw_page)
        pp = int(prev_raw_page)
    except (TypeError, ValueError):
        return current_vol
    if rp <= 20 and pp > 100:
        return current_vol + 1
    return current_vol


def page_label(vol, raw_page):
    if raw_page is None:
        return ""
    return f"vol{vol}_{raw_page}"


def main():
    # ---------------------------------------------------------------
    # Pass 1: collect all fragments, detect volumes, assign to letters
    # ---------------------------------------------------------------
    fragments = []  # (outer, vol, raw_page, letter_number_or_none, fragment_dict)

    current_vol = 1
    prev_raw = None

    for outer, raw_page, language, letter_frags in parse_jsonl(JSONL_PATH):
        current_vol = assign_volume(raw_page, prev_raw, current_vol)
        if raw_page is not None:
            try:
                prev_raw = int(raw_page)
            except (TypeError, ValueError):
                pass

        for frag in letter_frags:
            fragments.append({
                "outer": outer,
                "vol": current_vol,
                "raw_page": raw_page,
                "page_label": page_label(current_vol, raw_page),
                "language": language,
                "number": frag.get("number"),
                "heading": frag.get("heading"),
                "recipient": frag.get("recipient"),
                "location": frag.get("location"),
                "date": frag.get("date"),
                "body": (frag.get("body") or "").strip(),
                "footnote": frag.get("footnote"),
            })

    # ---------------------------------------------------------------
    # Pass 2: forward-scan to assign each fragment to a letter
    # ---------------------------------------------------------------
    # Build ordered list of letters; each entry accumulates body segments.
    # Key = (vol, number) since letter numbers restart in vol2.
    letter_order = []  # list of (vol, number) in first-seen order
    letter_meta = {}   # (vol, number) -> metadata dict
    letter_bodies = {}  # (vol, number) -> list of (outer, body) tuples
    letter_footnotes = {}  # (vol, number) -> latest footnote

    current_key = None

    for frag in fragments:
        if frag["number"]:
            key = (frag["vol"], frag["number"])
            if key not in letter_meta:
                letter_meta[key] = {
                    "number": frag["number"],
                    "heading": frag["heading"],
                    "recipient": frag["recipient"],
                    "location": frag["location"],
                    "date": frag["date"],
                    "start_page": frag["page_label"],
                    "language": frag["language"],
                }
                letter_bodies[key] = []
                letter_footnotes[key] = None
                letter_order.append(key)
            current_key = key

        if current_key and frag["body"]:
            letter_bodies[current_key].append((frag["outer"], frag["body"]))

        if current_key and frag["footnote"]:
            letter_footnotes[current_key] = frag["footnote"]

    # ---------------------------------------------------------------
    # Pass 3: deduplicate body segments and assemble full text
    # ---------------------------------------------------------------
    rows = []
    for key in letter_order:
        meta = letter_meta[key]

        # Deduplicate by exact body string (multiple runs produce identical text)
        seen_bodies = set()
        unique_segments = []
        for outer, body in letter_bodies[key]:
            if body not in seen_bodies:
                seen_bodies.add(body)
                unique_segments.append((outer, body))

        full_body = " ".join(body for _, body in unique_segments)

        rows.append({
            "number": meta["number"],
            "heading": meta["heading"] or "",
            "recipient": meta["recipient"] or "",
            "location": meta["location"] or "",
            "date": meta["date"] or "",
            "body": full_body,
            "footnote": letter_footnotes[key] or "",
            "start_page": meta["start_page"],
            "language": meta["language"],
        })

    # ---------------------------------------------------------------
    # Write CSV
    # ---------------------------------------------------------------
    fieldnames = ["number", "heading", "recipient", "location", "date",
                  "body", "footnote", "start_page", "language"]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} letters to {CSV_PATH}")


if __name__ == "__main__":
    main()
