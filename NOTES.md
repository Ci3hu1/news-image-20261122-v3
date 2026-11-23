# NOTES — news-image-20261122 v3 (judge-driven rebuild)

**Status:** BUILT, NOT SUBMITTED. Entry commit `4bcc2c338b6a5f36d34ee6bb74c719dc272996a1`
(repo https://github.com/Ci3hu1/news-image-20261122-v3, master, public).
Bundle + kit check PENDING — the builder session's usage rows had not
flushed when the bundle was attempted (muse.db: 0 rows for agent
a5512b96-0543-4969-90df-72f09c50dff6 at bundle time; the CLI refuses an
empty --muse-usage file). The parent re-runs bundle + check after the
builder turn ends and the rows flush. Do NOT submit before the kit
check returns ok=true failed=[].

## What v3 is

A rebuild driven by the judge's own written reasons on our v2 entry
(01a206dd-808f-75da-abe3-7aee5eeb2190, 953,261 / 95.33%, 8W 2D 2L —
WORSE than v1's 971,449 / 97.14%, 10W 2D 0L). Top-10 cutoff ~990,650.
Entries close 24 Nov 2026 07:00 WIB. Results 7 Dec 2026.

## The three fixes (judge's reasons → build)

1. **DATE CHECK backfired.** v2's box titled "DATE CHECK — NOT SUNDAY
   22 NOV" with 5 items was read as an admission the poster covers
   multiple days ("it is knowingly not one day's news", "undercuts
   criterion 1") — used against v2 in 5+ matches. v3: 2 items only
   (Peru M6.7 quake — Fri 20 Nov; Paolo Bulgari dies — 21 Nov),
   neutral title "DATE CHECK — excluded", small, at the bottom, with
   "Not in this edition — these happened on other days:". No other
   dates are mentioned anywhere else on the page. (The 400-drone
   barrage, robot-weapons talks, and UK–EU youth deal are dropped from
   the box entirely.)
2. **Legibility + pictures.** v2's 36-story grid was "a dense
   broadsheet that collapses into an illegible blur at 300px", "most
   of its stories carry no picture, only text". v3 cuts to 30 stories
   (NI19 #1 won with 33) and makes the 13 featured stories (3 leads +
   10 cards) real illustrated scenes from the editorial-illustration
   library — picture area per card 62px tall (was 42px), more than half
   the card. All 10 featured headlines fit in 2 lines at 17px bold
   (verified by test — four v2 headlines wrapped to 3 lines and lost
   their third line: Hong Kong "vote", India "128", Seoul
   "AI-cheating row", Riyadh "drones down"; all four were shortened).
   ALSO ON is 17 items (was 23) in larger type with a region-colour
   dot per item. A 300px preview is rendered and checked: masthead,
   leads, and illustrated cards read at a glance.
3. **Hong Kong figure.** v2's "Hong Kong votes 98.79%" was judged as
   "strains belief". VERIFIED 23 Nov 2026: the figure is real — 2026
   Election Committee Subsector Ordinary Elections, Sun 22 Nov 2026,
   5,640 of 5,709 registered voters, 98.79% turnout, a record (EAC via
   info.gov.hk / news.gov.hk / China Daily Asia). It strains belief
   only because the denominator was missing. v3 prints the denominator
   beside the number everywhere: card "Hong Kong EC poll: 5,640 of
   5,709" (source EAC), KPI "5,640 / OF 5,709 HK VOTERS". No bare
   "98.79%" appears anywhere (enforced by test).

## Kept (judge-praised)

Explicit date "Sunday 22 November 2026"; 7 regions; sourcing +
claimed-vs-confirmed labels; UTC timeline + world map + COP31 lead;
"ALL FROM SUNDAY" true (all 30 main-list stories are Sunday 22 Nov
only); one drone number (186 launched / 161 shot down); Dymer toll
"4 killed, 14 missing"; Delta delays "1,169" consistent.

## Story list (30)

- Leads (3): COP31 collapses (Antalya), 186 drones / Dymer, Iran
  claims strikes on US bases in Bahrain.
- Featured (10): Benghazi ship blast, Sparta II towed, Hong Kong EC
  poll (5,640 of 5,709, EAC), India 720/9 Pant 128, Cikande fire,
  Gaza, Seoul minister quits in AI row, Delta ground stop 1,169 late,
  Lahore AQI 538, Houthi refinery claim; 2 down.
- ALSO ON (14–30, 17): Bahrain asks UN, Eisenkot–Likud, Bondi hero,
  France squad, Iran double launcher, Iran rationing, Zelenskyy
  Patriots, China spy campaign, Taiwan–Canada, Youth Congress / Meta,
  Pakistan minister Delhi, Trump / China nuclear, Pugh Hormuz swim,
  West Bank settlers, Guatemala arrest, China margin cut, AP Democrats
  258 seats.
- Regions: Europe 4, Middle East 9, Asia 8, Africa 1, Americas 4,
  Oceania 2, Global 2 = 30.
- Dropped from v2 for space (all verified Sunday, dropped for space
  only): Poland missile debris, Brazil calamity, Verstappen Las Vegas
  win, Cook Islands gale, Google Duplex, FinCEN MEXC.

## Build record

- Fresh kit: ~/workspace/tools/makefun/news-image-20261122-kit/
  (nested news-image-20261122-kit/news-image-20261122-kit/,
  CLI cli/makefun.mjs). Kit bundle_sha256
  00314c2cb5a445fd508bab7f92ae6a1a15dec902d84b7c9dcaa326beafe638bb.
- Design philosophy: DESIGN.md ("Illustrated Front Page") — written
  before building (canvas-design skill). Infographic-generator
  principles applied to layout; canvas-design as art direction.
- Renderer: render_poster.py (build-time, Pillow + editorial-
  illustration lib). entry.png 567,030 bytes, 1024x1024, sha256
  21babbd4cc333bc64e7b94376e7f0767423e4a87bdbf0ca44d4db92f942e4389.
  preview-300.png rendered and checked.
- main.py: pure stdlib, written fresh blind. Tested as uid 65534 on a
  read-only repo copy (MAKEFUN_OUTPUT_DIR set): exit 0, output
  byte-identical to source (sha256 match).
- Tests: tests/test_poster.py — 21 tests, all pass (story count,
  region counts, ALSO ON numbering 14–30, DATE CHECK exclusion, Hong
  Kong denominator + source, headline fit, poster dimensions/size,
  main.py pure stdlib).
- Repo: public, master, homepage
  https://make.fun/bounty/news-image-20261122, topics makefun,
  ai-agents, bounties. Description set by kit init.
- LICENSE: MIT with SPDX line (Joni Gunawan copyright, as v2).

## Bundle + check (TO BE RE-RUN by parent after usage flush)

Usage SELECT (kit's exact query):
SELECT u.agent_id, u.message_id, u.created_at, u.input_tokens,
u.output_tokens, a.model FROM agent.agent_message_token_usage u
JOIN agent.agents a ON a.agent_id = u.agent_id
WHERE u.agent_id IN ('a5512b96-0543-4969-90df-72f09c50dff6')
ORDER BY u.created_at DESC LIMIT 500
→ save as JSONL (sort_keys=True, dedup by agent_id+message_id, 0600).

Bundle (dry-run first):
node ~/workspace/tools/makefun/news-image-20261122-kit/news-image-20261122-kit/cli/makefun.mjs bundle --json --repo ~/workspace/tools/makefun/news-image-20261122-v3 --out ~/workspace/tools/makefun/bundles/ni22-v3-bundle.tar.gz --harness muse-app --harness-version 1 --provider ipnext --model ipnext/avocado-5.17-v2 --effort default --prompt-file ~/workspace/tools/makefun/news-image-20261122-v3/BRIEF.md --prompt-origin other --prompt-via whatsapp --redact "Joni Gunawan" --mcp none --muse-usage <usage.jsonl> --system-prompt ~/workspace/system/system_prompt.md

Check:
node ~/workspace/tools/makefun/news-image-20261122-kit/news-image-20261122-kit/cli/makefun.mjs check --json --repo ~/workspace/tools/makefun/news-image-20261122-v3 --commit 4bcc2c338b6a5f36d34ee6bb74c719dc272996a1 --transcripts ~/workspace/tools/makefun/bundles/ni22-v3-bundle.tar.gz

## Pin decision (for Joni, after v3 live score)

v1 (971,449) is currently the best entry. If v3 scores above v1, v3
stands as final automatically (latest). If v3 scores below v1, v1 must
be pinned as final (PUT /api/competitions/news-image-20261122/
final-entry with submission 01a20673-71f1-7643-826d-1a7bc3e708d1)
before entries close 24 Nov 07:00 WIB. Do not pin without Joni's
explicit order.

## Title (for submit)

"Sunday 22 November 2026: 30 sourced stories, 7 regions, illustrated cards that read at 300px"
