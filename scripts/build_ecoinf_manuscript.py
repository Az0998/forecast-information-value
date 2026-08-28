"""Build Ecological Informatics submission Word manuscript from frozen Paper B tables."""
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


def maybe_csv(name: str):
    path = TABLES / name
    return pd.read_csv(path) if path.exists() else None


def main():
    river = pd.read_csv(TABLES / "river_1d_information_value.csv")
    climate = pd.read_csv(TABLES / "river_climate_all_horizons.csv")
    events = pd.read_csv(TABLES / "river_event_and_oracle.csv")
    qpf = pd.read_csv(TABLES / "river_qpf_ladder.csv")
    ocean = pd.read_csv(TABLES / "ocean_multilead_skill.csv")
    coast = pd.read_csv(TABLES / "ocean_coastal_mae.csv")
    xgb_csi = maybe_csv("climate_p90_csi.csv")
    xgb_ora = maybe_csv("climate_oracle_xgb.csv")
    bow_csi = maybe_csv("bow_p90_csi.csv")
    bow_ora = maybe_csv("bow_oracle_xgb.csv")
    lin_ora = maybe_csv("oracle_linear_vs_xgb.csv")
    ice_bow = maybe_csv("bow_ice_free.csv")

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
        "Verde: XGB beats routing at 1 d; LSTM and 3–7 d XGB do not.",
        "OLS rain ceiling is ~0 on snowmelt (Animas and Bow).",
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
        "Willamette. Model class is not a uniform upgrade: on the semi-arid Verde, XGBoost beats "
        "routing at 1 day (NSE 0.66 versus 0.61) while LSTM-Attention loses (0.38), and XGBoost "
        "NSE turns negative at 3–7 days. A nested Bow River transfer in Alberta reproduces "
        "next-day routing saturation outside the USGS network. An ordinary-least-squares "
        "precipitation ceiling is near zero at 3 days on snowmelt (Animas, Bow) and +0.07 on "
        "the Potomac. Perfect future precipitation raises Potomac 3- and "
        "7-day LSTM NSE by +0.12 and +0.20, but operational GFS quantitative precipitation "
        "forecasts are negative at 3 days (−0.03). P90 flood CSI of LSTM-Attention is 0.75 / "
        "0.29 / 0.26 at 1 / 3 / 7 days on the Potomac, while routing CSI falls to 0.04 at 7 "
        "days. On a WOA-informed East China Sea shelf oxygen cube, a spatiotemporal Transformer "
        "beats climatology at 1 month "
        "(RMSE 3.88 versus 5.30 µmol kg⁻¹) but a "
        "climatology–Transformer hybrid is required at 2 months, and Argo-like history raises "
        "lead-1 RMSE by about 35%. Residuals concentrate in the coastal tercile. Low-oxygen "
        "scores use the training 10th percentile, not hypoxia <60 µmol kg⁻¹. The contribution "
        "is the protocol—simple baseline, event score, information ceiling, failure locus—not "
        "a universal sequence model.",
    )

    h(doc, "Keywords")
    p = doc.add_paragraph()
    font(
        p.add_run(
            "environmental forecasting; information value; streamflow; dissolved oxygen; "
            "critical success index; climatology; quantitative precipitation forecast; "
            "sparse observations"
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
        "in the Muskingum transfer-function family [4] and month-of-year climatology for oxygen; "
        "(iii) a decision metric—P90 flood critical success index (CSI) [5] and low-tail oxygen "
        "F1/CSI at the training 10th percentile; (iv) an explicit bottleneck test—oracle "
        "precipitation versus operational GFS QPF, dense versus Argo-like oxygen history, and "
        "coastal residual maps. Learned models are instruments, not the claim.",
    )
    body(
        doc,
        "Rivers use public USGS discharge and Open-Meteo meteorology on the Potomac, "
        "James, Willamette, Animas and Verde, operational GFS QPF on the Potomac only, "
        "and a nested Water Survey of Canada transfer on "
        "the Bow River at Calgary (Cochrane and Banff upstream; native m³ s⁻¹). The ocean "
        "experiments use a WOA-informed East "
        "China Sea shelf oxygen cube with temperature, salinity, OISST and ERA5-backed wind at "
        "1–3 month leads. The oxygen target is a development cube (climatological structure plus "
        "synthetic autoregressive anomalies), not GOBAI-O2 [6]; that limitation bounds process "
        "claims, not the protocol. Daily estuary hypoxia AI [7] is a related but shorter-range "
        "task.",
    )

    h(doc, "2. Methods")
    h(doc, "2.1 Shared protocol", level=2)
    body(
        doc,
        "For each lead time we (1) apply persistence and the domain-simple baseline; (2) fit "
        "learned instruments on the same predictors (LSTM-Attention and XGBoost on rivers; "
        "spatiotemporal Transformer and a validation-tuned hybrid with climatology on oxygen); "
        "(3) report continuous skill and an event score; (4) remove or replace one information "
        "source and record the delta; (5) map residuals onto a physical axis (climate class, "
        "coastal proximity, 50 dbar). Ranking flips with lead time are retained; they are part "
        "of the protocol, not noise.",
    )
    h(doc, "2.2 Rivers", level=2)
    body(
        doc,
        "The routing baseline is ordinary least squares on lagged target and upstream discharge "
        "[4]. Ablation ΔNSE is full-network LSTM NSE minus local-only LSTM NSE. Flood events "
        "exceed the training-period 90th percentile. LSTM CSI and LSTM oracle precipitation are "
        "reported for the Potomac; XGBoost CSI and oracle precipitation complete the same "
        "grammar across the climate ladder when those tables are frozen. Operational QPF uses "
        "Open-Meteo GFS previous-run precipitation on Potomac 2024. SHAP on Potomac 1-day "
        "XGBoost ranks target discharge ahead of upstream flow and precipitation [8]. "
        "Climate-band CSI and oracle tables are a locked XGBoost re-fit (same chronological "
        "split). One-day NSE matches Table 1 within 0.02; Verde 3- and 7-day NSE from that "
        "re-fit is not used to overwrite Table 1b. The Bow transfer uses the same split on "
        "WSC HYDAT daily means (2006–2023 after the Cochrane inner join); winter values are "
        "often ice-flagged. Ablation ΔNSE on Bow is XGBoost full-network minus local-only. "
        "The precipitation ceiling used for transfer claims is ordinary least squares with "
        "perfect future rain; XGBoost oracle skill is reported as a sensitivity and is not "
        "used where it degrades relative to the observed-rain model.",
    )
    h(doc, "2.3 Shelf oxygen", level=2)
    body(
        doc,
        "History length is 12 months; leads are 1, 2 and 3 months with year-block splits. The "
        "event threshold is the 10th percentile of oxygen on the training cube (195 µmol kg⁻¹). "
        "Absolute hypoxia (<60 µmol kg⁻¹) occupies <1% of cells, so scores are low-tail F1/CSI, "
        "not hypoxia prevalence [10]. Sparse tests hide oxygen history while keeping physical "
        "drivers visible (point, block, sensor, station, mixed, Argo columns); they are "
        "information-ceiling tests, not a rank-reversal study [9]. Hybrid blend weights are "
        "tuned on validation and shrink toward climatology at longer leads (w = 1.0, 0.35, "
        "0.05).",
    )

    h(doc, "3. Results")
    h(doc, "3.1 Gauge information and model class are climate-conditional", level=2)
    v1 = climate[(climate.basin == "verde") & (climate.horizon == 1)].iloc[0]
    v3 = climate[(climate.basin == "verde") & (climate.horizon == 3)].iloc[0]
    v7 = climate[(climate.basin == "verde") & (climate.horizon == 7)].iloc[0]
    w7 = climate[(climate.basin == "willamette") & (climate.horizon == 7)].iloc[0]
    body(
        doc,
        "At 1-day lead, routing NSE already exceeds 0.86 on humid and snowmelt basins (Table 1). "
        "Upstream ablation ΔNSE is +0.13 on James, +0.02 on Potomac, ≈0 on Willamette, +0.01 on "
        "Animas, and +0.06 on Verde. The Verde result is a model-class × climate interaction, "
        f"not a blanket failure of learning: 1-day NSE is XGBoost {f3(v1.xgboost_NSE)} > routing "
        f"{f3(v1.routing_NSE)} > LSTM-Attention {f3(v1.lstm_attention_NSE)}. At 3 and 7 days "
        f"Verde XGBoost NSE is negative ({f3(v3.xgboost_NSE)} / {f3(v7.xgboost_NSE)}) while "
        f"routing remains positive ({f3(v3.routing_NSE)} / {f3(v7.routing_NSE)}). Willamette "
        f"7-day LSTM-Attention is {abs(float(w7.attn_minus_routing)):.2f} NSE below routing. Animas "
        "7-day routing NSE is still 0.85: seasonal memory, not architecture, carries the week. "
        "Rankings therefore flip with lead time.",
    )
    add_table(
        doc,
        ["Basin", "Climate", "Routing", "XGBoost", "LSTM-Attn", "Upstream ΔNSE", "LSTM−routing"],
        [
            [
                r.basin,
                r.climate,
                f3(r.routing_NSE),
                f3(r.xgboost_NSE),
                f3(r.lstm_attention_NSE),
                f3(r.ablation_delta),
                f3(r.attn_minus_routing),
            ]
            for r in river.itertuples()
        ],
    )
    caption(doc, "Table 1. One-day river skill. ΔNSE is LSTM full-network minus local-only.")

    add_table(
        doc,
        ["Basin", "Lead (d)", "Routing NSE", "XGBoost NSE", "LSTM NSE", "LSTM−routing"],
        [
            [
                r.basin,
                int(r.horizon),
                f3(r.routing_NSE),
                f3(r.xgboost_NSE),
                f3(r.lstm_attention_NSE),
                f3(r.attn_minus_routing),
            ]
            for r in climate[climate.horizon != 1].itertuples()
        ],
    )
    caption(doc, "Table 1b. Three- and seven-day NSE. Sign flips are retained as protocol output.")
    if bow_csi is not None:
        body(
            doc,
            "The same 1-day saturation appears on a non-US nested network: Bow River at Calgary "
            f"(routing NSE {f3(bow_csi.loc[bow_csi.horizon==1,'routing_NSE'].iloc[0])}, "
            f"persistence {f3(bow_csi.loc[bow_csi.horizon==1,'persist_NSE'].iloc[0])}, "
            f"XGBoost {f3(bow_csi.loc[bow_csi.horizon==1,'xgb_NSE'].iloc[0])}). XGBoost loses to "
            "routing on NSE and still wins P90 CSI. Seven-day persistence NSE remains 0.72.",
        )
        add_table(
            doc,
            ["Lead (d)", "Persist NSE", "Routing NSE", "XGB NSE", "Upstream ΔNSE", "XGB CSI"],
            [
                [
                    int(r.horizon),
                    f3(r.persist_NSE),
                    f3(r.routing_NSE),
                    f3(r.xgb_NSE),
                    f3(r.ablation_delta),
                    f3(r.xgb_CSI),
                ]
                for r in bow_csi.itertuples()
            ],
        )
        caption(doc, "Table 1c. Bow River at Calgary (WSC; m³ s⁻¹). Ablation is XGB full minus local-only.")

    h(doc, "3.2 Event skill, operational QPF, and the precipitation ceiling", level=2)
    body(
        doc,
        "On the Potomac, LSTM P90 CSI is 0.75 versus routing 0.62 and persistence 0.56 at 1 day; "
        "at 7 days routing CSI is 0.04 while learned CSI remains 0.26 (Table 2). LSTM oracle "
        "precipitation changes 1-day NSE by about 0, then +0.12 at 3 days and +0.20 at 7 days. "
        "The operational ladder is stricter (Table 2b; Potomac 2024): observation-only NSE 0.41 "
        f"at 3 days, GFS QPF {f3(qpf.loc[qpf.horizon==3,'qpf_NSE'].iloc[0])}, oracle "
        f"{f3(qpf.loc[qpf.horizon==3,'oracle_NSE'].iloc[0])}. Raw GFS QPF can degrade an "
        "uncorrected 3-day forecast; usable rain is not oracle rain.",
    )
    if xgb_csi is not None:
        v1 = xgb_csi[(xgb_csi.basin == "verde") & (xgb_csi.horizon == 1)].iloc[0]
        a3 = xgb_ora[(xgb_ora.basin == "animas") & (xgb_ora.horizon == 3)].iloc[0] if xgb_ora is not None else None
        extra = (
            f"XGBoost completes the same grammar on all five climates (Tables 2c–2d). "
            f"Verde 1-day P90 CSI is XGB {f3(v1.xgb_CSI)} > persistence {f3(v1.persist_CSI)} > "
            f"routing {f3(v1.routing_CSI)}: routing NSE looks acceptable but flood CSI is worse "
            f"than persistence. "
        )
        if a3 is not None:
            extra += (
                f"Oracle precipitation ΔNSE at 3 days is near zero on snowmelt Animas "
                f"({f3(a3.delta_NSE)}) and large on Verde/James/Potomac: the rain ceiling is "
                f"climate-conditional."
            )
        if lin_ora is not None:
            def lin_d(basin, h=3):
                return float(lin_ora.loc[(lin_ora.basin == basin) & (lin_ora.horizon == h), "lin_delta_NSE"].iloc[0])

            extra += (
                f" The architecture-free ceiling is OLS with perfect rain: 3-day linear ΔNSE is "
                f"{f3(lin_d('potomac'))} on Potomac, {f3(lin_d('verde'))} on Verde, "
                f"{f3(lin_d('animas'))} on Animas and {f3(lin_d('bow'))} on Bow. "
                "XGBoost 3-day Bow degradation is overfitting and is not a process result."
            )
        elif bow_ora is not None:
            b1 = bow_ora[bow_ora.horizon == 1].iloc[0]
            b3 = bow_ora[bow_ora.horizon == 3].iloc[0]
            extra += (
                f" On the Bow (Canada) 1-day oracle ΔNSE is {f3(b1.delta_NSE)}; "
                f"3-day perfect rain does not lift skill ({f3(b3.delta_NSE)}). "
                "The snowmelt rain-ceiling is not an Animas/USGS artefact."
            )
        body(doc, extra)
    add_table(
        doc,
        ["Lead (d)", "Routing CSI", "LSTM CSI", "Persist CSI", "LSTM oracle ΔNSE"],
        [[int(r.horizon), f3(r.routing_CSI), f3(r.attn_CSI), f3(r.pers_CSI), f3(r.delta_NSE)] for r in events.itertuples()],
    )
    caption(doc, "Table 2. Potomac LSTM P90 flood CSI and oracle-precipitation ΔNSE.")
    add_table(
        doc,
        ["Lead (d)", "Obs rain NSE", "GFS QPF NSE", "Oracle rain NSE"],
        [[int(r.horizon), f3(r.obs_NSE), f3(r.qpf_NSE), f3(r.oracle_NSE)] for r in qpf.itertuples()],
    )
    caption(doc, "Table 2b. Potomac 2024 observation-only versus GFS QPF versus oracle precipitation.")
    if xgb_csi is not None:
        add_table(
            doc,
            ["Basin", "Lead (d)", "Persist CSI", "Routing CSI", "XGB CSI", "N events"],
            [
                [r.basin, int(r.horizon), f3(r.persist_CSI), f3(r.routing_CSI), f3(r.xgb_CSI), int(r.n_events)]
                for r in xgb_csi.itertuples()
            ],
        )
        caption(doc, "Table 2c. Climate-band P90 CSI using XGBoost (training 90th percentile).")
    if xgb_ora is not None:
        add_table(
            doc,
            ["Basin", "Lead (d)", "XGB obs NSE", "XGB oracle NSE", "ΔNSE"],
            [
                [r.basin, int(r.horizon), f3(r.xgb_obs_NSE), f3(r.xgb_oracle_NSE), f3(r.delta_NSE)]
                for r in xgb_ora.itertuples()
            ],
        )
        caption(doc, "Table 2d. Climate-band XGBoost oracle-precipitation ceiling.")
    if lin_ora is not None:
        add_table(
            doc,
            ["Basin", "Lead (d)", "OLS ΔNSE", "XGB ΔNSE"],
            [
                [r.basin, int(r.horizon), f3(r.lin_delta_NSE), f3(r.xgb_delta_NSE)]
                for r in lin_ora.itertuples()
            ],
        )
        caption(
            doc,
            "Table 2e. Architecture-free precipitation ceiling (OLS) versus XGBoost. "
            "Snowmelt (Animas, Bow) remains ~0 for OLS; XGB Bow 3-day degradation is overfitting.",
        )
    if ice_bow is not None:
        i1 = ice_bow[ice_bow.horizon == 1].iloc[0]
        body(
            doc,
            f"Bow test-window ice flags are {i1.ice_frac_test * 100:.0f}% of days. "
            f"Open-water P90 CSI equals the all-day CSI ({f3(i1.open_xgb_CSI)}); all "
            f"{int(i1.open_n_events)} P90 events fall on ice-free days.",
        )

    h(doc, "3.3 Oxygen: Transformer at one month, climatology thereafter", level=2)
    f1_col = "lowtail_F1" if "lowtail_F1" in ocean.columns else "hypoxia_F1"
    body(
        doc,
        f"Lead-1 Transformer RMSE is {f3(oc(1,'st_transformer','RMSE'))} µmol kg⁻¹ "
        f"(skill versus climatology {f3(oc(1,'st_transformer','skill_vs_clim'))}; "
        f"low-tail F1 {f3(oc(1,'st_transformer',f1_col))}). At two months the hybrid "
        f"({f3(oc(2,'hybrid_clim_st','RMSE'))}) matches climatology "
        f"({f3(oc(2,'climatology','RMSE'))}) while the standalone Transformer "
        f"({f3(oc(2,'st_transformer','RMSE'))}) is worse than climatology. At three months the "
        "Transformer is unusable; the hybrid collapses to climatology. Argo- or station-column "
        "oxygen history raises lead-1 RMSE by about 35%. Physical drivers help mid-lead hybrid "
        "skill relative to oxygen-only history; they do not prevent climatology takeover. "
        "Seasonal test counts (JJAS n=8, DJF n=5) are not used as main claims.",
    )
    key_models = ["persistence", "climatology", "st_transformer", "hybrid_clim_st"]
    sub = ocean[ocean["model"].isin(key_models)]
    add_table(
        doc,
        ["Lead (mo)", "Model", "RMSE", "Skill vs clim", "Low-tail F1", "CSI"],
        [[int(r.lead_mo), r.model, f3(r.RMSE), f3(r.skill_vs_clim), f3(getattr(r, f1_col)), f3(r.CSI)] for r in sub.itertuples()],
    )
    caption(
        doc,
        "Table 3. East China Sea shelf oxygen multi-lead scores (µmol kg⁻¹ RMSE). "
        "Low-tail events are the training 10th percentile (195 µmol kg⁻¹), not hypoxia <60.",
    )

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
            "(b) One-day NSE by model class. (c) Oxygen RMSE versus lead. "
            "(d) Operational GFS QPF versus oracle precipitation (Potomac 2024).",
        )
    if maybe_fig(doc, FIGS / "fig_verde_model_class.png", 5.2):
        caption(doc, "Fig. 2. Semi-arid Verde: XGBoost wins at 1 day and collapses at 3–7 days.")
    if maybe_fig(doc, FIGS / "fig_climate_event_ceiling.png", 6.3):
        caption(
            doc,
            "Fig. 3. Climate-band protocol completion with XGBoost. (a) One-day P90 CSI. "
            "Verde routing CSI is below persistence despite competitive NSE. "
            "(b) Oracle precipitation ΔNSE: large at 3–7 days except snowmelt Animas (~0).",
        )
    if maybe_fig(doc, FIGS / "fig_bow_transfer.png", 6.0):
        caption(
            doc,
            "Fig. 4. Non-US transfer, Bow River at Calgary. (a) Routing saturates 1-day NSE. "
            "(b) XGBoost oracle is a sensitivity; the protocol ceiling is OLS (Fig. 5).",
        )
    if maybe_fig(doc, FIGS / "fig_oracle_linear_vs_xgb.png", 5.6):
        caption(
            doc,
            "Fig. 5. Three-day precipitation ceiling. OLS recovers rain value on Potomac/Verde "
            "and ~0 on Animas/Bow; XGBoost overfits on Bow.",
        )
    if maybe_fig(doc, FIGS / "fig_ocean_coastal_failure.png", 4.8):
        caption(doc, "Fig. 6. Coastal concentration of oxygen residuals on the development cube.")

    h(doc, "4. Discussion")
    body(
        doc,
        "The two media share one sentence: learned forecasts add skill only while the limiting "
        "input is present. On rivers that input is unsaturated autocorrelation plus usable "
        "precipitation foresight; on the shelf it is dense recent oxygen, and even then only "
        "near a one-month lead. Reporting only 1-day LSTM NSE on the Potomac, or only RMSE on a "
        "dense oxygen cube, hides both bottlenecks.",
    )
    body(
        doc,
        "Discharge and oxygen are not trained as one network. The shared object is the "
        "protocol. A sister study treats operational missingness as the factor that reverses "
        "imputer rankings [9]; this paper treats lead time and missing drivers as the factors "
        "that reverse forecast rankings. Limitations include the absence of a nested Chinese "
        "daily-discharge ladder (CAMELS-CN Yellow River gauges are normalized), a Bow record "
        "that starts in 2006 and is ice-flagged in winter, a WOA-informed oxygen cube with "
        "synthetic anomalies, GFS QPF from the Potomac, LSTM CSI from the Potomac "
        "(climate-band and Bow CSI use XGBoost), low-tail oxygen events that are not "
        "hypoxia, and the absence of GEFS ensemble probabilities.",
    )

    h(doc, "5. Conclusions")
    body(
        doc,
        "A four-part information-value protocol—simple baseline, event score, information "
        "ceiling, failure locus—yields consistent conclusions on rivers and a shelf oxygen cube "
        "without a new architecture. Operational recipes are conditional: routing or XGBoost "
        "next-day flow depending on climate, never LSTM-by-default on semi-arid flashy basins; "
        "a Transformer for oxygen at one month and climatology or a hybrid thereafter; never "
        "treat dense-history scores as Argo-ready skill; never treat raw QPF as oracle rain.",
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
        "(accessed 28 August 2026). Discharge from USGS NWIS and Water Survey of Canada HYDAT; meteorology from Open-Meteo; "
        "oxygen cube from WOA / OISST with ERA5-backed wind.",
    )
    h(doc, "Acknowledgments")
    body(
        doc,
        "The author thanks the USGS, Water Survey of Canada, NOAA WOA/OISST, and Open-Meteo data providers.",
    )
    h(doc, "Ethics statement")
    body(
        doc,
        "This study used publicly available hydrometric and ocean-climatology products. "
        "No human or animal subjects were involved.",
    )
    h(doc, "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process")
    body(
        doc,
        "During the preparation of this work the author used Cursor (an AI-assisted editor) "
        "to assemble English prose from locked numerical tables and to check formatting. "
        "After using this tool, the author reviewed and edited the content and takes full "
        "responsibility for the analyses and interpretations.",
    )

    h(doc, "References")
    refs = [
        "Kratzert, F.; Klotz, D.; Brenner, C.; Schulz, K.; Herrnegger, M. Rainfall–runoff prediction at multiple timescales with a single Long Short-Term Memory network. Hydrol. Earth Syst. Sci. 2018, 22, 6005–6022.",
        "Nearing, G.S.; et al. What role does hydrological science play in the age of machine learning? Water Resour. Res. 2021, 57, e2020WR028091.",
        "Frame, J.M.; et al. Deep learning rainfall–runoff predictions of extreme events. Hydrol. Earth Syst. Sci. 2022, 26, 3377–3392.",
        "Cunge, J.A. On the subject of a flood propagation computation method (Muskingum method). J. Hydraul. Res. 1969, 7, 205–230.",
        "Wilks, D.S. Statistical Methods in the Atmospheric Sciences, 4th ed.; Elsevier: Amsterdam, The Netherlands, 2019.",
        "Sharp, J.D.; et al. GOBAI-O2: temporally and spatially resolved fields of ocean interior dissolved oxygen over nearly two decades. Earth Syst. Sci. Data 2023, 15, 4481–4518.",
        "Zheng, G.; Friedrichs, M.A.M.; et al. Hypoxia forecasting for Chesapeake Bay using artificial intelligence. Artif. Intell. Earth Syst. 2024, 3, e230054.",
        "Lundberg, S.M.; Lee, S.-I. A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems; 2017.",
        "Zhang, S. Mask-View protocol for operational missingness in aquatic monitoring networks. Companion manuscript in preparation. https://github.com/Az0998/maskview-aquatic-protocol (accessed 28 August 2026).",
        "Breitburg, D.; et al. Declining oxygen in the global ocean and coastal waters. Science 2018, 359, eaam7240.",
        "Paerl, H.W.; Huisman, J. Blooms like it hot. Science 2008, 320, 57–58.",
        "Jolliffe, I.T.; Stephenson, D.B. Forecast Verification: A Practitioner’s Guide in Atmospheric Science, 2nd ed.; Wiley: Chichester, UK, 2012.",
        "Abu-El-Haija, S.; et al. MixHop: Higher-Order Graph Convolutional Architectures via Sparsified Neighborhood Mixing. In ICML; 2019.",
        "Vaswani, A.; et al. Attention is all you need. In Advances in Neural Information Processing Systems; 2017.",
        "World Ocean Atlas 2023. NOAA National Centers for Environmental Information.",
        "Huang, B.; et al. NOAA 1/4° Daily Optimum Interpolation Sea Surface Temperature (OISST).",
        "Open-Meteo. Historical weather API, ERA5-backed. https://open-meteo.com (accessed 28 August 2026).",
        "USGS. National Water Information System. https://waterdata.usgs.gov (accessed 28 August 2026).",
        "Environment and Climate Change Canada. HYDAT hydrometric database, Water Survey of Canada. https://wateroffice.ec.gc.ca (accessed 28 August 2026).",
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
                "- [x] Highlights ≤85 characters (5 bullets)",
                "- [x] Abstract (single paragraph, no citations); includes Bow transfer + OLS ceiling",
                "- [x] Figures 1–6 embedded in Word",
                "- [x] OLS precipitation ceiling and Bow ice-free CSI",
                "- [x] Oxygen events labelled as training p10 low-tail, not hypoxia",
                "- [x] CRediT, competing interest, funding, ethics, generative-AI declaration",
                "- [x] Cover letter (`paper/cover_letter.md` and `paper/cover_letter.txt`)",
                "- [x] Suggested reviewers (`paper/suggested_reviewers.md`; search emails in EM)",
                "- [x] Not a dual submission with Mask-View (different claim)",
                "- [x] Upload instructions (`paper/HOW_TO_SUBMIT_ECOINF.md`)",
                "- [x] Commit frozen tables and manuscript so the GitHub data URL can match this Word file",
                "- [ ] `git push origin main` if the public clone is behind",
                "- [ ] Upload via Editorial Manager",
                "",
                "Guide: https://www.elsevier.com/journals/ecological-informatics/1574-9541/guide-for-authors",
                "Manuscript: paper/EcoInf_information_value_manuscript.docx",
            ]
        ),
        encoding="utf-8",
    )
    print("Wrote", out)
    for item in highlights:
        print(f"  highlight {len(item)} chars: {item}")


if __name__ == "__main__":
    main()
