# Bow River (Canada) transfer — same protocol, non-US nested gauges

Source: WSC HYDAT via GeoMet (`hydrometric-daily-mean`), Open-Meteo archive precip/temp.
Target `05BH004` Calgary; upstream `05BH005` Cochrane and `05BB001` Banff.
Record after inner join: 2006-04-01 to 2023-10-31 (n=4235). Units: m³ s⁻¹.
Winter discharge is often ice-affected (Calgary ~35% of days flagged). Same chronological split as USGS basins (train≤2018, val 2019–2020, test 2021–2023; test n=756).

## 1 / 3 / 7 day (XGBoost instrument)

| lead | persist NSE | routing NSE | XGB NSE | XGB−local ΔNSE | persist CSI | routing CSI | XGB CSI | oracle ΔNSE |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.973 | 0.976 | 0.871 | +0.082 | 0.850 | 0.855 | 0.886 | −0.006 |
| 3 | 0.880 | 0.896 | 0.916 | +0.210 | 0.644 | 0.795 | 0.783 | −0.450 |
| 7 | 0.723 | 0.729 | 0.857 | +0.037 | 0.410 | 0.505 | 0.618 | −0.135 |

## Transfer reading vs Animas (US snowmelt)

- Next-day skill is already saturated by persistence/routing (NSE > 0.97), as on Animas.
- 1-day oracle precipitation ΔNSE ≈ 0, as on Animas: foresight is not the 1-day bottleneck.
- 3–7 day **perfect rain does not lift OLS skill** (ΔNSE −0.009 / +0.025). XGB 3-day ΔNSE −0.45 is overfitting, not the protocol ceiling.
- Ice-flagged days are 15% of the test window; P90 CSI is unchanged on ice-free days (74/74 events in open water).
- Upstream gauges still have mid-lead information (3-day ablation +0.21), unlike Willamette’s near-zero 1-day ablation.
- XGB **loses to routing on 1-day NSE** (0.87 vs 0.98) but **wins P90 CSI** (0.89 vs 0.86): event score ≠ NSE, same grammar as Verde.

Do not treat the large negative 3-day oracle ΔNSE as a process claim about rain; it is a ceiling test returning ≤0 on a snowmelt/regulated main stem (Bearspaw/Ghost influence downstream of Banff).
