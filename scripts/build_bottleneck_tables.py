"""Bottleneck tables for Paper B (standalone frozen snapshots)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RIVER = ROOT / "data" / "frozen" / "river"
OCEAN = ROOT / "data" / "frozen" / "ocean"
OUT = ROOT / "results" / "tables"
FIG = ROOT / "results" / "figures"


def df_md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def river_horizon() -> pd.DataFrame:
    df = pd.read_csv(RIVER / "climate_basin_compare.csv")
    # 1-day upstream ablation (information value) by climate
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
    # Parse compact rows from markdown table if present
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


def bottleneck_message(river: pd.DataFrame, ocean: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "domain": "river",
                "bottleneck": "usable precipitation foresight + unsaturated autocorrelation",
                "evidence": "James 1-d ablation ΔNSE +0.13; Willamette ~0; Verde LSTM can lose to routing",
            },
            {
                "domain": "ocean",
                "bottleneck": "time-varying oxygen / coastal structure at lead ≥2 months",
                "evidence": "lead-1 ST beats clim; lead-2 hybrid/clim wins; Argo history +35% RMSE",
            },
        ]
    )


def plot_bottleneck(river: pd.DataFrame, ocean: pd.DataFrame) -> None:
    import matplotlib.pyplot as plt

    FIG.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    r = river.set_index("basin")
    axes[0].bar(r.index, r["ablation_delta"], color="#1f6f8b")
    axes[0].axhline(0, color="#6b7c85", lw=0.8)
    axes[0].set_ylabel("1-day upstream ΔNSE (full − local)")
    axes[0].set_title("River: where gauges add information")
    axes[0].tick_params(axis="x", rotation=20)

    sub = ocean[ocean["model"].isin(["persistence", "climatology", "st_transformer", "hybrid_clim_st"])]
    for model, g in sub.groupby("model"):
        axes[1].plot(g["lead_mo"], g["RMSE"], marker="o", label=model)
    axes[1].set_xlabel("Lead (months)")
    axes[1].set_ylabel(r"RMSE ($\mu$mol kg$^{-1}$)")
    axes[1].set_title("Ocean: climatology takeover after lead-1")
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle("Information bottlenecks — two environmental forecast media", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "fig_information_bottleneck.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    river = river_horizon()
    ocean = ocean_leads()
    msg = bottleneck_message(river, ocean)
    river.to_csv(OUT / "river_1d_information_value.csv", index=False)
    ocean.to_csv(OUT / "ocean_multilead_skill.csv", index=False)
    msg.to_csv(OUT / "bottleneck_summary.csv", index=False)
    (OUT / "BOTTLENECK.md").write_text(
        "\n".join(
            [
                "# Forecast information-value protocol",
                "",
                "Standalone repo. Frozen numbers in `data/frozen/`.",
                "",
                "## River (1-day)",
                df_md(river),
                "",
                "## Ocean multi-lead",
                df_md(ocean),
                "",
                "## Bottlenecks",
                df_md(msg),
            ]
        ),
        encoding="utf-8",
    )
    plot_bottleneck(river, ocean)
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
