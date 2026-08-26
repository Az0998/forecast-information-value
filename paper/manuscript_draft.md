# Information bottlenecks, not architectures: a cross-media protocol for mid-range environmental forecasts

**Target:** *Ecological Informatics* (research article)  
**Backup:** *Artificial Intelligence for the Earth Systems* (AMS), if the oxygen cube is later replaced by GOBAI-O2  
**Authors:** Senjie Zhang (张森捷)¹,*  
**Affiliation:** ¹ Lanzhou University, Lanzhou 730000, Gansu, China  
**Correspondence:** 3079099853@qq.com  
**Code:** https://github.com/Az0998/forecast-information-value  
**Sister protocol paper (missingness):** https://github.com/Az0998/maskview-aquatic-protocol

**Status:** content draft from frozen open experiments; paste into the journal template before submission.

---

## Abstract

Machine-learning papers in hydrology and coastal biogeochemistry often report that a new network outperforms persistence on a single basin or shelf. Editors increasingly read such manuscripts as case studies. We instead ask a transferable question: **relative to a simple domain baseline, where does a learned forecast add decision skill, and which missing information caps that skill?** We apply one evaluation grammar to two media. On five USGS rivers spanning humid, snowmelt and semi-arid climates, a lagged-upstream linear routing baseline already captures most next-day Nash–Sutcliffe efficiency (NSE); upstream gauges add large information only on the James (ΔNSE +0.13) and almost none on the Willamette (≈0). Perfect future precipitation raises 3- and 7-day NSE by +0.12 and +0.20 while adding nothing at 1 day, so the weekly bottleneck is foresight, not attention. P90 flood critical success index (CSI) of the learned model remains 0.75 / 0.29 / 0.26 at 1 / 3 / 7 days, while routing CSI falls to 0.04 at 7 days. On an East China Sea shelf oxygen cube, a spatiotemporal Transformer beats climatology at 1 month (RMSE 3.88 vs 5.30 µmol kg⁻¹; hypoxia F1 0.74) but a climatology–Transformer hybrid is required at 2 months, and Argo-like history raises lead-1 RMSE by ~35%. Residual errors concentrate in the coastal tercile (MAE 3.30 vs 2.95 µmol kg⁻¹ offshore). The protocol—simple baseline, event score, information ceiling, failure locus—is the contribution. We do not claim a universal sequence model.

**Keywords:** environmental forecasting; information value; streamflow; dissolved oxygen; hypoxia; critical success index; climatology; sparse observations

---

## 1. Introduction

Two literatures look unrelated: short-range river forecasting with LSTM-class models, and monthly mapping or nowcasting of coastal hypoxia. Both, however, are often written as “model X on region Y,” which hydrology editors have repeatedly desk-rejected as regional case studies with standard techniques. The scientific gap is not another encoder. It is a **grammar for information value** that a reader in another basin or another ocean can falsify.

We take four ingredients that already exist separately and require them on every figure: (i) a naive baseline (persistence); (ii) a domain-simple baseline (lagged-upstream linear routing; month-of-year oxygen climatology); (iii) a decision metric (P90 flood CSI; hypoxia F1/CSI); (iv) an explicit bottleneck test (oracle precipitation; dense vs Argo-like oxygen history; coastal residual maps). Learned models are instruments, not the claim.

The river experiments use public USGS discharge and Open-Meteo / GFS precipitation on Potomac, James, Willamette, Animas and Verde. The ocean experiments use a WOA-informed East China Sea shelf oxygen cube with T/S, OISST and ERA5-backed wind, scored at 1–3 month leads. We state up front that the oxygen target is a development cube, not GOBAI-O2; that limitation bounds process claims, not the protocol.

---

## 2. Methods (evaluation grammar)

### 2.1 Shared protocol

For each lead time τ:

1. Fit or apply persistence and the domain-simple baseline.  
2. Fit one learned model with the same predictors (river: LSTM-Attention / XGBoost already reported; ocean: spatiotemporal Transformer and a validation-tuned hybrid with climatology).  
3. Report continuous skill (NSE or RMSE) **and** an event score.  
4. Remove or replace one information source (upstream gauges; observed vs oracle precipitation; dense vs column-limited oxygen) and record the delta.  
5. Map residuals onto a physical axis (climate class; coastal proximity; 50 dbar).

If a panel cannot be read as answering “relative to what, for which decision, capped by what,” it does not belong in the paper.

### 2.2 Rivers

