# Regenerates paper Figure 3 (seeds, controls, in-ball attack; Experiment A) from results/pA_results.csv -> figures/fig3_checks.png
# (a) three-seed error bars on the headline cells; (b) what the public anchor and the gate contribute:
# worst-case accuracy over the five update-space attacks for AG-PTR, the three controls, and the public anchor alone;
# (c) the defense-aware in-ball attack against AG-PTR with the gate's acceptance rate.
import os, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
a = pd.read_csv(os.path.join(ROOT, "results", "pA_results.csv")); a = a[a.status == "ok"]
plt.rcParams.update({"font.size": 10})
fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.35))

# (a) seeds
ax = axes[0]
groups = [("clean", "ALIE", 0.0), ("ALIE $f$=0.4", "ALIE", 0.4), ("MinMax $f$=0.4", "MinMax", 0.4)]
methods = ["AG-PTR", "DP-FedAvg", "TrimmedMean", "Krum", "SparseFed-style"]; w = 0.16
for j, m in enumerate(methods):
    means, stds = [], []
    for (_, att, f) in groups:
        s = a[(a.attack == att) & (a.f == f) & (a.method == m) & a.seed.isin([0, 1, 2])]
        means.append(s.acc.mean()); stds.append(s.acc.std(ddof=1))
    ax.bar(np.arange(len(groups)) + (j - 2) * w, means, w, yerr=stds, capsize=3, label=m)
ax.set_xticks(range(len(groups))); ax.set_xticklabels([g[0] for g in groups]); ax.set_ylim(0, 1.12)
ax.set_ylabel("accuracy (mean $\\pm$ std, 3 seeds)"); ax.set_title("(a) seed variability"); ax.legend(fontsize=8, loc="upper center", ncol=3, frameon=False); ax.grid(axis="y", alpha=0.3)

# (b) controls: worst case over the five update-space attacks
ax = axes[1]
s0 = a[(a.seed == 0) & a.attack.isin(["ALIE", "SF", "MinMax", "MinSum", "FoE"])]
for m, style, lab in [("FLTrust", "^-", "FLTrust (non-private)"), ("AG-PTR", "s-", "AG-PTR"),
                      ("AnchoredClip-NoGate", "v--", "anchored clipping, no gate"), ("DP-FedAvg+Public", "o--", "DP-FedAvg + public anchor"),
                      ("DP-FedAvg", "x:", "DP-FedAvg")]:
    w_ = s0[s0.method == m].groupby("f").acc.min(); ax.plot(w_.index, w_.values, style, label=lab)
po = a[a.method == "PublicOnly"].acc; ax.axhline(po.mean(), color="gray", ls="-.", label="public anchor alone (%.2f)" % po.mean())
ax.set_xlabel("Byzantine fraction $f$"); ax.set_ylabel("worst case over 5 attacks"); ax.set_ylim(0, 0.9); ax.grid(alpha=0.3)
ax.legend(fontsize=8, loc="lower left", frameon=False); ax.set_title("(b) public anchor and gate contributions")

# (c) in-ball attack
ax = axes[2]
sA = a[(a.method == "AG-PTR") & (a.seed == 0)]
ib = a[(a.method == "AG-PTR") & (a.attack == "InBall")].groupby("f").acc.agg(["mean", "std", "count"]).reset_index()
ax.errorbar(ib.f, ib["mean"], yerr=ib["std"].fillna(0), fmt="s-", capsize=3, label="in-ball attack (mean $\\pm$ std, 3 seeds)")
for att, style, lab in [("ALIE", "o--", "ALIE"), ("MinMax", "^--", "MinMax")]:
    t = sA[sA.attack == att].sort_values("f"); ax.plot(t.f, t.acc, style, label=lab)
t = sA[sA.attack == "InBall"].sort_values("f"); ax.plot(t.f, t.accept_rate, "x:", color="black", label="in-ball: fraction of rounds accepted")
ax.set_xlabel("Byzantine fraction $f$"); ax.set_ylabel("accuracy / acceptance"); ax.set_ylim(0, 1.12); ax.grid(alpha=0.3)
ax.legend(fontsize=8, loc="lower left", frameon=False); ax.set_title("(c) defense-aware in-ball attack")
fig.tight_layout(); out = os.path.join(ROOT, "figures", "fig3_checks.png"); fig.savefig(out, dpi=200); print("saved", out)
