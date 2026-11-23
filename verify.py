#!/usr/bin/env python3
"""Verify the Sunday Ledger v2 entry: story set, numbers, DATE CHECK,
legibility budget, image.

Every check is derived from render.py's own data tables, so a typo in
the data fails here instead of reaching the judge. Exits 0 and prints
ALL PASSED only when every check holds.

The legibility budget encodes the judge feedback on news-image-20261121
v2 (breadth won, legibility at 300px lost): short lead titles, short
decks, short card titles, short index lines. If a title grows past its
budget, the page slides back toward a wall of micro-text.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import (  # noqa: E402
    STORIES, LEADS, CARDS, INDEX, INDEX_STORIES, NUMBERS, REGIONS,
    DATE_CHECK, OUT,
)

failures = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        failures.append(label)


def main():
    # --- story set -------------------------------------------------------
    check(len(STORIES) == 33, "33 stories total")
    nums = sorted(s["n"] for s in STORIES)
    check(nums == list(range(1, 34)), "story numbers 1..33 unique, no gaps")
    check(all(s["title"] and s["deck"] and s["source"] and s["day"]
              and s["region"] for s in STORIES),
          "every story has title, deck, source, day, region")
    check(len(LEADS) == 3, "3 lead stories")
    check(len(CARDS) == 6, "6 medium cards")
    check(len(INDEX) == 24, "24 ALSO ON index items")
    check([n for n, _, _ in INDEX] == list(range(10, 34)),
          "index numbers 10..33")
    check([s["n"] for s in INDEX_STORIES] == list(range(10, 34)),
          "index records match index numbers")
    check(all(c["mini"] for c in CARDS), "every card has a mini-scene kind")
    check(all(s["art"] in ("drones", "cop31", "bahrain") for s in LEADS),
          "every lead has an illustration")
    check(all(s["tag"] in ("CONFIRMED", "REPORTED", "CLAIM") for s in LEADS),
          "every lead has a certainty tag")
    # pins: 9 places (3 leads + 6 cards), matching the map header claim
    pins = [s for s in STORIES if s.get("pin")]
    check(len(pins) == 9, "9 map pins")

    # --- regions ---------------------------------------------------------
    check(sum(c for _, c in REGIONS) == 33, "region counts sum to 33")
    check(len(REGIONS) == 7, "7 regions")
    per_region = {}
    for s in STORIES:
        per_region[s["region"]] = per_region.get(s["region"], 0) + 1
    check(per_region == dict(REGIONS), "region counts match the story set")

    # --- number strip ----------------------------------------------------
    check(len(NUMBERS) == 6, "6 numbers on the strip")
    check([n for n, _, _ in NUMBERS] ==
          ["186", "161", "35%", "98.79%", "720/9", "50"],
          "strip figures are the verified ones")
    text_all = " ".join(s["title"] + " " + s["deck"] for s in STORIES)
    check("186" in LEADS[0]["title"], "strip figure 186 ties to the hero title")
    check("161" in LEADS[0]["title"], "strip figure 161 ties to the hero title")
    check("35%" in LEADS[1]["deck"], "strip figure 35% ties to the COP31 deck")
    check("98.79%" in CARDS[0]["title"],
          "strip figure 98.79% ties to the Hong Kong card")
    check("720/9" in CARDS[1]["title"],
          "strip figure 720/9 ties to the India card")
    check("50 points" in CARDS[3]["deck"],
          "strip figure 50 ties to the Wembanyama card")

    # --- legibility budget (300px gate, data-level) ----------------------
    check(len(LEADS[0]["title"]) <= 45, "hero title <= 45 chars")
    check(all(len(s["title"]) <= 40 for s in LEADS[1:]),
          "panel titles <= 40 chars (one line at 20pt)")
    check(len(LEADS[0]["deck"]) <= 185, "hero deck <= 185 chars")
    check(all(len(s["deck"]) <= 145 for s in LEADS[1:]),
          "panel decks <= 145 chars (two lines at 10pt)")
    check(all(len(s["title"]) <= 55 for s in CARDS),
          "card titles <= 55 chars")
    check(all(len(t + " — " + s) <= 62 for _, t, s in INDEX),
          "index lines <= 62 chars")

    # --- DATE CHECK ------------------------------------------------------
    check(len(DATE_CHECK) == 6, "6 DATE CHECK exclusions")
    dc_text = " ".join(n + " " + d for n, d in DATE_CHECK).lower()
    check("landmine" in dc_text,
          "Sudan landmine is in DATE CHECK, not a story")
    check("landmine" not in text_all.lower(),
          "landmine does not appear as a story")
    check("fbi" in dc_text,
          "FBI breach is in DATE CHECK, not a story")
    check("fbi" not in text_all.lower(),
          "FBI breach does not appear as a story")
    check("sparta" in dc_text,
          "Sparta II is in DATE CHECK, not a story")
    check("sparta" not in text_all.lower(),
          "Sparta II does not appear as a story")
    check("chapo" in dc_text,
          "El Chapo Isidro is in DATE CHECK, not a story")
    check("chapo" not in text_all.lower(),
          "El Chapo Isidro does not appear as a story")
    check("bepicolombo" in dc_text,
          "BepiColombo is in DATE CHECK, not a story")
    check("bepicolombo" not in text_all.lower(),
          "BepiColombo does not appear as a story")
    check("icj" in dc_text,
          "ICJ Myanmar ruling is in DATE CHECK, not a story")
    check("icj" not in text_all.lower(),
          "ICJ ruling does not appear as a story")

    # --- forbidden wrong figures -----------------------------------------
    for bad in ("23 killed", "no injuries", "98.37%", "$120bn", "27–12",
                "26 dead", "Juventus 2–0", "final 2–0", "M5.9",
                "El Clásico", "mbappé", "93.55%", "seven feared"):
        check(bad not in text_all, "wrong figure absent: %s" % bad)
    # The Nigeria toll conflict: NEMA's Sunday toll is 24; rank 3 prints 26.
    nigeria = [s for s in STORIES if s["n"] == 9][0]
    check("24" in nigeria["title"], "Nigeria card prints the verified toll 24")
    # Hong Kong: official final turnout 98.79%, not the 14:00/17:00 figures.
    hk = [s for s in STORIES if s["n"] == 4][0]
    check("98.79%" in hk["title"], "Hong Kong card prints the final 98.79%")

    # --- image -----------------------------------------------------------
    check(os.path.exists(OUT), "entry.png exists")
    if os.path.exists(OUT):
        with open(OUT, "rb") as f:
            head = f.read(8)
        check(head == b"\x89PNG\r\n\x1a\n", "entry.png is a PNG")
        size = os.path.getsize(OUT)
        check(size <= 1048576, "entry.png <= 1 MiB (%d bytes)" % size)
        from PIL import Image
        img = Image.open(OUT)
        check(img.size == (1024, 1024), "entry.png is 1024x1024")

    if failures:
        print("FAILED: %d check(s)" % len(failures))
        sys.exit(1)
    print("ALL PASSED")


if __name__ == "__main__":
    main()
