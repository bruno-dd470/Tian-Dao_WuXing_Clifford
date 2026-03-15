# Code – Python scripts for the Tian-Dao_WuXing_Clifford project

This directory contains all Python scripts developed to support the mathematical demonstrations, data analysis, and visualisations presented in the articles of the Tian-Dao_WuXing_Clifford project.

## Structure

- [`zeeman/`](zeeman/) – Scripts dedicated to the study of the Zeeman effect, Fermi‑LAT magnetar analysis, Bott periodicity, and cross‑validation of the pentadic model.
- [`pentadic/`](pentadic/) – Core modules for constructing the 72 pentads, implementing group actions (PSL₂(7), SL₂(25)), verifying the Barnes ⊗ Leech tensor product, and providing a graphical user interface.

Each subdirectory contains its own `README.md` with detailed descriptions of the scripts, usage examples, and output files.

## Requirements

All scripts are written in **Python ≥ 3.8** and depend on standard scientific libraries. The required packages are listed in the main [`requirements.txt`](../requirements.txt) at the project root. For a complete environment that includes `fermipy` and optional 3D visualisation tools, use the provided [`environment.yml`](../environment.yml) (Conda).

Quick installation with pip:

```
pip install -r ../requirements.txt
```

## General notes

- Scripts are meant to be run independently. They generate figures and text reports in the current working directory.
- Some scripts (especially the Fermi‑LAT analysis) may require an internet connection to download data and can take several hours to complete.
- If you encounter any issues, please consult the detailed README in the relevant subfolder or open an issue on the main repository.

For further information, refer to the project‑level [README](../README.md).
```
