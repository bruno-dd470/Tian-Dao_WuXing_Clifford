#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 1 : CONSTRUCTION DES 72 PENTADES - VERSION FINALE AVEC TOUTES LES CORRECTIONS
6 familles × 6 structures × 2 signes = 72 pentades
Toutes les pentades contiennent les 6 générateurs
"""

import json
from dataclasses import dataclass
from typing import List, Tuple, Set
from collections import Counter

# =====================================================================
# CLASSE POUR UNE PENTADE
# =====================================================================

@dataclass
class Pentade:
    """Une pentade : 3 bivecteurs + Feu + Eau"""
    structure: Tuple[str, str, str]
    feu: str
    eau: str
    signe: int = 1
    famille: str = ""
    
    def __post_init__(self):
        self.elements = list(self.structure) + [self.feu, self.eau]
        if self.signe == -1:
            self.elements = [f"-{e}" if not e.startswith('-') else e[1:] 
                             for e in self.elements]
    
    def generateurs_presents(self) -> Set[str]:
        presents = set()
        for e in self.elements:
            e_str = str(e).replace('-', '')
            for gen in ['i', 'j', 'k', 'I', 'J', 'K']:
                if gen in e_str:
                    presents.add(gen)
        return presents
    
    def est_valide(self) -> bool:
        return len(self.generateurs_presents()) == 6
    
    def __repr__(self):
        sign = "+" if self.signe == 1 else "-"
        return f"P{sign}({','.join(str(e) for e in self.elements)})"
    
    def to_dict(self):
        return {
            'famille': self.famille,
            'signe': self.signe,
            'structure': list(self.structure),
            'feu': self.feu,
            'eau': self.eau,
            'elements': [str(e) for e in self.elements],
            'generateurs': sorted(list(self.generateurs_presents()))
        }


# =====================================================================
# CONSTRUCTION DES 72 PENTADES - TOUTES LES FAMILLES AVEC 6 STRUCTURES
# =====================================================================

def construire_toutes_pentades() -> List[Pentade]:
    """Construit les 72 pentades : 6 familles × 6 structures × 2 signes"""
    
    pentades = []
    
    # ===== FAMILLE I : DIRECTE (Rowlands) =====
    famille = "FI"
    structures_I = [
        (("iI", "iJ", "iK"), "i'k", "1j"),
        (("iI", "iK", "iJ"), "i'k", "1j"),
        (("jI", "jJ", "jK"), "i'i", "1k"),
        (("jI", "jK", "jJ"), "i'i", "1k"),
        (("kI", "kJ", "kK"), "i'j", "1i"),
        (("kI", "kK", "kJ"), "i'j", "1i"),
    ]
    
    for struct, feu, eau in structures_I:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE II : ÉCHANGE FEU-EAU =====
    famille = "FII"
    structures_II = [
        (("iI", "iJ", "iK"), "i'j", "1k"),
        (("iI", "iK", "iJ"), "i'j", "1k"),
        (("jI", "jJ", "jK"), "i'k", "1i"),
        (("jI", "jK", "jJ"), "i'k", "1i"),
        (("kI", "kJ", "kK"), "i'i", "1j"),
        (("kI", "kK", "kJ"), "i'i", "1j"),
    ]
    
    for struct, feu, eau in structures_II:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE III : DUALE - CORRIGÉE AVEC 6 GÉNÉRATEURS =====
    famille = "FIII"
    structures_III = [
        # Ces structures mélangent les axes pour couvrir tous les générateurs
        (("Ii", "Jj", "Kk"), "i'i", "1j"),  # Ii,Jj,Kk + i + j
        (("Ii", "Jk", "Kj"), "i'i", "1k"),  # Ii,Jk,Kj + i + k
        (("Ij", "Ji", "Kk"), "i'j", "1i"),  # Ij,Ji,Kk + j + i
        (("Ij", "Jk", "Ki"), "i'j", "1k"),  # Ij,Jk,Ki + j + k
        (("Ik", "Ji", "Kj"), "i'k", "1i"),  # Ik,Ji,Kj + k + i
        (("Ik", "Jj", "Ki"), "i'k", "1j"),  # Ik,Jj,Ki + k + j
    ]
    
    for struct, feu, eau in structures_III:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE IV : ÉCHANGE DUAL - CORRIGÉE AVEC 6 GÉNÉRATEURS =====
    famille = "FIV"
    structures_IV = [
        # Même principe avec Feu = i'1
        (("Ii", "Jj", "Kk"), "i'1", "1j"),
        (("Ii", "Jk", "Kj"), "i'1", "1k"),
        (("Ij", "Ji", "Kk"), "i'1", "1i"),
        (("Ij", "Jk", "Ki"), "i'1", "1k"),
        (("Ik", "Ji", "Kj"), "i'1", "1i"),
        (("Ik", "Jj", "Ki"), "i'1", "1j"),
    ]
    
    for struct, feu, eau in structures_IV:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE V : ESPACE-ESPACE (document Word) =====
    famille = "FV"
    structures_V = [
        (("iI", "jJ", "ij"), "i'k", "1K"),
        (("iJ", "jI", "ij"), "i'k", "1K"),
        (("iI", "kJ", "ik"), "i'j", "1K"),
        (("iJ", "kI", "ik"), "i'j", "1K"),
        (("jI", "kJ", "jk"), "i'i", "1K"),
        (("jJ", "kI", "jk"), "i'i", "1K"),
    ]
    
    for struct, feu, eau in structures_V:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE VI : CHARGE-CHARGE (document Word) =====
    famille = "FVI"
    structures_VI = [
        (("iI", "jJ", "IJ"), "i'k", "1K"),
        (("iJ", "jI", "IJ"), "i'k", "1K"),
        (("iI", "kJ", "IK"), "i'j", "1J"),
        (("iK", "jI", "IK"), "i'k", "1J"),
        (("jI", "kJ", "JK"), "i'i", "1J"),
        (("jK", "kI", "JK"), "i'i", "1J"),
    ]
    
    for struct, feu, eau in structures_VI:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    return pentades


# =====================================================================
# TESTS ET VALIDATION
# =====================================================================

def test_comptage(pentades):
    print(f"📊 Total pentades construites: {len(pentades)}")
    assert len(pentades) == 72, f"ERREUR: {len(pentades)} pentades (devrait être 72)"
    print("✅ Nombre correct: 72")

def test_validite(pentades):
    valides = [p for p in pentades if p.est_valide()]
    invalides = [p for p in pentades if not p.est_valide()]
    
    print(f"✅ Pentades valides: {len(valides)}/72")
    
    if invalides:
        print(f"\n⚠ {len(invalides)} pentades invalides:")
        for p in invalides[:5]:
            print(f"  {p}")
            print(f"    Générateurs: {sorted(p.generateurs_presents())}")
    
    assert len(valides) == 72, f"{len(valides)} valides seulement"

def test_equilibre_yang_yin(pentades):
    yang = len([p for p in pentades if p.signe == 1])
    yin = len([p for p in pentades if p.signe == -1])
    print(f"✅ Yang/Yin: {yang}/{yin}")
    assert yang == yin == 36

def test_repartition_familles(pentades):
    familles = Counter([p.famille for p in pentades])
    print("\n📊 RÉPARTITION PAR FAMILLE:")
    total = 0
    for f in sorted(familles.keys()):
        count = familles[f]
        print(f"  {f}: {count} pentades ({count//2} Yang + {count//2} Yin)")
        assert count == 12, f"{f} a {count} pentades (devrait être 12)"
        total += count
    print(f"  TOTAL: {total} pentades")
    print("✅ Toutes les familles ont 12 pentades")

def test_generateurs(pentades):
    """Vérifie que chaque pentade a exactement les 6 générateurs"""
    print("\n🔍 VÉRIFICATION DES 6 GÉNÉRATEURS (premières de chaque famille):")
    for famille in ["FI", "FII", "FIII", "FIV", "FV", "FVI"]:
        p = next(p for p in pentades if p.famille == famille and p.signe == 1)
        print(f"  {famille}: {p}")
        print(f"     Générateurs: {sorted(p.generateurs_presents())}")

def exporter_pentades(pentades, fichier="pentades_72_finales.json"):
    data = [p.to_dict() for p in pentades]
    with open(fichier, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"💾 Exporté dans {fichier}")


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("="*70)
    print("CONSTRUCTION DES 72 PENTADES - VERSION FINALE")
    print("="*70)
    
    # Construction
    pentades = construire_toutes_pentades()
    
    # Tests
    print("\n🔍 TESTS:")
    test_comptage(pentades)
    test_validite(pentades)
    test_equilibre_yang_yin(pentades)
    test_repartition_familles(pentades)
    
    # Vérification visuelle
    test_generateurs(pentades)
    
    # Export
    exporter_pentades(pentades)
    
    print("\n" + "="*70)
    print("✅ CONSTRUCTION TERMINÉE AVEC SUCCÈS")
    print("="*70)