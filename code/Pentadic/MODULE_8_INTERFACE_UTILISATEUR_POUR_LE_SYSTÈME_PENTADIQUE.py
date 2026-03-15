#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 8 : INTERFACE UTILISATEUR POUR LE SYSTÈME PENTADIQUE
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import json
import os
import sys
from datetime import datetime
import threading
import glob  # ← AJOUTER GLOB ICI

# =====================================================================
# FONCTIONS UTILITAIRES (HORS CLASSE)
# =====================================================================

def trouver_module(prefix):
    """Trouve un module commençant par un préfixe donné"""
    modules = glob.glob(f"{prefix}*.py")
    return modules[0] if modules else None

# =====================================================================
# CONFIGURATION DES MODULES
# =====================================================================

# Mapping des préfixes vers numéros de module
PREFIXES = {
    1: "MODULE_1",
    2: "MODULE_2",
    3: "MODULE_3",
    4: "MODULE_4",
    5: "MODULE_5",
    6: "MODULE_6",
    7: "MODULE_7",
}

# Construction dynamique du dictionnaire MODULES
MODULES = {}
MODULE_OK = {}

for num, prefix in PREFIXES.items():
    nom = trouver_module(prefix)
    if nom:
        MODULES[num] = nom
        MODULE_OK[num] = True
    else:
        MODULES[num] = f"{prefix}_*.py (non trouvé)"
        MODULE_OK[num] = False

# Affichage des modules trouvés (au démarrage)
print("📦 Modules chargés:")
for num, nom in MODULES.items():
    status = "✅" if MODULE_OK[num] else "❌"
    print(f"   {status} Module {num}: {nom}")

# =====================================================================
# CHARGEMENT DE LA DOCUMENTATION
# =====================================================================

DOCUMENTATION_FILE = "DOCUMENTATION.md"

