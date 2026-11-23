# news-image-20261122
[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/sipemburu23/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/sipemburu23/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

The World in One Day — Sunday 22 November 2026. A single image summing up the day's world news: 33 stories (3 leads + 10 cards + 20 briefs), 13 drawn, across 7 regions.

**Leads:** COP31 collapses with no deal in Antalya · Two tankers hit by mines near Hormuz · Drone flattens flats in Dymer — boy, 7, pulled alive.

**Cards:** Democrats take 258 House seats · Russian corvette hit off Benghazi · 34 missing in Indonesia candy factory fire · Alcaraz wins first ATP Finals title · Shuri Castle rises again after 7 years · Nepal's PM lands in New Delhi · Settlers burn 12 cars in West Bank · US–China power gap narrows to 5.3 · Bessent presses Nvidia on China chips · India piles up 720/9 in Wellington.

**Briefs (14–33):** Delta outage delays 1,600+ flights · China cuts margin ratio to 80% · Drone strikes kill 4 in Khartoum · Fighting disrupts Ebola response in Congo · Molly Meldrum dies aged 83 · Australia's flash PMI falls to 46.1 · Poland: Russia tried to kill Kyivstoner · Iran unveils double missile launcher · BJP MP Wadkute dies at 72 · Bessent warns the Fed not to overtighten · Army to detonate lead azide in Iowa · India, China conclude border talks · S. Korea education minister quits · Thitikul wins third straight $4m title · Brazil storm toll: 5 dead, 25,212 hit · Peru quake: 1 dead, 152 homes lost · FBI probes suspected NCIC hack · Poland: all three objects were Kh-101s · Liverpool thrash 10-man United 4-0 · Price wins fourth Grand Slam of Darts.

## How to run

```sh
node main.ts            # copies entry.png to /output/entry.png
OUTPUT_DIR=/tmp/out node main.ts
```

`main.ts` is copy-only: it never runs `draw.py`. The front page is baked into `entry.png` at build time by `draw.py` (Python + Pillow, all artwork drawn in code — no external images).

## License

MIT — see LICENSE.
