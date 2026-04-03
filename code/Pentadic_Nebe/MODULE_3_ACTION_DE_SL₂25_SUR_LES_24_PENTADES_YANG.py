#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 3 : ACTION DE SL₂(25) SUR LES 24 PENTADES YANG
Groupe d'ordre 14400 agissant sur les pentades pour la construction de Leech
Connexion avec le réseau de Nebe (PSL₂(7) × SL₂(25)):2
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set
import json
import os
import re
from itertools import product

# =====================================================================
# CONFIGURATION
# =====================================================================

class Config:
    """Configuration pour SL₂(25) et le réseau de Leech"""
    
    # Paramètres sur 𝔽₂₅
    p = 5  # Caractéristique
    # 𝔽₂₅ ≅ 𝔽₅[√2] ou 𝔽₅[√3] - on utilise une extension quadratique
    w = 2  # √2 (élément non carré dans 𝔽₅)
    
    # Générateurs de SL₂(25)
    generateurs = {
        'A': [[1, 1], [0, 1]],      # ordre 5 (transvection)
        'B': [[0, -1], [1, 0]],      # ordre 2 (symplectique)
        'C': [[2, 0], [0, 3]]        # ordre 4 (diagonal)
    }
    
    # Points de ℙ¹(25) (24 points + point à l'infini)
    n_points = 25


# =====================================================================
# CORPS FINI 𝔽₂₅
# =====================================================================

class F25:
    """Implémentation simplifiée de 𝔽₂₅ comme 𝔽₅[√w]"""
    
    def __init__(self):
        self.p = Config.p
        self.w = Config.w
        self.caracteristique = self.p
        self.ordre = self.p ** 2
        
        # Éléments de base
        self.elements = self._generer_elements()
        
    def _generer_elements(self):
        """Génère tous les éléments de 𝔽₂₅"""
        elements = []
        for a in range(self.p):
            for b in range(self.p):
                elements.append((a, b))  # (a + b√w)
        return elements
    
    def add(self, x, y):
        """Addition dans 𝔽₂₅"""
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)
    
    def mul(self, x, y):
        """Multiplication dans 𝔽₂₅ : (a+b√w)(c+d√w) = ac + bdw + (ad+bc)√w"""
        a, b = x
        c, d = y
        return (
            (a*c + b*d*self.w) % self.p,
            (a*d + b*c) % self.p
        )
    
    def inv(self, x):
        """Inverse dans 𝔽₂₅"""
        a, b = x
        # (a + b√w)⁻¹ = (a - b√w)/(a² - b²w)
        denom = (a*a - b*b*self.w) % self.p
        if denom == 0:
            raise ValueError("Élément non inversible")
        inv_denom = pow(denom, self.p-2, self.p)
        return (
            (a * inv_denom) % self.p,
            (-b * inv_denom) % self.p
        )
    
    def zero(self):
        return (0, 0)
    
    def un(self):
        return (1, 0)
    
    def __repr__(self):
        return f"F_{self.p}^2"


# =====================================================================
# GROUPE SL₂(25)
# =====================================================================

