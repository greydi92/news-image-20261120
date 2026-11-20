[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/greydi92/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/greydi92/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — Friday 20 November 2026

Built for the [make.fun "Sum up 20 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261120).

One image that sums up the world's news of Friday 20 November 2026: a front-page infographic with six stories from that day, across regions and fields — Trump pushing the Iran war decision to 2027, the Trump–Putin–Xi peace declaration out of Shenzhen, Cyclone Akvan making landfall on India's east coast, Anthropic jumping 17% on its stock-market debut, GTA VI sales passing $1.8 billion, and a tanker catching fire after hitting a mine east of the Strait of Hormuz. Every story was verified as happening, or first reported, on 20 November 2026.

Sources: Reuters (Trump on Iran), BBC (peace declaration), India Meteorological Department / The Hindu (Cyclone Akvan), The Hindu (Anthropic debut), Mezha (GTA VI sales), Daily Baku (tanker mine strike).

`main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory. The image was rendered at build time by `gen_image.py` (Pillow, DejaVu fonts). No network, no timestamps, no randomness — two runs write byte-identical output.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024, ~110 KB).

---

<sub>Entered on [make.fun](https://make.fun/?ref=qgn48q27&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
