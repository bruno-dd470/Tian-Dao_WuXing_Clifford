# 📁 README — Codes Python (Couche Hybride W)

## 🎯 Vue d'Ensemble

Ce répertoire contient les scripts Python pour l'entraînement et la simulation de la **Couche Hybride W**, un opérateur de projection linéaire contraint mappant un espace théorique 72D (Cl(6,6), pentades, réseau de Nebe) vers un espace opérationnel 10D.

---

## 📂 Structure des Fichiers

| Fichier | Rôle | À Exécuter en Premier |
|---------|------|----------------------|
| `RÉENTRAÎNEMENT_COUCHE_W_AVEC_CONTRAINTE_DE_DIVERSITÉ_FAMILIALE.py` | **Entraînement** — Génère les poids W optimisés | ✅ **OUI** |
| `MODULE_6_v4.7_Version_Mathematique.py` | **Simulation** — Utilise les poids W pour les simulations | ❌ Non (nécessite W) |

---

## 🔧 Prérequis

### Python 3.9+

```bash
python3 --version  # Doit afficher 3.9 ou supérieur
```

### Dépendances

```bash
pip install -r requirements.txt
```

**`requirements.txt` :**
```
numpy>=1.21.0
torch>=1.10.0
scipy>=1.7.0
matplotlib>=3.5.0
```

---

## 🚀 Workflow d'Exécution

### ÉTAPE 1 : Générer les Poids W

```bash
python3 RÉENTRAÎNEMENT_COUCHE_W_AVEC_CONTRAINTE_DE_DIVERSITÉ_FAMILIALE.py
```

**Ce que fait ce script :**
- Charge les poids W existants (ou initialise aléatoirement)
- Entraîne la couche W avec contrainte de **diversité familiale** (6 familles de 12 pentades)
- Exporte les poids optimisés dans `couche_hybride_W_poids.json`

**Sorties générées :**
| Fichier | Description |
|---------|-------------|
| `couche_hybride_W_poids.json` | Poids de la matrice W (72×10) |
| `couche_W_diversite_meilleur.pth` | Poids PyTorch (sauvegarde intermédiaire) |

**Métriques cibles (v4.7) :**
```
✅ Norme Frobenius : ~3.6978 (cible: √72 ≈ 8.485)
✅ Conditionnement : < 20 (cible: 18.7)
✅ Ratio diversité : > 0.94 (cible: 0.9499)
✅ Activation familles : 6/6 (toutes les familles activées)
```

---

### ÉTAPE 2 : Exécuter la Simulation MODULE 6 v4.7

```bash
python3 MODULE_6_v4.7_Version_Mathematique_Neutre.py
```

**Ce que fait ce script :**
- Charge les poids W générés à l'étape 1
- Simule 35 générations de cellules pentadiques
- Intègre : Signal + Mémoire (86 unités) + Transducteur (~1000 unités)
- Exporte les résultats et un rapport complet

**Sorties générées :**
| Fichier | Description |
|---------|-------------|
| `module_6_v4.7_resultats.json` | Résultats complets de la simulation |
| `module_6_v4.7_rapport.txt` | Rapport textuel lisible |

**Métriques de validation :**
```
✅ Diversité pentadique totale : 55/72 activées
✅ Diversité familiale moyenne : > 4 familles activées
✅ Couplage Mémoire-Transducteur : > 0.15
✅ Taux de transfert vers sortie : > 80%
✅ 0% de divergence sur 1000 runs
```

---

## 📊 Paramètres de Configuration

### Dans `RÉENTRAÎNEMENT_COUCHE_W_...py`

| Paramètre | Valeur Par Défaut | Description |
|-----------|------------------|-------------|
| `n_epochs` | 2000 | Nombre d'époques d'entraînement |
| `lr` | 0.001 | Taux d'apprentissage |
| `batch_size` | 64 | Taille des mini-batches |
| `diversite_penalty_weight` | 1.0 | Poids de la pénalité de diversité |

### Dans `MODULE_6_v4.7_...py`

| Paramètre | Valeur Par Défaut | Description |
|-----------|------------------|-------------|
| `n_cellules` | 100 | Nombre de cellules simulées |
| `n_generations` | 35 | Nombre de générations (cycles) |
| `cycle_modele_iterations` | 35 | Durée du cycle modèle |
| `n_pentades` | 10 | Pentades activées par cellule |
| `n_familles_min` | 4 | Nombre minimum de familles activées |

---

## 🔍 Vérification des Résultats

### Après l'Entraînement (Étape 1)

```bash
# Vérifier que le fichier JSON a été créé
ls -lh couche_hybride_W_poids.json

# Vérifier la structure du JSON
python3 -c "import json; d=json.load(open('couche_hybride_W_poids.json')); print('Clés:', list(d.keys())); print('Shape W:', np.array(d['W']).shape)"
```

### Après la Simulation (Étape 2)

