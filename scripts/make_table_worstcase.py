# Prints paper Table I: worst-case final accuracy over the five update-space attacks
# (FedVRDP = faithful implementation of Zhang & Hu 2023; FedVRDP-10ep = the same with the paper's 10 local epochs;
#  the earlier fixed-support variant "FedVRDP-style" is kept in the result files but not in the table)
# (ALIE, SF, Min-Max, Min-Sum, FoE), seed 0, per method and dataset, from results/.
import os, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); R = os.path.join(ROOT, "results")
ATT = ["ALIE", "SF", "MinMax", "MinSum", "FoE"]
rows = {}
for tag in "ABC":
    r = pd.read_csv(os.path.join(R, f"p{tag}_results.csv")); r = r[(r.status == "ok") & (r.seed == 0) & (r.source == "run")]
    w = r[r.attack.isin(ATT)].groupby(["method", "f"]).acc.min().unstack("f")
    for m in w.index:
        for f in [0.3, 0.4, 0.49]:
            rows.setdefault(m, {})[(tag, f)] = w.loc[m, f] if f in w.columns else float("nan")
tab = pd.DataFrame(rows).T.sort_index(axis=1)
order = ["AG-PTR", "DP-FedAvg+Public", "AnchoredClip-NoGate", "DP-FedAvg", "FedVRDP", "FedVRDP-10ep", "Median", "TrimmedMean", "Krum", "SparseFed-style", "FLTrust"]
tab = tab.reindex([m for m in order if m in tab.index])
with pd.option_context("display.width", 200, "display.float_format", "{:.2f}".format):
    print(tab)
po = pd.read_csv(os.path.join(R, "pA_results.csv")); po = po[po.method == "PublicOnly"]
print("\nPublic anchor alone (Exp A, 3 seeds): %.3f +/- %.3f" % (po.acc.mean(), po.acc.std()))
