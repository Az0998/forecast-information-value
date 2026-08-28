# Information bottlenecks, not architectures: a cross-media protocol for mid-range environmental forecasts

**Target:** *Ecological Informatics* (research article)  
**Backup:** *Artificial Intelligence for the Earth Systems* (AMS), if the oxygen cube is later replaced by GOBAI-O2  
**Authors:** Senjie Zhang (张森捷)¹,*  
**Affiliation:** ¹ Lanzhou University, Lanzhou 730000, Gansu, China  
**Correspondence:** 3079099853@qq.com  
**Code:** https://github.com/Az0998/forecast-information-value  
**Sister protocol paper (missingness):** https://github.com/Az0998/maskview-aquatic-protocol

**Status:** Ecological Informatics submission package (28 August 2026). Rebuild Word with `python scripts/build_ecoinf_manuscript.py`. Word file is the submission artifact; this markdown is the working draft.

---

## Abstract

Machine-learning papers in hydrology and coastal biogeochemistry often report that a new network outperforms persistence on a single basin or shelf. We instead ask a transferable question: **relative to a simple domain baseline, where does a learned forecast add decision skill, and which missing information caps that skill?** We apply one evaluation grammar to two media. On five USGS rivers spanning humid, snowmelt and semi-arid climates, a lagged-upstream linear routing baseline already captures most next-day Nash–Sutcliffe efficiency (NSE). Upstream gauges add large information only on the James (ΔNSE +0.13) and almost none on the Willamette (≈0). Model class is not a uniform upgrade: on the semi-arid Verde, XGBoost beats routing at 1 day (NSE 0.66 versus 0.61) while LSTM-Attention loses (0.38), and XGBoost NSE turns negative at 3–7 days. A nested Bow River transfer in Alberta reproduces next-day routing saturation outside the USGS network. An ordinary-least-squares precipitation ceiling is ~0 at 3 days on snowmelt (Animas, Bow) and +0.07 on the Potomac. Perfect future precipitation raises 3- and 7-day LSTM NSE by +0.12 and +0.20 on the Potomac, but operational GFS QPF is negative at 3 days (−0.03). P90 flood CSI of LSTM-Attention remains 0.75 / 0.29 / 0.26 at 1 / 3 / 7 days on the Potomac, while routing CSI falls to 0.04 at 7 days. On a WOA-informed East China Sea shelf oxygen cube, a spatiotemporal Transformer beats climatology at 1 month (RMSE 3.88 versus 5.30 µmol kg⁻¹) but a climatology–Transformer hybrid is required at 2 months, and Argo-like history raises lead-1 RMSE by ~35%. Residual errors concentrate in the coastal tercile (MAE 3.30 versus 2.95 µmol kg⁻¹ offshore). Low-oxygen scores use the training 10th percentile (195 µmol kg⁻¹), not hypoxia <60 µmol kg⁻¹, which is rare on this development cube. The protocol—simple baseline, event score, information ceiling, failure locus—is the contribution. We do not claim a universal sequence model.

**Keywords:** environmental forecasting; information value; streamflow; dissolved oxygen; critical success index; climatology; quantitative precipitation forecast; sparse observations

---

## 1. Introduction

Two literatures look unrelated: short-range river forecasting with LSTM-class models, and monthly mapping or nowcasting of coastal oxygen. Both, however, are often written as “model X on region Y.” The scientific gap is not another encoder. It is a **grammar for information value** that a reader in another basin or another ocean can falsify.

We take four ingredients that already exist separately and require them on every figure: (i) a naive baseline (persistence); (ii) a domain-simple baseline (lagged-upstream linear routing in the Muskingum transfer-function family; month-of-year oxygen climatology); (iii) a decision metric (P90 flood CSI; low-tail oxygen F1/CSI at the training 10th percentile); (iv) an explicit bottleneck test (oracle precipitation versus operational GFS QPF; dense versus Argo-like oxygen history; coastal residual maps). Learned models are instruments, not the claim.

The river experiments use public USGS discharge and Open-Meteo meteorology on Potomac, James, Willamette, Animas and Verde, operational GFS QPF on the Potomac only, and a nested Water Survey of Canada transfer on the Bow River at Calgary (upstream Cochrane and Banff; Open-Meteo meteorology; native m³ s⁻¹). The ocean experiments use a WOA-informed East China Sea shelf oxygen cube with T/S, OISST and ERA5-backed wind, scored at 1–3 month leads. We state up front that the oxygen target is a development cube (climatological structure plus synthetic autoregressive anomalies), not GOBAI-O2; that limitation bounds process claims, not the protocol.

---

