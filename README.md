# AG-PTR: Anchor-Gated Propose-Test-Release — artifact (anonymized submission to IEEE SaTML 2027)

This artifact contains the complete implementation, every run behind every figure and table in the
paper, and scripts that regenerate the figures from the saved results.

## Layout
```
notebooks/   one self-contained Colab notebook per experiment, WITH saved outputs (the logs and plots
             of the runs reported in the paper)
results/     one CSV row per training run (final test accuracy, AG-PTR acceptance rate, ...)
figures/     the figure files used in the paper (Final2.png, Exp_D.png, Exp_E.png, Exp_F_checks.png)
             and their regenerated counterparts produced by the scripts (*_regenerated.png)
scripts/     figure regeneration from results/ (pure pandas/matplotlib, no GPU needed)
requirements.txt
```

## Paper -> artifact map
| Paper | Notebook (cells) | Result file | Figure script |
|---|---|---|---|
| Figure 2, row 1 (Fashion-MNIST IID) | `Exp_A_FashionMNIST_IID.ipynb`, Cell 15 | `results/expA_all_results.csv` | `scripts/make_fig_main.py` |
| Figure 2, row 2 (Fashion-MNIST non-IID) | `Exp_B_FashionMNIST_nonIID.ipynb`, Cell 15 | `results/expB_all_results.csv` | `scripts/make_fig_main.py` |
| Figure 2, row 3 (CIFAR-10 IID) | `Exp_C_CIFAR10_IID.ipynb`, Cell 15 | `results/expC_all_results.csv` | `scripts/make_fig_main.py` |
| Figure 3 and Table I (FedAdam server, geometry ablation) | `Exp_D_FedAdam_geometry.ipynb`, Cell 16 | `results/expD_allmethods_smoke_all_results.csv` | `scripts/make_fig_expD.py` |
| Table I, last two rows and seed statistics | `Exp_D_FedAdam_geometry.ipynb`, Cells 17b-17c | `results/expD_results.csv`, `results/expD_seed_summary.csv` | - |
| Figure 4 (effective-noise proxy) | `Exp_E_effective_noise.ipynb` | `results/results.csv` (combined A/B/C) | `scripts/make_fig_expE.py` |
| Figure 5 / Section V-C-3 (seeds, certified-2.0 calibration, in-ball attack) | `Exp_A_FashionMNIST_IID.ipynb`, Cells 16b-16d | `results/expA_results.csv`, `results/expA_seed_summary.csv` | `scripts/make_fig_checks.py` |

`results/results.csv` is the concatenation of the three `exp{A,B,C}_all_results.csv` files with a `Dataset`
column, in the column format the Exp E notebook reads.

## Result-file columns
- `exp*_all_results.csv`, `expD_allmethods_smoke_all_results.csv`: `attack, method, f, acc, accept_rate`
  (one run per row; `accept_rate` is defined for AG-PTR only; single seed, executed calibration).
- `expA_results.csv`, `expD_results.csv`: the runs of Section V-C-3, one row per run with `seed`,
  `sigma_mode` (`nominal` = executed calibration, `certified` = certified-2.0 calibration), the noise
  multipliers used, both epsilon readings (`eps_nominal` = per-phase shortcut, `eps_certified` = composed
  accountant), wall time, and a timestamp. `source = legacy` rows are the seed-0 rows copied from the
  `*_all_results.csv` files so that seed statistics can be computed in one place.
- `*_seed_summary.csv`: mean/std over seeds per (sigma_mode, attack, method, f).

## Privacy accounting
Cell 9 of every training notebook contains the accountant (built on Opacus 1.4.0 RDP routines):
`find_sigma_for_target_eps_single` calibrates the single-release baselines;
`find_sigma_rel_for_target_eps_two` / `epsilon_from_sigma_two` is the per-phase shortcut that produced the
executed calibration; `epsilon_certified_two` / `find_sigma_rel_certified_two` is the composed accountant
(one Gaussian mechanism at sigma_eff = (sigma_sel^-2 + sigma_rel^-2)^-1/2, amplified once) that certifies
epsilon <= 2.59 / 2.53 for the executed calibration and gives sigma_rel = 1.0871 / 1.1558 for a certified
epsilon = 2.0. The driver cells print both readings for every run.

## Reproducing
Environment: Google Colab with a T4 GPU (`requirements.txt` lists the pinned packages; Cell 1 of each
notebook installs `opacus==1.4.0`). Datasets are downloaded by torchvision on first run.
- Training notebooks: run Cell 1 through Cell 13.5 (setup, model, methods; ~2 min), then the run cell you
  want. Cell 4b caches the datasets as tensors (identical numbers, faster). A full 180-round run takes about
  1-3 minutes on a T4; a full grid (6 attacks x 7 fractions x 7 methods) takes several hours. In Exp A and
  Exp D the job cells (16a-16d / 17a-17c) are resumable: every finished run is appended to a CSV, and
  re-running a job cell skips finished runs.
- Figures: `python scripts/make_fig_main.py` (Figure 2), `make_fig_expD.py` (Figure 3), `make_fig_expE.py`
  (Figure 4), `make_fig_checks.py` (Figure 5). They read `results/` and write `figures/*_regenerated.png`
  (Figure 5 is written as `figures/Exp_F_checks.png`). The paper's original PNGs were exported from the
  notebooks' plots; the regenerated versions use the same numbers with minor styling differences.

## Notes
- GPU floating-point non-determinism: re-running a seed on different hardware reproduces accuracies to
  within about 0.01 (the seed-0 runs were executed on H100/G4 GPUs, the Section V-C-3 runs on a T4).
- Everything here is anonymized for review. License: to be added by the authors upon acceptance.
