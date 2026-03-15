#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 7 : VISUALISATION 3D DU RÉSEAU Γ - VERSION CORRIGÉE
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyBboxPatch
from matplotlib.collections import LineCollection
import json
import os
from datetime import datetime
import colorsys

# =====================================================================
# CONFIGURATION
# =====================================================================

class Config:
    """Configuration pour la visualisation 3D"""
    
    # Fichiers de données
    FICHIER_PENTADES = "pentades_72_finales.json"
    FICHIER_RESULTATS = "resultats_eht/resultats_eht.json"
    
    # Mapping des familles vers indices
    FAMILLE_TO_INDEX = {
        'FI': 0, 'FII': 1, 'FIII': 2, 
        'FIV': 3, 'FV': 4, 'FVI': 5
    }
    
    # Couleurs par famille
    COULEURS_FAMILLES = {
        'FI': '#FF6B6B',  # rouge
        'FII': '#4ECDC4', # turquoise
        'FIII': '#45B7D1', # bleu
        'FIV': '#96CEB4', # vert
        'FV': '#FFEEAD',  # jaune
        'FVI': '#D4A5A5', # rose
    }
    
    # Couleurs par type
    COULEURS_TYPE = {
        '🌟 PLUGSTAR ACTIVE': '#FF4444',
        '✨ PLUGSTAR PARTIELLE': '#FFA500',
        '⚫ PLUGSTAR FERMÉE': '#888888',
    }
    
    # Dimensions de la figure
    FIG_SIZE = (16, 10)
    DPI = 150


# =====================================================================
# GÉNÉRATEUR DE COORDONNÉES 3D
# =====================================================================

class GenerateurCoordonnees:
    """Génère des coordonnées 3D pour les pentades"""
    
    def __init__(self):
        self.positions = {}
        self.connexions = []
        
    def generer_positions_sphere(self, n_points, rayon=1.0):
        """
        Génère des positions sur une sphère (distribution de Fibonacci)
        """
        positions = []
        phi = np.pi * (3 - np.sqrt(5))  # angle d'or
        
        for i in range(n_points):
            y = 1 - (i / (n_points - 1)) * 2  # y de 1 à -1
            radius = np.sqrt(1 - y * y)
            theta = phi * i
            
            x = np.cos(theta) * radius
            z = np.sin(theta) * radius
            
            positions.append((x * rayon, y * rayon, z * rayon))
        
        return positions
    
    def generer_positions_tore(self, n_points, R=2.0, r=0.5):
        """
        Génère des positions sur un tore
        """
        positions = []
        for i in range(n_points):
            u = 2 * np.pi * i / n_points
            v = 2 * np.pi * (i * 7) / n_points  # deuxième angle
            
            x = (R + r * np.cos(v)) * np.cos(u)
            y = (R + r * np.cos(v)) * np.sin(u)
            z = r * np.sin(v)
            
            positions.append((x, y, z))
        
        return positions
    
    def generer_positions_reseau(self, pentades):
        """
        Génère les positions 3D pour toutes les pentades
        """
        n = len(pentades)
        
        # Position sur une sphère pour la vue d'ensemble
        positions_sphere = self.generer_positions_sphere(n, rayon=3.0)
        
        # Position sur un tore pour la vue cyclique
        positions_tore = self.generer_positions_tore(n, R=3.0, r=1.0)
        
        # Mélanger les deux pour plus de variété
        for i, p in enumerate(pentades):
            # Récupérer l'indice de la famille (CORRECTION)
            famille = p['famille']
            idx_famille = Config.FAMILLE_TO_INDEX.get(famille, 0)
            
            # Interpolation entre sphère et tore
            t = idx_famille / 5.0  # 5 car 6 familles de 0 à 5
            pos_sphere = positions_sphere[i % len(positions_sphere)]
            pos_tore = positions_tore[i % len(positions_tore)]
            
            x = pos_sphere[0] * (1 - t) + pos_tore[0] * t
            y = pos_sphere[1] * (1 - t) + pos_tore[1] * t
            z = pos_sphere[2] * (1 - t) + pos_tore[2] * t
            
            # Ajouter un peu de bruit pour éviter les superpositions parfaites
            x += np.random.normal(0, 0.1)
            y += np.random.normal(0, 0.1)
            z += np.random.normal(0, 0.1)
            
            self.positions[f"{famille}_{i}"] = (x, y, z)
        
        return self.positions
    
    def generer_connexions(self, pentades, rayon=2.5):
        """
        Génère les connexions entre pentades proches
        """
        self.connexions = []
        
        # Créer une liste de positions avec indices
        items = list(self.positions.items())
        
        for i, (nom1, pos1) in enumerate(items):
            for j, (nom2, pos2) in enumerate(items[i+1:], i+1):
                # Distance
                dist = np.sqrt(sum((a - b)**2 for a, b in zip(pos1, pos2)))
                
                # Connexion si proche
                if dist < rayon * 0.8:
                    # Vérifier si même famille
                    famille1 = nom1.split('_')[0]
                    famille2 = nom2.split('_')[0]
                    
                    self.connexions.append({
                        'de': nom1,
                        'vers': nom2,
                        'distance': dist,
                        'meme_famille': famille1 == famille2
                    })
        
        # Trier par distance et garder les plus significatives
        self.connexions.sort(key=lambda x: x['distance'])
        self.connexions = self.connexions[:min(300, len(self.connexions))]
        
        return self.connexions


