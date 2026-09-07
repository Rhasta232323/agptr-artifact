# Generates Exp_F_checks.png (robustness checks on Experiment A) from expA_results.csv.
# Panels: (a) three-seed error bars on the headline cells; (b) AG-PTR at the executed vs the
# certified eps=2 calibration, mean and range over the six attacks; (c) the defense-aware
# in-ball attack against AG-PTR, with the gate's acceptance rate.
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = pd.read_csv(os.path.join(ROOT, "results", "expA_results.csv")); a = a[a.status == "ok"]
fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.6))

# (a) seeds
ax = axes[0]
nom = a[a.sigma_mode == "nominal"]
groups = [("clean ($f=0$)", "ALIE", 0.0), ("ALIE, $f=0.4$", "ALIE", 0.4), ("MinMax, $f=0.4$", "MinMax", 0.4)]
methods = ["AG-PTR", "DP-FedAvg", "TrimmedMean"]; w = 0.25
for j, m in enumerate(methods):
    means, stds = [], []
    for (_, att, f) in groups:
        s = nom[(nom.attack == att) & (nom.f == f) & (nom.method == m) & nom.seed.isin([0, 1, 2])]
        means.append(s.acc.mean()); stds.append(s.acc.std(ddof=1))
    ax.bar(np.arange(len(groups)) + (j - 1) * w, means, w, yerr=stds, capsize=4, label=m)
ax.set_xticks(range(len(groups))); ax.set_xticklabels([g[0] for g in groups]); ax.set_ylim(0, 1.0)
ax.set_ylabel("test accuracy (mean $\\pm$ std, 3 seeds)"); ax.set_title("(a) seed variability"); ax.legend(fontsize=8, loc="upper center", ncol=3); ax.grid(axis="y", alpha=0.3)

# (b) certified vs nominal
ax = axes[1]
for mode, style, lab in [("nominal", "o-", "executed calibration ($\\sigma_{\\mathrm{rel}}=0.983$, $\\varepsilon\\leq2.59$)"), ("certified", "s--", "certified-2.0 calibration ($\\sigma_{\\mathrm{rel}}=1.087$)")]:
    s = a[(a.method == "AG-PTR") & (a.sigma_mode == mode) & (a.seed == 0) & (a.attack != "InBall")]
    g = s.groupby("f").acc; fs = sorted(g.groups.keys())
    mean = [g.get_group(f).mean() for f in fs]; lo = [g.get_group(f).min() for f in fs]; hi = [g.get_group(f).max() for f in fs]
    ax.plot(fs, mean, style, label=lab); ax.fill_between(fs, lo, hi, color=("0.35" if mode == "nominal" else "0.6"), alpha=0.35, label=("range over attacks (executed)" if mode == "nominal" else "range over attacks (certified-2.0)"))
ax.set_xlabel("Byzantine fraction $f$"); ax.set_ylabel("AG-PTR test accuracy"); ax.set_title("(b) AG-PTR: executed vs. certified-2.0 calibration")
ax.legend(fontsize=8, loc="lower left"); ax.grid(alpha=0.3); ax.set_ylim(0, 0.85)

# (c) in-ball attack — one [0,1] axis: accuracy (solid/dashed) and acceptance rate (dotted line with markers)
ax = axes[2]
s0 = a[(a.method == "AG-PTR") & (a.sigma_mode == "nominal") & (a.seed == 0)]
for att, style, lab in [("InBall", "s-", "accuracy, in-ball (defense-aware)"), ("ALIE", "o--", "accuracy, ALIE"), ("MinMax", "^--", "accuracy, MinMax")]:
    t = s0[s0.attack == att].sort_values("f"); ax.plot(t.f, t.acc, style, label=lab)
t = s0[s0.attack == "InBall"].sort_values("f")
ax.plot(t.f, t.accept_rate, "x:", color="black", label="fraction of rounds accepted, in-ball")
ax.set_xlabel("Byzantine fraction $f$"); ax.set_ylabel("accuracy / fraction of rounds accepted"); ax.set_ylim(0, 1.05); ax.grid(alpha=0.3)
ax.legend(fontsize=8, loc="lower left"); ax.set_title("(c) defense-aware in-ball attack")
fig.tight_layout(); out = os.path.join(ROOT, "figures", "Exp_F_checks.png"); fig.savefig(out, dpi=200); print("saved", out)
