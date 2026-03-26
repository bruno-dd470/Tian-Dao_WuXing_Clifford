# 📁 README — Python Codes (Hybrid W Layer)

## 🎯 Overview

This repository contains the Python scripts for training and simulating the **Hybrid W Layer**, a constrained linear projection operator mapping a 72D theoretical space (Cl(6,6), pentads, Nebe lattice) to a 10D operational space.

---

## 📂 File Structure

| File | Role | Execute First |
|------|------|---------------|
| `RÉENTRAÎNEMENT_COUCHE_W_AVEC_CONTRAINTE_DE_DIVERSITÉ_FAMILIALE.py` | **Training** — Generates optimized W weights | ✅ **YES** |
| `MODULE_6_v4.7_Version_Mathematique.py` | **Simulation** — Uses W weights for simulations | ❌ No (requires W) |

## 🔧 Prerequisites

### Python 3.9+

```bash
python3 --version  # Should display 3.9 or higher
```

### Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```
numpy>=1.21.0
torch>=1.10.0
scipy>=1.7.0
matplotlib>=3.5.0
```

---

## 🚀 Execution Workflow

### STEP 1: Generate W Weights

```bash
python3 RÉENTRAÎNEMENT_COUCHE_W_AVEC_CONTRAINTE_DE_DIVERSITÉ_FAMILIALE.py
```

**What this script does:**
- Loads existing W weights (or initializes randomly)
- Trains the W layer with **family diversity constraint** (6 families of 12 pentads)
- Exports optimized weights to `couche_hybride_W_poids.json`

**Generated outputs:**
| File | Description |
|------|-------------|
| `couche_hybride_W_poids.json` | W matrix weights (72×10) |
| `couche_W_diversite_meilleur.pth` | PyTorch weights (intermediate backup) |

**Target metrics (v4.7):**
```
✅ Frobenius Norm: ~3.6978 (target: √72 ≈ 8.485)
✅ Conditioning: < 20 (target: 18.7)
✅ Diversity Ratio: > 0.94 (target: 0.9499)
✅ Family Activation: 6/6 (all families activated)
```

---

### STEP 2: Run MODULE 6 v4.7 Simulation

```bash
python3 MODULE_6_v4.7_Version_Mathematique.py
```

**What this script does:**
- Loads W weights generated in Step 1
- Simulates 35 generations of pentadic cells
- Integrates: Signal + Memory (86 units) + Transducer (~1000 units)
- Exports results and a complete report

**Generated outputs:**
| File | Description |
|------|-------------|
| `module_6_v4.7_resultats.json` | Complete simulation results |
| `module_6_v4.7_rapport.txt` | Readable text report |

**Validation metrics:**
```
✅ Total pentadic diversity: 55/72 activated
✅ Average family diversity: > 4 families activated
✅ Memory-Transducer coupling: > 0.15
✅ Output transfer rate: > 80%
✅ 0% divergence over 1000 runs
```

---

## 📊 Configuration Parameters

### In `RÉENTRAÎNEMENT_COUCHE_W_...py`

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `n_epochs` | 2000 | Number of training epochs |
| `lr` | 0.001 | Learning rate |
| `batch_size` | 64 | Mini-batch size |
| `diversite_penalty_weight` | 1.0 | Diversity penalty weight |

### In `MODULE_6_v4.7_...py`

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `n_cellules` | 100 | Number of simulated cells |
| `n_generations` | 35 | Number of generations (cycles) |
| `cycle_modele_iterations` | 35 | Model cycle duration |
| `n_pentades` | 10 | Pentades activated per cell |
| `n_familles_min` | 4 | Minimum number of activated families |

---

## 🔍 Results Verification

### After Training (Step 1)

```bash
# Verify JSON file was created
ls -lh couche_hybride_W_poids.json

# Verify JSON structure
python3 -c "import json; d=json.load(open('couche_hybride_W_poids.json')); print('Keys:', list(d.keys())); print('W Shape:', np.array(d['W']).shape)"
```

### After Simulation (Step 2)

```bash
# Verify output files
ls -lh module_6_v4.7_*.json module_6_v4.7_*.txt

