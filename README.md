# AG-PTR: Anchor-Gated Propose-Test-Release - artifact (anonymized submission to IEEE SaTML 2027)

Complete implementation, every run behind every figure and table in the paper, and scripts that regenerate the
figures and tables from the saved results. Every run uses Poisson client sampling (each client joins a round
independently with probability q = 100/N), which is the sampler the privacy accountant assumes; every AG-PTR run is
at the certified client-level budget eps = 2.0 (composed accountant, sigma_rel = 1.0871 on Fashion-MNIST, 1.1558 on
CIFAR-10; baselines at sigma_dp = 0.9723 / 1.0338).

## Layout
```
notebooks/   one self-contained Colab notebook per experiment, WITH the saved outputs of the reported runs
results/     one CSV row per training run (pA/pB/pC/pD_results.csv), seed summaries, and results.csv (Figure 1 input)
figures/     fig1_main_results.png, fig2_effective_noise.png, fig3_checks.png (Figures 1-3 of the paper)
scripts/     regenerate Figures 1-3 and print Tables I and II (pandas/matplotlib, no GPU)
requirements.txt
```

## Paper -> artifact map
| Paper | Notebook cells | Result file | Script |
|---|---|---|---|
| Figure 1 (Experiments A-C, seven methods, six attacks) | `Exp_{A,B,C}_*.ipynb` cell 16b (grid) and the FedVRDP cells (A: 16i; B, C: 16c) | `results/results.csv` (built from `p{A,B,C}_results.csv`) | `scripts/make_fig_main.py` -> `figures/fig1_main_results.png` |
| Figure 2 (effective-noise proxy; Experiment A) | `Exp_E_effective_noise.ipynb` (Cell E0 builds `results.csv`) | `results/results.csv`, `results/pA_results.csv` | `scripts/make_fig_expE.py` -> `figures/fig2_effective_noise.png` |
| Figure 3 (seeds, controls, in-ball attack; Experiment A) | `Exp_A_*.ipynb` cells 16c-16h | `results/pA_results.csv` | `scripts/make_fig_checks.py` -> `figures/fig3_checks.png` |
| Public-set-size check (Section V, controls paragraph) | `Exp_A_*.ipynb` cell 16k (rows `AG-PTR (pub=50)`, `AG-PTR (pub=800)`) | `results/pA_results.csv` | - |
| Table I (worst case over five attacks; Experiments A-C, controls, FedVRDP) | `Exp_{A,B,C}` cell 16b, `Exp_A` cells 16c, 16g, 16i, 16j, `Exp_{B,C}` cell 16c | `results/p{A,B,C}_results.csv` | `scripts/make_table_worstcase.py` (prints the table) |
| Table II (FedAdam server, geometry ablation; Experiment D) | `Exp_D_FedAdam_geometry.ipynb` cells 17b (table), 17c (seeds), 17d (FedVRDP) | `results/pD_results.csv` | `scripts/make_table_geometry.py` (prints the table) |

## Methods in the result files
`FedVRDP` is the faithful implementation of Zhang & Hu (2023), Algorithm 1 (Cell 13.7 of the training notebooks):
momentum SGD reset each round, mask = top-k coordinates of the global model refreshed every round (random initial
mask), clipping at C = 0.5, noise on the k = 30% kept coordinates at the certified budget. `FedVRDP-10ep` is the same
with the paper's 10 local epochs (Experiment A). `FedVRDP-style` is the earlier fixed-support variant (mask refreshed
from the masked aggregate, so the support never changed); it is kept in the result files for completeness but is not
reported in the paper. `FedVRDP (FedAdam)` is the faithful method with the FedAdam server (Experiment D).

## Result-file columns
`p*_results.csv`: `attack, attack_key, method, f, seed, sampling (poisson), is_private, sigma_dp, sigma_sel, sigma_rel,
eps_certified (blank for non-private methods), rounds, acc, accept_rate (AG-PTR only), wall_sec, status, timestamp`.
`p*_seed_summary.csv`: mean/std over seeds per (attack, method, f). `results.csv`: the seven main methods, seed 0,
in the format the Exp E notebook and the Figure 2 script read. `pA_results_fltrust_v1.csv` (if present) holds the
FLTrust rows of an earlier root-update implementation that were replaced (see the FLTrust docstring in Cell 13.6).

## Privacy accounting
Cell 9 of every training notebook contains the accountant (Opacus 1.4.0 RDP routines for the Poisson-subsampled
Gaussian mechanism, converted to (eps, delta) with the tighter conversion of Balle et al. 2020 as implemented in
Opacus): `find_sigma_for_target_eps_single` calibrates the single-release methods; `epsilon_certified_two` /
`find_sigma_rel_certified_two` implement the composed accountant for AG-PTR's two releases per round (one Gaussian
mechanism with sigma_eff = (sigma_sel^-2 + sigma_rel^-2)^-1/2, amplified once). Cell 4c is the Poisson sampler;
denominators that enter a sensitivity bound are public (expected cohort size 100; AG-PTR count cap 200).

## Reproducing
Google Colab with a T4 GPU (`requirements.txt`; Cell 1 installs `opacus==1.4.0` without touching Colab's torch).
Datasets are downloaded by torchvision on first run. Run Cells 1 ... 13.5, then the definition cells 13.6 (ablation controls,
Exp A) and 13.7 (FedVRDP) where present (about 2 min in total), the DEFINITIONS cell, then the job cells; every job appends
each finished run to a CSV on Google Drive and skips finished runs when re-run. The public-set-size jobs must be launched
through Cell 16k, whose wrapper rebuilds the partition and calibration before `run_job("pub50")` / `run_job("pub800")`
and restores the default afterwards; calling those jobs directly would run at the default 200-sample partition.
A 180-round run takes 1-3 minutes; the full Exp A grid about 8 hours. Figures and tables: `python scripts/<name>.py`
from the artifact root; the figure scripts overwrite the files in `figures/`, the table scripts print the tables.

## Notes
- GPU floating-point non-determinism: re-running a seed on different hardware reproduces accuracies to within
  about 0.01.
- Everything here is anonymized for review. License: to be added by the authors upon acceptance.
