# Présentation des modules Python du projet Tian-Dao_WuXing_Clifford

## Introduction

Le projet **Tian-Dao_WuXing_Clifford** repose sur une architecture modulaire en Python, où chaque module remplit une fonction spécifique dans la chaîne de traitement allant de la construction des pentades à la visualisation 3D du réseau, en passant par l'analyse de données expérimentales (EHT) et l'interface utilisateur. Les modules sont conçus pour être indépendants mais interconnectés, partageant des structures de données communes (fichiers JSON, vecteurs numpy). L'ensemble est disponible dans le dépôt GitHub sous `code/python/`.

Les modules couvrent les aspects suivants :

1. **Module 1** : Construction des 72 pentades.
2. **Module 1b** : Entraînement (ou réentraînement) de la couche W avec contrainte de diversité familiale.
3. **Module 2** : Action de PSL₂(7) sur les 7 générateurs.
4. **Module 3** : Action de SL₂(25) sur les 24 pentades Yang.
5. **Module 4** : Vérification du produit tensoriel Barnes ⊗ Leech.
6. **Module 5** : Calcul des vecteurs minimaux du réseau de Nebe.
7. **Module 6** : Architecture complète (Signal + Mémoire + Transducteur) – cycle modèle 35 itérations.
8. **Module 7** : Visualisation 3D du réseau Γ.
9. **Module 8** : Interface graphique utilisateur.

Chaque module peut être exécuté indépendamment (avec `python3 module_x.py`), mais ils s'appuient souvent sur les fichiers produits par les précédents (notamment `pentades_72_finales.json`). La section suivante détaille chacun d'eux.

---

## Module 1 : Construction des 72 pentades  
**Fichier** : `MODULE_1_72_pentades.py`

Ce module est le point de départ. Il implémente la construction systématique des 72 pentades à partir des règles de Rowlands étendues.  
- **Fonctionnalités** :
  - Définition d'une classe `Pentade` avec attributs : structure (3 bivecteurs), feu, eau, signe, famille.
  - Construction des 6 familles (I à VI), chacune avec 6 structures de base × 2 signes → 12 pentades par famille, soit 72 au total.
  - Validation automatique : chaque pentade doit contenir les 6 générateurs `{i,j,k,I,J,K}`.
  - Tests intégrés : comptage, équilibre Yang/Yin, répartition par famille.
  - Export au format JSON (`pentades_72_finales.json`) pour les modules suivants.
- **Exemple de sortie** :
  ```json
  {
    "famille": "FI",
    "signe": 1,
    "structure": ["iI", "iJ", "iK"],
    "feu": "i'k",
    "eau": "1j",
    "elements": ["iI", "iJ", "iK", "i'k", "1j"],
    "generateurs": ["I", "J", "K", "i", "j", "k"]
  }
  ```

---

## Module 1b : Entraînement de la couche W avec contrainte de diversité familiale  
**Fichier** : `MODULE_1b_TRAIN_W_DIVERSITE.py`

Ce module construit ou affine les poids de la **couche hybride W** qui projette linéairement l’espace Cl(6,6) (10 dimensions) vers l’espace des 72 pentades. Il utilise une régularisation originale pour forcer l’activation équilibrée des six familles de pentades (FI à FVI).

- **Fonctionnalités** :
  - Chargement des pentades (`pentades_72_finales.json`) pour définir une cible physique.
  - Recherche d’un fichier `couche_hybride_W_poids.json` existant :
    - **Si le fichier existe** : chargement des poids, ajout d’un faible bruit, puis **réentraînement** avec la nouvelle pénalité de diversité.
    - **Si le fichier n’existe pas** : initialisation aléatoire orthogonale et **premier entraînement**.
  - Pénalités de régularisation :
    - **Orthogonalité** : `W^T·W ≈ I_10`
    - **Norme** : `||W||_F ≈ √72`
    - **Rang** : préserver les 10 valeurs singulières au‑dessus de 0.1
    - **Diversité familiale** : minimiser la variance des activations moyennes entre les six blocs de 12 pentades.
  - Génération de données synthétiques (vecteurs aléatoires 10D) et optimisation par Adam.
  - Early stopping basé sur le ratio de diversité (activation minimale / maximale).
  - Sauvegarde des meilleurs poids et export final vers `couche_hybride_W_poids.json`.
  - Affichage des statistiques : norme, conditionnement, valeurs singulières, activations par famille, ratio de diversité.

