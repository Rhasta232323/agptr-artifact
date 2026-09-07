# Regenerates figures/Exp_D.png (paper Figure 3: FedAdam server, ALIE/SF/MinMax) from results/expD_allmethods_smoke_all_results.csv.
import os, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
df = pd.read_csv(os.path.join(ROOT, "results", "expD_allmethods_smoke_all_results.csv"))
methods = [("DP-FedAvg (FedAdam)", "DP-FedAvg", "o"), ("FedVRDP-style (FedAdam)", "FedVRDP-style", "s"), ("Median (FedAdam)", "Median", "D"),
           ("TrimmedMean (FedAdam)", "TrimmedMean", "^"), ("Krum (FedAdam)", "Krum", "P"), ("SparseFed-style (FedAdam)", "SparseFed-style", "X"), ("AG-PTR (FedAdam-diag P)", "Ours", "o")]
fig, axes = plt.subplots(1, 3, figsize=(20, 5))
for ax, att in zip(axes, ["ALIE", "SF", "MinMax"]):
    sub = df[df.attack == att]; fs = sorted(sub.f.unique()); x = np.arange(len(fs))
    ag = sub[sub.method == "AG-PTR (FedAdam-diag P)"].set_index("f").reindex(fs)
    ax2 = ax.twinx(); TWINS = globals().setdefault("TWINS", []); TWINS.append(ax2); ax2.bar(x, ag.accept_rate.fillna(0).values, width=0.35, alpha=0.2, color="tab:blue", label="Ours accept rate"); ax2.set_ylim(0, 1.05)
    for m, lab, mk in methods:
        s = sub[sub.method == m].set_index("f").reindex(fs)
        ax.plot(x, s.acc.values, marker=mk, label=lab, lw=2.5 if lab == "Ours" else 2, color=("tab:pink" if lab == "Ours" else None))
    ax.axhline(0.1, ls="--", color="tab:blue", lw=1.5, label="Random-guess baseline")
    ax.set_xticks(x); ax.set_xticklabels([f"{f:g}" for f in fs]); ax.set_ylim(0, 1.05); ax.grid(alpha=0.3); ax.set_title(att, fontsize=18)
    if att == "ALIE": ax.set_ylabel("Accuracy", fontsize=14)
    if att == "MinMax": ax2.set_ylabel("Accept rate", fontsize=14)
    else: ax2.set_yticks([])
axes[1].set_xlabel("Byzantine fraction", fontsize=14)
h, l = axes[0].get_legend_handles_labels(); h2, l2 = TWINS[0].get_legend_handles_labels()
fig.legend(h + h2, l + l2, loc="upper center", ncol=5, fontsize=12, bbox_to_anchor=(0.5, 1.02))
fig.tight_layout(rect=(0, 0, 1, 0.9)); out = os.path.join(ROOT, "figures", "Exp_D_regenerated.png"); fig.savefig(out, dpi=150); print("saved", out)
