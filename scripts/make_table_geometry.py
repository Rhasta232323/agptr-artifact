# Prints paper Table II: Experiment D (FedAdam server), final accuracy at f = 0 / 0.3 / 0.49 under ALIE / SF / MinMax
# for all methods, plus the three-seed clean statistics, from results/pD_results.csv.
import os, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
d = pd.read_csv(os.path.join(ROOT, "results", "pD_results.csv")); d = d[d.status == "ok"]
order = ["DP-FedAvg (FedAdam)", "FedVRDP (FedAdam)", "Median (FedAdam)", "TrimmedMean (FedAdam)", "Krum (FedAdam)", "SparseFed-style (FedAdam)",
         "AG-PTR (P=I)", "AG-PTR (FedAdam-diag P)", "AG-PTR (FedAdam-scalar P)"]
cols = [(att, f) for att in ["ALIE", "SF", "MinMax"] for f in [0.0, 0.3, 0.49]]
tab = pd.DataFrame({m: [d[(d.method == m) & (d.seed == 0) & (d.attack == a) & (d.f == f)].acc.iloc[0] for (a, f) in cols] for m in order},
                   index=pd.MultiIndex.from_tuples(cols, names=["attack", "f"])).T
with pd.option_context("display.width", 200, "display.float_format", "{:.2f}".format):
    print(tab)
sd = d[(d.attack == "ALIE") & (d.f == 0.0) & d.method.isin(["AG-PTR (P=I)", "AG-PTR (FedAdam-diag P)"])].groupby("method").acc.agg(["mean", "std", "count"])
print("\nclean accuracy over seeds (ALIE, f=0):"); print(sd.round(3))
