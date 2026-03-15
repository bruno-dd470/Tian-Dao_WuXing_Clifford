#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 2 : ACTION DE PSL₂(7) SUR LES 7 GÉNÉRATEURS
Version avec simplification des expressions
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set
import json
import os
import re
from itertools import product

# =====================================================================
# REPRÉSENTATION DES 7 GÉNÉRATEURS
# =====================================================================

@dataclass
class Generateur7:
    nom: str
    indice: int
    
    def __repr__(self):
        return self.nom
    
    def __hash__(self):
        return hash(self.nom)
    
    def __eq__(self, other):
        if isinstance(other, Generateur7):
            return self.nom == other.nom
        return False

class Generateurs7:
    def __init__(self):
        self.i = Generateur7('i', 0)
        self.j = Generateur7('j', 1)
        self.k = Generateur7('k', 2)
        self.I = Generateur7('I', 3)
        self.J = Generateur7('J', 4)
        self.K = Generateur7('K', 5)
        self.i_prime = Generateur7("i'", 6)
        
        self.tous = [self.i, self.j, self.k, self.I, self.J, self.K, self.i_prime]
        self.par_nom = {g.nom: g for g in self.tous}
    
    def __getitem__(self, idx):
        return self.tous[idx]
    
    def __len__(self):
        return len(self.tous)


# =====================================================================
# GROUPE PSL₂(7)
# =====================================================================

class PSL2_7:
    def __init__(self):
        self.generateurs = {
            'S': [[0, -1], [1, 0]],
            'T': [[0, -1], [1, 1]],
            'U': [[1, 1], [0, 1]]
        }
    
    def action(self, matrice, point):
        a, b = matrice[0][0], matrice[0][1]
        c, d = matrice[1][0], matrice[1][1]
        
        if point == 6:
            return (a * pow(c, 5, 7)) % 7 if c != 0 else 6
        
        num = (a * point + b) % 7
        den = (c * point + d) % 7
        
        if den == 0:
            return 6
        return (num * pow(den, 5, 7)) % 7


# =====================================================================
# ACTION SUR LES GÉNÉRATEURS
# =====================================================================

class ActionPSL2_7:
    def __init__(self):
        self.gen = Generateurs7()
        self.psl2 = PSL2_7()
        
        self.point_to_gen = {
            0: self.gen.i, 1: self.gen.j, 2: self.gen.k,
            3: self.gen.I, 4: self.gen.J, 5: self.gen.K,
            6: self.gen.i_prime
        }
        self.gen_to_point = {g: p for p, g in self.point_to_gen.items()}
    
    def table_action(self):
        table = {}
        for nom, matrice in self.psl2.generateurs.items():
            mapping = {}
            image_vers_source = {}
            
            for g in self.gen.tous:
                point = self.gen_to_point[g]
                new_point = self.psl2.action(matrice, point)
                new_gen = self.point_to_gen[new_point]
                mapping[g.nom] = new_gen.nom
                
                if new_gen.nom in image_vers_source:
                    image_vers_source[new_gen.nom].append(g.nom)
                else:
                    image_vers_source[new_gen.nom] = [g.nom]
            
            non_bijectif = any(len(v) > 1 for v in image_vers_source.values())
            
            table[nom] = {
                'matrice': matrice,
                'mapping': mapping,
                'images': image_vers_source,
                'ordre': self._calculer_ordre(mapping),
                'non_bijectif': non_bijectif
            }
        return table
    
    def _calculer_ordre(self, mapping):
        vu = set()
        ordre = 1
        for depart in mapping:
            if depart not in vu:
                courant = depart
                cycle = []
                while courant not in vu:
                    vu.add(courant)
                    cycle.append(courant)
                    courant = mapping[courant]
                if cycle:
                    ordre = np.lcm(ordre, len(cycle))
        return ordre


# =====================================================================
# GÉOMÉTRIE
# =====================================================================

class GeometriePSL2_7:
    def __init__(self, action):
        self.action = action
        self.gen = action.gen
    
    def plan_fano(self):
        droites = [
            [0, 1, 3], [1, 2, 4], [2, 3, 5],
            [3, 4, 6], [4, 5, 0], [5, 6, 1], [6, 0, 2]
        ]
        return [[self.gen.tous[p].nom for p in droite] for droite in droites]


# =====================================================================
# TRANSFORMATION DES PENTADES - AVEC SIMPLIFICATION
# =====================================================================

