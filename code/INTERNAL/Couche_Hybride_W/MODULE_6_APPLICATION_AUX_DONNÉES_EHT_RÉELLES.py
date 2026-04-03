#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 6 : APPLICATION AUX DONNÉES EHT RÉELLES
Analyse des trous noirs M87*, SgrA*, Centaurus A, 3C279 avec le modèle pentadique
Utilise les fichiers .npy déjà téléchargés
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

# =====================================================================
# CONFIGURATION
# =====================================================================

class Config:
    """Configuration pour l'analyse des données EHT"""
    
    # Chemin vers les fichiers .npy (déjà téléchargés)
    DOSSIER_NPY = "/home/bruno_dd/Téléchargements/Model_IA_Cl66/astropy/NPY"
    
    # Fichiers de données disponibles
    FICHIERS_DISPONIBLES = {
        'M87': 'm87_spineur.npy',
        'SGRA': 'sgra_spineur.npy',
        'CENTAURUS_A': 'centaurus_a_spineur.npy',
        '3C279': '3c279_spineur.npy',
    }
    
    # Fichier des pentades
    FICHIER_PENTADES = "pentades_72_finales.json"
    
    # Paramètres des pentades
    NB_COMPOSANTES = 32
    SEUILS = {
        'P4': (6, 10),
        'N4': (18, 22),
        "P'4": (24, 28),
        "N'4": (28, 32)
    }
    
    # Dossier pour les résultats
    DOSSIER_RESULTATS = "resultats_eht"


# =====================================================================
# CHARGEUR DE DONNÉES
# =====================================================================

class ChargeurDonnees:
    """Charge les données EHT depuis les fichiers .npy"""
    
    def __init__(self):
        self.creer_dossiers()
        self.donnees = {}
        self.informations = {}
        
    def creer_dossiers(self):
        """Crée les dossiers nécessaires"""
        if not os.path.exists(Config.DOSSIER_RESULTATS):
            os.makedirs(Config.DOSSIER_RESULTATS)
            print(f"📁 Dossier créé: {Config.DOSSIER_RESULTATS}")
    
    def charger_toutes_donnees(self):
        """Charge tous les fichiers .npy disponibles"""
        print("\n" + "="*70)
        print("CHARGEMENT DES DONNÉES EHT")
        print("="*70)
        
        if not os.path.exists(Config.DOSSIER_NPY):
            print(f"❌ Dossier {Config.DOSSIER_NPY} non trouvé!")
            return False
        
        fichiers_trouves = 0
        for nom, fichier in Config.FICHIERS_DISPONIBLES.items():
            chemin = os.path.join(Config.DOSSIER_NPY, fichier)
            if os.path.exists(chemin):
                try:
                    data = np.load(chemin)
                    self.donnees[nom] = data
                    self.informations[nom] = {
                        'fichier': fichier,
                        'shape': data.shape,
                        'min': float(np.min(data)),
                        'max': float(np.max(data)),
                        'moyenne': float(np.mean(data)),
                        'ecart_type': float(np.std(data))
                    }
                    fichiers_trouves += 1
                    print(f"✅ {nom}: {fichier} chargé - shape {data.shape}")
                except Exception as e:
                    print(f"❌ Erreur chargement {nom}: {e}")
            else:
                print(f"⚠ {nom}: fichier {fichier} non trouvé")
        
        print(f"\n📊 {fichiers_trouves}/{len(Config.FICHIERS_DISPONIBLES)} fichiers chargés")
        return fichiers_trouves > 0
    
    def get_donnees(self, nom):
        """Retourne les données pour un objet"""
        return self.donnees.get(nom)
    
    def afficher_info(self):
        """Affiche les informations sur les données chargées"""
        print("\n" + "="*70)
        print("INFORMATIONS SUR LES DONNÉES")
        print("="*70)
        
        for nom, info in self.informations.items():
            print(f"\n🔹 {nom}:")
            print(f"   Fichier: {info['fichier']}")
            print(f"   Shape: {info['shape']}")
            print(f"   Min: {info['min']:.4f}")
            print(f"   Max: {info['max']:.4f}")
            print(f"   Moyenne: {info['moyenne']:.4f}")
            print(f"   Écart-type: {info['ecart_type']:.4f}")


# =====================================================================
# MODÈLE PENTADIQUE
# =====================================================================