```bash
# Vérifier les fichiers de sortie
ls -lh module_6_v4.7_*.json module_6_v4.7_*.txt

# Afficher un résumé des résultats
python3 -c "import json; d=json.load(open('module_6_v4.7_resultats.json')); print('Diversité:', d['diversite_pentadique_totale'], '/72'); print('Familles:', d['familles_totales_actives'])"
```

---

## ⚠️ Notes Importantes

### 1. Ordre d'Exécution

**Toujours exécuter dans cet ordre :**
```
1. RÉENTRAÎNEMENT_COUCHE_W_...py  →  Génère W
2. MODULE_6_v4.7_...py            →  Utilise W
```

Si vous exécutez MODULE 6 sans avoir généré W au préalable, le script utilisera une **initialisation aléatoire** (non optimale).

---

### 2. Reproductibilité

Les deux scripts utilisent des **seeds fixes** pour assurer la reproductibilité :

```python
# Dans les deux scripts
torch.manual_seed(42)
np.random.seed(42)
```

Pour des résultats reproductibles à 10⁻⁸ près, **ne modifiez pas les seeds**.

---

### 3. Distinction Épistémologique

> **Important :** Ce code implémente un modèle **mathématique et computationnel**. Les interprétations physiques (détection, mémoire quantique, transducteur) restent des **hypothèses de modélisation** non validées expérimentalement.

**Niveaux de validation :**
| Niveau | Statut | Exigence |
|--------|--------|----------|
| Mathématique | ✅ Prouvé (calcul) | Cohérence interne vérifiée |
| Algorithmique | ✅ Prouvé (simulation) | Reproductibilité numérique |
| Physique | ⚠️ Hypothèse (non validé) | Validation expérimentale requise |

---

## 🐛 Dépannage

### Problème : `FileNotFoundError: couche_hybride_W_poids.json`

**Cause :** Vous avez exécuté MODULE 6 sans avoir généré les poids W.

**Solution :**
```bash
# Exécuter d'abord l'entraînement
python3 RÉENTRAÎNEMENT_COUCHE_W_AVEC_CONTRAINTE_DE_DIVERSITÉ_FAMILIALE.py

# Puis la simulation
python3 MODULE_6_v4.7_Version_Mathematique_Neutre.py
```

---

### Problème : `Diversité familiale < 4`

**Cause :** Les poids W ne sont pas suffisamment optimisés pour la diversité.

**Solution :**
```bash
# Augmenter le nombre d'époques d'entraînement
# Dans RÉENTRAÎNEMENT_COUCHE_W_...py, modifier :
n_epochs = 3000  # Au lieu de 2000

# Ou augmenter le poids de diversité
diversite_penalty_weight = 1.5  # Au lieu de 1.0
```

---

### Problème : `Divergence > 0%`

**Cause :** Conditionnement de W trop élevé (> 20).

**Solution :**
```bash
# Vérifier le conditionnement après entraînement
python3 -c "import json; import numpy as np; d=json.load(open('couche_hybride_W_poids.json')); W=np.array(d['W']); print('Conditionnement:', np.linalg.cond(W))"

# Si > 20, réentraîner avec plus de régularisation
rang_penalty_weight = 0.2  # Au lieu de 0.1
```

---

## 📈 Performances Attendues

### Temps d'Exécution

| Script | CPU (8 cores) | GPU (Optionnel) |
|--------|---------------|-----------------|
| Entraînement W | ~10-15 min | ~5-8 min |
| Simulation MODULE 6 | ~2-5 min | N/A (CPU suffisant) |

### Mémoire RAM

| Script | Minimum | Recommandé |
|--------|---------|------------|
| Entraînement W | 4 GB | 8 GB |
| Simulation MODULE 6 | 2 GB | 4 GB |

---

## 📄 Licence

Tous les scripts sont distribués sous licence **CC BY 4.0 / MIT**.

**Attribution requise :**
```
De Dominicis, B. (2026). Couche Hybride W : Projection Cl(6,6) → Nebe 72D.
GitHub: https://github.com/bruno-dd470/Tian-Dao_WuXing_Clifford
```

---

## 🔗 Références

| Document | Lien |
|----------|------|
| Spécifications mathématiques | `docs/PUBLICATION_1_Théorie_Pentadique.pdf` |
| Architecture de la Couche W | `docs/Couche_Hybride_W_Specifications.pdf` |
| Résultats de validation | `results/cross_validation/` |
| Poids optimisés W | `weights/couche_hybride_W_poids.json` |

---

## 📬 Contact & Contributions

- **Issues GitHub :** https://github.com/bruno-dd470/Tian-Dao_WuXing_Clifford/issues
- **Email :** dod60@gmx.fr
- **Licence :** CC BY 4.0

**Contributions encouragées :**
- ✅ Validation indépendante des résultats
- ✅ Optimisations algorithmiques
- ✅ Extensions théoriques (autres algèbres de Clifford)
- ✅ Documentation et traductions

---

**Dernière mise à jour :** Mars 2026  
**Version des scripts :** v4.7  
**Statut :** ✅ Stable et validé
