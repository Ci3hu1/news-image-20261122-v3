# BRIEF — news-image-20261122 v3 (judge-driven rebuild)

**Competition:** news-image-20261122 — "Sum up 22 November's world news in one image". $100 total (50 paid places), free entry. **Closes 24 Nov 2026 07:00 WIB** (2026-11-24T00:00:00Z). Results 7 Dec 2026. Harness program/v1, bundle-type (transcript bundle via kit CLI, no `record`).

**v1 live:** 971,449 (97.14%), rank 3,741/12,530, 10W 2D 0L.
**v2 live:** 953,261 (95.33%), 8W 2D 2L — WORSE than v1. Top-10 cutoff ~990,650.

## Why v3 exists — the judge's written reasons on v2

Read from `GET /api/submissions/01a206dd-808f-75da-abe3-7aee5eeb2190`,
`scores[0].judge.heat.matches[].calls[].reason`. The v2 judge's losing
calls (M6c0, M7c1, M9c0, M10c0, M10c1, M12c1) name three flaws:

**Fixes (all three are in this build):**
1. DATE CHECK backfired — v2's box titled 'DATE CHECK — NOT SUNDAY
   22 NOV' with 5 items was read as an admission that the poster
   covers multiple days ("it is knowingly not one day's news",
   "undercuts criterion 1"). v3 shrinks it to 2 items, neutral title
   "DATE CHECK — excluded", small, at the bottom, unmistakably framed
   as items EXCLUDED from this poster (not in it). No other dates are
   mentioned anywhere else on the page.
2. Legibility + pictures — v2's 36-story grid was "a dense broadsheet
   that collapses into an illegible blur at 300px", "most of its
   stories carry no picture, only text". The winning opponents had six
   clearly labelled, PICTURED stories in one clean composition. v3
   cuts to 30 stories (NI19 #1 won with 33) and makes the 13 featured
   stories (3 leads + 10 cards) real illustrated scenes from the
   editorial-illustration library — bigger picture area per card, larger
   type, generous leading. ALSO ON is 17 items in larger type with a
   region marker each. A 300px preview is rendered and checked: the
   WHOLE poster must read at 300px.
3. Hong Kong figure — v2's "Hong Kong votes 98.79%" was judged as
   "strains belief". VERIFIED 23 Nov 2026: the figure is real — 2026
   Election Committee Subsector Ordinary Elections, Sun 22 Nov 2026,
   5,640 of 5,709 registered voters, 98.79% turnout, a record
   (EAC via info.gov.hk / news.gov.hk / China Daily). It strains
   belief only because the denominator was missing: this is a small
   5,709-voter committee poll, not a general election. v3 prints the
   denominator beside the number everywhere it appears: "5,640 of
   5,709" (card) and "5,640 / OF 5,709 HK VOTERS" (KPI strip), source
   EAC. Never print an extraordinary number without its denominator
   and source beside it.

**Kept:** explicit date "Sunday 22 November 2026" (Criterion 1);
broad coverage across 7 regions (Criterion 2); sourcing +
claimed-vs-confirmed labels; UTC timeline + world map + big COP31 lead;
header "ALL FROM SUNDAY" true (all 30 main-list stories are Sunday
22 Nov only); one drone number (186 launched / 161 shot down); Dymer
toll "4 killed, 14 missing"; Delta delays "1,169" consistent.

## Story list (30, 7 regions)

- Leads (3): COP31 collapses (Antalya), 186 drones / Dymer, Iran claims
  strikes on US bases in Bahrain.
- Featured (10): Benghazi ship blast, Sparta II towed, Hong Kong EC
  poll (5,640 of 5,709, source EAC), India 720/9 Pant 128, Cikande
  fire, Gaza, Seoul minister quits, Delta ground stop 1,169 late,
  Lahore AQI 538, Riyadh Houthi claim.
- ALSO ON (14–30, 17 items): Bahrain asks UN, Eisenkot–Likud, Bondi
  hero, France squad, Iran double launcher, Iran rationing, Zelenskyy
  Patriots, China spy campaign, Taiwan–Canada, Youth Congress / Meta,
  Pakistan minister Delhi, Trump / China nuclear, Pugh Hormuz swim,
  West Bank settlers, Guatemala arrest, China margin cut, AP Democrats
  258.
- DATE CHECK (excluded, 2 items only): Peru M6.7 quake — Fri 20 Nov;
  Paolo Bulgari dies — 21 Nov. Framed as "Not in this edition".
- Regions: Europe 4, Middle East 9, Asia 8, Africa 1, Americas 4,
  Oceania 2, Global 2 = 30.

## Design

Design philosophy in DESIGN.md ("Illustrated Front Page"): every story
a drawn scene first and a headline second; cream paper, navy ink, one
red accent; strict grid, generous breathing room, nothing overlaps;
the whole poster must read at 300px. Infographic-generator principles
applied to the layout (card anatomy, typography hierarchy, section
patterns); canvas-design principles applied as art direction
(visual hierarchy, craftsmanship, precision, breathing room).

## Technical

- Python stdlib ONLY for the graded program (`main.py` copies the
  bundled `entry.png`, SHA-256 verified). Render at build time
  (`render_poster.py`, needs Pillow + editorial-illustration library).
- Test as uid 65534 on a read-only copy; output byte-identical.
- Title: "Sunday 22 November 2026: 30 sourced stories, 7 regions, illustrated cards that read at 300px"
- Do NOT submit without Joni's 'Setuju' on the exact entry.
