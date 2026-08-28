# Forecast information-value protocol

Public frozen artifact for the Ecological Informatics manuscript
*Information bottlenecks, not architectures: a cross-media protocol for mid-range environmental forecasts*.

[![pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://az0998.github.io/forecast-information-value/)

**Author:** Senjie Zhang, Lanzhou University (`3079099853@qq.com`)

Mid-range environmental skill is an **information bottleneck**: extra model capacity does not help once the limiting input is missing. Numbers in the Word file are locked to `data/frozen/`.

## Quick start

```bash
git clone https://github.com/Az0998/forecast-information-value.git
cd forecast-information-value
pip install -r requirements.txt
python scripts/build_bottleneck_tables.py
python scripts/build_ecoinf_manuscript.py
python scripts/verify_submission.py
```

- Manuscript: `paper/EcoInf_information_value_manuscript.docx`
- Highlights: `paper/highlights.txt`
- Cover letter: `paper/cover_letter.txt`
- Upload steps: `paper/HOW_TO_SUBMIT_ECOINF.md`

## Layout

```
data/frozen/river   USGS climate ladder, Bow (WSC) transfer, OLS rain ceiling
data/frozen/ocean   ECS multi-lead skill, sparse-history ceiling, coastal MAE
scripts/            tables, figures, Word builder, submission checks
results/            regenerated tables and protocol figures
paper/              EcoInf submission files
docs/               GitHub Pages
```

Sibling experiment engines (`hydro-ml-paper`, `ocean-do-forecast`) produced the frozen snapshots. This repository is sufficient to rebuild tables, figures, and the Word manuscript.

## License

MIT
