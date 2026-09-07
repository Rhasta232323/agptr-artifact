# Regenerates figures/Final2.png (paper Figure 2: Experiments A-C, six attacks) from results/results.csv.
import os, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
df = pd.read_csv(os.path.join(ROOT, "results", "results.csv"))
df = df.rename(columns={"Percentage of Byzantine Cliets (%)": "f", "Accuracy": "acc", "Accept_Rate": "accept"})
datasets = ["Fashion-MNIST-IID", "Fashion-MNIST-non-IID", "CIFAR-10-IID"]
attacks = ["ALIE", "FoE", "LF", "MinMax", "MinSum", "SF"]
methods = [("DP-FedAvg", "o"), ("FedVRDP-style", "s"), ("Median", "D"), ("TrimmedMean", "^"), ("Krum", "*"), ("SparseFed-style", "P"), ("AG-PTR", "X")]
fig, axes = plt.subplots(3, 6, figsize=(30, 13), sharex=False)
for r, ds in enumerate(datasets):
    for c, att in enumerate(attacks):
        ax = axes[r, c]; sub = df[(df.Dataset == ds) & (df.Attack == att)]
        fs = sorted(sub.f.unique()); x = np.arange(len(fs))
        ag = sub[sub.Method == "AG-PTR"].set_index("f").reindex(fs)
        ax2 = ax.twinx(); TWINS = globals().setdefault("TWINS", []); TWINS.append(ax2); ax2.bar(x, ag.accept.fillna(0).values, width=0.35, alpha=0.25, color="tab:blue", label="AG-PTR accept rate"); ax2.set_ylim(0, 1.05)
        for m, mk in methods:
            s = sub[sub.Method == m].set_index("f").reindex(fs)
            ax.plot(x, s.acc.values, marker=mk, label=("Ours" if m == "AG-PTR" else m), lw=2 if m == "AG-PTR" else 1.5, color=("tab:pink" if m == "AG-PTR" else None))
        ax.axhline(0.1, ls="--", color="tab:blue", lw=1, label="Random-guess baseline")
        ax.set_xticks(x); ax.set_xticklabels([f"{f:g}" for f in fs]); ax.set_ylim(0, 1.05 if r < 2 else 0.9); ax.grid(alpha=0.3)
        ax.set_title(att)
        if c == 0: ax.set_ylabel(f"{ds}\nAccuracy")
        if c == 5: ax2.set_ylabel("Accept rate")
        else: ax2.set_yticks([])
        if r == 2: ax.set_xlabel("Byzantine fraction")
h, l = axes[0, 0].get_legend_handles_labels(); h2, l2 = TWINS[0].get_legend_handles_labels()
fig.legend(h + h2, l + l2, loc="upper center", ncol=5, fontsize=14, bbox_to_anchor=(0.5, 1.0))
fig.tight_layout(rect=(0, 0, 1, 0.94)); out = os.path.join(ROOT, "figures", "Final2_regenerated.png"); fig.savefig(out, dpi=120); print("saved", out)
