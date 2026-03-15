#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de fusion et traduction des articles Markdown pour DeepL
Version avec extraction du titre depuis l'en-tête YAML et sauts de page HTML.
"""

import os
import glob
import subprocess
import sys

try:
    import yaml
except ImportError:
    print("❌ La bibliothèque PyYAML est nécessaire.")
    print("   Installez-la avec : pip install pyyaml")
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = "/home/bruno_dd/Téléchargements/Model_IA_Cl66/GITHUB/Tian-Dao_WuXing_Clifford/articles"
OUTPUT_DIR = "/home/bruno_dd/Téléchargements/Model_IA_Cl66/GITHUB/Tian-Dao_WuXing_Clifford"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fusion_articles.docx")
TEMP_MD = os.path.join(OUTPUT_DIR, "fusion_temp.md")

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def extraire_front_matter(contenu):
    """Extrait le front matter YAML et le corps du document."""
    lignes = contenu.splitlines()
    if not lignes or not lignes[0].startswith('---'):
        return None, contenu
    
    end_line = None
    for i in range(1, len(lignes)):
        if lignes[i].startswith('---'):
            end_line = i
            break
    
    if end_line is None:
        return None, contenu
    
    yaml_text = '\n'.join(lignes[1:end_line])
    corps = '\n'.join(lignes[end_line+1:])
    
    try:
        front = yaml.safe_load(yaml_text)
        if not isinstance(front, dict):
            front = {}
    except yaml.YAMLError:
        front = {}
    
    return front, corps

def extraire_titre(contenu, nom_fichier):
    """Extrait le titre : d'abord depuis le front matter, sinon cherche '# '."""
    front, corps = extraire_front_matter(contenu)
    if front and 'title' in front:
        titre = front['title']
        if isinstance(titre, str):
            titre = titre.strip('"').strip("'")
        return titre, corps
    else:
        lignes = contenu.splitlines()
        for ligne in lignes:
            if ligne.startswith('# '):
                titre = ligne[2:].strip()
                # Enlever cette ligne du corps
                corps_sans_titre = '\n'.join([l for l in lignes if not l.startswith('# ')])
                return titre, corps_sans_titre
        titre = os.path.splitext(os.path.basename(nom_fichier))[0]
        return titre, contenu

# ============================================================================
# RECHERCHE DES FICHIERS MARKDOWN
# ============================================================================

print("🔍 Recherche des fichiers Markdown dans :", BASE_DIR)
md_files = glob.glob(os.path.join(BASE_DIR, "**/*.md"), recursive=True)
md_files.sort()

if not md_files:
    print("❌ Aucun fichier .md trouvé.")
    exit(1)

print(f"✅ {len(md_files)} fichier(s) trouvé(s) :")
for i, f in enumerate(md_files, 1):
    rel_path = os.path.relpath(f, OUTPUT_DIR)
    print(f"  {i:2d}. {rel_path}")

# ============================================================================
# FUSION AVEC TITRES ET SAUTS DE PAGE HTML
# ============================================================================

print("\n📝 Création du fichier Markdown temporaire avec titres...")

with open(TEMP_MD, 'w', encoding='utf-8') as out:
    for idx, fichier in enumerate(md_files):
        # Lecture du fichier
        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Extraction du titre et du corps
        titre, corps = extraire_titre(contenu, fichier)
        
        # Écriture du titre
        out.write(f"# {titre}\n\n")
        
        # Écriture du corps
        out.write(corps)
        out.write("\n\n")
        
        # Saut de page après chaque article (sauf le dernier)
        if idx < len(md_files) - 1:
            out.write('<div style="page-break-after: always;"></div>\n\n')
        # Pas de saut après le dernier article

print(f"✅ Fichier temporaire créé : {TEMP_MD}")

# ============================================================================
# CONVERSION EN DOCX
# ============================================================================

print("\n📦 Conversion en DOCX avec pandoc...")
cmd = ["pandoc", TEMP_MD, "-o", OUTPUT_FILE]
print("   Commande :", " ".join(cmd))

try:
    subprocess.run(cmd, check=True)
    print(f"✅ Fusion réussie : {OUTPUT_FILE}")
except subprocess.CalledProcessError as e:
    print("❌ Erreur lors de l'exécution de pandoc :", e)
    exit(1)
except FileNotFoundError:
    print("❌ pandoc n'est pas installé ou introuvable dans le PATH.")
    exit(1)

# Nettoyage optionnel
# os.remove(TEMP_MD)

# ============================================================================
# INSTRUCTIONS POUR LA TRADUCTION
# ============================================================================

print("\n" + "="*60)
print("📤 ÉTAPE SUIVANTE : TRADUCTION AVEC DEEPL")
print("="*60)
print(f"""
1. Connectez-vous à votre compte DeepL (abonnement web) :
   https://www.deepl.com/translator

2. Allez dans l'onglet "Traduire des fichiers" (Translate files).

3. Téléchargez le fichier fusionné :
   {OUTPUT_FILE}

4. Choisissez la langue cible (par exemple anglais).

5. DeepL générera un fichier traduit (DOCX) que vous pourrez télécharger.

6. Si vous souhaitez retravailler le texte en Markdown, convertissez-le avec :
   pandoc chemin/vers/fichier_traduit.docx -o articles_traduits.md
""")

print("\n🎯 Script terminé.")