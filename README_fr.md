# Tian-Dao_WuXing_Clifford

[English](README.md) | [中文](README_zh.md)

## Philosophie et inspiration

Ce travail révèle que les intuitions des anciens scribes‑devins chinois et de leurs successeurs étaient remarquablement prophétiques lorsqu'ils ont établi le socle dogmatique de l'Empire Céleste sur les 64 hexagrammes du *Yijing* (I Ching) et les cinq éléments générateurs du *Wuxing*.

En effet, dans notre projet, le *Yijing* apparaît comme une préfiguration empirique des 64 éléments de l'algèbre de Clifford Cl(6,0), tandis que le *Wuxing* émerge comme une préfiguration empirique des pentades développées par le physicien britannique Peter Rowlands.

À partir de ces intuitions, nous développons une **physique pentadique** autant dire une **physique du Wuxing** – selon laquelle l'univers est constitué d'une série infinie d'octaves, chacune incluant 72 dimensions organisées en six familles de douze pentades. Le *Wuxing* apparaît ainsi comme constitutif de la substance de l'univers à toutes les échelles.

## Publications

Le projet comprend cinq articles principaux, chacun disponible en anglais et en français.

| Titre (français) | Fichier |
|------------------|---------|
| **1. Le modèle pentadique Cl(6,6) : une unification fondamentale** | [`PUBLICATION_1_Théorie_Pentadique.md`](articles/PUBLICATION_1_Théorie_Pentadique/PUBLICATION_1_Théorie_Pentadique.md) |
| **2. Validation expérimentale du réseau 72-dimensionnel de Nebe par l'effet Zeeman** | [`PUBLICATION_2_Effet_Zeeman.md`](articles/PUBLICATION_2_Effet_Zeeman/PUBLICATION_2_Effet_Zeeman.md) |
| **3. Découverte d'une résonance gamma à 200 MeV dans le magnétar 1E 1048.1‑5937** | [`PUBLICATION_3_Magnetars.md`](articles/PUBLICATION_3_Magnetars/PUBLICATION_3_Magnetars.md) |
| **4. Unification cosmologique par les systèmes pentadiques et l'algèbre de Clifford Cl(6,6)** | [`PUBLICATION_4_RAPPORT_DE_SYNTHÈSE.md`](articles/PUBLICATION_4_Rapport_de_Synthese/PUBLICATION_4_RAPPORT_DE_SYNTHÈSE.md) |
| **5. Transitions angulaires entre particules – Une réinterprétation géométrique** | [`PUBLICATION_5_TRANSITIONS_PENTADIQUES.md`](articles/PUBLICATION_5_Transitions_Pentadiques/PUBLICATION_5_TRANSITIONS_PENTADIQUES.md) |
| **6. Prédictions du Modèle Pentadique Cl(6,6) : Validation Numérique et Signatures Astrophysiques** | [`PUBLICATION_6_Consolidé.md`](articles/PUBLICATION_6_Zeeman_consolidé/PUBLICATION_6_Consolidé.md) |

Les PDF et les fichiers Markdown se trouvent dans les mêmes dossiers. Chaque article peut être compilé en PDF à l'aide de Pandoc avec le modèle LaTeX fourni (voir [Compilation des articles](#compilation-des-articles)).

## Structure du dépôt

- `articles/` : fichiers Markdown des publications (chacun dans son propre sous-dossier)
- `code/` : scripts Python (voir ci-dessous)
- `data/` : fichiers de données (JSON, FITS, tableaux numpy)
- `docs/` : documentation supplémentaire
- `drafts/` : documents de travail (ODT, DOCX)
- `figures/` : images et figures
- `reports/` : rapports textes
- `references/` : références PDF
- `templates/` : modèle LaTeX
- `requirements.txt` : dépendances Python (pip)
- `environment.yml` : fichier d'environnement Conda

## Scripts Python

Le répertoire `code/` contient tous les scripts Python développés pour ce projet. Ils sont organisés en deux sous-répertoires principaux :

