"""Lock headline claims in the EcoInf package to frozen tables."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
RIVER = ROOT / "data" / "frozen" / "river"
OCEAN = ROOT / "data" / "frozen" / "ocean"
PAPER = ROOT / "paper"
FIGS = ROOT / "results" / "figures"


def near(a, b, tol=0.015):
    return abs(float(a) - float(b)) <= tol


def fail(msg: str) -> None:
    print("FAIL:", msg)
    sys.exit(1)


def main() -> None:
    climate = pd.read_csv(RIVER / "climate_basin_compare.csv")
    qpf = pd.read_csv(RIVER / "qpf_ladder.csv")
    csi = pd.read_csv(RIVER / "flood_csi.csv")
    ora = pd.read_csv(RIVER / "oracle_precip.csv")
    bow = pd.read_csv(RIVER / "bow_p90_csi.csv")
    ice = pd.read_csv(RIVER / "bow_ice_free.csv")
    lin = pd.read_csv(RIVER / "oracle_linear_vs_xgb.csv")
    xgb_csi = pd.read_csv(RIVER / "climate_p90_csi.csv")
    mask = json.loads((OCEAN / "maskview_ablation.json").read_text(encoding="utf-8"))

    james = climate[(climate.basin == "james") & (climate.horizon == 1)].iloc[0]
    will = climate[(climate.basin == "willamette") & (climate.horizon == 1)].iloc[0]
    verde1 = climate[(climate.basin == "verde") & (climate.horizon == 1)].iloc[0]
    verde3 = climate[(climate.basin == "verde") & (climate.horizon == 3)].iloc[0]
    verde7 = climate[(climate.basin == "verde") & (climate.horizon == 7)].iloc[0]
    if not near(james.ablation_delta, 0.13):
        fail(f"James ΔNSE {james.ablation_delta}")
    if abs(float(will.ablation_delta)) > 0.02:
        fail(f"Willamette ΔNSE {will.ablation_delta}")
    if not (verde1.xgboost_NSE > verde1.routing_NSE > verde1.lstm_attention_NSE):
        fail("Verde 1-d ranking")
    if not (verde3.xgboost_NSE < 0 and verde7.xgboost_NSE < 0):
        fail("Verde 3/7-d XGB should be negative in Table 1b")
    q3 = qpf[qpf.horizon == 3].iloc[0]
    if not near(q3.qpf_NSE, -0.03, 0.02):
        fail(f"QPF 3-d {q3.qpf_NSE}")
    if not near(q3.oracle_NSE, 0.58, 0.02):
        fail(f"oracle 3-d {q3.oracle_NSE}")
    if not near(csi.loc[csi.horizon == 1, "attn_CSI"].iloc[0], 0.75):
        fail("CSI 1-d")
    if not near(csi.loc[csi.horizon == 7, "attn_CSI"].iloc[0], 0.26):
        fail("CSI 7-d")
    if not near(csi.loc[csi.horizon == 7, "routing_CSI"].iloc[0], 0.04):
        fail("routing CSI 7-d")
    if not near(ora.loc[ora.horizon == 3, "delta_NSE"].iloc[0], 0.12):
        fail("LSTM oracle 3-d")
    if not near(ora.loc[ora.horizon == 7, "delta_NSE"].iloc[0], 0.20):
        fail("LSTM oracle 7-d")
    b1 = bow[bow.horizon == 1].iloc[0]
    if not (b1.routing_NSE > b1.xgb_NSE and near(b1.routing_NSE, 0.98, 0.02)):
        fail("Bow 1-d routing saturation")
    lin3 = lin[lin.horizon == 3]
    if not near(lin3.loc[lin3.basin == "potomac", "lin_delta_NSE"].iloc[0], 0.07, 0.02):
        fail("OLS Potomac 3-d")
    if abs(float(lin3.loc[lin3.basin == "animas", "lin_delta_NSE"].iloc[0])) > 0.02:
        fail("OLS Animas 3-d should be ~0")
    if abs(float(lin3.loc[lin3.basin == "bow", "lin_delta_NSE"].iloc[0])) > 0.02:
        fail("OLS Bow 3-d should be ~0")
    if float(lin3.loc[lin3.basin == "bow", "xgb_delta_NSE"].iloc[0]) > -0.2:
        fail("XGB Bow 3-d should remain a large negative (overfit flag)")
    if int(ice.loc[ice.horizon == 1, "open_n_events"].iloc[0]) != 74:
        fail("Bow ice-free events")
    v1c = xgb_csi[(xgb_csi.basin == "verde") & (xgb_csi.horizon == 1)].iloc[0]
    if not (v1c.xgb_CSI > v1c.persist_CSI > v1c.routing_CSI):
        fail("Verde CSI ranking")
    full = next(x for x in mask if x["sparse"] == "none")["lead1_st_rmse"]
    argo = next(x for x in mask if x["sparse"] == "argo")["lead1_st_rmse"]
    lift = (argo - full) / full
    if not near(lift, 0.35, 0.03):
        fail(f"Argo RMSE lift {lift:.3f}")

    highlights = (PAPER / "highlights.txt").read_text(encoding="utf-8").strip().splitlines()
    if len(highlights) != 5:
        fail(f"{len(highlights)} highlights")
    for line in highlights:
        body = line.lstrip("• ").strip()
        if len(body) > 85:
            fail(f"highlight {len(body)} chars: {body}")

    needed = [
        "fig_information_bottleneck.png",
        "fig_verde_model_class.png",
        "fig_climate_event_ceiling.png",
        "fig_bow_transfer.png",
        "fig_oracle_linear_vs_xgb.png",
        "fig_ocean_coastal_failure.png",
    ]
    for name in needed:
        path = FIGS / name
        if not path.exists() or path.stat().st_size < 10_000:
            fail(f"missing/small figure {name}")

    docx = PAPER / "EcoInf_information_value_manuscript.docx"
    if not docx.exists():
        fail("Word manuscript missing")
    doc = Document(str(docx))
    n_blips = sum(1 for rel in doc.part.rels.values() if "image" in rel.reltype)
    if n_blips < 6:
        fail(f"Word embeds {n_blips} images, expected ≥6")
    text = "\n".join(p.text for p in doc.paragraphs)
    for needle in [
        "training 10th percentile",
        "not hypoxia",
        "Bow River",
        "ordinary-least-squares",
        "Companion manuscript in preparation",
        "Declaration of generative AI",
        "Water Survey of Canada",
    ]:
        if needle not in text:
            fail(f"Word missing phrase: {needle}")
    if "Do not resubmit" in text or "HSJ" in text:
        fail("Word still contains prior-journal operational notes")

    for req in [
        PAPER / "cover_letter.txt",
        PAPER / "highlights.txt",
        PAPER / "HOW_TO_SUBMIT_ECOINF.md",
        PAPER / "suggested_reviewers.md",
        RIVER / "bow_daily.csv",
    ]:
        if not req.exists():
            fail(f"missing {req}")

    print("OK: frozen numbers, highlights, six figures, and Word manuscript lock.")


if __name__ == "__main__":
    main()