## 2. Methods (evaluation grammar)

### 2.1 Shared protocol

For each lead time τ:

1. Fit or apply persistence and the domain-simple baseline.  
2. Fit more than one learned instrument with the same predictors (rivers: LSTM-Attention and XGBoost; ocean: spatiotemporal Transformer and a validation-tuned hybrid with climatology).  
3. Report continuous skill (NSE or RMSE) **and** an event score.  
4. Remove or replace one information source (upstream gauges; observed vs GFS vs oracle precipitation; dense vs column-limited oxygen) and record the delta.  
5. Map residuals onto a physical axis (climate class; coastal proximity; 50 dbar).

If a panel cannot be read as answering “relative to what, for which decision, capped by what,” it does not belong in the paper.

### 2.2 Rivers

Routing baseline: ordinary least squares on lagged target and upstream discharge, a linear transfer-function analogue of Muskingum routing. Ablation ΔNSE = full-network LSTM NSE minus local-only LSTM NSE. Flood events: exceedance of the training-period 90th percentile; CSI / POD / FAR. LSTM CSI and LSTM oracle precipitation are reported for the Potomac; XGBoost completes the event-score leg across the five USGS climates. Operational QPF uses Open-Meteo GFS previous-run precipitation on Potomac 2024. The precipitation ceiling used for transfer claims is ordinary least squares with perfect future rain. SHAP on Potomac 1-day XGBoost ranks target discharge ≫ upstream Q ≫ temperature/precipitation.

### 2.3 Shelf oxygen

History length 12 months; leads 1, 2, 3 months; year-block splits. Event threshold: 10th percentile of oxygen on the training cube (195.09 µmol kg⁻¹). Absolute hypoxia (<60 µmol kg⁻¹) occupies <1% of cells; we therefore report **low-tail** F1/CSI, not hypoxia prevalence. Sparse tests (Mask-View / Argo columns) keep physics visible and hide oxygen history; they are information-ceiling tests, not a rank-reversal study (that is the sister Mask-View paper). Failure-mode bins: SST-front gradient, N², coastal proximity, depth. Hybrid blend weights are tuned on validation and shrink toward climatology at longer leads (w = 1.0, 0.35, 0.05).

---

## 3. Results

### 3.1 Gauge information and model class are climate-conditional

At 1-day lead, routing NSE already exceeds 0.86 on humid and snowmelt basins (Table 1). Upstream ablation ΔNSE is **+0.13 on James**, **+0.02 on Potomac**, **≈0 on Willamette**, **+0.01 on Animas**, and **+0.06 on Verde**.

The Verde result is a model-class × climate interaction, not a blanket failure of learning. One-day NSE is **XGBoost 0.66 > routing 0.61 > LSTM-Attention 0.38**. At 3 and 7 days Verde XGBoost NSE is negative (−0.12 / −0.11) while routing remains positive (0.25 / 0.19). On the Willamette, 7-day LSTM-Attention is **0.15 NSE worse than routing**. Animas 7-day routing NSE is still 0.85: seasonal memory, not architecture, carries the week. James LSTM already loses to routing at 3 days. On the Bow at Calgary the same 1-day saturation appears **outside the USGS network** (routing NSE 0.98, persistence 0.97, XGBoost 0.87): XGB again loses to routing on NSE but wins P90 CSI (0.89 vs 0.86). Architectures are therefore not uniformly safer than a linear hydrologic reference, and the ranking **flips with lead time and with the score**.

### 3.2 Event skill, operational QPF, and the precipitation ceiling

On the Potomac, LSTM P90 CSI is 0.75 versus routing 0.62 and persistence 0.56 at 1 day; at 7 days routing CSI is 0.04 while learned CSI remains 0.26 (Table 2). LSTM oracle precipitation changes 1-day NSE by ≈0, then **+0.12 at 3 days and +0.20 at 7 days**.

The operational ladder is stricter than the oracle (Fig. 1d; Potomac 2024): observation-only NSE 0.41 at 3 days, **GFS QPF −0.03**, oracle 0.58. Weekly river skill is limited by rain information, and **usable** rain information is not the same as a perfect future field.

