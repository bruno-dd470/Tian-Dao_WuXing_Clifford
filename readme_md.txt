# Tian-Dao_WuXing_Clifford

This repository contains the source files for a series of articles on the pentadic theory and Clifford algebra Cl(6,6), as well as Python scripts implementing mathematical models and data analysis related to the Nebe lattice, magnetar observations, and the Zeeman effect.

## Compiling the articles

To generate a PDF from a Markdown file, use `pandoc` with the provided template:

```bash
pandoc article.md --template=templates/tian-dao-article.tex -o article.pdf --pdf-engine=xelatex
Prerequisites
Pandoc (version ≥ 2.10)

A LaTeX distribution with xelatex (TeX Live, MikTeX)

Additional fonts (optional but recommended):

Libertinus Serif, Libertinus Mono, Libertinus Math

Noto Serif CJK SC (for Chinese support)

If the fonts are not installed, you can replace them in the template with default fonts (e.g., TeX Gyre Termes).

Repository structure
articles/ : Markdown files of the publications

templates/ : LaTeX template

code/ : Python scripts (see below)

figures/ : Images and figures

requirements.txt : Python dependencies (pip)

environment.yml : Conda environment file

Python scripts
The code/ directory contains several Python scripts used for mathematical demonstrations, data analysis, and predictions. All scripts are written in Python 3.8+ and rely on standard scientific libraries.

List of scripts
Étude_mathématique_et_analogies_physiques_du_réseau_de_Nebe_en_dimension_72.py – explores the properties of the Nebe lattice (dimension 72, kissing number, automorphism group) and its numerical coincidences with physical constants.

FERMI-LAT_MAGNETAR_ANALYSIS_v2.0.py – analyzes Fermi-LAT data for magnetars, searching for a resonance at 0.2 GeV (octave 6) using fermipy and easyFermi.

BOTT_PERIODICITY_v2.0.py – investigates higher octaves based on Bott periodicity and empirical projection factors, predicting magnetic fields for various astrophysical regimes.

CROSS-VALIDATION_PENTADIQUE_v1.0.py – evaluates the feasibility of different experiments to test the pentadic model.

ZEEMAN-PENTADIC-ANALYSIS_v1.0.py – extracts model parameters (g‑factor, lattice coupling, bicosmic coupling) from simulated data and generates predictions for future observations.

Installation of dependencies
You have two options to install the required Python packages:

Option 1: Using pip (minimal installation)
bash
pip install -r requirements.txt
This installs packages available on PyPI. Note that fermipy is not included in this list because it requires conda; if you need to run the Fermi‑LAT analysis, use the conda environment instead.

Option 2: Using conda (full environment)
Create the pentadic environment with all dependencies (including fermipy and optional 3D visualisation tools):

bash
conda env create -f environment.yml
conda activate pentadic
After installation, you can run any script from the command line, for example:

bash
python code/ZEEMAN-PENTADIC-ANALYSIS_v1.0.py
Notes
The scripts generate figures and reports in the current working directory. Output files are saved with descriptive names (e.g., preuve_dimension_72_math.png, pentadic_predictions_report.txt).

Some scripts (especially the Fermi‑LAT analysis) may require an internet connection to download data and can take several hours to complete.

For details on the mathematical background and interpretation of results, refer to the corresponding articles in the articles/ folder.

Batch compilation
To generate PDFs for all articles from the Markdown sources, run the following command from the repository root:

bash
for d in articles/*/; do
    (cd "$d" && for f in *.md; do
        pandoc "$f" \
            --template=../../templates/tian-dao-article.tex \
            --resource-path=".:../.." \
            -o "${f%.md}.pdf" \
            --pdf-engine=xelatex
    done)
done
This command iterates through each subfolder in articles/ and compiles every .md file to PDF using the provided LaTeX template, with images looked up in the figures/ folder at the root.

Dependencies:

Pandoc (≥ 2.10)

A LaTeX distribution with xelatex (TeX Live, MikTeX)

Libertinus fonts (included in TeX Live)

Project Title
English version

Version française
