"""Paper B tables + protocol plates from frozen snapshots."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RIVER = ROOT / "data" / "frozen" / "river"
OCEAN = ROOT / "data" / "frozen" / "ocean"
OUT = ROOT / "results" / "tables"
FIG = ROOT / "results" / "figures"

RIVER_COLOR = "#1f6f8b"
OCEAN_COLOR = "#0f5f78"
MUTED = "#6b7c85"
XGB_COLOR = "#c47b2b"
ATTN_COLOR = "#2d6a4f"


def df_md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def climate_all() -> pd.DataFrame:
    df = pd.read_csv(RIVER / "climate_basin_compare.csv")
    keep = [
        "basin",
        "climate",
        "horizon",
        "persistence_NSE",
        "routing_NSE",
        "xgboost_NSE",
        "lstm_attention_NSE",
        "ablation_delta",
        "attn_minus_routing",
    ]
    return df[keep].round(3)


def river_1d(climate: pd.DataFrame) -> pd.DataFrame:
    return climate[climate["horizon"] == 1].drop(columns=["horizon"]).reset_index(drop=True)


def ocean_leads() -> pd.DataFrame:
    md = (OCEAN / "multilead_full_physics.md").read_text(encoding="utf-8")
    rows = []
    for line in md.splitlines():
        if not line.startswith("|") or "Lead" in line or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 8:
            continue
        try:
            lead = int(parts[0])
        except ValueError:
            continue
        rows.append(
            {
                "lead_mo": lead,
                "model": parts[1],
                "RMSE": float(parts[2]),
                "skill_vs_persist": float(parts[4]),
                "skill_vs_clim": float(parts[5]),
                "lowtail_F1": float(parts[6]),
                "CSI": float(parts[7]),
            }
        )
    return pd.DataFrame(rows)


def river_events() -> pd.DataFrame:
    csi = pd.read_csv(RIVER / "flood_csi.csv")
    ora = pd.read_csv(RIVER / "oracle_precip.csv")
    return csi.merge(ora, on="horizon").round(3)


def qpf_ladder() -> pd.DataFrame:
    return pd.read_csv(RIVER / "qpf_ladder.csv").round(3)


def coastal_mae() -> pd.DataFrame:
    raw = json.loads((OCEAN / "failure_modes.json").read_text(encoding="utf-8"))
    rows = [b for b in raw["bins"] if b["driver"] == "coastal_proximity"]
    return pd.DataFrame(rows)[["bin", "n_cells", "mae", "p90"]].round(3)


def extra_event_tables() -> dict[str, pd.DataFrame]:
    """Optional protocol-completion CSVs written by hydro-ml-paper/run_protocol_events.py."""
    out = {}
    for name in (
        "climate_p90_csi.csv",
        "climate_oracle_xgb.csv",
        "bow_p90_csi.csv",
        "bow_oracle_xgb.csv",
        "oracle_linear_vs_xgb.csv",
        "bow_ice_free.csv",
    ):
        path = RIVER / name
        if path.exists():
            out[name] = pd.read_csv(path).round(3)
    return out


def bottleneck_message(climate: pd.DataFrame) -> pd.DataFrame:
    v = climate[(climate.basin == "verde") & (climate.horizon == 1)].iloc[0]
    w7 = climate[(climate.basin == "willamette") & (climate.horizon == 7)].iloc[0]
    return pd.DataFrame(
        [
            {
                "domain": "river",
                "bottleneck": "climate × model-class × lead; rain foresight after day 1",
                "evidence": (
                    f"James 1-d upstream ΔNSE +0.13 vs Willamette ≈0; "
                    f"Verde 1-d XGB {v.xgboost_NSE} > routing {v.routing_NSE} > LSTM {v.lstm_attention_NSE}; "
                    f"Verde 3/7-d XGB NSE negative; Willamette 7-d LSTM−routing {w7.attn_minus_routing}; "
                    "GFS QPF 3-d NSE −0.03 while oracle +0.58; LSTM P90 CSI still Potomac-only"
                ),
            },
            {
                "domain": "ocean",
                "bottleneck": "learned anomaly skill collapses at lead ≥ 2 months; errors coastal",
                "evidence": (
                    "Lead-1 ST RMSE 3.88 vs clim 5.30; lead-2 hybrid 5.08 ≈ clim 5.23; "
                    "Argo +35% RMSE; coastal MAE 3.30 vs 2.95 offshore; "
                    "low-tail events are training p10 (195 µmol kg⁻¹), not hypoxia <60"
                ),
            },
        ]
    )


def plot_plate(d1: pd.DataFrame, ocean: pd.DataFrame, qpf: pd.DataFrame) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.4))
    basins = [b.capitalize() for b in d1["basin"]]

    axes[0, 0].bar(basins, d1["ablation_delta"], color=RIVER_COLOR)
    axes[0, 0].axhline(0, color=MUTED, lw=0.8)
    axes[0, 0].set_ylabel("1-day upstream ΔNSE")
    axes[0, 0].set_title("(a) Gauge information is climate-conditional")
    axes[0, 0].tick_params(axis="x", rotation=15)

    x = np.arange(len(d1))
    w = 0.25
    axes[0, 1].bar(x - w, d1["routing_NSE"], w, color=MUTED, label="Routing")
    axes[0, 1].bar(x, d1["xgboost_NSE"], w, color=XGB_COLOR, label="XGBoost")
    axes[0, 1].bar(x + w, d1["lstm_attention_NSE"], w, color=ATTN_COLOR, label="LSTM-Attn")
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(basins, rotation=15)
    axes[0, 1].set_ylabel("1-day NSE")
    axes[0, 1].set_ylim(0, 1.05)
    axes[0, 1].set_title("(b) Model class is not uniformly safer than routing")
    axes[0, 1].legend(frameon=False, fontsize=8)

    sub = ocean[ocean["model"].isin(["persistence", "climatology", "st_transformer", "hybrid_clim_st"])]
    for model, g in sub.groupby("model"):
        axes[1, 0].plot(g["lead_mo"], g["RMSE"], marker="o", label=model)
    axes[1, 0].set_xlabel("Lead (months)")
    axes[1, 0].set_ylabel(r"RMSE ($\mu$mol kg$^{-1}$)")
    axes[1, 0].set_title("(c) Oxygen: climatology takeover after lead-1")
    axes[1, 0].legend(frameon=False, fontsize=8)

    hx = np.arange(len(qpf))
    w2 = 0.25
    axes[1, 1].bar(hx - w2, qpf["obs_NSE"], w2, color=MUTED, label="Obs rain")
    axes[1, 1].bar(hx, qpf["qpf_NSE"], w2, color=XGB_COLOR, label="GFS QPF")
    axes[1, 1].bar(hx + w2, qpf["oracle_NSE"], w2, color=RIVER_COLOR, label="Oracle rain")
    axes[1, 1].axhline(0, color=MUTED, lw=0.8)
    axes[1, 1].set_xticks(hx)
    axes[1, 1].set_xticklabels([f"{int(h)} d" for h in qpf["horizon"]])
    axes[1, 1].set_xlabel("Lead (days)")
    axes[1, 1].set_ylabel("Potomac 2024 NSE")
    axes[1, 1].set_title("(d) Operational QPF can hurt; oracle still lifts the ceiling")
    axes[1, 1].legend(frameon=False, fontsize=8)

    fig.suptitle("Information-value protocol across rivers and a shelf oxygen cube", fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG / "fig_information_bottleneck.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_verde_leads(climate: pd.DataFrame) -> None:
    v = climate[climate["basin"] == "verde"].sort_values("horizon")
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    x = np.arange(len(v))
    w = 0.25
    ax.bar(x - w, v["routing_NSE"], w, color=MUTED, label="Routing")
    ax.bar(x, v["xgboost_NSE"], w, color=XGB_COLOR, label="XGBoost")
    ax.bar(x + w, v["lstm_attention_NSE"], w, color=ATTN_COLOR, label="LSTM-Attn")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{int(h)} d" for h in v["horizon"]])
    ax.set_ylabel("Verde NSE")
    ax.set_title("Semi-arid Verde: XGB wins at 1 day, then collapses")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_verde_model_class.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_climate_events(csi: pd.DataFrame, ora: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.2))
    d1 = csi[csi["horizon"] == 1].copy()
    basins = [b.capitalize() for b in d1["basin"]]
    x = np.arange(len(d1))
    w = 0.25
    axes[0].bar(x - w, d1["persist_CSI"], w, color=MUTED, label="Persistence")
    axes[0].bar(x, d1["routing_CSI"], w, color=RIVER_COLOR, label="Routing")
    axes[0].bar(x + w, d1["xgb_CSI"], w, color=XGB_COLOR, label="XGBoost")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(basins, rotation=15)
    axes[0].set_ylabel("1-day P90 CSI")
    axes[0].set_title("(a) Event skill is not NSE")
    axes[0].legend(frameon=False, fontsize=8)

    for basin, g in ora.groupby("basin"):
        axes[1].plot(g["horizon"], g["delta_NSE"], marker="o", label=basin.capitalize())
    axes[1].axhline(0, color=MUTED, lw=0.8)
    axes[1].set_xticks([1, 3, 7])
    axes[1].set_xlabel("Lead (days)")
    axes[1].set_ylabel("XGB oracle − obs ΔNSE")
    axes[1].set_title("(b) Rain ceiling is climate-conditional")
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Climate-band event score and precipitation ceiling (XGBoost instrument)", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "fig_climate_event_ceiling.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_bow(csi: pd.DataFrame, ora: pd.DataFrame | None) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.0))
    x = np.arange(len(csi))
    w = 0.25
    axes[0].bar(x - w, csi["routing_NSE"], w, color=MUTED, label="Routing")
    axes[0].bar(x, csi["xgboost_NSE"] if "xgboost_NSE" in csi.columns else csi["xgb_NSE"], w, color=XGB_COLOR, label="XGBoost")
    axes[0].bar(x + w, csi["persist_NSE"], w, color=RIVER_COLOR, label="Persistence")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([f"{int(h)} d" for h in csi["horizon"]])
    axes[0].set_ylabel("Bow NSE (test)")
    axes[0].set_title("(a) Calgary: routing saturates 1-day NSE")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].set_ylim(0, 1.05)

    if ora is not None:
        axes[1].plot(ora["horizon"], ora["delta_NSE"], "o-", color=RIVER_COLOR)
        axes[1].axhline(0, color=MUTED, lw=0.8)
        axes[1].set_xticks([1, 3, 7])
        axes[1].set_xlabel("Lead (days)")
        axes[1].set_ylabel("XGB oracle − obs ΔNSE")
        axes[1].set_title("(b) XGBoost oracle (sensitivity; OLS in Fig. 5)")
    fig.suptitle("Non-US transfer: Bow River at Calgary (WSC nested gauges)", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "fig_bow_transfer.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_oracle_robust(ceil: pd.DataFrame) -> None:
    sub = ceil[ceil["horizon"] == 3].copy()
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    x = np.arange(len(sub))
    w = 0.35
    ax.bar(x - w / 2, sub["lin_delta_NSE"], w, color=MUTED, label="OLS oracle ΔNSE")
    ax.bar(x + w / 2, sub["xgb_delta_NSE"], w, color=XGB_COLOR, label="XGBoost oracle ΔNSE")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([b.capitalize() for b in sub["basin"]])
    ax.set_ylabel("3-day oracle − obs ΔNSE")
    ax.set_title("Precipitation ceiling is linear on snowmelt; XGB can overfit")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_oracle_linear_vs_xgb.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_coast(coast: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.bar(coast["bin"], coast["mae"], color=OCEAN_COLOR)
    ax.set_ylabel(r"Lead-1 MAE ($\mu$mol kg$^{-1}$)")
    ax.set_xlabel("Coastal proximity tercile")
    ax.set_title("ECS residual error is coastal, not frontal")
    fig.tight_layout()
    fig.savefig(FIG / "fig_ocean_coastal_failure.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    climate = climate_all()
    d1 = river_1d(climate)
    ocean = ocean_leads()
    events = river_events()
    qpf = qpf_ladder()
    coast = coastal_mae()
    msg = bottleneck_message(climate)
    extra = extra_event_tables()

    climate.to_csv(OUT / "river_climate_all_horizons.csv", index=False)
    d1.to_csv(OUT / "river_1d_information_value.csv", index=False)
    ocean.to_csv(OUT / "ocean_multilead_skill.csv", index=False)
    events.to_csv(OUT / "river_event_and_oracle.csv", index=False)
    qpf.to_csv(OUT / "river_qpf_ladder.csv", index=False)
    coast.to_csv(OUT / "ocean_coastal_mae.csv", index=False)
    msg.to_csv(OUT / "bottleneck_summary.csv", index=False)
    for name, df in extra.items():
        df.to_csv(OUT / name, index=False)

    shap = json.loads((RIVER / "shap_summary.json").read_text(encoding="utf-8"))
    summary = {
        "claim": "mid-range skill is capped by missing information, not model class",
        "verde_1d": {
            "routing_NSE": float(d1.loc[d1.basin == "verde", "routing_NSE"].iloc[0]),
            "xgboost_NSE": float(d1.loc[d1.basin == "verde", "xgboost_NSE"].iloc[0]),
            "lstm_NSE": float(d1.loc[d1.basin == "verde", "lstm_attention_NSE"].iloc[0]),
        },
        "qpf_3d_NSE": {
            "obs": float(qpf.loc[qpf.horizon == 3, "obs_NSE"].iloc[0]),
            "qpf": float(qpf.loc[qpf.horizon == 3, "qpf_NSE"].iloc[0]),
            "oracle": float(qpf.loc[qpf.horizon == 3, "oracle_NSE"].iloc[0]),
        },
        "river_oracle_delta_NSE": {
            str(int(r.horizon)): float(r.delta_NSE) for r in events.itertuples()
        },
        "river_attn_CSI": {str(int(r.horizon)): float(r.attn_CSI) for r in events.itertuples()},
        "ocean_lead1_ST_RMSE": float(
            ocean.loc[(ocean.lead_mo == 1) & (ocean.model == "st_transformer"), "RMSE"].iloc[0]
        ),
        "ocean_lead2_hybrid_RMSE": float(
            ocean.loc[(ocean.lead_mo == 2) & (ocean.model == "hybrid_clim_st"), "RMSE"].iloc[0]
        ),
        "shap_top_channel": max(shap["channel_mean_abs_shap"], key=shap["channel_mean_abs_shap"].get),
        "coastal_high_mae": float(coast.loc[coast["bin"] == "high", "mae"].iloc[0]),
        "oxygen_event_note": "low-tail = training 10th percentile (195 µmol kg⁻¹), not hypoxia <60",
        "protocol_gaps": {
            "lstm_csi_basins": ["potomac"],
            "qpf_basins": ["potomac"],
            "xgb_csi_frozen": "climate_p90_csi.csv" in extra,
            "xgb_oracle_frozen": "climate_oracle_xgb.csv" in extra,
        },
    }
    (OUT / "paper_b_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    sections = [
        "# Forecast information-value protocol",
        "",
        "## River climate (all leads)",
        df_md(climate),
        "",
        "## River climate (1-day)",
        df_md(d1),
        "",
        "## River P90 CSI and LSTM oracle (Potomac)",
        df_md(events),
        "",
        "## River GFS QPF vs oracle (Potomac 2024)",
        df_md(qpf),
        "",
        "## Ocean multi-lead (low-tail F1 = training p10, not hypoxia)",
        df_md(ocean),
        "",
        "## Ocean coastal MAE",
        df_md(coast),
        "",
        "## Bottlenecks",
        df_md(msg),
    ]
    if "climate_p90_csi.csv" in extra:
        sections += ["", "## Climate-band P90 CSI (XGBoost protocol)", df_md(extra["climate_p90_csi.csv"])]
    if "climate_oracle_xgb.csv" in extra:
        sections += ["", "## Climate-band XGB oracle precipitation", df_md(extra["climate_oracle_xgb.csv"])]
    if "bow_p90_csi.csv" in extra:
        sections += ["", "## Bow River Canada (non-US transfer) P90 CSI", df_md(extra["bow_p90_csi.csv"])]
    if "bow_oracle_xgb.csv" in extra:
        sections += ["", "## Bow River XGB oracle precipitation", df_md(extra["bow_oracle_xgb.csv"])]
    if "oracle_linear_vs_xgb.csv" in extra:
        sections += ["", "## Linear vs XGB precipitation ceiling", df_md(extra["oracle_linear_vs_xgb.csv"])]
    if "bow_ice_free.csv" in extra:
        sections += ["", "## Bow ice-free test days", df_md(extra["bow_ice_free.csv"])]
    (OUT / "BOTTLENECK.md").write_text("\n".join(sections), encoding="utf-8")

    plot_plate(d1, ocean, qpf)
    plot_verde_leads(climate)
    plot_coast(coast)
    if "climate_p90_csi.csv" in extra and "climate_oracle_xgb.csv" in extra:
        plot_climate_events(extra["climate_p90_csi.csv"], extra["climate_oracle_xgb.csv"])
    if "bow_p90_csi.csv" in extra:
        plot_bow(extra["bow_p90_csi.csv"], extra.get("bow_oracle_xgb.csv"))
    if "oracle_linear_vs_xgb.csv" in extra:
        plot_oracle_robust(extra["oracle_linear_vs_xgb.csv"])
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