XGBoost completes the same event-score and ceiling legs on all five climates (Fig. 3). One-day P90 CSI: Verde XGB 0.83 > persistence 0.79 > routing 0.54 — routing NSE looks acceptable (0.61) but flood CSI is worse than persistence. James XGB CSI 0.85 / 0.36 / 0.16 at 1 / 3 / 7 days; routing CSI collapses to 0.09 at 7 days. Animas events are already easy (1-day persist CSI 0.93). Oracle precipitation ΔNSE at 3 days is **+0.27 Verde, +0.17 James, +0.24 Potomac, +0.11 Willamette, +0.008 Animas**: the rain ceiling is climate-conditional, and snowmelt memory does not buy future rain. Verde 1-day oracle ΔNSE is slightly negative (−0.03), consistent with next-day skill already being routing/local flow, not foresight. Climate-band CSI/oracle are a locked XGBoost re-fit; 1-day NSE matches Table 1 within 0.02, and Verde 3/7-day NSE from that re-fit is not used to overwrite Table 1b.

The same grammar on the Bow River (Canada) reproduces the snowmelt ceiling. The **protocol ceiling is ordinary least squares with perfect future rain**, not XGBoost: 3-day linear ΔNSE is +0.07 on Potomac, +0.08 on Verde, **+0.002 on Animas and −0.009 on Bow**. XGBoost 3-day Bow ΔNSE (−0.45) is instrument overfitting and is not used as a process result. Ice-flagged days are 15% of the Bow test window; P90 CSI is **identical** on ice-free days (all 74 events fall in open water).

### 3.3 Oxygen: use the Transformer at one month, climatology thereafter

Lead-1 ST RMSE 3.88 µmol kg⁻¹ (skill vs climatology 0.47; low-tail F1 0.74). Lead-2 hybrid 5.08 vs climatology 5.23; standalone ST 5.83 is worse than climatology. Lead-3 ST 9.81 is unusable; hybrid ≈ climatology. Under Argo/station column history, lead-1 ST RMSE rises to ≈5.23–5.24 (~+35%). Physics drivers help mid-lead hybrid skill relative to oxygen-only history; they do not remove the climatology takeover. Seasonal test counts are small (JJAS n=8, DJF n=5) and are not used as main claims.

### 3.4 Where residuals live

Coastal-proximity high tercile MAE 3.30 vs 2.95–2.97 offshore/mid. Depth MAE peaks at 50 dbar (3.18). SST-front terciles are **not** monotonic on this cube; we do not claim frontal process skill until a time-varying oxygen target is used.

Figures: `results/figures/fig_information_bottleneck.png`, `fig_verde_model_class.png`, `fig_climate_event_ceiling.png`, `fig_bow_transfer.png`, `fig_ocean_coastal_failure.png`.

---

## 4. Discussion

The two media share a sentence: **learned forecasts add skill only while the limiting input is present.** On rivers that is unsaturated autocorrelation plus *usable* precipitation foresight; on the shelf that is dense recent oxygen (and even then only near lead-1). Publishing only 1-day LSTM NSE on the Potomac, or only RMSE on a dense oxygen cube, hides both bottlenecks.

We are not merging discharge and oxygen into one network. Reviewers should treat the shared object as the **protocol**. Sister work (Mask-View aquatic missingness) addresses how observation holes change imputer ranking; this paper addresses how **lead time and missing drivers** change forecast ranking.

Limitations: no nested Chinese daily-discharge ladder yet (CAMELS-CN Yellow River gauges are normalized, not raw nested Q); Bow record starts 2006 and is ice-affected / regulated; WOA-informed oxygen cube with synthetic anomalies; GFS QPF from Potomac only; low-tail oxygen events are not hypoxia; no GEFS ensemble probabilities. LSTM CSI remains Potomac-only; climate-band and Bow event scores use XGBoost.

---

## 5. Conclusions

A four-part information-value protocol—simple baseline, event score, information ceiling, failure locus—reproduces consistent conclusions on rivers and a shelf oxygen cube without a new architecture. Operational recipes are conditional: routing or XGBoost next-day flow depending on climate, never LSTM-by-default on semi-arid flashy basins; Transformer oxygen at 1 month and climatology/hybrid beyond; never interpret dense-history scores as Argo-ready skill; never treat raw QPF as oracle rain.

---

## Data availability

Frozen tables in this repository (`data/frozen/`). Discharge from USGS NWIS and Water Survey of Canada HYDAT; meteorology from Open-Meteo; oxygen cube from WOA / OISST with ERA5-backed wind. Code: https://github.com/Az0998/forecast-information-value.

## Ethics

This study used publicly available hydrometric and ocean-climatology products. No human or animal subjects were involved.

## Declaration of generative AI

During the preparation of this work the author used Cursor (an AI-assisted editor) to assemble English prose from locked numerical tables and to check formatting. After using this tool, the author reviewed and edited the content and takes full responsibility for the analyses and interpretations.

## Funding

This research received no external funding.

## Conflicts of interest

The author declares no conflicts of interest.

## Author contributions

S.Z.: conceptualization, methodology, software, analysis, writing.
