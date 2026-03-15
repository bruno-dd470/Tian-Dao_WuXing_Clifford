# Tian-Dao_WuXing_Clifford

This repository contains the source files for a series of articles on the pentadic theory and Clifford algebra Cl(6,6).

## Compiling the articles

To generate a PDF from a Markdown file, use `pandoc` with the provided template:

```bash
pandoc article.md --template=templates/tian-dao-article.tex -o article.pdf --pdf-engine=xelatex
```

### Prerequisites
- Pandoc (version ≥ 2.10)
- A LaTeX distribution with xelatex (TeX Live, MikTeX)
- Additional fonts (optional but recommended):
- Libertinus Serif, Libertinus Mono, Libertinus Math
- Noto Serif CJK SC (for Chinese support)

If the fonts are not installed, you can replace them in the template with default fonts (e.g., TeX Gyre Termes).

### Repository structure
- `articles/` : Markdown files of the publications
- `templates/` : LaTeX template
- `code/` : Python scripts
- `figures/` : Images and figures
- ...

## Batch compilation

To generate PDFs for all articles from the Markdown sources, run the following command from the repository root:

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

This command iterates through each subfolder in articles/ and compiles every .md file to PDF using the provided LaTeX template, with images looked up in the figures/ folder at the root.

**Dependencies:**
- Pandoc (≥ 2.10)
- A LaTeX distribution with xelatex (TeX Live, MikTeX)
- Libertinus fonts (included in TeX Live)

# Project Title
- [English version](README_en.md)
- [Version française](README_fr.md)
