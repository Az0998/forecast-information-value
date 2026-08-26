"""Build Ecological Informatics submission Word manuscript from frozen Paper B tables."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
TABLES = ROOT / "results" / "tables"
FIGS = ROOT / "results" / "figures"
PAPER.mkdir(parents=True, exist_ok=True)


def font(run, size=11, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def h(doc, text, level=1):
    p = doc.add_paragraph()
    font(p.add_run(text), size=12 if level == 1 else 11, bold=True)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)


def body(doc, text):
    p = doc.add_paragraph()
    font(p.add_run(text), size=11)
    p.paragraph_format.first_line_indent = Inches(0.25)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE


def center(doc, text, size=11, italic=False, after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    font(p.add_run(text), size=size, italic=italic)
    p.paragraph_format.space_after = Pt(after)


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    font(p.add_run(text), size=10)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)


def add_table(doc, headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    for i, ht in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = ""
        font(cell.paragraphs[0].add_run(ht), size=9, bold=True)
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            cell = t.rows[r_i + 1].cells[c_i]
            cell.text = ""
            font(cell.paragraphs[0].add_run(str(val)), size=9)
    return t


def maybe_fig(doc, path: Path, width=6.2) -> bool:
    if path.exists():
        doc.add_picture(str(path), width=Inches(width))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        return True
    return False


def f3(x):
    return f"{float(x):.3f}"


def main():
    river = pd.read_csv(TABLES / "river_1d_information_value.csv")
    events = pd.read_csv(TABLES / "river_event_and_oracle.csv")
    ocean = pd.read_csv(TABLES / "ocean_multilead_skill.csv")
    coast = pd.read_csv(TABLES / "ocean_coastal_mae.csv")
    summary = json.loads((TABLES / "paper_b_summary.json").read_text(encoding="utf-8"))

    def oc(lead, model, col):
        return float(ocean.loc[(ocean.lead_mo == lead) & (ocean.model == model), col].iloc[0])

    doc = Document()
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(11)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    font(
        title.add_run(
            "Information bottlenecks, not architectures: a cross-media protocol "
            "for mid-range environmental forecasts"
        ),
        size=14,
        bold=True,
    )
    center(doc, "Senjie Zhang 1,*", size=11)
    center(doc, "(张森捷)", size=10, italic=True)
    center(doc, "1 Lanzhou University, Lanzhou 730000, Gansu, China", size=10, italic=True)
    center(doc, "*Correspondence: 3079099853@qq.com", size=10, italic=True)
    center(
        doc,
        "Journal: Ecological Informatics (Elsevier)  ·  Article type: Research paper",
        size=9,
        italic=True,
        after=8,
    )
    note = doc.add_paragraph()
    font(
        note.add_run(
            "Elsevier does not require a journal-specific Word template. "
            "Numeric results are locked to data/frozen/ in the companion repository."
        ),
        size=9,
        italic=True,
    )
    note.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    h(doc, "Highlights")
    highlights = [
        "Protocol: domain baseline, event score, information ceiling, failure locus.",
        "Gauge value is climate-conditional: James ΔNSE +0.13 vs Willamette ~0.",
        "Verde LSTM loses to linear routing (NSE 0.39 versus 0.61).",
        "Oracle rain adds ~0 NSE at 1 day but +0.20 at 7 days.",
        "Oxygen Transformer wins at 1 month; climatology takes over later.",
    ]
    for item in highlights:
        p = doc.add_paragraph()
        font(p.add_run("• " + item), size=11)
        p.paragraph_format.space_after = Pt(2)
    cap = doc.add_paragraph()
    font(cap.add_run("(Each highlight ≤85 characters, Elsevier style.)"), size=8, italic=True)

    h(doc, "Abstract")
    body(
        doc,
        "Learned environmental forecasts are often reported as a new network beating persistence "
        "on one basin or shelf. We instead ask a transferable question: relative to a simple "
        "domain baseline, where does a learned model add decision skill, and which missing "
        "information caps that skill? One evaluation grammar is applied to two media. On five "
        "USGS rivers spanning humid, snowmelt and semi-arid climates, lagged-upstream linear "
        "routing already captures most next-day Nash–Sutcliffe efficiency. Upstream gauges add "
        "substantial information only on the James (ΔNSE +0.13) and almost none on the "
        "Willamette. Perfect future precipitation raises 3- and 7-day NSE by +0.12 and +0.20 "
        "and adds nothing at 1 day, so the weekly bottleneck is foresight rather than "
        "architecture. P90 flood critical success index of the learned model is 0.75 / 0.29 / "
        "0.26 at 1 / 3 / 7 days, while routing CSI falls to 0.04 at 7 days. On an East China Sea "
        "shelf oxygen cube, a spatiotemporal Transformer beats climatology at 1 month "
        f"(RMSE {f3(summary['ocean_lead1_ST_RMSE'])} versus 5.30 µmol kg⁻¹) but a "
        "climatology–Transformer hybrid is required at 2 months, and Argo-like history raises "
        "lead-1 RMSE by about 35%. Residuals concentrate in the coastal tercile. The "
        "contribution is the protocol—simple baseline, event score, information ceiling, "
        "failure locus—not a universal sequence model.",
    )

    h(doc, "Keywords")
    p = doc.add_paragraph()
    font(
        p.add_run(
            "environmental forecasting; information value; streamflow; dissolved oxygen; "
            "hypoxia; critical success index; climatology; sparse observations"
        ),
        size=11,
    )

    h(doc, "1. Introduction")
    body(
        doc,
        "Short-range river forecasting with recurrent networks and monthly coastal-oxygen "
        "prediction look like separate literatures. Both, however, are frequently written as "
        "“model X on region Y.” Without a baseline that a hydrologist or oceanographer already "
        "trusts, without an event score tied to a decision, and without a test of what "
        "information is missing, such papers read as case studies even when the experiments are "
        "careful [1–3].",
    )
    body(
        doc,
        "The gap is not another encoder. It is a grammar for information value that a reader in "
        "another basin or another ocean can falsify. We require four ingredients on every "
        "figure: (i) persistence; (ii) a domain-simple baseline—lagged-upstream linear routing "
        "for rivers [4] and month-of-year climatology for oxygen; (iii) a decision metric—P90 "
        "flood critical success index (CSI) [5] and hypoxia-style F1/CSI; (iv) an explicit "
        "bottleneck test—oracle precipitation, dense versus Argo-like oxygen history, and "
        "coastal residual maps. Learned models are instruments, not the claim.",
    )
    body(
        doc,
        "Rivers use public USGS discharge with Open-Meteo / GFS precipitation on the Potomac, "
        "James, Willamette, Animas and Verde. The ocean experiments use a WOA-informed East "
        "China Sea shelf oxygen cube with temperature, salinity, OISST and ERA5-backed wind at "
        "1–3 month leads. The oxygen target is a development cube, not GOBAI-O2 [6]; that "
        "limitation bounds process claims, not the protocol. Daily estuary hypoxia AI [7] is a "
        "related but shorter-range task.",
    )

    h(doc, "2. Methods")
    h(doc, "2.1 Shared protocol", level=2)
    body(
        doc,
        "For each lead time we (1) apply persistence and the domain-simple baseline; (2) fit "
        "one learned model on the same predictors (LSTM-Attention / XGBoost on rivers; "
        "spatiotemporal Transformer and a validation-tuned hybrid with climatology on oxygen); "
        "(3) report continuous skill and an event score; (4) remove or replace one information "
        "source and record the delta; (5) map residuals onto a physical axis (climate class, "
        "coastal proximity, 50 dbar). If a panel cannot be read as “relative to what, for which "
        "decision, capped by what,” it is omitted.",
    )
    h(doc, "2.2 Rivers", level=2)
    body(
        doc,
        "The routing baseline is a linear map from lagged upstream discharge to the target "
        "gauge. Ablation ΔNSE is full-network learned NSE minus local-only learned NSE at 1 "
        "day. Flood events exceed the training-period 90th percentile. Oracle precipitation "
        "replaces observed catchment rain with perfect future rain. SHAP on Potomac 1-day "
        "XGBoost ranks target discharge ahead of upstream flow and precipitation [8].",
    )
    h(doc, "2.3 Shelf oxygen", level=2)
    body(
        doc,
        "History length is 12 months; leads are 1, 2 and 3 months with year-block splits. The "
        "event threshold is the 10th percentile of oxygen. Sparse tests hide oxygen history "
        "while keeping physical drivers visible (point, block, sensor, station, mixed, Argo "
        "columns). Hybrid blend weights are tuned on validation and shrink toward climatology "
        "at longer leads.",
    )

    h(doc, "3. Results")
    h(doc, "3.1 Gauge information is climate-conditional", level=2)
    body(
        doc,
        "At 1-day lead, routing NSE already exceeds 0.86 on humid and snowmelt basins (Table 1). "
        "Upstream ablation ΔNSE is +0.13 on James, +0.02 on Potomac, ≈0 on Willamette, +0.01 on "
        "Animas, and +0.06 on Verde, where the learned model (NSE 0.39) loses to routing "
        "(0.61). Architectures are therefore not uniformly safer than a linear hydrologic "
        "reference.",
    )
    add_table(
        doc,
        ["Basin", "Climate", "Routing NSE", "Learned NSE", "Upstream ΔNSE", "Learned−routing"],
        [[r.basin, r.climate, f3(r.routing_NSE), f3(r.lstm_attention_NSE), f3(r.ablation_delta), f3(r.attn_minus_routing)] for r in river.itertuples()],
    )
    caption(doc, "Table 1. One-day river skill. ΔNSE is the information value of upstream gauges.")

    h(doc, "3.2 Event skill and the precipitation ceiling", level=2)
    body(
        doc,
        "On the Potomac, P90 CSI is 0.75 (learned) versus 0.62 (routing) and 0.56 (persistence) "
        "at 1 day; at 7 days routing CSI is 0.04 while learned CSI remains 0.26 (Table 2). "
        "Oracle precipitation changes 1-day NSE by about 0, then +0.12 at 3 days and +0.20 at "
        "7 days. Weekly river skill is limited by rain information, not by replacing attention "
        "with another block.",
    )
    add_table(
        doc,
        ["Lead (d)", "Routing CSI", "Learned CSI", "Persist CSI", "Oracle ΔNSE"],
        [[int(r.horizon), f3(r.routing_CSI), f3(r.attn_CSI), f3(r.pers_CSI), f3(r.delta_NSE)] for r in events.itertuples()],
    )
    caption(doc, "Table 2. Potomac P90 flood CSI and oracle-precipitation ΔNSE.")

    h(doc, "3.3 Oxygen: Transformer at one month, climatology thereafter", level=2)
    body(
        doc,
        f"Lead-1 Transformer RMSE is {f3(oc(1,'st_transformer','RMSE'))} µmol kg⁻¹ "
        f"(skill versus climatology {f3(oc(1,'st_transformer','skill_vs_clim'))}; "
        f"F1 {f3(oc(1,'st_transformer','hypoxia_F1'))}). At two months the hybrid "
        f"({f3(oc(2,'hybrid_clim_st','RMSE'))}) matches climatology "
        f"({f3(oc(2,'climatology','RMSE'))}) while the standalone Transformer "
        f"({f3(oc(2,'st_transformer','RMSE'))}) is worse than climatology. At three months the "
        "Transformer is unusable; the hybrid collapses to climatology. Argo- or station-column "
        "oxygen history raises lead-1 RMSE by about 35%. Physical drivers help mid-lead hybrid "
        "skill relative to oxygen-only history; they do not prevent climatology takeover.",
    )
    key_models = ["persistence", "climatology", "st_transformer", "hybrid_clim_st"]
    sub = ocean[ocean["model"].isin(key_models)]
    add_table(
        doc,
        ["Lead (mo)", "Model", "RMSE", "Skill vs clim", "Hypoxia F1", "CSI"],
        [[int(r.lead_mo), r.model, f3(r.RMSE), f3(r.skill_vs_clim), f3(r.hypoxia_F1), f3(r.CSI)] for r in sub.itertuples()],
    )
    caption(doc, "Table 3. East China Sea shelf oxygen multi-lead scores (µmol kg⁻¹ RMSE).")

    h(doc, "3.4 Where residuals live", level=2)
    body(
        doc,
        "Coastal-proximity high tercile MAE is 3.30 µmol kg⁻¹ versus 2.95–2.97 offshore and mid "
        "(Table 4). Depth MAE peaks at 50 dbar. SST-front terciles are not monotonic on this "
        "cube; frontal process skill is not claimed until a time-varying oxygen target is used.",
    )
    add_table(
        doc,
        ["Coastal tercile", "N cells", "MAE", "P90 MAE"],
        [[r.bin, int(r.n_cells), f3(r.mae), f3(r.p90)] for r in coast.itertuples()],
    )
    caption(doc, "Table 4. Lead-1 oxygen MAE by coastal-proximity tercile.")

    h(doc, "3.5 Protocol figures", level=2)
    if maybe_fig(doc, FIGS / "fig_information_bottleneck.png", 6.3):
        caption(
            doc,
            "Fig. 1. Information-value protocol. (a) Climate-conditional gauge ΔNSE. "
            "(b) P90 flood CSI versus lead. (c) Oxygen RMSE versus lead. "
            "(d) Oracle precipitation ceiling.",
        )
    if maybe_fig(doc, FIGS / "fig_ocean_coastal_failure.png", 4.8):
        caption(doc, "Fig. 2. Coastal concentration of oxygen residuals on the development cube.")

    h(doc, "4. Discussion")
    body(
        doc,
        "The two media share one sentence: learned forecasts add skill only while the limiting "
        "input is present. On rivers that input is unsaturated autocorrelation plus usable "
        "precipitation foresight; on the shelf it is dense recent oxygen, and even then only "
        "near a one-month lead. Reporting only NSE on the Potomac, or only RMSE on a dense "
        "oxygen cube, hides both bottlenecks.",
    )
    body(
        doc,
        "Discharge and oxygen are not trained as one network. The shared object is the "
        "protocol. A sister study treats operational missingness as the factor that reverses "
        "imputer rankings [9]; this paper treats lead time and missing drivers as the factors "
        "that reverse forecast rankings. Limitations include a USGS-centric climate ladder, a "
        "WOA-informed oxygen cube, flood CSI from one mid-Atlantic pair, and the absence of "
        "GEFS ensemble probabilities.",
    )

    h(doc, "5. Conclusions")
    body(
        doc,
        "A four-part information-value protocol—simple baseline, event score, information "
        "ceiling, failure locus—yields consistent conclusions on rivers and a shelf oxygen cube "
        "without a new architecture. Operational recipes are conditional: routing or a learned "
        "next-day flow depending on climate; a Transformer for oxygen at one month and "
        "climatology or a hybrid thereafter; never treat dense-history scores as Argo-ready skill.",
    )

    h(doc, "CRediT authorship contribution statement")
    body(
        doc,
        "Senjie Zhang: Conceptualization, Methodology, Software, Formal analysis, "
        "Visualization, Writing — original draft.",
    )
    h(doc, "Declaration of competing interest")
    body(doc, "The author declares that there are no competing interests.")
    h(doc, "Funding")
    body(doc, "This research received no external funding.")
    h(doc, "Data availability")
    body(
        doc,
        "Frozen tables and figure sources: https://github.com/Az0998/forecast-information-value "
        "(accessed 26 August 2026). Discharge from USGS NWIS; meteorology from Open-Meteo; "
        "oxygen cube from WOA / OISST with ERA5-backed wind.",
    )
    h(doc, "Acknowledgments")
    body(
        doc,
        "The author thanks the USGS, NOAA WOA/OISST, and Open-Meteo data providers.",
    )

    h(doc, "References")
    refs = [
        "Kratzert, F.; Klotz, D.; Brenner, C.; Schulz, K.; Herrnegger, M. Rainfall–runoff prediction at multiple timescales with a single Long Short-Term Memory network. Hydrol. Earth Syst. Sci. 2018, 22, 6005–6022.",
        "Nearing, G.S.; et al. What role does hydrological science play in the age of machine learning? Water Resour. Res. 2021, 57, e2020WR028091.",
        "Frame, J.M.; et al. Deep learning rainfall–runoff predictions of extreme events. Hydrol. Earth Syst. Sci. 2022, 26, 3377–3392.",
        "Morin, J.; et al. Linear routing and lagged upstream discharge as operational references for short-range flow forecasts. (Use the specific routing/regression baseline citation from the hydro-ml-paper methods when copy-editing.)",
        "Wilks, D.S. Statistical Methods in the Atmospheric Sciences, 4th ed.; Elsevier: Amsterdam, The Netherlands, 2019.",
        "Sharp, J.D.; et al. GOBAI-O2: temporally and spatially resolved fields of ocean interior dissolved oxygen over nearly two decades. Earth Syst. Sci. Data 2023, 15, 4481–4518.",
        "Zheng, G.; Friedrichs, M.A.M.; et al. Hypoxia forecasting for Chesapeake Bay using artificial intelligence. Artif. Intell. Earth Syst. 2024, 3, e230054.",
        "Lundberg, S.M.; Lee, S.-I. A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems; 2017.",
        "Zhang, S. Mask-View protocol for operational missingness in aquatic monitoring networks. Companion repository: https://github.com/Az0998/maskview-aquatic-protocol (accessed 26 August 2026).",
        "Breitburg, D.; et al. Declining oxygen in the global ocean and coastal waters. Science 2018, 359, eaam7240.",
        "Paerl, H.W.; Huisman, J. Blooms like it hot. Science 2008, 320, 57–58.",
        "Jolliffe, I.T.; Stephenson, D.B. Forecast Verification: A Practitioner’s Guide in Atmospheric Science, 2nd ed.; Wiley: Chichester, UK, 2012.",
        "Abu-El-Haija, S.; et al. MixHop: Higher-Order Graph Convolutional Architectures via Sparsified Neighborhood Mixing. In ICML; 2019.",
        "Vaswani, A.; et al. Attention is all you need. In Advances in Neural Information Processing Systems; 2017.",
        "World Ocean Atlas 2023. NOAA National Centers for Environmental Information.",
        "Huang, B.; et al. NOAA 1/4° Daily Optimum Interpolation Sea Surface Temperature (OISST).",
        "Open-Meteo. Historical weather API, ERA5-backed. https://open-meteo.com (accessed 26 August 2026).",
        "USGS. National Water Information System. https://waterdata.usgs.gov (accessed 26 August 2026).",
    ]
    for i, r in enumerate(refs, 1):
        p = doc.add_paragraph()
        font(p.add_run(f"[{i}] {r}"), size=10)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_after = Pt(2)

    out = PAPER / "EcoInf_information_value_manuscript.docx"
    try:
        doc.save(out)
    except PermissionError:
        out = PAPER / "EcoInf_information_value_manuscript_v2.docx"
        doc.save(out)
        print("NOTE: docx locked; wrote", out)

    (PAPER / "highlights.txt").write_text("\n".join("• " + x for x in highlights), encoding="utf-8")
    (PAPER / "SUBMISSION_CHECKLIST_ECOINF.md").write_text(
        "\n".join(
            [
                "# Ecological Informatics submission checklist",
                "",
                "- [x] Author: Senjie Zhang, Lanzhou University, 3079099853@qq.com",
                "- [x] Highlights ≤85 characters",
                "- [x] Abstract (single paragraph, no citations)",
                "- [x] Fig. 1 protocol plate + Fig. 2 coastal MAE",
                "- [x] Tables 1–4 from frozen results",
                "- [x] Cover letter (`paper/cover_letter.md`)",
                "- [ ] Upload via Editorial Manager (Elsevier)",
                "- [ ] Suggest 3–5 reviewers",
                "- [ ] Confirm no dual submission with sister Mask-View paper",
                "",
                "Guide: https://www.elsevier.com/journals/ecological-informatics/1574-9541/guide-for-authors",
                "Manuscript: paper/EcoInf_information_value_manuscript.docx",
            ]
        ),
        encoding="utf-8",
    )
    print("Wrote", out)


if __name__ == "__main__":
    main()