Routing baseline: linear map from lagged upstream discharge to the target gauge. Ablation ΔNSE = full-network learned NSE minus local-only learned NSE at 1 day. Flood events: exceedance of the training-period 90th percentile; CSI / POD / FAR. Oracle precipitation replaces observed catchment rain with perfect future rain at 3–7 days. SHAP on Potomac 1-day XGBoost ranks target discharge ≫ upstream Q ≫ temperature/precipitation.

### 2.3 Shelf oxygen

History length 12 months; leads 1, 2, 3 months; year-block splits. Event threshold: 10th percentile of oxygen (hypoxia-style low-O₂). Sparse tests (Mask-View / Argo columns) keep physics visible and hide oxygen history. Failure-mode bins: SST-front gradient, N², coastal proximity, depth. Hybrid blend weights are tuned on validation and shrink toward climatology at longer leads.

---

## 3. Results

### 3.1 Gauge information is not a universal constant

At 1-day lead, routing NSE already exceeds 0.86 on humid and snowmelt basins. Upstream ablation ΔNSE is **+0.13 on James**, **+0.02 on Potomac**, **≈0 on Willamette**, **+0.01 on Animas**, and **+0.06 on Verde** where the learned model (NSE 0.39) **loses to routing (0.61)**. Learned architectures are therefore not uniformly safer than a linear hydrologic reference.

### 3.2 Event skill and the precipitation ceiling

On Potomac, P90 CSI is 0.75 (learned) vs 0.62 (routing) vs 0.56 (persistence) at 1 day; at 7 days routing CSI is 0.04 while the learned CSI is 0.26. Oracle precipitation changes 1-day NSE by ≈0, then **+0.12 at 3 days and +0.20 at 7 days**. Weekly river skill is limited by rain information, not by replacing attention with another block.

### 3.3 Oxygen: use the Transformer at one month, climatology thereafter

Lead-1 ST RMSE 3.88 µmol kg⁻¹ (skill vs climatology 0.47; F1 0.74). Lead-2 hybrid 5.08 vs climatology 5.23; standalone ST 5.83 is worse than climatology. Lead-3 ST 9.81 is unusable; hybrid ≈ climatology. Under Argo/station column history, lead-1 ST RMSE rises to ≈5.23–5.24 (~+35%). Physics drivers help mid-lead hybrid skill relative to oxygen-only history; they do not remove the climatology takeover.

### 3.4 Where residuals live

Coastal-proximity high tercile MAE 3.30 vs 2.95–2.97 offshore/mid. Depth MAE peaks at 50 dbar (3.18). SST-front terciles are **not** monotonic on this cube; we do not claim frontal process skill until a time-varying oxygen target is used.

Figures: `results/figures/fig_information_bottleneck.png` (four-panel protocol) and `fig_ocean_coastal_failure.png`.

---

## 4. Discussion

The two media share a sentence: **learned forecasts add skill only while the limiting input is present.** On rivers that is unsaturated autocorrelation plus usable QPF; on the shelf that is dense recent oxygen (and even then only near lead-1). Publishing only NSE on Potomac, or only RMSE on a dense oxygen cube, hides both bottlenecks and invites a “case study” desk reject.

We are not merging discharge and oxygen into one network. Reviewers should treat the shared object as the **protocol**. Sister work (Mask-View aquatic missingness) addresses how observation holes change imputer ranking; this paper addresses how **lead time and missing drivers** change forecast ranking.

Limitations: USGS-centric rivers (no Chinese basin in the climate ladder yet); WOA-informed oxygen cube; flood CSI from one mid-Atlantic pair; no GEFS ensemble probabilities.

---

## 5. Conclusions

A four-part information-value protocol—simple baseline, event score, information ceiling, failure locus—reproduces consistent conclusions on rivers and a shelf oxygen cube without a new architecture. Recommended operational recipes are conditional: routing or learned next-day flow depending on climate; Transformer oxygen at 1 month and climatology/hybrid beyond; never interpret dense-history scores as Argo-ready skill.

---

## Data availability

Frozen tables in this repository (`data/frozen/`). Underlying engines: USGS NWIS, Open-Meteo, WOA/OISST, Open-Meteo ERA5-backed wind. Code: https://github.com/Az0998/forecast-information-value.

## Funding

This research received no external funding.

## Conflicts of interest

The author declares no conflicts of interest.

## Author contributions

S.Z.: conceptualization, methodology, software, analysis, writing.
