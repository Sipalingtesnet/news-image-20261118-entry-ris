# news-image-20261118-entry-ris

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Sipalingtesnet/news-image-20261118-entry-ris/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Sipalingtesnet/news-image-20261118-entry-ris/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

The world news of Wednesday 18 November 2026 in one image: **THE WORLD IN ONE DAY**.

`entry.png` is a 1024×1024 editorial poster — a dark-navy page with a bold date masthead
("WEDNESDAY 18 NOVEMBER 2026"), five warm-accent story panels across the middle, and a
footer strip with the day's three secondary headlines. Every element (skylines, bridge,
tanker, cyclone, handshake) is drawn from scratch with Pillow primitives — no external
images — and all text is auto-fitted so nothing is clipped.

## The five stories

1. **TRUMP LANDS IN MANILA** — US president arrives for Quad talks ahead of China visit; ASEAN summit under way.
2. **CRIMEA BRIDGE HIT AGAIN** — Ukraine strikes the bridge a 2nd day; Russia hits bridges in Kyiv, cutting water and power.
3. **TANKER ATTACKED IN HORMUZ** — MT TARA GAS hit in the Strait; 21 of 24 Indian crew evacuated safely to Khasab.
4. **CYCLONE AKVAN BEARS DOWN** — Storm intensifies over Bay of Bengal; Andhra Pradesh and Odisha on high alert.
5. **CANADA-CHINA TRADE DEAL** — Xi meets Carney as Ottawa and Beijing extend trade deals ahead of APEC.

Footer: Britain sanctions Israeli settlement firms • MS Dhoni retires from IPL, to mentor
Chennai Super Kings • India re-elected to ITU Council 2027-2030.

## Run it

Rebuild the poster with the build venv (Pillow), then copy it to the output dir with the
stdlib-only entry program:

```sh
/data/home/makefun/news-image-venv/bin/python tools/generate_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, stdlib only — `os`, `pathlib`, `shutil`) copies the pre-rendered
`entry.png` beside it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The generator
is deterministic: running it twice produces byte-identical PNGs, so both make.fun runs of
`main.py` write identical output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=Sipalingtesnet&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>