# Tian-Dao_WuXing_Clifford

This repository contains the source files for a series of articles on the pentadic theory and Clifford algebra Cl(6,6), as well as Python scripts implementing mathematical models and data analysis related to the Nebe lattice, magnetar observations, and the Zeeman effect.

## Compiling the articles

To generate a PDF from a Markdown file, use `pandoc` with the provided template:

```
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
- `code/` : Python scripts (see below)
- `figures/` : Images and figures
- `requirements.txt` : Python dependencies (pip)
- `environment.yml` : Conda environment file

## Python scripts

The [`code/`](code/) directory contains all Python scripts developed for this project. They are organized into two main subdirectories:

- **[`code/zeeman/`](code/zeeman/)** – Scripts for Zeeman effect analysis, Fermi‑LAT magnetar data processing, Bott periodicity studies, and cross‑validation of the pentadic model.  
  See the [`README.md`](code/zeeman/README.md) in that folder for detailed descriptions.

- **[`code/pentadic/`](code/pentadic/)** – Core modules implementing the pentadic algebra: construction of the 72 pentads, group actions (PSL₂(7), SL₂(25)), verification of the Barnes ⊗ Leech tensor product, and a graphical user interface.  
  See the [`README.md`](code/pentadic/README.md) for full documentation.

All scripts are written in Python 3.8+ and rely on standard scientific libraries. The required packages are listed in the main [`requirements.txt`](requirements.txt) (pip) and [`environment.yml`](environment.yml) (Conda).

### Installation of dependencies

You have two options to install the required Python packages:

#### Option 1: Using pip (minimal installation)
```
pip install -r requirements.txt
```
This installs packages available on PyPI. Note that `fermipy` is not included in this list because it requires conda; if you need to run the Fermi‑LAT analysis, use the conda environment instead.

#### Option 2: Using conda (full environment)
Create the `pentadic` environment with all dependencies (including `fermipy` and optional 3D visualisation tools):
```
conda env create -f environment.yml
conda activate pentadic
```

After installation, you can run any script from the command line, for example:
```
python code/zeeman/ZEEMAN-PENTADIC-ANALYSIS_v1.0.py
```

### Notes
- The scripts generate figures and reports in the current working directory. Output files are saved with descriptive names (e.g., `preuve_dimension_72_math.png`, `pentadic_predictions_report.txt`).
- Some scripts (especially the Fermi‑LAT analysis) may require an internet connection to download data and can take several hours to complete.
- For details on the mathematical background and interpretation of results, refer to the corresponding articles in the `articles/` folder and to the README files in each subdirectory.

Cette version allège le README principal tout en donnant des orientations claires vers les documentations spécialisées.

### Installation of dependencies

You have two options to install the required Python packages:

#### Option 1: Using pip (minimal installation)
```
pip install -r requirements.txt
```
This installs packages available on PyPI. Note that `fermipy` is not included in this list because it requires conda; if you need to run the Fermi‑LAT analysis, use the conda environment instead.

#### Option 2: Using conda (full environment)
Create the `pentadic` environment with all dependencies (including `fermipy` and optional 3D visualisation tools):
```
conda env create -f environment.yml
conda activate pentadic
```

After installation, you can run any script from the command line, for example:
```
python code/ZEEMAN-PENTADIC-ANALYSIS_v1.0.py
```

### Notes
- The scripts generate figures and reports in the current working directory. Output files are saved with descriptive names (e.g., `preuve_dimension_72_math.png`, `pentadic_predictions_report.txt`).
- Some scripts (especially the Fermi‑LAT analysis) may require an internet connection to download data and can take several hours to complete.
- For details on the mathematical background and interpretation of results, refer to the corresponding articles in the `articles/` folder.

## Batch compilation

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

This command iterates through each subfolder in `articles/` and compiles every `.md` file to PDF using the provided LaTeX template, with images looked up in the `figures/` folder at the root.

**Dependencies:**
- Pandoc (≥ 2.10)
- A LaTeX distribution with xelatex (TeX Live, MikTeX)
- Libertinus fonts (included in TeX Live)