- **`code/pentadic/`** – modules fondamentaux implémentant l'algèbre pentadique : construction des 72 pentades, actions de groupes (PSL₂(7), SL₂(25)), vérification du produit tensoriel Barnes ⊗ Leech, et une interface graphique utilisateur. Voir le `README.md` pour une documentation complète.
- **`code/zeeman/`** – scripts pour l'analyse de l'effet Zeeman, le traitement des données Fermi‑LAT des magnétars, les études de périodicité de Bott et la validation croisée du modèle pentadique. Voir le `README.md` pour des descriptions détaillées.

Tous les scripts sont écrits en Python 3.8+ et reposent sur des bibliothèques scientifiques standard. Les paquets requis sont listés dans `requirements.txt` (pip) et `environment.yml` (Conda).

## Installation des dépendances

Vous avez deux options pour installer les paquets Python nécessaires :

### Option 1 : Utilisation de pip (installation minimale)

```
pip install -r requirements.txt
```

Ceci installe les paquets disponibles sur PyPI. Notez que `fermipy` n'est pas inclus dans cette liste car il nécessite conda ; si vous devez exécuter l'analyse Fermi‑LAT, utilisez plutôt l'environnement conda.

### Option 2 : Utilisation de conda (environnement complet)

Créez l'environnement `pentadic` avec toutes les dépendances (y compris `fermipy` et les outils de visualisation 3D optionnels) :

```
conda env create -f environment.yml
conda activate pentadic
```

Après installation, vous pouvez exécuter n'importe quel script en ligne de commande, par exemple :

```
python code/zeeman/ZEEMAN-PENTADIC-ANALYSIS_v1.0.py
```

## Remarques

- Les scripts Python génèrent des figures et des rapports dans le répertoire de travail courant. Les fichiers de sortie sont sauvegardés avec des noms explicites (par exemple `preuve_dimension_72_math.png`, `pentadic_predictions_report.txt`).
- Certains scripts (notamment l'analyse Fermi‑LAT) peuvent nécessiter une connexion Internet pour télécharger les données et peuvent être longs à s'exécuter.
- Pour plus de détails sur le contexte mathématique et l'interprétation des résultats, reportez-vous aux articles correspondants dans le dossier `articles/` et aux fichiers README dans chaque sous-répertoire.

## Compilation des articles Markdown

Pour générer un PDF à partir d'un fichier Markdown, utilisez `pandoc` avec le modèle fourni :

```
pandoc article.md --template=../../templates/tian-dao-article.tex --listings --citeproc --toc -o article.pdf --pdf-engine=xelatex
```

### Prérequis

- Pandoc (version ≥ 2.10)
- Une distribution LaTeX avec `xelatex` (TeX Live, MikTeX)
- Polices supplémentaires (optionnelles mais recommandées) :
  - Libertinus Serif, Libertinus Mono, Libertinus Math
  - Noto Serif CJK SC (pour le support du chinois)

Si les polices ne sont pas installées, vous pouvez les remplacer dans le modèle par des polices par défaut (par exemple TeX Gyre Termes).

### Compilation par lots

Pour générer les PDF de tous les articles à partir des sources Markdown, exécutez la commande suivante depuis la racine du dépôt :

```
for d in articles/*/; do
    (cd "$d" && for f in *.md; do
        pandoc "$f" \
            --template=../../templates/tian-dao-article.tex \
            --resource-path=".:../.." \
            -o "${f%.md}.pdf" \
            --pdf-engine=xelatex
    done)
done
```

Cette commande parcourt chaque sous-dossier de `articles/` et compile chaque fichier `.md` en PDF en utilisant le modèle LaTeX fourni, avec les images recherchées dans le dossier `figures/` à la racine.

### Dépendances :

- Pandoc (≥ 2.10)
- Une distribution LaTeX avec xelatex (TeX Live, MikTeX)
- Polices Libertinus (incluses dans TeX Live)

## Licence

Ce projet est sous licence MIT – voir le fichier [LICENSE](LICENSE) pour plus de détails.
