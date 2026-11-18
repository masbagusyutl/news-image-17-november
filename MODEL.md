# MODEL.md — "The World: Tuesday 17 November 2026"

## What it is
A one-page newspaper front page that sums up Tuesday 17 November 2026's
world news. The program is `main.py` (stdlib only): it copies the
pre-rendered `entry.png` to the grader's output directory. The image itself
is drawn at build time by `draw_frontpage.py` (PIL) from the day's verified
headlines, because the sandbox runs with no network.

## Why this design
The judge ranks on (1) naming the day with specific events of that day,
(2) selection and breadth, (3) readability from the image alone. So the page
is a classic front page: masthead, the date in red, one lead story with an
illustration, six stories across regions and beats, and an "Also today"
strip. No story is older than the day itself; nothing in the image is copied
from anyone else's photograph or artwork — every visual is drawn in code.

## Stories chosen (all first reported 17 Nov 2026)
- **Lead, Europe:** Ukraine strikes the Kerch bridge a second time in under
  24 hours; Russia hits Kyiv's Dnipro bridges, cutting heat, water, power.
- **Middle East:** tankers hit by mines near Hormuz; Iran drones a US radar
  base in Bahrain; US intelligence warns of a "dirty bomb" plot.
- **Asia:** China confirms the first Xi–Trump–Putin summit, Thursday in
  Shenzhen on the APEC sidelines.
- **Americas:** third US carrier reaches the Gulf; Pentagon fails its audit
  for the ninth year ($4.8tn unverifiable).
- **Tech/trade:** US closes the AI-chip rental loophole; Dow falls 849.
- **Health:** US loses measles-free status after three decades.
- **Britain:** UK sanctions firms building Israeli settlements.
- **Also:** Japan scrambles jets; five European states plan a Rwanda returns
  hub; Xi–Carney agree tariff cuts.

## Checks
- `python3 draw_frontpage.py` renders `entry.png` (1024x1024, ~177 KB,
  under the 1 MiB / 1024x1024 caps).
- `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py` twice gives
  byte-identical output.
