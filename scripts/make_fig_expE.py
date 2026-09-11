# Regenerates paper Figure 2 (effective-noise proxy, Experiment A) and prints the proxies quoted in Section V,
# from results/results.csv and results/pA_results.csv -> figures/fig2_effective_noise.png
# Same computation as notebooks/Exp_E_effective_noise.ipynb: sqrt(acceptance rate) * sigma_rel * rho / tau, mean over the six attacks.
import os, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
df = pd.read_csv(os.path.join(ROOT, "results", "results.csv")).rename(columns={"Percentage of Byzantine Cliets (%)": "f", "Accept_Rate": "accept"})
ag = df[(df.Dataset == "Fashion-MNIST-IID") & (df.Method == "AG-PTR")].copy()
M, C, rho, tau = 100, 1.0, 0.4, 50
sigma_dp = 0.9723217465539842                                        # DP-FedAvg, certified eps = 2.0 (one release per round)
# AG-PTR at the certified-2.0 calibration (composed accountant); read from the runs so figure and runs cannot disagree
_c = pd.read_csv(os.path.join(ROOT, "results", "pA_results.csv"))
sigma_rel = float(_c[(_c.method == "AG-PTR") & (_c.sigma_mode == "certified")].sigma_rel.dropna().iloc[0])
ag["proxy"] = np.sqrt(ag.accept.fillna(0).clip(1e-12, 1.0)) * sigma_rel * rho / tau
agg = ag.groupby("f").proxy.mean().reset_index()
plt.rcParams.update({"font.size": 8})
fig, ax = plt.subplots(figsize=(3.4, 2.05)); x = np.arange(len(agg))
ax.plot(x, agg.proxy, "o-", lw=2.5, label="AG-PTR effective noise")
ax.plot(x, [sigma_dp * C / M] * len(agg), "s-", lw=2.5, label="DP-FedAvg noise proxy")
ax.set_xticks(x); ax.set_xticklabels([f"{f:g}" for f in agg.f]); ax.set_xlabel("Byzantine fraction $f$", fontsize=8); ax.set_ylabel("noise std. dev. (proxy)", fontsize=8)
ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=7)
fig.tight_layout(); out = os.path.join(ROOT, "figures", "fig2_effective_noise.png"); fig.savefig(out, dpi=150); print("saved", out)
print(agg.round(6).to_string(index=False))