class ModelePentadique:
    """Modèle d'analyse basé sur les pentades"""
    
    def __init__(self, fichier_pentades=Config.FICHIER_PENTADES):
        self.pentades = []
        self.familles = {}
        self.charger_pentades(fichier_pentades)
        
    def charger_pentades(self, fichier):
        """Charge les pentades depuis le fichier JSON"""
        if not os.path.exists(fichier):
            print(f"⚠ Fichier {fichier} non trouvé - utilisation des pentades par défaut")
            self._initialiser_pentades_defaut()
            return
        
        with open(fichier, 'r', encoding='utf-8') as f:
            self.pentades = json.load(f)
        
        # Organiser par famille
        for p in self.pentades:
            famille = p['famille']
            if famille not in self.familles:
                self.familles[famille] = []
            self.familles[famille].append(p)
        
        print(f"\n📚 {len(self.pentades)} pentades chargées")
        print(f"   {len(self.familles)} familles: {', '.join(self.familles.keys())}")
    
    def _initialiser_pentades_defaut(self):
        """Initialise des pentades par défaut si le fichier n'existe pas"""
        # Version simplifiée pour le test
        self.pentades = [
            {'famille': 'FI', 'signe': 1, 'elements': ['iI','iJ','iK',"i'k",'1j']},
            {'famille': 'FI', 'signe': -1, 'elements': ['-iI','-iJ','-iK',"-i'k",'-1j']},
        ]
    
    def calculer_activation(self, donnees, pentade):
        """
        Calcule l'activation d'une pentade pour des données
        """
        if len(donnees) < 32:
            donnees = np.pad(donnees, (0, 32 - len(donnees)))
        else:
            donnees = donnees[:32]
        
        # Projection simple (produit scalaire)
        # Dans un modèle complet, utiliser les bivecteurs
        activation = 0.0
        for i, elem in enumerate(pentade['elements'][:5]):
            if i < len(donnees):
                # Poids basé sur l'élément
                poids = hash(str(elem)) % 100 / 100.0
                activation += abs(donnees[i]) * poids
        
        return activation
    
    def calculer_tension(self, donnees):
        """
        Calcule la tension basée sur les pentades seuil
        """
        if len(donnees) < 32:
            donnees = np.pad(donnees, (0, 32 - len(donnees)))
        
        # Activer les seuils
        activations = []
        
        # P4 (indices 6-10)
        p4 = np.mean(np.abs(donnees[6:10])) if len(donnees) > 10 else 0
        activations.append(p4)
        
        # N4 (indices 18-22)
        n4 = np.mean(np.abs(donnees[18:22])) if len(donnees) > 22 else 0
        activations.append(n4)
        
        # P'4 (indices 24-28)
        p4p = np.mean(np.abs(donnees[24:28])) if len(donnees) > 28 else 0
        activations.append(p4p)
        
        # N'4 (indices 28-32)
        n4p = np.mean(np.abs(donnees[28:32])) if len(donnees) > 32 else 0
        activations.append(n4p)
        
        return np.mean(activations) if activations else 0
    
    def calculer_eta(self, donnees):
        """
        Calcule le déséquilibre Sheng/Ke
        """
        if len(donnees) < 32:
            donnees = np.pad(donnees, (0, 32 - len(donnees)))
        
        # Sheng (cycles positifs)
        sheng = (np.mean(np.abs(donnees[6:10])) + 
                 np.mean(np.abs(donnees[24:28]))) / 2
        
        # Ke (cycles négatifs)
        ke = (np.mean(np.abs(donnees[18:22])) + 
              np.mean(np.abs(donnees[28:32]))) / 2
        
        if sheng + ke == 0:
            return 0.0
        return (sheng - ke) / (sheng + ke)
    
    def analyser_objet(self, donnees, nom):
        """
        Analyse complète d'un objet
        """
        tension = self.calculer_tension(donnees)
        eta = self.calculer_eta(donnees)
        
        # Classification
        if tension > 0.8:
            type_objet = "🌟 PLUGSTAR ACTIVE"
            description = "Connexion forte, redshift z=2"
        elif tension > 0.3:
            type_objet = "✨ PLUGSTAR PARTIELLE"
            description = "Connexion modérée, redshift z=1"
        else:
            type_objet = "⚫ PLUGSTAR FERMÉE"
            description = "Connexion faible, redshift z=0"
        
        return {
            'nom': nom,
            'tension': float(tension),
            'eta': float(eta),
            'type': type_objet,
            'description': description,
            'activation_P4': float(np.mean(np.abs(donnees[6:10]))) if len(donnees) > 10 else 0,
            'activation_N4': float(np.mean(np.abs(donnees[18:22]))) if len(donnees) > 22 else 0,
            'activation_P4p': float(np.mean(np.abs(donnees[24:28]))) if len(donnees) > 28 else 0,
            'activation_N4p': float(np.mean(np.abs(donnees[28:32]))) if len(donnees) > 32 else 0,
        }


