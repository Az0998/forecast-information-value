"""Paper B tables + four-panel plate from frozen snapshots."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RIVER = ROOT / "data" / "frozen" / "river"
OCEAN = ROOT / "data" / "frozen" / "ocean"
OUT = ROOT / "results" / "tables"
FIG = ROOT / "results" / "figures"

RIVER_COLOR = "#1f6f8b"
OCEAN_COLOR = "#0f5f78"
MUTED = "#6b7c85"


def df_md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def river_horizon() -> pd.DataFrame:
    df = pd.read_csv(RIVER / "climate_basin_compare.csv")
    d1 = df[df["horizon"] == 1].copy()
    keep = [
        "basin",
        "climate",
        "routing_NSE",
        "lstm_attention_NSE",
        "ablation_delta",
        "attn_minus_routing",
    ]
    return d1[keep].round(3)


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
                "hypoxia_F1": float(parts[6]),
                "CSI": float(parts[7]),
            }
        )
    return pd.DataFrame(rows)


def river_events() -> pd.DataFrame:
    csi = pd.read_csv(RIVER / "flood_csi.csv")
    ora = pd.read_csv(RIVER / "oracle_precip.csv")
    out = csi.merge(ora, on="horizon")
    return out.round(3)


def coastal_mae() -> pd.DataFrame:
    raw = json.loads((OCEAN / "failure_modes.json").read_text(encoding="utf-8"))
    rows = [b for b in raw["bins"] if b["driver"] == "coastal_proximity"]
    return pd.DataFrame(rows)[["bin", "n_cells", "mae", "p90"]].round(3)


def bottleneck_message() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "domain": "river",
                "bottleneck": "precipitation foresight after day 1; climate-conditional gauge value",
                "evidence": "Oracle precip ΔNSE ≈ 0 at 1 d, +0.12 at 3 d, +0.20 at 7 d; James ΔNSE +0.13, Willamette ≈ 0; Verde LSTM NSE 0.39 < routing 0.61",
            },
            {
                "domain": "ocean",
                "bottleneck": "learned anomaly skill collapses at lead ≥ 2 months; errors concentrate coastally",
                "evidence": "Lead-1 ST RMSE 3.88 vs clim 5.30; lead-2 hybrid 5.08 ≈ clim 5.23; Argo +35% RMSE; coastal MAE 3.30 vs 2.95 offshore",
            },
        ]
    )


def plot_plate(river: pd.DataFrame, ocean: pd.DataFrame, events: pd.DataFrame) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.2))

    r = river.set_index("basin")
    axes[0, 0].bar(r.index.str.capitalize(), r["ablation_delta"], color=RIVER_COLOR)
    axes[0, 0].axhline(0, color=MUTED, lw=0.8)
    axes[0, 0].set_ylabel("1-day upstream ΔNSE")
    axes[0, 0].set_title("(a) Gauge information is climate-conditional")
    axes[0, 0].tick_params(axis="x", rotation=15)

    axes[0, 1].plot(events["horizon"], events["routing_CSI"], "s--", color=MUTED, label="Routing CSI")
    axes[0, 1].plot(events["horizon"], events["attn_CSI"], "o-", color=RIVER_COLOR, label="Learned CSI")
    axes[0, 1].set_xticks(list(events["horizon"]))
    axes[0, 1].set_xlabel("Lead (days)")
    axes[0, 1].set_ylabel("P90 flood CSI")
    axes[0, 1].set_title("(b) Event skill decays; routing collapses first")
    axes[0, 1].legend(frameon=False, fontsize=8)

    sub = ocean[ocean["model"].isin(["persistence", "climatology", "st_transformer", "hybrid_clim_st"])]
    for model, g in sub.groupby("model"):
        axes[1, 0].plot(g["lead_mo"], g["RMSE"], marker="o", label=model)
    axes[1, 0].set_xlabel("Lead (months)")
    axes[1, 0].set_ylabel(r"RMSE ($\mu$mol kg$^{-1}$)")
    axes[1, 0].set_title("(c) Oxygen: climatology takeover after lead-1")
    axes[1, 0].legend(frameon=False, fontsize=8)

    axes[1, 1].plot(events["horizon"], events["delta_NSE"], "o-", color=RIVER_COLOR)
    axes[1, 1].axhline(0, color=MUTED, lw=0.8)
    axes[1, 1].set_xticks(list(events["horizon"]))
    axes[1, 1].set_xlabel("Lead (days)")
    axes[1, 1].set_ylabel("Oracle − observed precip ΔNSE")
    axes[1, 1].set_title("(d) River bottleneck is future rain, not architecture")

    fig.suptitle("Information-value protocol across rivers and a shelf oxygen cube", fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG / "fig_information_bottleneck.png", dpi=300, bbox_inches="tight")
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
    river = river_horizon()
    ocean = ocean_leads()
    events = river_events()
    coast = coastal_mae()
    msg = bottleneck_message()

    river.to_csv(OUT / "river_1d_information_value.csv", index=False)
    ocean.to_csv(OUT / "ocean_multilead_skill.csv", index=False)
    events.to_csv(OUT / "river_event_and_oracle.csv", index=False)
    coast.to_csv(OUT / "ocean_coastal_mae.csv", index=False)
    msg.to_csv(OUT / "bottleneck_summary.csv", index=False)

    shap = json.loads((RIVER / "shap_summary.json").read_text(encoding="utf-8"))
    summary = {
        "claim": "mid-range skill is capped by missing information, not model class",
        "river_oracle_delta_NSE": {
            str(int(r.horizon)): float(r.delta_NSE) for r in events.itertuples()
        },
        "river_attn_CSI": {str(int(r.horizon)): float(r.attn_CSI) for r in events.itertuples()},
        "ocean_lead1_ST_RMSE": float(ocean.loc[(ocean.lead_mo == 1) & (ocean.model == "st_transformer"), "RMSE"].iloc[0]),
        "ocean_lead2_hybrid_RMSE": float(ocean.loc[(ocean.lead_mo == 2) & (ocean.model == "hybrid_clim_st"), "RMSE"].iloc[0]),
        "shap_top_channel": max(shap["channel_mean_abs_shap"], key=shap["channel_mean_abs_shap"].get),
        "coastal_high_mae": float(coast.loc[coast["bin"] == "high", "mae"].iloc[0]),
    }
    (OUT / "paper_b_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    (OUT / "BOTTLENECK.md").write_text(
        "\n".join(
            [
                "# Forecast information-value protocol",
                "",
                "## River climate (1-day)",
                df_md(river),
                "",
                "## River P90 CSI and oracle precipitation",
                df_md(events),
                "",
                "## Ocean multi-lead",
                df_md(ocean),
                "",
                "## Ocean coastal MAE",
                df_md(coast),
                "",
                "## Bottlenecks",
                df_md(msg),
            ]
        ),
        encoding="utf-8",
    )
    plot_plate(river, ocean, events)
    plot_coast(coast)
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