- **Position dans la chaîne** : à exécuter **après** le Module 1 (car il a besoin du fichier JSON des pentades) et **avant** tout module qui utiliserait ces poids (notamment le Module 6).

- **Exemple d’exécution** :
  ```bash
  python3 MODULE_1b_TRAIN_W_DIVERSITE.py
  ```

- **Dépendances** : PyTorch (`torch`), NumPy, JSON.

---

## Module 2 : Action de PSL₂(7) sur les 7 générateurs  
**Fichier** : `MODULE_2_ACTION_DE_PSL27_SUR_LES_7_GÉNÉRATEURS.py`

Ce module implémente le groupe $\text{PSL}_2(7)$ (ordre 168) et son action sur les 7 générateurs de base : $i,j,k,I,J,K,i'$.  
- **Fonctionnalités** :
  - Représentation des 7 générateurs via une classe `Generateurs7`.
  - Définition des matrices génératrices de $\text{PSL}_2(7)$ (S, T, U).
  - Calcul de l'action projective sur les points 0…6 (les générateurs).
  - Génération de tables de permutation pour chaque générateur.
  - Application de ces permutations aux pentades (simplification automatique des expressions comme `i''` → `i'`).
  - Lien avec la géométrie du plan de Fano (les 7 droites).
- **Utilisation** : Vérifie que l'action du groupe respecte la structure pentadique et prépare les symétries pour la construction du réseau de Leech (module 3).

---

## Module 3 : Action de SL₂(25) sur les 24 pentades Yang  
**Fichier** : `MODULE_3_ACTION_DE_SL₂25_SUR_LES_24_PENTADES_YANG.py`