# =====================================================================
# CHARGEUR DE DONNÉES
# =====================================================================

class ChargeurDonnees:
    """Charge les pentades et les résultats d'analyse"""
    
    def __init__(self):
        self.pentades = []
        self.resultats = {}
        self.activations = {}
        
    def charger_pentades(self, fichier=Config.FICHIER_PENTADES):
        """Charge les pentades depuis le fichier JSON"""
        if not os.path.exists(fichier):
            print(f"⚠ Fichier {fichier} non trouvé")
            return False
        
        with open(fichier, 'r', encoding='utf-8') as f:
            self.pentades = json.load(f)
        
        print(f"📚 {len(self.pentades)} pentades chargées")
        return True
    
    def charger_resultats(self, fichier=Config.FICHIER_RESULTATS):
        """Charge les résultats d'analyse EHT"""
        if not os.path.exists(fichier):
            print(f"⚠ Fichier {fichier} non trouvé")
            return False
        
        with open(fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for r in data['resultats']:
            self.resultats[r['nom']] = r
        
        print(f"📊 {len(self.resultats)} résultats d'analyse chargés")
        return True
    
    def get_couleur_pentade(self, pentade):
        """
        Détermine la couleur d'une pentade
        """
        famille = pentade['famille']
        return Config.COULEURS_FAMILLES.get(famille, '#999999')
    
    def get_taille_pentade(self, pentade):
        """
        Détermine la taille d'une pentade
        """
        # Taille de base
        taille_base = 80
        
        # Variation par famille
        famille = pentade['famille']
        idx = Config.FAMILLE_TO_INDEX.get(famille, 0)
        
        return taille_base + idx * 10


# =====================================================================
# VISUALISATEUR 3D
# =====================================================================

class Visualisateur3D:
    """Visualisation 3D du réseau de pentades"""
    
    def __init__(self, chargeur, generateur):
        self.chargeur = chargeur
        self.generateur = generateur
        self.fig = None
        self.ax = None
        
    def creer_figure(self):
        """Crée la figure 3D"""
        self.fig = plt.figure(figsize=Config.FIG_SIZE, dpi=Config.DPI)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#f0f0f0')
        
    def ajouter_pentades(self):
        """Ajoute les pentades comme points 3D"""
        if not self.generateur.positions:
            return
        
        xs, ys, zs = [], [], []
        couleurs = []
        tailles = []
        noms = []
        
        for nom, pos in self.generateur.positions.items():
            xs.append(pos[0])
            ys.append(pos[1])
            zs.append(pos[2])
            
            # Extraire la famille du nom
            famille = nom.split('_')[0]
            couleur = Config.COULEURS_FAMILLES.get(famille, '#999999')
            couleurs.append(couleur)
            
            # Taille basée sur l'importance
            taille = 50 + (hash(nom) % 50)
            tailles.append(taille)
            
            noms.append(nom)
        
        # Tracer les points
        scatter = self.ax.scatter(xs, ys, zs, 
                                 c=couleurs, 
                                 s=tailles, 
                                 alpha=0.7,
                                 edgecolors='white',
                                 linewidth=0.5)
        
        return scatter
    
    def ajouter_connexions(self):
        """Ajoute les connexions entre pentades"""
        if not self.generateur.connexions:
            return
        
        for conn in self.generateur.connexions:
            if conn['de'] in self.generateur.positions and conn['vers'] in self.generateur.positions:
                pos1 = self.generateur.positions[conn['de']]
                pos2 = self.generateur.positions[conn['vers']]
                
                # Style selon la connexion
                if conn['meme_famille']:
                    self.ax.plot([pos1[0], pos2[0]], 
                                [pos1[1], pos2[1]], 
                                [pos1[2], pos2[2]], 
                                color='#cccccc', 
                                alpha=0.3,
                                linewidth=0.5)
                else:
                    self.ax.plot([pos1[0], pos2[0]], 
                                [pos1[1], pos2[1]], 
                                [pos1[2], pos2[2]], 
                                color='#999999', 
                                alpha=0.15,
                                linewidth=0.3)
    
    def ajouter_legende(self):
        """Ajoute une légende pour les familles"""
        from matplotlib.patches import Patch
        
        legend_elements = []
        for famille, couleur in Config.COULEURS_FAMILLES.items():
            legend_elements.append(Patch(facecolor=couleur, 
                                       label=f'Famille {famille}'))
        
        self.ax.legend(handles=legend_elements, 
                      loc='upper left', 
                      bbox_to_anchor=(0, 1),
                      frameon=True,
                      facecolor='white',
                      edgecolor='none',
                      fontsize=10)
    
    def ajouter_titre(self):
        """Ajoute un titre"""
        titre = "Réseau 72D des pentades - Projection 3D"
        if self.chargeur.resultats:
            objets = ', '.join(self.chargeur.resultats.keys())
            titre += f"\nObjets analysés: {objets}"
        
        self.ax.set_title(titre, fontsize=14, pad=20)
    
    def configurer_axes(self):
        """Configure les axes 3D"""
        self.ax.set_xlabel('X', fontsize=10, labelpad=10)
        self.ax.set_ylabel('Y', fontsize=10, labelpad=10)
        self.ax.set_zlabel('Z', fontsize=10, labelpad=10)
        
        # Définir les limites
        self.ax.set_xlim(-4.5, 4.5)
        self.ax.set_ylim(-4.5, 4.5)
        self.ax.set_zlim(-4.5, 4.5)
        
        # Grille
        self.ax.grid(True, alpha=0.2)
    
    def ajouter_annotations(self):
        """Ajoute des annotations pour les objets analysés"""
        if not self.chargeur.resultats:
            return
        
        # Position des objets dans le réseau
        positions_objets = {
            'M87': (2.0, 2.0, 2.0),
            'SGRA': (-2.0, -2.0, 2.0),
            'CENTAURUS_A': (2.0, -2.0, -2.0),
            '3C279': (-2.0, 2.0, -2.0),
        }
        
        for nom, res in self.chargeur.resultats.items():
            if nom in positions_objets:
                pos = positions_objets[nom]
                
                # Déterminer la couleur selon le type
                type_objet = res['type']
                if 'ACTIVE' in type_objet:
                    couleur = '#FF4444'
                elif 'PARTIELLE' in type_objet:
                    couleur = '#FFA500'
                else:
                    couleur = '#888888'
                
                self.ax.text(pos[0], pos[1], pos[2], 
                           f"{nom}\nT={res['tension']:.2f}",
                           fontsize=9,
                           color='black',
                           weight='bold',
                           ha='center',
                           va='center',
                           bbox=dict(boxstyle="round,pad=0.3",
                                   facecolor=couleur,
                                   alpha=0.9,
                                   edgecolor='white',
                                   linewidth=1))
    
    def sauvegarder(self, nom="reseau_3d.png"):
        """Sauvegarde la figure"""
        chemin = os.path.join("resultats_eht", nom)
        self.fig.savefig(chemin, dpi=Config.DPI, bbox_inches='tight')
        print(f"💾 Figure sauvegardée: {chemin}")
    
    def afficher(self):
        """Affiche la figure"""
        plt.tight_layout()
        plt.show()


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("="*70)
    print("MODULE 7 : VISUALISATION 3D DU RÉSEAU Γ")
    print("="*70)
    
    # Créer le dossier des résultats si nécessaire
    if not os.path.exists("resultats_eht"):
        os.makedirs("resultats_eht")
    
    # Initialisation
    chargeur = ChargeurDonnees()
    generateur = GenerateurCoordonnees()
    
    # Charger les données
    if not chargeur.charger_pentades():
        print("❌ Impossible de charger les pentades")
        exit(1)
    
    chargeur.charger_resultats()
    
    # Générer les positions
    print("\n🔷 Génération des positions 3D...")
    positions = generateur.generer_positions_reseau(chargeur.pentades)
    print(f"✅ {len(positions)} positions générées")
    
    # Générer les connexions
    print("🔷 Génération des connexions...")
    connexions = generateur.generer_connexions(chargeur.pentades, rayon=2.5)
    print(f"✅ {len(connexions)} connexions générées")
    
    # Visualisation 3D
    print("\n🔷 Création de la visualisation 3D...")
    visu = Visualisateur3D(chargeur, generateur)
    visu.creer_figure()
    visu.ajouter_pentades()
    visu.ajouter_connexions()
    visu.ajouter_legende()
    visu.ajouter_titre()
    visu.configurer_axes()
    visu.ajouter_annotations()
    visu.sauvegarder("reseau_3d.png")
    visu.afficher()
    
    print("\n" + "="*70)
    print("✅ MODULE 7 EXÉCUTÉ AVEC SUCCÈS")
    print("="*70)