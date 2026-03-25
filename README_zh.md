# 天道五行 Clifford 项目 (Tiān Dào Wǔ Xíng Clifford)

[English](README.md) | [Français](README_fr.md)

## 哲学与灵感

本研究揭示了古代中国卜筮者及其后继者的直觉具有惊人的先见之明——他们以《易经》的64卦和五行的五个生成元素奠定了天朝帝国的教义基础。

事实上，在我们的项目中，《易经》可视为克利福德代数 Cl(6,0) 的64个元素的经验预兆，而五行则预演了英国物理学家 Peter Rowlands 提出的五元组结构。

基于这些洞见，我们发展了一种**五元组物理学**——一**种五行物理学**——根据这种物理学，宇宙由无限多个八度组成，每个八度包含72个维度，这些维度又分为六族，每族十二个五元组。因此，五行在所有尺度上构成了宇宙的本质。

这项工作旨在帮助中国人民在经历了150年的狂热西化之后，重新找回对自己悠久文化遗产的自豪感和认同感。为此，Python 代码在未经预先发表的情况下即开放供公众使用。 作为一名居住在山村的退休人员，我并无学术上的野心。如果这项工作在中国能引起积极反响，对我来说就是一种荣誉。

## 出版物

本项目包含五篇主要文章，每篇均提供英文版（点击标题可访问）。法语版本也存放在相同文件夹中。

| 英文标题 | 文件 |
|----------|------|
| **1. The Cl(6,6) Pentadic Model: A Fundamental Unification** | [`PUBLICATION_1_Pentadic_Theory.md`](articles/PUBLICATION_1_Théorie_Pentadique/PUBLICATION_1_Pentadic_Theory.md) |
| **2. Experimental Validation of Nebe's 72‑Dimensional Network via the Zeeman Effect** | [`PUBLICATION_2_Zeeman_Effect.md`](articles/PUBLICATION_2_Effet_Zeeman/PUBLICATION_2_Zeeman_Effect.md) |
| **3. Discovery of a 200 MeV Gamma Resonance in the Magnetar 1E 1048.1‑5937** | [`PUBLICATION_3_Magnetars_en.md`](articles/PUBLICATION_3_Magnetars/PUBLICATION_3_Magnetars_en.md) |
| **4. Cosmological Unification through Pentadic Systems and Clifford Algebra Cl(6,6)** | [`PUBLICATION_4_UNIFYING_SYNTHESIS.md`](articles/PUBLICATION_4_Rapport_de_Synthese/PUBLICATION_4_UNIFYING_SYNTHESIS.md) |
| **5. Angular Transitions between Particles – A Geometric Reinterpretation** | [`PUBLICATION_5_PENTADIC_TRANSITIONS.md`](articles/PUBLICATION_5_Transitions_Pentadiques/PUBLICATION_5_PENTADIC_TRANSITIONS.md) |
| **6. Pentadic Cl(6,6) Model Predictions for the Zeeman Effect and Astrophysical Signatures** | [`PUBLICATION_6_Consolidated.md`](articles/PUBLICATION_6_Zeeman_consolidé/PUBLICATION_6_Consolidated.md) |
| **7. The Hybrid W Layer: A Mathematical Bridge between Cl(6,6) and the 72D Nebe Lattice** | [`PUBLICATION_7_Hybrid_W_Layer.md`](articles/PUBLICATION_7_Couche_hybride_W/PUBLICATION_7_Hybrid_W_Layer.md) |

PDF 和 Markdown 文件均位于相应文件夹中。每篇文章均可使用 Pandoc 和提供的 LaTeX 模板编译为 PDF（参见[编译文章](#编译文章)）。

## 仓库结构

- `articles/` : 出版物 Markdown 文件（每个文章有自己的子文件夹）
- `code/` : Python 脚本（见下文）
- `data/` : 数据文件（JSON、FITS、numpy 数组）
- `docs/` : 附加文档
- `drafts/` : 工作草稿（ODT、DOCX）
- `figures/` : 图像和图表
- `reports/` : 文本报告
- `references/` : PDF 参考文献
- `templates/` : LaTeX 模板
- `requirements.txt` : Python 依赖项（pip）
- `environment.yml` : Conda 环境文件

## Python 脚本

`code/` 目录包含本项目开发的所有 Python 脚本。它们分为两个主要子目录：

- **`code/pentadic/`** – 实现五元组代数的核心模块：构建72个五元组、群作用（PSL₂(7)、SL₂(25)）、验证 Barnes ⊗ Leech 张量积，以及图形用户界面。详见 `README.md`。
- **`code/zeeman/`** – 用于塞曼效应分析、Fermi‑LAT 磁星数据处理、Bott 周期性研究和五元组模型交叉验证的脚本。详见 `README.md`。

所有脚本均使用 Python 3.8+ 编写，并依赖标准科学计算库。所需包列在 `requirements.txt`（pip）和 `environment.yml`（Conda）中。

## 安装依赖项

您有两种方式安装所需的 Python 包：

### 选项 1：使用 pip（最小安装）

```
pip install -r requirements.txt
```

这将安装 PyPI 上可用的包。注意，`fermipy` 未包含在此列表中，因为它需要 conda；如果您需要运行 Fermi‑LAT 分析，请改用 conda 环境。

### 选项 2：使用 conda（完整环境）

创建包含所有依赖项（包括 `fermipy` 和可选的 3D 可视化工具）的 `pentadic` 环境：

```
conda env create -f environment.yml
conda activate pentadic
```

安装后，您可以从命令行运行任何脚本，例如：

```
python code/zeeman/ZEEMAN-PENTADIC-ANALYSIS_v1.0.py
```

## 说明

- Python 脚本会在当前工作目录生成图表和报告。输出文件使用描述性名称保存（如 `preuve_dimension_72_math.png`、`pentadic_predictions_report.txt`）。
- 某些脚本（尤其是 Fermi‑LAT 分析）可能需要互联网连接以下载数据，并可能需要数小时才能完成。
- 有关数学背景和结果解释的详细信息，请参阅 `articles/` 文件夹中的相应文章以及各子目录中的 README 文件。

## 编译 Markdown 文章

要使用提供的模板从 Markdown 文件生成 PDF，请运行：

```
pandoc article.md --template=../../templates/tian-dao-article.tex --listings --citeproc --toc -o article.pdf --pdf-engine=xelatex
```

### 先决条件

- Pandoc（版本 ≥ 2.10）
- 带有 `xelatex` 的 LaTeX 发行版（TeX Live、MikTeX）
- 附加字体（可选但推荐）：
  - Libertinus Serif、Libertinus Mono、Libertinus Math
  - Noto Serif CJK SC（用于中文支持）

如果未安装这些字体，您可以在模板中用默认字体（例如 TeX Gyre Termes）替换。

### 批量编译

要从 Markdown 源为所有文章生成 PDF，请在仓库根目录运行以下命令：

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

此命令遍历 `articles/` 中的每个子文件夹，并使用提供的 LaTeX 模板将每个 `.md` 文件编译为 PDF，图像将在根目录的 `figures/` 文件夹中查找。

### 依赖项：

- Pandoc（≥ 2.10）
- 带有 xelatex 的 LaTeX 发行版（TeX Live、MikTeX）
- Libertinus 字体（包含在 TeX Live 中）

## 许可证

本项目采用 MIT 许可证 – 详见 [LICENSE](LICENSE) 文件。