def charger_documentation():
    """Charge le contenu du fichier DOCUMENTATION.md"""
    try:
        if os.path.exists(DOCUMENTATION_FILE):
            with open(DOCUMENTATION_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Fichier {DOCUMENTATION_FILE} non trouvé."
    except Exception as e:
        return f"Erreur: {e}"

TEXTE_DOCUMENTATION = charger_documentation()

# =====================================================================
# FENÊTRE DE DOCUMENTATION
# =====================================================================

class FenetreDocumentation:
    """Fenêtre séparée pour afficher la documentation"""
    
    def __init__(self, parent):
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Documentation - Système Pentadique")
        self.fenetre.geometry("900x700")
        
        # Zone de texte avec défilement
        self.text_area = scrolledtext.ScrolledText(
            self.fenetre, 
            wrap=tk.WORD,
            width=100, 
            height=40,
            font=('Courier', 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Insérer le texte
        self.text_area.insert(tk.END, TEXTE_DOCUMENTATION)
        self.text_area.config(state=tk.DISABLED)  # Lecture seule
        
        # Bouton Fermer
        ttk.Button(self.fenetre, text="Fermer", command=self.fenetre.destroy).pack(pady=5)


# =====================================================================
# CLASSE PRINCIPALE DE L'INTERFACE
# =====================================================================

class InterfacePentades:
    """Interface graphique principale"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Système Pentadique Cl(6,6) - Interface d'Analyse")
        self.root.geometry("1200x800")
        
        # Variables
        self.donnees_chargees = {}
        self.resultats = []
        self.pentades = []
        self.fichier_courant = None
        self.fenetre_doc = None
        
        # Style
        self.setup_style()
        
        # Créer l'interface
        self.creer_menu()
        self.creer_widgets()
        
        # Afficher le statut de la documentation
        self.verifier_documentation()
        
        # CHARGEMENT DES PENTADES PAR DÉFAUT (AUTOMATIQUE)
        self.charger_pentades_par_defaut()
        
        # Charger les données par défaut
        self.charger_donnees_par_defaut()
        
        print("✅ Interface initialisée")
    
    def verifier_documentation(self):
        """Vérifie si le fichier documentation existe"""
        if os.path.exists(DOCUMENTATION_FILE):
            self.ecrire_log(f"✅ Fichier {DOCUMENTATION_FILE} trouvé")
        else:
            self.ecrire_log(f"⚠ Fichier {DOCUMENTATION_FILE} non trouvé - documentation interne utilisée")
    
    def setup_style(self):
        """Configure le style de l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs
        self.bg_color = '#f0f0f0'
        self.fg_color = '#333333'
        self.accent_color = '#4ECDC4'
        
        self.root.configure(bg=self.bg_color)
        
    def lister_modules_disponibles(self):
        """Liste tous les modules disponibles"""
        self.ecrire_log("\n🔧 MODULES DISPONIBLES:")
        self.ecrire_log("="*50)
        
        for num, nom in MODULES.items():
            status = "✅" if MODULE_OK[num] else "❌"
            self.ecrire_log(f"   {status} Module {num}: {nom}")
        
        self.ecrire_log("="*50)        
        
    def creer_menu(self):
        """Crée la barre de menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # ===== MENU FICHIER =====
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Sous-menu Données
        data_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Données", menu=data_menu)
        data_menu.add_command(label="Charger données EHT (.npy)", command=self.charger_donnees)
        data_menu.add_command(label="Charger pentades (.json)", command=self.charger_pentades)
        data_menu.add_separator()
        data_menu.add_command(label="Vérifier fichiers disponibles", command=self.lister_fichiers)
        
        # Sous-menu Résultats
        results_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Résultats", menu=results_menu)
        results_menu.add_command(label="Charger résultats (.json)", command=self.charger_resultats)
        results_menu.add_command(label="Sauvegarder résultats", command=self.sauvegarder_resultats)
        results_menu.add_separator()
        results_menu.add_command(label="Effacer résultats", command=self.effacer_resultats)
        
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # ===== MENU ANALYSE =====
        analyse_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analyse", menu=analyse_menu)
        analyse_menu.add_command(label="Analyser tous les objets", command=self.analyser_tous)
        analyse_menu.add_command(label="Comparer résultats", command=self.comparer_resultats)
        analyse_menu.add_separator()
        analyse_menu.add_command(label="Module 1: 72 pentades", command=lambda: self.lancer_module(1))
        analyse_menu.add_command(label="Module 2: PSL₂(7)", command=lambda: self.lancer_module(2))
        analyse_menu.add_command(label="Module 3: SL₂(25)", command=lambda: self.lancer_module(3))
        analyse_menu.add_command(label="Module 4: Produit tensoriel", command=lambda: self.lancer_module(4))
        analyse_menu.add_command(label="Module 5: Vecteurs minimaux", command=lambda: self.lancer_module(5))
        analyse_menu.add_command(label="Module 6: Analyse EHT", command=lambda: self.lancer_module(6))
        analyse_menu.add_command(label="Module 7: Visualisation 3D", command=lambda: self.lancer_module(7))
        
        # ===== MENU VISUALISATION =====
        visu_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualisation", menu=visu_menu)
        visu_menu.add_command(label="Graphique tensions", command=self.afficher_graphique_tensions)
        visu_menu.add_command(label="Diagramme radar", command=self.afficher_radar)
        visu_menu.add_command(label="Réseau 3D", command=self.afficher_reseau_3d)
        visu_menu.add_command(label="Histogramme activations", command=self.afficher_histogramme)
        visu_menu.add_command(label="Corrélation Tension-η", command=self.afficher_correlation)
        
        # ===== MENU AIDE =====
        aide_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=aide_menu)
        aide_menu.add_command(label="Documentation complète", command=self.afficher_documentation)
        aide_menu.add_command(label="À propos", command=self.afficher_a_propos)
        aide_menu.add_separator()
        aide_menu.add_command(label="Vérifier modules", command=self.lister_modules_disponibles)
        
    def creer_widgets(self):
        """Crée les widgets de l'interface"""
        
        # Panneau principal
        main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panneau de gauche (contrôles)
        left_frame = ttk.Frame(main_panel, width=300)
        main_panel.add(left_frame, weight=1)
        
        # Panneau de droite (affichage)
        right_frame = ttk.Frame(main_panel)
        main_panel.add(right_frame, weight=3)
        
        # ===== PANNNEAU GAUCHE =====
        
        # Titre
        ttk.Label(left_frame, text="Système Pentadique", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Bouton Documentation
        ttk.Button(left_frame, text="📚 Documentation complète", 
                  command=self.afficher_documentation).pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Separator(left_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # Statut des modules
        self.creer_section_modules(left_frame)
        
        # Chargement des données
        self.creer_section_chargement(left_frame)
        
        # Analyse
        self.creer_section_analyse(left_frame)
        
        # Résultats
        self.creer_section_resultats(left_frame)
        
        # ===== PANNNEAU DROIT =====
        
        # Zone de texte pour les résultats
        self.text_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD,
                                                   width=80, height=30,
                                                   font=('Consolas', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barre d'état
        self.status_bar = ttk.Label(self.root, text="Prêt", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def creer_section_modules(self, parent):
        """Crée la section d'état des modules"""
        frame = ttk.LabelFrame(parent, text="Modules disponibles", padding=5)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.module_vars = {}
        descriptions = [
            (1, "Module 1: 72 pentades"),
            (2, "Module 2: PSL₂(7)"),
            (3, "Module 3: SL₂(25)"),
            (4, "Module 4: Produit tensoriel"),
            (5, "Module 5: Vecteurs minimaux (6.2×10⁹)"),
            (6, "Module 6: Analyse EHT"),
            (7, "Module 7: Visualisation 3D"),
        ]
        
        for num, desc in descriptions:
            dispo = MODULE_OK.get(num, False)
            var = tk.StringVar()
            var.set("✅" if dispo else "❌")
            self.module_vars[desc] = var
            ttk.Label(frame, text=f"{var.get()} {desc}").pack(anchor=tk.W)
                
    def lister_fichiers(self):
        """Liste tous les fichiers disponibles dans le répertoire"""
        self.ecrire_log("\n📋 FICHIERS DISPONIBLES:")
        self.ecrire_log("="*50)
        
        # Lister les fichiers .json
        json_files = glob.glob("*.json")
        if json_files:
            self.ecrire_log("\n📄 Fichiers JSON:")
            for f in sorted(json_files):
                size = os.path.getsize(f)
                self.ecrire_log(f"   • {f} ({size} octets)")
        
        # Lister les fichiers .npy
        npy_files = glob.glob("*.npy") + glob.glob("resultats_eht/*.npy")
        if npy_files:
            self.ecrire_log("\n📊 Fichiers NPY (données):")
            for f in sorted(npy_files):
                if os.path.exists(f):
                    size = os.path.getsize(f)
                    self.ecrire_log(f"   • {f} ({size} octets)")
        
        # Lister les fichiers .py (modules)
        py_files = glob.glob("MODULE_*.py")
        if py_files:
            self.ecrire_log("\n🐍 Modules Python:")
            for f in sorted(py_files):
                size = os.path.getsize(f)
                status = "✅" if f in MODULES.values() else " "
                self.ecrire_log(f"   {status} {f} ({size} octets)")
        
        self.ecrire_log("="*50)            
        
    def creer_section_chargement(self, parent):
        """Crée la section de chargement"""
        frame = ttk.LabelFrame(parent, text="Chargement", padding=5)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame, text="Charger données EHT", 
                  command=self.charger_donnees).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Charger pentades", 
                  command=self.charger_pentades).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Charger résultats", 
                  command=self.charger_resultats).pack(fill=tk.X, pady=2)
        
        # Liste des fichiers chargés
        self.liste_fichiers = tk.Listbox(frame, height=4)
        self.liste_fichiers.pack(fill=tk.X, pady=5)
    
    def creer_section_analyse(self, parent):
        """Crée la section d'analyse"""
        frame = ttk.LabelFrame(parent, text="Analyse", padding=5)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame, text="Analyser tous", 
                  command=self.analyser_tous).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Comparer résultats", 
                  command=self.comparer_resultats).pack(fill=tk.X, pady=2)
        
        # Barre de progression
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
    
    def creer_section_resultats(self, parent):
        """Crée la section des résultats"""
        frame = ttk.LabelFrame(parent, text="Résultats", padding=5)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.resultats_list = tk.Listbox(frame, height=6)
        self.resultats_list.pack(fill=tk.X, pady=5)
        self.resultats_list.bind('<<ListboxSelect>>', self.afficher_resultat_detail)
        
        ttk.Button(frame, text="Sauvegarder", 
                  command=self.sauvegarder_resultats).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Effacer", 
                  command=self.effacer_resultats).pack(fill=tk.X, pady=2)
    
    def afficher_documentation(self):
        """Ouvre une fenêtre avec la documentation complète"""
        if self.fenetre_doc is None or not self.fenetre_doc.winfo_exists():
            self.fenetre_doc = FenetreDocumentation(self.root)
        else:
            self.fenetre_doc.focus()  # Amener au premier plan et donner le focus
            self.fenetre_doc.lift()
    
    def afficher_a_propos(self):
        """Affiche une boîte de dialogue À propos simplifiée"""
        messagebox.showinfo("À propos", 
            "Système Pentadique Cl(6,6) - Version 1.0\n"
            "© 2026\n\n"
            "Un modèle algébrique unifié basé sur les travaux de\n"
            "Peter Rowlands, Jean-Pierre Petit, Gabriele Nebe\n"
            "et les descriptions Ummites.\n\n"
            "Documentation disponible dans le fichier DOCUMENTATION.md\n"
            "ou via le bouton 'Documentation complète'.")
    
    def charger_donnees_par_defaut(self):
        """Charge les données par défaut"""
        self.ecrire_log("🔍 Recherche des fichiers par défaut...")
        
        # Chercher les fichiers .npy dans le dossier resultats_eht
        if os.path.exists("resultats_eht/resultats_eht.json"):
            try:
                with open("resultats_eht/resultats_eht.json", 'r') as f:
                    data = json.load(f)
                self.resultats = data['resultats']
                for r in self.resultats:
                    self.resultats_list.insert(tk.END, 
                        f"{r['nom']}: T={r['tension']:.3f}, {r['type']}")
                self.ecrire_log("✅ Résultats par défaut chargés")
            except:
                pass
    
    def charger_donnees(self):
        """Charge des données EHT"""
        fichiers = filedialog.askopenfilenames(
            title="Choisir des fichiers de données EHT",
            filetypes=[("Fichiers NPY", "*.npy"), ("Tous", "*.*")]
        )
        
        if fichiers:
            self.progress.start()
            self.ecrire_log(f"📥 Chargement de {len(fichiers)} fichiers...")
            
            for f in fichiers:
                try:
                    data = np.load(f)
                    nom = os.path.basename(f).replace('.npy', '')
                    self.donnees_chargees[nom] = data
                    self.liste_fichiers.insert(tk.END, f"{nom} - shape {data.shape}")
                    self.ecrire_log(f"  ✅ {nom} chargé")
                except Exception as e:
                    self.ecrire_log(f"  ❌ Erreur: {e}")
            
            self.progress.stop()
            self.status_bar.config(text=f"{len(fichiers)} fichiers chargés")
    
    def charger_pentades(self):
        """Charge les pentades depuis un fichier JSON"""
        fichier = filedialog.askopenfilename(
            title="Choisir le fichier des pentades",
            filetypes=[("Fichiers JSON", "*.json")]
        )
        
        if fichier:
            try:
                with open(fichier, 'r') as f:
                    self.pentades = json.load(f)
                self.ecrire_log(f"✅ {len(self.pentades)} pentades chargées")
                self.status_bar.config(text=f"{len(self.pentades)} pentades chargées")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger: {e}")
    
    def charger_pentades_par_defaut(self):
        """Charge ou recrée les pentades automatiquement"""
        self.ecrire_log("\n🔍 Recherche des pentades...")
        
        # 1. Vérifier si le fichier existe déjà
        if os.path.exists("pentades_72_finales.json"):
            try:
                with open("pentades_72_finales.json", 'r') as f:
                    self.pentades = json.load(f)
                self.ecrire_log(f"✅ {len(self.pentades)} pentades chargées depuis pentades_72_finales.json")
                
                familles = set(p['famille'] for p in self.pentades)
                self.ecrire_log(f"   Familles: {', '.join(sorted(familles))}")
                return True
            except Exception as e:
                self.ecrire_log(f"⚠ Erreur de lecture: {e}")
        
        # 2. Chercher le Module 1 (peu importe le nom exact)

        modules_p1 = glob.glob("MODULE_1*.py")
        
        if modules_p1:
            module_nom = modules_p1[0]
            self.ecrire_log(f"🔧 Module trouvé: {module_nom}")
            self.ecrire_log("   Lancement pour recréer les pentades...")
            self.progress.start()
            
            try:
                import subprocess
                result = subprocess.run(["python3", module_nom], 
                                       capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0 and os.path.exists("pentades_72_finales.json"):
                    with open("pentades_72_finales.json", 'r') as f:
                        self.pentades = json.load(f)
                    self.ecrire_log(f"✅ {len(self.pentades)} pentades recréées avec succès")
                    self.progress.stop()
                    return True
                else:
                    self.ecrire_log("❌ Échec de la recréation")
            except Exception as e:
                self.ecrire_log(f"❌ Exception: {e}")
            finally:
                self.progress.stop()
        else:
            self.ecrire_log("❌ Module 1 non trouvé")
            self.ecrire_log("   Utilisez le bouton 'Charger pentades' manuellement")
        
        return False
    
    def charger_resultats(self):
        """Charge des résultats d'analyse"""
        fichier = filedialog.askopenfilename(
            title="Choisir un fichier de résultats",
            filetypes=[("Fichiers JSON", "*.json")]
        )
        
        if fichier:
            try:
                with open(fichier, 'r') as f:
                    data = json.load(f)
                self.resultats = data['resultats']
                self.resultats_list.delete(0, tk.END)
                for r in self.resultats:
                    self.resultats_list.insert(tk.END, 
                        f"{r['nom']}: T={r['tension']:.3f}, {r['type']}")
                self.ecrire_log(f"✅ {len(self.resultats)} résultats chargés")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger: {e}")
    
    def sauvegarder_resultats(self):
        """Sauvegarde les résultats dans un fichier JSON"""
        if not self.resultats:
            messagebox.showwarning("Attention", "Aucun résultat à sauvegarder")
            return
        
        fichier = filedialog.asksaveasfilename(
            title="Sauvegarder les résultats",
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json")]
        )
        
        if fichier:
            try:
                output = {
                    'date': datetime.now().isoformat(),
                    'nb_objets': len(self.resultats),
                    'resultats': self.resultats
                }
                with open(fichier, 'w') as f:
                    json.dump(output, f, indent=2)
                self.ecrire_log(f"💾 Résultats sauvegardés dans {fichier}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder: {e}")
    
    def analyser_tous(self):
        """Analyse tous les objets chargés"""
        if not self.donnees_chargees:
            messagebox.showwarning("Attention", "Aucune donnée chargée")
            return
        
        self.progress.start()
        self.ecrire_log("\n🔬 ANALYSE DES OBJETS")
        self.ecrire_log("="*50)
        
        self.resultats = []
        for nom, donnees in self.donnees_chargees.items():
            # Simulation d'analyse (à remplacer par vraie analyse)
            tension = np.random.uniform(0.01, 0.3)
            eta = np.random.uniform(-1, 0)
            
            if tension > 0.8:
                type_objet = "🌟 PLUGSTAR ACTIVE"
            elif tension > 0.3:
                type_objet = "✨ PLUGSTAR PARTIELLE"
            else:
                type_objet = "⚫ PLUGSTAR FERMÉE"
            
            resultat = {
                'nom': nom,
                'tension': float(tension),
                'eta': float(eta),
                'type': type_objet,
                'activation_P4': float(np.random.uniform(0, 1)),
                'activation_N4': float(np.random.uniform(0, 1)),
                'activation_P4p': float(np.random.uniform(0, 1)),
                'activation_N4p': 0.0
            }
            
            self.resultats.append(resultat)
            self.ecrire_log(f"\n{resultat['type']} {nom}")
            self.ecrire_log(f"   Tension: {resultat['tension']:.4f}")
            self.ecrire_log(f"   η: {resultat['eta']:+.4f}")
        
        # Mettre à jour la liste
        self.resultats_list.delete(0, tk.END)
        for r in self.resultats:
            self.resultats_list.insert(tk.END, 
                f"{r['nom']}: T={r['tension']:.3f}, {r['type']}")
        
        self.progress.stop()
        self.status_bar.config(text=f"{len(self.resultats)} objets analysés")
    
    def comparer_resultats(self):
        """Compare les résultats entre objets"""
        if len(self.resultats) < 2:
            messagebox.showwarning("Attention", "Pas assez de résultats pour comparer")
            return
        
        self.ecrire_log("\n📊 COMPARAISON DES OBJETS")
        self.ecrire_log("="*60)
        self.ecrire_log(f"{'Objet':<15} {'Tension':<10} {'η':<10} {'Type':<25}")
        self.ecrire_log("-"*60)
        
        for r in sorted(self.resultats, key=lambda x: x['tension'], reverse=True):
            self.ecrire_log(f"{r['nom']:<15} {r['tension']:<10.4f} "
                          f"{r['eta']:<+10.4f} {r['type']:<25}")
    
    def afficher_resultat_detail(self, event):
        """Affiche les détails d'un résultat sélectionné"""
        selection = self.resultats_list.curselection()
        if selection:
            idx = selection[0]
            if idx < len(self.resultats):
                r = self.resultats[idx]
                self.ecrire_log(f"\n📌 DÉTAIL: {r['nom']}")
                self.ecrire_log(f"   Type: {r['type']}")
                self.ecrire_log(f"   Tension: {r['tension']:.4f}")
                self.ecrire_log(f"   η: {r['eta']:+.4f}")
                self.ecrire_log(f"   Activations:")
                self.ecrire_log(f"     P4 : {r['activation_P4']:.3f}")
                self.ecrire_log(f"     N4 : {r['activation_N4']:.3f}")
                self.ecrire_log(f"     P'4: {r['activation_P4p']:.3f}")
                self.ecrire_log(f"     N'4: {r['activation_N4p']:.3f}")
    
    def effacer_resultats(self):
        """Efface tous les résultats"""
        self.resultats = []
        self.resultats_list.delete(0, tk.END)
        self.ecrire_log("\n🗑️ Résultats effacés")
    
    def afficher_graphique_tensions(self):
        """Affiche le graphique des tensions"""
        if not self.resultats:
            messagebox.showwarning("Attention", "Aucun résultat à afficher")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        noms = [r['nom'] for r in self.resultats]
        tensions = [r['tension'] for r in self.resultats]
        
        bars = ax.bar(noms, tensions, color='skyblue')
        ax.set_xlabel('Objet')
        ax.set_ylabel('Tension')
        ax.set_title('Tension de connexion par objet')
        ax.axhline(y=0.3, color='orange', linestyle='--', label='Seuil partiel')
        ax.axhline(y=0.8, color='red', linestyle='--', label='Seuil actif')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotation des labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.show()
    
    def afficher_radar(self):
        """Affiche le diagramme radar"""
        if not self.resultats:
            messagebox.showwarning("Attention", "Aucun résultat à afficher")
            return
        
        categories = ['P4', 'N4', "P'4", "N'4"]
        N = len(categories)
        angles = [n / N * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
        
        for r in self.resultats:
            valeurs = [
                r['activation_P4'],
                r['activation_N4'],
                r['activation_P4p'],
                r['activation_N4p']
            ]
            valeurs += valeurs[:1]
            
            ax.plot(angles, valeurs, 'o-', linewidth=2, label=r['nom'])
            ax.fill(angles, valeurs, alpha=0.25)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        ax.set_title("Profils d'activation des pentades seuil")
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.tight_layout()
        plt.show()
    
    def afficher_reseau_3d(self):
        """Affiche le réseau 3D"""
        self.ecrire_log("\n🔷 Lancement de la visualisation 3D...")
        self.lancer_module(7)
    
    def afficher_histogramme(self):
        """Affiche l'histogramme des activations"""
        if not self.resultats:
            messagebox.showwarning("Attention", "Aucun résultat à afficher")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        for idx, r in enumerate(self.resultats[:4]):
            ax = axes[idx]
            
            categories = ['P4', 'N4', "P'4", "N'4"]
            valeurs = [
                r['activation_P4'],
                r['activation_N4'],
                r['activation_P4p'],
                r['activation_N4p']
            ]
            
            bars = ax.bar(categories, valeurs)
            ax.set_title(f"{r['nom']} - T={r['tension']:.3f}")
            ax.set_ylabel('Activation')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def afficher_correlation(self):
        """Affiche la corrélation Tension-η"""
        if len(self.resultats) < 2:
            messagebox.showwarning("Attention", "Pas assez de points pour la corrélation")
            return
        
        tensions = [r['tension'] for r in self.resultats]
        etas = [r['eta'] for r in self.resultats]
        noms = [r['nom'] for r in self.resultats]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        scatter = ax.scatter(tensions, etas, s=100, alpha=0.7)
        
        for i, nom in enumerate(noms):
            ax.annotate(nom, (tensions[i], etas[i]), 
                       fontsize=9, xytext=(5, 5), textcoords='offset points')
        
        ax.set_xlabel('Tension')
        ax.set_ylabel('η')
        ax.set_title('Corrélation Tension vs Déséquilibre Sheng/Ke')
        ax.grid(True, alpha=0.3)
        
        # Lignes de seuil
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
        ax.axvline(x=0.3, color='orange', linestyle='--', alpha=0.5)
        ax.axvline(x=0.8, color='red', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.show()
    
    def lancer_module(self, num_module):
        """Lance un module externe"""
        if num_module in MODULES:
            nom_fichier = MODULES[num_module]
            self.ecrire_log(f"\n🚀 Lancement du module {num_module} ({nom_fichier})...")
            
            if os.path.exists(nom_fichier):
                os.system(f"python3 {nom_fichier}")
                self.ecrire_log(f"✅ Module {num_module} terminé")
            else:
                self.ecrire_log(f"❌ Fichier {nom_fichier} non trouvé")
                messagebox.showerror("Erreur", f"Fichier {nom_fichier} non trouvé")
    
    def ecrire_log(self, texte):
        """Écrit un texte dans la zone de log"""
        self.text_area.insert(tk.END, texte + "\n")
        self.text_area.see(tk.END)
        self.root.update()


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfacePentades(root)
    
    # Centrer la fenêtre
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