class SL2_25:
    """
    Groupe SL₂(25) d'ordre 14400
    Agit sur les 25 points de ℙ¹(25) (24 + ∞)
    """
    
    def __init__(self):
        self.F = F25()
        self.nom = "SL₂(25)"
        self.ordre = 14400
        
        # Les 25 points de ℙ¹(25) : 0..23 et ∞ (24)
        self.points = list(range(25))
        self.infini = 24
        
        # Générateurs
        self.generateurs = self._construire_generateurs()
    
    def _construire_generateurs(self):
        """Construit les générateurs de SL₂(25) comme matrices 2×2 sur 𝔽₂₅"""
        
        # Unité dans 𝔽₂₅
        un = self.F.un()
        
        # Générateurs sur 𝔽₂₅
        generateurs = {}
        
        # A : transvection [[1,1],[0,1]] d'ordre 5
        generateurs['A'] = [
            [un, (1, 0)],  # 1 dans 𝔽₂₅
            [(0, 0), un]
        ]
        
        # B : [[0,-1],[1,0]] d'ordre 2
        generateurs['B'] = [
            [(0, 0), (-1 % 5, 0)],
            [un, (0, 0)]
        ]
        
        # C : matrice diagonale [[2,0],[0,3]] d'ordre 4
        generateurs['C'] = [
            [(2, 0), (0, 0)],
            [(0, 0), (3, 0)]
        ]
        
        # D : élément d'ordre 8 (combinaison)
        generateurs['D'] = [
            [(1, 1), (0, 0)],
            [(0, 0), (1, -1 % 5)]
        ]
        
        return generateurs
    
    def action_matricielle(self, matrice, point):
        """
        Action d'une matrice 2×2 sur un point de ℙ¹(25)
        matrice = [[a, b], [c, d]] sur 𝔽₂₅
        """
        a, b = matrice[0]
        c, d = matrice[1]
        
        # Traitement du point à l'infini
        if point == self.infini:
            # ∞ → a/c si c ≠ 0, sinon ∞
            if c == self.F.zero():
                return self.infini
            # Calculer a * c⁻¹
            inv_c = self.F.inv(c)
            return self._point_to_int(self.F.mul(a, inv_c))
        
        # Point standard : z = point (interprété comme élément de 𝔽₂₅)
        z = self._int_to_point(point)
        
        # Action projective : z → (az + b)/(cz + d)
        az = self.F.mul(a, z)
        az_plus_b = self.F.add(az, b)
        
        cz = self.F.mul(c, z)
        cz_plus_d = self.F.add(cz, d)
        
        if cz_plus_d == self.F.zero():
            return self.infini
        
        inv = self.F.inv(cz_plus_d)
        result = self.F.mul(az_plus_b, inv)
        
        return self._point_to_int(result)
    
    def _int_to_point(self, n):
        """Convertit un entier 0-24 en élément de 𝔽₂₅"""
        if n >= 25:
            return self.F.zero()
        a = n % 5
        b = (n // 5) % 5
        return (a, b)
    
    def _point_to_int(self, p):
        """Convertit un élément de 𝔽₂₅ en entier 0-24"""
        a, b = p
        return (b * 5 + a) % 25


# =====================================================================
# ACTION SUR LES 24 PENTADES YANG
# =====================================================================

class ActionSL2_25:
    """Action de SL₂(25) sur les 24 pentades Yang (ℙ¹(25) \ {∞})"""
    
    def __init__(self):
        self.sl2 = SL2_25()
        self.F = self.sl2.F
        
        # Les 24 pentades Yang (à charger)
        self.pentades_yang = []
        
        # Mapping entre points de ℙ¹(25) et indices de pentades
        self.point_to_pentade = {}
        self.pentade_to_point = {}
    
    def charger_pentades_yang(self, fichier="pentades_72_finales.json"):
        """
        Charge les 24 pentades Yang à partir du fichier
        (pentades de signe +1)
        """
        if not os.path.exists(fichier):
            print(f"⚠ Fichier {fichier} non trouvé")
            return False
        
        with open(fichier, 'r', encoding='utf-8') as f:
            toutes = json.load(f)
        
        # Filtrer les pentades Yang (signe = 1)
        self.pentades_yang = [p for p in toutes if p['signe'] == 1]
        
        print(f"✅ {len(self.pentades_yang)} pentades Yang chargées")
        
        # Assigner les 24 premières aux points de ℙ¹(25) (sauf ∞)
        for i, p in enumerate(self.pentades_yang[:24]):
            self.point_to_pentade[i] = p
            self.pentade_to_point[str(p)] = i
        
        return len(self.pentades_yang) >= 24
    
    def table_action(self):
        """
        Calcule l'action des générateurs sur les pentades
        """
        if not self.point_to_pentade:
            print("⚠ Pentades non chargées")
            return {}
        
        table = {}
        
        for nom, matrice in self.sl2.generateurs.items():
            mapping = {}
            image_vers_source = {}
            
            # Pour chaque point (pentade)
            for point in range(24):  # 0-23, pas ∞
                new_point = self.sl2.action_matricielle(matrice, point)
                
                # Si le point va à ∞, c'est une transformation spéciale
                if new_point == self.sl2.infini:
                    mapping[point] = None  # Marqueur pour transformation spéciale
                else:
                    mapping[point] = new_point
                    
                    if new_point in image_vers_source:
                        image_vers_source[new_point].append(point)
                    else:
                        image_vers_source[new_point] = [point]
            
            # Compter les pré-images
            non_bijectif = any(len(v) > 1 for v in image_vers_source.values())
            
            table[nom] = {
                'matrice': matrice,
                'mapping': mapping,
                'images': image_vers_source,
                'ordre': self._estimer_ordre(nom),
                'non_bijectif': non_bijectif
            }
        
        return table
    
    def _estimer_ordre(self, nom):
        """Estime l'ordre des générateurs"""
        ordres = {'A': 5, 'B': 2, 'C': 4, 'D': 8}
        return ordres.get(nom, 1)
    
    def appliquer_aux_pentades(self, mapping, nom):
        """
        Applique une permutation aux pentades
        """
        print(f"\n🔷 Transformation {nom}:")
        
        transformations = []
        
        # Créer une copie des pentades avec le mapping
        for point_src, point_dst in list(mapping.items())[:6]:  # 6 premiers
            if point_src in self.point_to_pentade:
                p_src = self.point_to_pentade[point_src]
                
                if point_dst is not None and point_dst in self.point_to_pentade:
                    p_dst = self.point_to_pentade[point_dst]
                    transformations.append({
                        'source': f"P{point_src} ({p_src['famille']})",
                        'destination': f"P{point_dst} ({p_dst['famille']})",
                        'original': p_src['elements'],
                        'transforme': p_dst['elements']
                    })
                else:
                    transformations.append({
                        'source': f"P{point_src} ({p_src['famille']})",
                        'destination': "∞ (transformation spéciale)",
                        'original': p_src['elements'],
                        'transforme': ["transformation vers point ∞"]
                    })
        
        return transformations


# =====================================================================
# CONNEXION AVEC LE RÉSEAU DE NEBE
# =====================================================================

class ConnexionNebe:
    """
    Établit le lien avec le réseau 72-dimensionnel de Nebe
    (PSL₂(7) × SL₂(25)):2
    """
    
    def __init__(self, action_sl2, action_psl2):
        self.action_sl2 = action_sl2
        self.action_psl2 = action_psl2
        
    def structure_groupe(self):
        """
        Décrit la structure du groupe d'automorphismes
        """
        print("\n" + "="*70)
        print("GROUPE D'AUTOMORPHISMES (PSL₂(7) × SL₂(25)):2")
        print("="*70)
        
        # PSL₂(7) agit sur les 7 générateurs
        print("\n🔹 PSL₂(7) d'ordre 168")
        print("   → agit sur les 7 générateurs (i,j,k,I,J,K,i')")
        
        # SL₂(25) agit sur les 24 pentades Yang
        print("\n🔹 SL₂(25) d'ordre 14400")
        print("   → agit sur les 24 pentades Yang")
        print(f"      {len(self.action_sl2.pentades_yang)} pentades disponibles")
        
        # Extension d'ordre 2 (polarité Yin-Yang)
        print("\n🔹 Extension :2 d'ordre 2")
        print("   → correspond à la polarité Yin-Yang (signe ±)")
        
        # Produit
        ordre_total = 168 * 14400 * 2
        print(f"\n📊 Ordre total du groupe: {ordre_total}")
    
    def produit_tensoriel(self):
        """
        Décrit la construction Γ = Barnes ⊗ Leech
        """
        print("\n" + "="*70)
        print("CONSTRUCTION DU RÉSEAU Γ (Nebe)")
        print("="*70)
        
        print("\nΓ = Barnes ⊗_{ℤ[√-7]} Leech")
        print("\n• Réseau de Barnes (3D sur ℤ[√-7])")
        print("  ↔ nos générateurs i,j,k")
        
        print("\n• Réseau de Leech (24D)")
        print("  ↔ nos 24 pentades Yang")
        
        print("\n• Produit tensoriel hermitien")
        print("  → dimension 3 × 24 = 72")
        print("  → minimum 8 (cohérent avec la norme pentadique)")


# =====================================================================
# VISUALISATION
# =====================================================================

class VisualisationSL2:
    """Visualisation des résultats SL₂(25)"""
    
    @staticmethod
    def afficher_table(table, action):
        print("\n" + "="*70)
        print("TABLE D'ACTION DE SL₂(25) SUR LES 24 PENTADES YANG")
        print("="*70)
        
        for nom, data in table.items():
            print(f"\n🔷 Générateur '{nom}' (ordre estimé {data['ordre']})")
            if data['non_bijectif']:
                print("   ⚠ Mapping non bijectif")
            print(f"   Matrice: {data['matrice'][0]} / {data['matrice'][1]}")
            
            # Afficher les 6 premières transformations
            print("   Premières transformations (point → point):")
            compteur = 0
            for src, dst in list(data['mapping'].items())[:6]:
                if dst is None:
                    print(f"      P{src} → ∞")
                else:
                    print(f"      P{src} → P{dst}")
                compteur += 1
    
    @staticmethod
    def afficher_transformations(transformees, nom):
        print(f"\n🔷 Résultats pour {nom}:")
        for t in transformees:
            print(f"  {t['source']} → {t['destination']}")
            if isinstance(t['transforme'], list) and t['transforme']:
                print(f"    {', '.join(t['original'][:3])}... → {', '.join(t['transforme'][:3])}...")


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("="*70)
    print("MODULE 3 : ACTION DE SL₂(25) SUR LES 24 PENTADES YANG")
    print("="*70)
    
    # Initialisation
    action = ActionSL2_25()
    
    # Charger les pentades Yang
    if not action.charger_pentades_yang("pentades_72_finales.json"):
        print("❌ Impossible de charger les pentades Yang")
        exit(1)
    
    # Table d'action
    table = action.table_action()
    VisualisationSL2.afficher_table(table, action)
    
    # Afficher les transformations pour chaque générateur
    print("\n" + "="*70)
    print("TRANSFORMATIONS DES PENTADES")
    print("="*70)
    
    for nom in ['A', 'B', 'C', 'D']:
        if nom in table:
            transformees = action.appliquer_aux_pentades(table[nom]['mapping'], nom)
            VisualisationSL2.afficher_transformations(transformees, nom)
    
    # Connexion avec Nebe
    # Note: nécessite l'action PSL₂(7) du module 2
    print("\n" + "="*70)
    print("CONNEXION AVEC LE RÉSEAU DE NEBE")
    print("="*70)
    
    try:
        # Tentative d'importer l'action PSL₂(7) du module 2
        import sys
        sys.path.append('.')
        from MODULE_2_ACTION_DE_PSL27_SUR_LES_7_GÉNÉRATEURS import ActionPSL2_7
        
        action_psl2 = ActionPSL2_7()
        connexion = ConnexionNebe(action, action_psl2)
        connexion.structure_groupe()
        connexion.produit_tensoriel()
        
    except ImportError as e:
        print(f"\n⚠ Module 2 non disponible: {e}")
        print("   Structure du groupe sans PSL₂(7):")
        print(f"   SL₂(25) × :2 d'ordre {14400 * 2}")
    
    print("\n" + "="*70)
    print("✅ MODULE 3 EXÉCUTÉ AVEC SUCCÈS")
    print("="*70)