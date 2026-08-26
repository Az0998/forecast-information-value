# Forecast information-value protocol

Standalone repository for **Paper B**. Clone and run — frozen tables live in `data/frozen/`.

[![pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://az0998.github.io/forecast-information-value/)

**Target journal:** *Ecological Informatics* (or *AIES* if ocean-led)  
**Do not resubmit to HSJ / JHRS / Journal of Hydrology / Water (MDPI).**  
**Author:** Senjie Zhang, Lanzhou University (`3079099853@qq.com`)

Mid-range environmental skill is an **information bottleneck**: extra model capacity does not help once the limiting input is missing.

## Quick start

```bash
git clone https://github.com/Az0998/forecast-information-value.git
cd forecast-information-value
pip install -r requirements.txt
python scripts/build_bottleneck_tables.py
```

## Layout

```
data/frozen/river   climate-zone ΔNSE (Potomac / James / Willamette / Animas / Verde)
data/frozen/ocean   ECS multi-lead skill + Mask-View / failure notes
scripts/            bottleneck tables + figure
results/
docs/               GitHub Pages
```

Experiment engines: `hydro-ml-paper`, `ocean-do-forecast`. This repo is the fused paper’s public artifact.

## License

MIT