# =====================================================================
# ANALYSEUR
# =====================================================================

class AnalyseurEHT:
    """Analyse les données EHT avec le modèle pentadique"""
    
    def __init__(self, chargeur, modele):
        self.chargeur = chargeur
        self.modele = modele
        self.resultats = []
        
    def analyser_tous(self):
        """Analyse tous les objets disponibles"""
        print("\n" + "="*70)
        print("ANALYSE DES OBJETS")
        print("="*70)
        
        for nom in self.chargeur.donnees.keys():
            donnees = self.chargeur.get_donnees(nom)
            if donnees is not None:
                resultat = self.modele.analyser_objet(donnees, nom)
                self.resultats.append(resultat)
                self._afficher_resultat(resultat)
        
        return self.resultats
    
    def _afficher_resultat(self, r):
        """Affiche le résultat d'une analyse"""
        print(f"\n{r['type']} {r['nom']}")
        print(f"   Tension: {r['tension']:.4f}")
        print(f"   η: {r['eta']:+.4f}")
        print(f"   {r['description']}")
        print(f"   Activations: P4={r['activation_P4']:.3f}, "
              f"N4={r['activation_N4']:.3f}, "
              f"P'4={r['activation_P4p']:.3f}, "
              f"N'4={r['activation_N4p']:.3f}")
    
    def comparer_resultats(self):
        """Compare les résultats entre objets"""
        if len(self.resultats) < 2:
            return
        
        print("\n" + "="*70)
        print("COMPARAISON DES OBJETS")
        print("="*70)
        
        # Trier par tension
        tries = sorted(self.resultats, key=lambda x: x['tension'], reverse=True)
        
        print(f"\n{'Objet':<15} {'Tension':<10} {'η':<10} {'Type':<25}")
        print("-" * 60)
        for r in tries:
            print(f"{r['nom']:<15} {r['tension']:<10.4f} {r['eta']:<+10.4f} {r['type']:<25}")
    
    def sauvegarder_resultats(self, fichier="resultats_eht.json"):
        """Sauvegarde les résultats dans un fichier JSON"""
        chemin = os.path.join(Config.DOSSIER_RESULTATS, fichier)
        
        # Ajouter métadonnées
        output = {
            'date': datetime.now().isoformat(),
            'nb_objets': len(self.resultats),
            'resultats': self.resultats
        }
        
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résultats sauvegardés dans {chemin}")


# =====================================================================
# VISUALISATION
# =====================================================================

