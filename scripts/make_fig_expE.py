# Regenerates figures/Exp_E.png (paper Figure 4: effective-noise proxy) from results/results.csv.
# Same computation as notebooks/Exp_E_effective_noise.ipynb: sqrt(acceptance rate) * sigma_rel * rho / tau, mean over the six attacks.
import os, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
df = pd.read_csv(os.path.join(ROOT, "results", "results.csv")).rename(columns={"Percentage of Byzantine Cliets (%)": "f", "Accept_Rate": "accept"})
ag = df[(df.Dataset == "Fashion-MNIST-IID") & (df.Method == "AG-PTR")].copy()
M, C, rho, tau = 100, 1.0, 0.4, 50
sigma_dp, sigma_rel = 0.9723217465539842, 0.9829512225866845          # executed calibration (Experiment A)
ag["proxy"] = np.sqrt(ag.accept.fillna(0).clip(1e-12, 1.0)) * sigma_rel * rho / tau
agg = ag.groupby("f").proxy.mean().reset_index()
fig, ax = plt.subplots(figsize=(6.5, 4.6)); x = np.arange(len(agg))
ax.plot(x, agg.proxy, "o-", lw=2.5, label="AG-PTR effective noise")
ax.plot(x, [sigma_dp * C / M] * len(agg), "s-", lw=2.5, label="DP-FedAvg noise proxy")
ax.set_xticks(x); ax.set_xticklabels([f"{f:g}" for f in agg.f]); ax.set_xlabel("Byzantine fraction", fontsize=13); ax.set_ylabel("Noise standard deviation (proxy)", fontsize=13)
ax.grid(alpha=0.3); ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize=11)
fig.tight_layout(); out = os.path.join(ROOT, "figures", "Exp_E_regenerated.png"); fig.savefig(out, dpi=150); print("saved", out)
print(agg.round(6).to_string(index=False))
