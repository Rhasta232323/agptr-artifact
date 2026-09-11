# Regenerates paper Figure 1 (Experiments A-C, seven methods, six attacks) from results/results.csv -> figures/fig1_main_results.png
import os, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
df = pd.read_csv(os.path.join(ROOT, "results", "results.csv"))
df = df.rename(columns={"Percentage of Byzantine Cliets (%)": "f", "Accuracy": "acc", "Accept_Rate": "accept"})
datasets = [("Fashion-MNIST-IID", "F-MNIST IID"), ("Fashion-MNIST-non-IID", "F-MNIST non-IID"), ("CIFAR-10-IID", "CIFAR-10")]
attacks = ["ALIE", "FoE", "LF", "MinMax", "MinSum", "SF"]
methods = [("DP-FedAvg", "o"), ("FedVRDP", "s"), ("Median", "D"), ("TrimmedMean", "^"), ("Krum", "*"), ("SparseFed-style", "P"), ("AG-PTR", "X")]
plt.rcParams.update({"font.size": 15})
fig, axes = plt.subplots(3, 6, figsize=(20, 8.4), sharex=True, sharey="row")
TWINS = []
for r, (ds, ds_label) in enumerate(datasets):
    for c, att in enumerate(attacks):
        ax = axes[r, c]; sub = df[(df.Dataset == ds) & (df.Attack == att)]
        fs = sorted(sub.f.unique()); x = np.arange(len(fs))
        ag = sub[sub.Method == "AG-PTR"].set_index("f").reindex(fs)
        ax2 = ax.twinx(); TWINS.append(ax2)
        ax2.bar(x, ag.accept.fillna(0).values, width=0.35, alpha=0.25, color="tab:blue", label="AG-PTR accept rate"); ax2.set_ylim(0, 1.05)
        for m, mk in methods:
            s = sub[sub.Method == m].set_index("f").reindex(fs)
            ax.plot(x, s.acc.values, marker=mk, label=("Ours (AG-PTR)" if m == "AG-PTR" else m), lw=2.2 if m == "AG-PTR" else 1.5, color=("tab:pink" if m == "AG-PTR" else None))
        ax.axhline(0.1, ls="--", color="tab:blue", lw=1, label="random guess")
        ax.set_xticks(x); ax.set_xticklabels(["0", ".1", ".2", ".3", ".4", ".49", ".6"], fontsize=13)
        ax.set_ylim(0, 1.05 if r < 2 else 0.9); ax.grid(alpha=0.3); ax.tick_params(axis="y", labelsize=13)
        if r == 0: ax.set_title(att, fontsize=18)
        if c == 0: ax.set_ylabel(f"{ds_label}\naccuracy", fontsize=15)
        if c == 5: ax2.set_ylabel("accept rate", fontsize=14); ax2.tick_params(axis="y", labelsize=13)
        else: ax2.set_yticks([])
        if r == 2: ax.set_xlabel("Byzantine fraction $f$", fontsize=14)
h, l = axes[0, 0].get_legend_handles_labels(); h2, l2 = TWINS[0].get_legend_handles_labels()
fig.legend(h + h2, l + l2, loc="upper center", ncol=5, fontsize=15, frameon=False, bbox_to_anchor=(0.5, 1.0))
fig.tight_layout(rect=(0, 0, 1, 0.905)); out = os.path.join(ROOT, "figures", "fig1_main_results.png"); fig.savefig(out, dpi=150); print("saved", out)