class TransformateurPentades:
    def __init__(self, fichier_pentades="pentades_72_finales.json"):
        self.fichier = fichier_pentades
        self.pentades = []
        self.charger_pentades()
    
    def charger_pentades(self):
        if not os.path.exists(self.fichier):
            print(f"⚠ Fichier {self.fichier} non trouvé")
            return
        
        with open(self.fichier, 'r', encoding='utf-8') as f:
            self.pentades = json.load(f)
        print(f"✅ {len(self.pentades)} pentades chargées")
    
    def _simplifier_expression(self, expr):
        """
        Simplifie les expressions comme i''i' → i'
        """
        if not isinstance(expr, str):
            return expr
        
        # Remplacer les doubles i' par un seul
        expr = re.sub(r"i''+", "i'", expr)
        
        # Remplacer les séquences comme i'i' par i'
        expr = re.sub(r"i'i'", "i'", expr)
        
        # Supprimer les i' en trop
        if expr.count("i'") > 1:
            expr = "i'"
        
        return expr
    
    def _remplacer_sequence(self, chaine, mapping):
        """
        Remplace les générateurs dans l'ordre correct et simplifie
        """
        if not isinstance(chaine, str):
            return chaine
        
        # Préserver le signe
        signe = ''
        if chaine.startswith('-'):
            signe = '-'
            chaine = chaine[1:]
        
        # Remplacer dans l'ordre spécifique
        resultat = chaine
        ordre = ["i'", "i", "j", "k", "I", "J", "K"]
        
        # Compter les remplacements pour éviter les boucles infinies
        max_iter = 10
        for _ in range(max_iter):
            ancien = resultat
            for gen in ordre:
                if gen in resultat:
                    resultat = resultat.replace(gen, mapping.get(gen, gen))
            if ancien == resultat:
                break
        
        # Simplifier le résultat
        resultat = self._simplifier_expression(resultat)
        
        return signe + resultat
    
    def appliquer_mapping(self, nom, mapping, images=None):
        """
        Applique un mapping aux pentades
        """
        print(f"\n🔷 Transformation {nom}:")
        if images:
            non_bijectifs = {cible: sources for cible, sources in images.items() 
                           if len(sources) > 1}
            if non_bijectifs:
                print("   ⚠ Conflits de mapping:")
                for cible, sources in non_bijectifs.items():
                    print(f"      {sources} → {cible}")
        
        transformations = []
        familles_vues = set()
        
        for p in self.pentades:
            if p['famille'] not in familles_vues and len(transformations) < 6:
                familles_vues.add(p['famille'])
                
                nouveaux = []
                for elem in p['elements']:
                    nouveau = self._remplacer_sequence(elem, mapping)
                    nouveaux.append(nouveau)
                
                transformations.append({
                    'famille': p['famille'],
                    'signe': p['signe'],
                    'original': p['elements'],
                    'transforme': nouveaux
                })
        
        return transformations


# =====================================================================
# VISUALISATION
# =====================================================================

class Visualisation:
    @staticmethod
    def afficher_table(table, gen):
        print("\n" + "="*70)
        print("TABLE D'ACTION DE PSL₂(7) SUR LES 7 GÉNÉRATEURS")
        print("="*70)
        
        for nom, data in table.items():
            print(f"\n🔷 Générateur '{nom}' (ordre {data['ordre']})")
            if data['non_bijectif']:
                print("   ⚠ Mapping non bijectif")
            print(f"   Matrice: {data['matrice'][0]} / {data['matrice'][1]}")
            print("   Mapping:")
            for g in gen.tous:
                print(f"      {g.nom} → {data['mapping'][g.nom]}")
    
    @staticmethod
    def afficher_plan_fano(droites):
        print("\n" + "="*70)
        print("CORRESPONDANCE AVEC LE PLAN DE FANO")
        print("="*70)
        for i, droite in enumerate(droites):
            print(f"  Droite {i+1}: {' — '.join(droite)}")
    
    @staticmethod
    def afficher_transformations(transformees, nom):
        print(f"\n🔷 Résultats pour {nom}:")
        for t in transformees:
            print(f"  {t['famille']} {'+' if t['signe']==1 else '-'}:")
            print(f"    {', '.join(t['original'])}")
            print(f"    → {', '.join(t['transforme'])}")


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("="*70)
    print("MODULE 2 : ACTION DE PSL₂(7) SUR LES 7 GÉNÉRATEURS")
    print("="*70)
    
    # Initialisation
    action = ActionPSL2_7()
    geo = GeometriePSL2_7(action)
    visu = Visualisation()
    table = action.table_action()
    
    # Affichage
    visu.afficher_table(table, action.gen)
    visu.afficher_plan_fano(geo.plan_fano())
    
    # Transformation des pentades
    print("\n" + "="*70)
    print("APPLICATION AUX PENTADES")
    print("="*70)
    
    transformateur = TransformateurPentades("pentades_72_finales.json")
    
    for nom in ['S', 'T', 'U']:
        data = table[nom]
        transformees = transformateur.appliquer_mapping(
            f"{nom} (ordre {data['ordre']})",
            data['mapping'],
            data.get('images')
        )
        visu.afficher_transformations(transformees, nom)
    
    print("\n" + "="*70)
    print("✅ MODULE 2 EXÉCUTÉ AVEC SUCCÈS")
    print("="*70)