Ce module traite du groupe $\text{SL}_2(25)$ (ordre 14400) et de son action sur les 24 pentades de signe Yang (celles qui formeront le réseau de Leech).  
- **Fonctionnalités** :
  - Implémentation simplifiée du corps fini $\mathbb{F}_{25}$ (via une extension quadratique de $\mathbb{F}_5$).
  - Définition des matrices génératrices de $\text{SL}_2(25)$.
  - Action sur les 25 points de $\mathbb{P}^1(25)$ (24 points finis + point à l'infini).
  - Mapping entre ces points et les 24 pentades Yang.
  - Calcul des permutations induites sur les pentades.
  - Mise en évidence des éventuels conflits (non‑bijectivité).
- **Connexion** : Ce module, couplé au module 2, permet de construire le groupe d'automorphismes complet $(\text{PSL}_2(7) \times \text{SL}_2(25)):2$ du réseau de Nebe.

---

## Module 4 : Vérification du produit tensoriel Barnes ⊗ Leech  
**Fichier** : `MODULE_4_VÉRIFICATION_EXPLICITE_DU_PRODUIT_TENSORIEL.py`

Ce module recrée explicitement le produit tensoriel hermitien qui définit le réseau de Nebe $\Gamma = \text{Barnes} \otimes_{\mathbb{Z}[\sqrt{-7}]} \text{Leech}$.  
- **Fonctionnalités** :
  - Classe `BarnesLattice` : représente le réseau de Barnes (3D sur $\mathbb{Z}[\sqrt{-7}]$) via ses vecteurs de base.
  - Classe `LeechLattice` : construit une approximation du réseau de Leech à partir des 24 pentades Yang chargées depuis le fichier JSON.
  - Calcul du produit tensoriel $v \otimes w$ (vecteur de dimension 72) et de sa norme $||v \otimes w||^2 = ||v||^2 \times ||w||^2$.
  - Génération d'un échantillon de vecteurs et vérification que le minimum est proche de 8 (norme cible de Nebe).
  - Affichage des statistiques et de la factorisation des normes.
- **Résultat** : confirme que la construction produit bien une dimension 72 et un minimum cohérent avec les propriétés attendues.

---

## Module 5 : Calcul des vecteurs minimaux du réseau de Nebe  
**Fichier** : `MODULE_5_CALCUL_DES_VECTEURS_MINIMAUX.py`

Ce module ne cherche pas à calculer les $6{,}218\times10^9$ vecteurs (impossible directement), mais propose une analyse combinatoire et des estimations Monte Carlo pour comprendre la structure du nombre.  
- **Fonctionnalités** :
  - Analyse de la factorisation du nombre de kissing : $6\,218\,175\,600 = 2^4 \times 3^2 \times 5 \times 7 \times 13 \times 31 \times 72$ ? (détail des calculs).
  - Calcul du rapport avec l'ordre du groupe d'automorphismes.
  - Estimation Monte Carlo sur un échantillon de vecteurs aléatoires pour estimer la densité de vecteurs de norme 8.
  - Simulation de vecteurs de norme 8 et vérification de leurs propriétés (orthogonalité, distribution).
  - Visualisation sommaire des résultats (histogramme).
- **Note** : Ce module montre pourquoi le nombre exact est une propriété mathématique profonde, inaccessible par simple tirage aléatoire.

---

## Module 6 : Architecture complète (Signal + Mémoire + Transducteur) – cycle modèle 35 itérations  
**Fichier** : `MODULE_6_ARCHITECTURE_COMPLETE_v4.7.py`

Ce module implémente une simulation unifiée intégrant :
- **Signal d’entrée** : interface de détection collective avec cohérence quantique, verrouillage de phase.
- **Mémoire** : 86 unités de décodage (basées sur l’élément Z=36, krypton), niveaux d’énergie électroniques, électrons de valence, capacité de stockage.
- **Transducteur** : environ 1000 unités (Z=2, hélium) avec état métastable à longue durée de vie, résonance à 1.42 GHz.
- **Réseau couplé Mémoire‑Transducteur** : associations systématiques, calcul du couplage, transfert d’information.
- **Algèbre de Clifford Cl(6,6)** et projection via la couche W (normalisée avec diversité familiale 0.9499).
- **Modèle bimétrique** : pression système, gradient d’information.
- **Cycle modèle** : 35 itérations (référence biologique).

- **Fonctionnalités** :
  - Chargement automatique de la matrice W (depuis `couche_hybride_W_poids.json`, sinon aléatoire).
  - Initialisation de 100 cellules, chacune contenant une interface signal, un réseau mémoire‑transducteur, un encodeur patchwork.
  - À chaque génération, calcul de la pression système, verrouillage de phase, projection des vecteurs 10D → 72 pentades, décodage avec contrainte de diversité (au moins 4 familles).
  - Simulation du transfert d’information entre mémoire et transducteur, puis vers la sortie système.
  - Collecte des statistiques : SNR effectif, diversité pentadique, diversité familiale, couplage moyen, taux de transfert.
  - Export des résultats dans `module_6_v4.7_resultats.json` et d’un rapport textuel.

- **Position dans la chaîne** : doit être exécuté **après** le Module 1b (pour disposer de la couche W optimisée) ; indépendant des modules 2 à 5.

- **Exemple d’exécution** :
  ```bash
  python3 MODULE_6_ARCHITECTURE_COMPLETE_v4.7.py
  ```

- **Dépendances** : NumPy, JSON, dataclasses, collections, pathlib.

- **Résultats typiques** (extrait du rapport) :
  ```
  SNR moyen final : -215.3 dB
  Gain système : 2.8×
  Diversité pentadique moyenne : 8.7 / 10
  Diversité familiale moyenne : 5.2 / 6
  Couplage moyen : 0.68
  Transfert vers sortie : 73%
  ```

---

## Module 7 : Visualisation 3D du réseau Γ  
**Fichier** : `MODULE_7_VISUALISATION_3D_DU_RÉSEAU_Γ.py`

Ce module produit une représentation 3D artistique du réseau de 72 pentades.  
- **Fonctionnalités** :
  - Génération de positions 3D pour chaque pentade en combinant une distribution sur sphère (Fibonacci) et sur tore, avec un mélange dépendant de la famille.
  - Ajout de connexions entre pentades proches (distance < 2.5), colorées selon qu'elles sont intra‑ ou inter‑famille.
  - Annotation des objets analysés (M87, etc.) avec leur type et tension.
  - Sauvegarde de la figure au format PNG et affichage interactif.
- **Rendu** : permet de visualiser la structure relationnelle du réseau, avec des clusters correspondant aux familles.

---

## Module 8 : Interface utilisateur pour le système pentadique  
**Fichier** : `MODULE_8_INTERFACE_UTILISATEUR_POUR_LE_SYSTÈME_PENTADIQUE.py`

C'est le module d'entrée principal pour les utilisateurs non‑programmeurs. Il propose une interface graphique (Tkinter) intégrant l'ensemble des fonctionnalités.  
- **Fonctionnalités** :
  - Menu complet : Fichier (charger données EHT, pentades, résultats), Analyse (lancer les modules 1…7), Visualisation (graphiques, radar, 3D), Aide (documentation).
  - Panneau d'état des modules (présence/absence).
  - Zone de texte pour afficher les logs et résultats.
  - Liste des fichiers chargés et des résultats d'analyse.
  - Barre de progression pendant les calculs longs.
  - Intégration de la documentation (fichier `DOCUMENTATION.md` dans une fenêtre dédiée).
- **Usage** : Lancement simple par `python3 MODULE_8_...`. L'interface permet de découvrir le système sans écrire de code.

---

## Relations entre modules

- **Module 1** produit `pentades_72_finales.json` utilisé par tous les modules suivants (y compris 1b).
- **Module 1b** utilise `pentades_72_finales.json` pour construire ou affiner `couche_hybride_W_poids.json`. Il doit être exécuté après le Module 1 et avant le Module 6.
- **Modules 2, 3, 4, 5** sont indépendants des poids W (ils travaillent sur les pentades et les groupes).
- **Module 6** utilise la couche W produite par le Module 1b (ou en crée une par défaut). Il ne dépend pas des modules 2‑5.
- **Module 7** utilise les pentades et les positions calculées pour la visualisation.
- **Module 8** peut appeler les autres modules (via `subprocess`) ou importer leurs fonctions.

---

## Utilisation et dépendances

Chaque module nécessite Python 3 avec les bibliothèques suivantes :
- `numpy` (calculs matriciels)
- `matplotlib` (graphiques 2D et 3D)
- `scipy` (éventuellement pour quelques calculs)
- `tkinter` (inclus avec Python, pour le module 8)
- `torch` (pour le module 1b)
- `json`, `os`, `sys`, `glob`, `itertools`, `time`, `dataclasses`, `enum`, `collections` (modules standards)

Installation rapide :
```bash
pip install numpy matplotlib scipy torch
```

Exécution typique (depuis le dossier `code/python/`) :
```bash
python3 MODULE_1_72_pentades.py
python3 MODULE_1b_TRAIN_W_DIVERSITE.py          # entraînement/réentraînement de la couche W
python3 MODULE_2_ACTION_DE_PSL27_SUR_LES_7_GÉNÉRATEURS.py
python3 MODULE_3_ACTION_DE_SL₂25_SUR_LES_24_PENTADES_YANG.py
python3 MODULE_4_VÉRIFICATION_EXPLICITE_DU_PRODUIT_TENSORIEL.py
python3 MODULE_5_CALCUL_DES_VECTEURS_MINIMAUX.py
python3 MODULE_6_ARCHITECTURE_COMPLETE_v4.7.py  # simulation unifiée
python3 MODULE_7_VISUALISATION_3D_DU_RÉSEAU_Γ.py
python3 MODULE_8_INTERFACE_UTILISATEUR_POUR_LE_SYSTÈME_PENTADIQUE.py
```

---

## Conclusion

Les modules forment une boîte à outils complète pour explorer, valider et visualiser la théorie pentadique. Ils couvrent la chaîne allant de la construction algébrique à l’analyse de systèmes complexes (signal, mémoire, transducteur), en passant par la théorie des groupes, l’apprentissage automatique (entraînement de la couche W) et la visualisation 3D. Leur conception modulaire facilite la maintenance, les tests et l'extension future. L'interface graphique (module 8) rend le système accessible à un public plus large, tandis que les modules spécialisés permettent des investigations approfondies.

**Prochaines étapes** :
- Améliorer la documentation interne (docstrings).
- Ajouter des tests unitaires pour chaque module.
- Intégrer plus étroitement les modules 2, 3, 4 avec le module 1b pour une optimisation conjointe.
- Développer une version en ligne avec Jupyter notebooks.

Pour toute question ou contribution, rendez-vous sur le dépôt GitHub.
```

Ce README est prêt à être copié dans votre fichier `README.md`. Il reflète exactement le nouveau Module 6 v4.7 et conserve l’ordre logique (module 1b avant module 6).
