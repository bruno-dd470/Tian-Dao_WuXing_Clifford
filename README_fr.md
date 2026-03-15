# Tian-Dao_WuXing_Clifford

Ce dépôt contient les sources des articles sur la théorie pentadique et l'algèbre Cl(6,6).

## Compilation des articles

Pour générer un PDF à partir d'un fichier Markdown, utilisez `pandoc` avec le template fourni :

```bash
pandoc article.md --template=templates/tian-dao-article.tex -o article.pdf --pdf-engine=xelatex
```

### Prérequis
- [Pandoc](https://pandoc.org/) (version ≥ 2.10)
- Une distribution LaTeX avec `xelatex` (TeX Live, MikTeX)
- Polices supplémentaires (optionnelles mais recommandées) :
  - Libertinus Serif, Libertinus Mono, Libertinus Math
  - Noto Serif CJK SC (pour le support chinois)

Si les polices ne sont pas installées, vous pouvez les remplacer dans le template par des polices par défaut (ex: `TeX Gyre Termes`).

### Structure du dépôt
- `articles/` : fichiers Markdown des publications
- `templates/` : template LaTeX
- `code/` : scripts Python
- ...

## Compilation des articles

Pour générer les PDF de tous les articles à partir des sources Markdown, utilisez la commande suivante (depuis la racine du dépôt) :

```bash
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

Cette commande parcourt chaque sous-dossier de `articles/` et compile tous les fichiers `.md` en PDF en utilisant le template LaTeX fourni et en cherchant les images dans le dossier `figures/` à la racine.

**Prérequis** : 
- [Pandoc](https://pandoc.org/) (≥ 2.10)
- Une distribution LaTeX avec `xelatex` (TeX Live, MikTeX)
- Polices Libertinus (incluses dans TeX Live)
