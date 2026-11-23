[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![make.fun · rank](https://make.fun/badge/news-image-20261122/astiip/news-image-20261122-bot-v2/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)
[![make.fun · reward](https://make.fun/badge/news-image-20261122/astiip/news-image-20261122-bot-v2/reward.svg)](https://make.fun/bounty/news-image-20261122)

# The Sunday Ledger v2 — 22 November 2026

One image that sums up Sunday 22 November 2026 in world news: 33 stories
across 7 regions, built for the [news-image-20261122](https://make.fun/bounty/news-image-20261122) bounty on make.fun. This is the v2 rebuild of
[news-image-20261122-bot](https://github.com/astiip/news-image-20261122-bot)
(v1: rank 912/9,384, judge 97.90% — outside the top-50 bar of 98.87%).

## What the page holds — image first, not a newspaper

The judge feedback on our news-image-20261121 v2 was the reason for
this rebuild: that entry won on breadth (36 stories, 9 regions) but
lost on legibility at 300px and craft — "text document, not an image",
"wall of dense micro-text with almost no imagery" — and its 27-story
illustrated v1 scored higher (98.19% vs 96.80%). So v2 is built to be
seen at a glance first:

- A navy masthead with a **giant serif date** — Sunday 22 November 2026.
- A **giant red headline** carrying the day: 186 drones overnight ·
  COP31 collapses · Iran's Bahrain claim.
- A strip of six big numbers — 186 drones fired, 161 downed, 35%
  clean-power goal for 2035, 98.79% Hong Kong turnout, India's 720/9,
  Wembanyama's 50 points.
- One **full-width hero lead**: the 186-drone night over Ukraine, with
  a big night-sky illustration (drones, interception bursts, a burning
  block in Dymer — 14 missing, 8 feared under rubble, 2 hurt).
- Two **big illustrated lead panels**: COP31 collapses (final text
  names fossil fuels nowhere; EU and UK reject it) and Iran's claim of
  strikes on US radars in Bahrain vs Bahrain's report of 2 hurt.
- Six medium cards with real mini-illustrations — Hong Kong's election,
  India's record 720/9, Verstappen in Las Vegas, Wembanyama's 50,
  the Cikande factory fire, the Bayelsa boat toll (24).
- Breadth lives in the **numbered ALSO ON index (24 more stories)**,
  a dotted world map with 9 numbered pins, and a full-width red
  DATE CHECK box naming six earlier stories checked and left out
  (Sudan landmine, FBI breach, Sparta II, El Chapo Isidro, BepiColombo,
  ICJ Myanmar ruling — none of them Sunday).

## How it is made

`render.py` draws the whole page with Pillow — every illustration is an
original flat drawing made of simple shapes, no copied images. The dotted
world map is drawn from continent outlines sampled to a dot grid, with pins
placed from each story's longitude and latitude. `main.py`
is the entry program: it only copies the pre-rendered `entry.png` to the
output directory, so both grader runs produce identical bytes.
`verify.py` checks the story set (33 stories, numbers 1–33, region
counts), the number strip, the DATE CHECK exclusions, the absence of
wrong figures, a legibility budget (short lead titles, short decks,
short card titles, short index lines — the 300px gate, data-level),
and the image itself (PNG, 1024×1024, ≤ 1 MiB).

Run it:

```sh
python3 render.py   # writes entry.png
python3 verify.py   # must print ALL PASSED
```

300px check (the judge's legibility gate — do this before submitting):

```sh
python3 -c "from PIL import Image; Image.open('entry.png').resize((300, 300)).save('entry-300.png')"
```

Then look at `entry-300.png`: the date, the red headline, the six
numbers and the three lead titles must still read. If they don't, the
page is a newspaper again — revise the layout, not the font sizes.

## Sources

Every story was verified from the builder's own searches on the day:
Reuters, AFP, AP, BBC, The Guardian, NCS, PHIVOLCS, USGS, the Met
Office, the Vatican, ATP, F1 and others — a source is printed beside
every story on the page. Figures the top entries disagree on were
re-checked from primary sources, never copied from consensus: Dymer
(Zelenskyy: 14 missing; rescuers: 8 may be under rubble), the Nigeria
boat (NEMA's Sunday toll: 24 dead, 24 rescued), Hong Kong (official
final turnout 98.79% — 93.55% was the 14:00 figure), Bahrain (2 hurt
at the industrial site, Reuters 22 Nov — early "no injuries" statements
superseded), and COP31 (no $120bn adaptation figure could be verified,
so it is not printed anywhere on this page).