class VisualisationEHT:
    """Visualisation des résultats d'analyse"""
    
    def __init__(self, analyseur):
        self.analyseur = analyseur
        self.resultats = analyseur.resultats
        
    def graphique_tensions(self):
        """Graphique des tensions par objet"""
        if not self.resultats:
            return
        
        plt.figure(figsize=(12, 6))
        
        noms = [r['nom'] for r in self.resultats]
        tensions = [r['tension'] for r in self.resultats]
        etas = [r['eta'] for r in self.resultats]
        
        x = np.arange(len(noms))
        width = 0.35
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Graphique des tensions
        bars1 = ax1.bar(x, tensions, width, color='skyblue', label='Tension')
        ax1.axhline(y=0.3, color='orange', linestyle='--', label='Seuil partiel')
        ax1.axhline(y=0.8, color='red', linestyle='--', label='Seuil actif')
        ax1.set_xlabel('Objet')
        ax1.set_ylabel('Tension')
        ax1.set_title('Tension de connexion par objet')
        ax1.set_xticks(x)
        ax1.set_xticklabels(noms, rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Ajouter les valeurs
        for bar, tension in zip(bars1, tensions):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{tension:.3f}', ha='center', va='bottom')
        
        # Graphique de η
        bars2 = ax2.bar(x, etas, width, color='lightgreen', label='η')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.set_xlabel('Objet')
        ax2.set_ylabel('η')
        ax2.set_title('Déséquilibre Sheng/Ke')
        ax2.set_xticks(x)
        ax2.set_xticklabels(noms, rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Ajouter les valeurs
        for bar, eta in zip(bars2, etas):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{eta:+.3f}', ha='center', va='bottom' if height > 0 else 'top')
        
        plt.tight_layout()
        
        # Sauvegarder
        chemin = os.path.join(Config.DOSSIER_RESULTATS, "graphique_tensions.png")
        plt.savefig(chemin, dpi=150)
        print(f"📊 Graphique sauvegardé: {chemin}")
        plt.show()
    
    def graphique_radar(self):
        """Graphique radar des activations"""
        if len(self.resultats) == 0:
            return
        
        categories = ['P4', 'N4', "P'4", "N'4"]
        N = len(categories)
        
        # Créer une figure avec sous-graphiques pour chaque objet
        n_objets = len(self.resultats)
        cols = min(3, n_objets)
        rows = (n_objets + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
        if rows == 1 and cols == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        for idx, resultat in enumerate(self.resultats):
            if idx >= len(axes):
                break
            
            ax = axes[idx]
            
            # Valeurs
            valeurs = [
                resultat['activation_P4'],
                resultat['activation_N4'],
                resultat['activation_P4p'],
                resultat['activation_N4p']
            ]
            
            # Compléter le cycle
            valeurs += valeurs[:1]
            angles = [n / N * 2 * np.pi for n in range(N)]
            angles += angles[:1]
            
            ax.plot(angles, valeurs, 'o-', linewidth=2, color='blue')
            ax.fill(angles, valeurs, alpha=0.25, color='blue')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, max(1, max(valeurs) * 1.1))
            ax.set_title(f"{resultat['nom']}\n{resultat['type']}")
            ax.grid(True)
        
        # Cacher les axes vides
        for idx in range(len(self.resultats), len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle("Profils d'activation des pentades seuil", fontsize=16)
        plt.tight_layout()
        
        # Sauvegarder
        chemin = os.path.join(Config.DOSSIER_RESULTATS, "graphique_radar.png")
        plt.savefig(chemin, dpi=150)
        print(f"📊 Graphique sauvegardé: {chemin}")
        plt.show()
    
    def rapport_texte(self):
        """Génère un rapport texte détaillé"""
        chemin = os.path.join(Config.DOSSIER_RESULTATS, "rapport_eht.txt")
        
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RAPPORT D'ANALYSE DES DONNÉES EHT\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            f.write("RÉSULTATS PAR OBJET:\n")
            f.write("-"*40 + "\n\n")
            
            for r in sorted(self.resultats, key=lambda x: x['tension'], reverse=True):
                f.write(f"{r['type']} {r['nom']}\n")
                f.write(f"  Tension: {r['tension']:.4f}\n")
                f.write(f"  η: {r['eta']:+.4f}\n")
                f.write(f"  {r['description']}\n")
                f.write(f"  Activations:\n")
                f.write(f"    P4 : {r['activation_P4']:.3f}\n")
                f.write(f"    N4 : {r['activation_N4']:.3f}\n")
                f.write(f"    P'4: {r['activation_P4p']:.3f}\n")
                f.write(f"    N'4: {r['activation_N4p']:.3f}\n\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("FIN DU RAPPORT\n")
            f.write("="*80 + "\n")
        
        print(f"📄 Rapport sauvegardé: {chemin}")


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("="*70)
    print("MODULE 6 : APPLICATION AUX DONNÉES EHT RÉELLES")
    print("="*70)
    
    # Initialisation
    chargeur = ChargeurDonnees()
    modele = ModelePentadique(Config.FICHIER_PENTADES)
    
    # Charger les données
    if not chargeur.charger_toutes_donnees():
        print("❌ Aucune donnée chargée - arrêt du programme")
        exit(1)
    
    chargeur.afficher_info()
    
    # Analyser
    analyseur = AnalyseurEHT(chargeur, modele)
    resultats = analyseur.analyser_tous()
    analyseur.comparer_resultats()
    analyseur.sauvegarder_resultats()
    
    # Visualiser
    visu = VisualisationEHT(analyseur)
    visu.graphique_tensions()
    visu.graphique_radar()
    visu.rapport_texte()
    
    print("\n" + "="*70)
    print("✅ MODULE 6 EXÉCUTÉ AVEC SUCCÈS")
    print("="*70)