# Tian-Dao_WuXing_Clifford

[Français](README_fr.md) | [中文](README_zh.md)

## Philosophy & Inspiration

This work reveals that the intuitions of the ancient Chinese scribe‑diviners and their successors were remarkably prescient when they established the dogmatic foundations of the Celestial Empire on the 64 hexagrams of the *Yijing* (I Ching) and the five generating elements of the *Wuxing*.

Indeed, within our project the *Yijing* appears as an empirical prefiguration of the 64 elements of Clifford algebra Cl(6,0), while the *Wuxing* emerges as an empirical prefiguration of the pentads developed by the British physicist Peter Rowlands.

Building on these insights, we develop a **pentadic physics** – a physics of the *Wuxing* – according to which the universe consists of an infinite series of octaves, each including 72 dimensions organised into six families of twelve pentads. The *Wuxing* thus appears as constitutive of the substance of the universe at all scales.

## Publications

The project includes five main articles, each available in English (click the title to access). French versions are also available in the same folders.

| Title (English) | File |
|-----------------|------|
| **1. The Cl(6,6) Pentadic Model: A Fundamental Unification** | [`PUBLICATION_1_Pentadic_Theory.md`](articles/PUBLICATION_1_Théorie_Pentadique/PUBLICATION_1_Pentadic_Theory.md) |
| **2. Experimental Validation of Nebe's 72‑Dimensional Network via the Zeeman Effect** | [`PUBLICATION_2_Zeeman_Effect.md`](articles/PUBLICATION_2_Effet_Zeeman/PUBLICATION_2_Zeeman_Effect.md) |
| **3. Discovery of a 200 MeV Gamma Resonance in the Magnetar 1E 1048.1‑5937** | [`PUBLICATION_3_Magnetars_en.md`](articles/PUBLICATION_3_Magnetars/PUBLICATION_3_Magnetars_en.md) |
| **4. Cosmological Unification through Pentadic Systems and Clifford Algebra Cl(6,6)** | [`PUBLICATION_4_UNIFYING_SYNTHESIS.md`](articles/PUBLICATION_4_Rapport_de_Synthese/PUBLICATION_4_UNIFYING_SYNTHESIS.md) |
| **5. Angular Transitions between Particles – A Geometric Reinterpretation** | [`PUBLICATION_5_PENTADIC_TRANSITIONS.md`](articles/PUBLICATION_5_Transitions_Pentadiques/PUBLICATION_5_PENTADIC_TRANSITIONS.md) |
| **6. Pentadic Cl(6,6) Model Predictions for the Zeeman Effect and Astrophysical Signatures** | [`PUBLICATION_6_Consolidated.md`](articles/PUBLICATION_6_Zeeman_consolidé/PUBLICATION_6_Consolidated.pdf) |


Pentadic Cl(6,6) Model Predictions for the Zeeman Effect and Astrophysical Signatures: Consolidated Analysis of Magnetar
Flares with Fermi-LAT

The PDFs and Markdowns are available in the same folders. Each article can be compiled to PDF using Pandoc with the provided LaTeX template (see [Compiling the articles](#compiling-the-articles)).

## Repository structure

- `articles/` : Markdown files of the publications (each in its own subfolder)
- `code/` : Python scripts (see below)
- `data/` : Data files (JSON, FITS, numpy arrays)
- `docs/` : Additional documentation
- `drafts/` : Working documents (ODT, DOCX)
- `figures/` : Images and figures
- `reports/` : Text reports
- `references/` : PDF references
- `templates/` : LaTeX template
- `requirements.txt` : Python dependencies (pip)
- `environment.yml` : Conda environment file

## Python scripts

The `code/` directory contains all Python scripts developed for this project. They are organized into two main subdirectories:

- **`code/pentadic/`** – Core modules implementing the pentadic algebra: construction of the 72 pentads, group actions (PSL₂(7), SL₂(25)), verification of the Barnes ⊗ Leech tensor product, and a graphical user interface. See the `README.md` for full documentation.
- **`code/zeeman/`** – Scripts for Zeeman effect analysis, Fermi‑LAT magnetar data processing, Bott periodicity studies, and cross‑validation of the pentadic model. See the `README.md` for detailed descriptions.

All scripts are written in Python 3.8+ and rely on standard scientific libraries. The required packages are listed in the main `requirements.txt` (pip) and `environment.yml` (Conda).

## Installation of dependencies

You have two options to install the required Python packages:

### Option 1: Using pip (minimal installation)

```
pip install -r requirements.txt
```

This installs packages available on PyPI. Note that fermipy is not included in this list because it requires conda; if you need to run the Fermi‑LAT analysis, use the conda environment instead.

### Option 2: Using conda (full environment)

Create the pentadic environment with all dependencies (including fermipy and optional 3D visualisation tools):

```
conda env create -f environment.yml
conda activate pentadic
```
After installation, you can run any script from the command line, for example:

```
python code/zeeman/ZEEMAN-PENTADIC-ANALYSIS_v1.0.py
```

## Notes

The python scripts generate figures and reports in the current working directory. Output files are saved with descriptive names (e.g., preuve_dimension_72_math.png, pentadic_predictions_report.txt).
Some scripts (especially the Fermi‑LAT analysis) may require an internet connection to download data and can take several hours to complete.
For details on the mathematical background and interpretation of results, refer to the corresponding articles in the articles/ folder and to the README files in each subdirectory.

## Compiling the Markdown articles

To generate a PDF from a Markdown file, use `pandoc` with the provided template:

pandoc article.md --template=../../templates/tian-dao-article.tex --listings --citeproc --toc -o article.pdf --pdf-engine=xelatex

### Prerequisites

- Pandoc (version ≥ 2.10)
- A LaTeX distribution with xelatex (TeX Live, MikTeX)
- Additional fonts (optional but recommended):
- Libertinus Serif, Libertinus Mono, Libertinus Math
- Noto Serif CJK SC (for Chinese support)
- If the fonts are not installed, you can replace them in the template with default fonts (e.g., TeX Gyre Termes).

### Batch compilation

To generate PDFs for all articles from the Markdown sources, run the following command from the repository root:

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

This command iterates through each subfolder in articles/ and compiles every .md file to PDF using the provided LaTeX template, with images looked up in the figures/ folder at the root.

### Dependencies:

- Pandoc (≥ 2.10)
- A LaTeX distribution with xelatex (TeX Live, MikTeX)
- Libertinus fonts (included in TeX Live)

## License

This project is licensed under the MIT License – see the LICENSE file for details.