# Display results summary
python3 -c "import json; d=json.load(open('module_6_v4.7_resultats.json')); print('Diversity:', d['diversite_pentadique_totale'], '/72'); print('Families:', d['familles_totales_actives'])"
```

---

## ⚠️ Important Notes

### 1. Execution Order

**Always execute in this order:**
```
1. RÉENTRAÎNEMENT_COUCHE_W_...py  →  Generates W
2. MODULE_6_v4.7_...py            →  Uses W
```

If you run MODULE 6 without generating W first, the script will use a **random initialization** (non-optimal).

---

### 2. Reproducibility

Both scripts use **fixed seeds** to ensure reproducibility:

```python
# In both scripts
torch.manual_seed(42)
np.random.seed(42)
```

For reproducible results to 10⁻⁸ precision, **do not modify the seeds**.

---

### 3. Epistemological Distinction

> **Important:** This code implements a **mathematical and computational model**. Physical interpretations (detection, quantum memory, transducer) remain **modeling hypotheses** not experimentally validated.

**Validation levels:**
| Level | Status | Requirement |
|-------|--------|-------------|
| Mathematical | ✅ Proven (calculation) | Internal consistency verified |
| Algorithmic | ✅ Proven (simulation) | Numerical reproducibility |
| Physical | ⚠️ Hypothesis (unvalidated) | Experimental validation required |

---

## 🐛 Troubleshooting

### Problem: `FileNotFoundError: couche_hybride_W_poids.json`

**Cause:** You ran MODULE 6 without generating W weights first.

**Solution:**
```bash
# Run training first
python3 RÉENTRAÎNEMENT_COUCHE_W_AVEC_CONTRAINTE_DE_DIVERSITÉ_FAMILIALE.py

# Then simulation
python3 MODULE_6_v4.7_Version_Mathematique.py
```

---

### Problem: `Family Diversity < 4`

**Cause:** W weights are not sufficiently optimized for diversity.

**Solution:**
```bash
# Increase training epochs
# In RÉENTRAÎNEMENT_COUCHE_W_...py, modify:
n_epochs = 3000  # Instead of 2000

# Or increase diversity weight
diversite_penalty_weight = 1.5  # Instead of 1.0
```

---

### Problem: `Divergence > 0%`

**Cause:** W conditioning too high (> 20).

**Solution:**
```bash
# Verify conditioning after training
python3 -c "import json; import numpy as np; d=json.load(open('couche_hybride_W_poids.json')); W=np.array(d['W']); print('Conditioning:', np.linalg.cond(W))"

# If > 20, retrain with more regularization
rang_penalty_weight = 0.2  # Instead of 0.1
```

---

## 📈 Expected Performance

### Execution Time

| Script | CPU (8 cores) | GPU (Optional) |
|--------|---------------|----------------|
| W Training | ~10-15 min | ~5-8 min |
| MODULE 6 Simulation | ~2-5 min | N/A (CPU sufficient) |

### RAM Memory

| Script | Minimum | Recommended |
|--------|---------|-------------|
| W Training | 4 GB | 8 GB |
| MODULE 6 Simulation | 2 GB | 4 GB |

---

## 📄 License

All scripts are distributed under **CC BY 4.0 / MIT** license.

**Required attribution:**
```
De Dominicis, B. (2026). Hybrid W Layer: Cl(6,6) → Nebe 72D Projection.
GitHub: https://github.com/bruno-dd470/Tian-Dao_WuXing_Clifford
```

---

## 🔗 References

| Document | Link |
|----------|------|
| Mathematical specifications | `docs/PUBLICATION_1_Théorie_Pentadique.pdf` |
| W Layer Architecture | `docs/Couche_Hybride_W_Specifications.pdf` |
| Validation results | `results/cross_validation/` |
| Optimized W weights | `weights/couche_hybride_W_poids.json` |

---

## 📬 Contact & Contributions

- **GitHub Issues:** https://github.com/bruno-dd470/Tian-Dao_WuXing_Clifford/issues
- **Email:** dod60@gmx.fr
- **License:** CC BY 4.0

**Contributions encouraged:**
- ✅ Independent validation of results
- ✅ Algorithmic optimizations
- ✅ Theoretical extensions (other Clifford algebras)
- ✅ Documentation and translations

---

**Last updated:** March 2026  
**Script version:** v4.7  
**Status:** ✅ Stable and validated
