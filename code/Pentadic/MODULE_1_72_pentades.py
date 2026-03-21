#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 1 : CONSTRUCTION DES 72 PENTADES - VERSION FINALE CORRIGÉE
6 familles × 6 structures × 2 signes = 72 pentades
CORRECTION CRITIQUE : FIII/FIV avec dualité complète (Feu et Eau inversés)
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
        """Extrait les 6 générateurs présents dans la pentade"""
        presents = set()
        for e in self.elements:
            e_str = str(e).replace('-', '').replace("'", '')
            for gen in ['i', 'j', 'k', 'I', 'J', 'K']:
                if gen in e_str:
                    presents.add(gen)
        return presents
    
    def est_valide(self) -> bool:
        """Vérifie que les 6 générateurs sont présents"""
        return len(self.generateurs_presents()) == 6
    
    def est_rowlands_pur(self) -> bool:
        """Vérifie si la pentade respecte le principe Rowlands strict"""
        for b in self.structure:
            b_clean = str(b).replace('-', '').replace("'", '')
            espace = any(g in b_clean for g in ['i', 'j', 'k'])
            charge = any(g in b_clean for g in ['I', 'J', 'K'])
            if not (espace and charge):
                return False
        return True
    
    def type_pentade(self) -> str:
        """Retourne le type de pentade"""
        return "rowlands_pur" if self.est_rowlands_pur() else "rowlands_etendu"
    
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
            'generateurs': sorted(list(self.generateurs_presents())),
            'type': self.type_pentade()
        }

# =====================================================================
# CONSTRUCTION DES 72 PENTADES - TOUTES LES FAMILLES CORRIGÉES
# =====================================================================
def construire_toutes_pentades() -> List[Pentade]:
    """Construit les 72 pentades : 6 familles × 6 structures × 2 signes"""
    pentades = []
    
    # ===== FAMILLE I : DIRECTE (Rowlands original) =====
    # Espace FIXE, Charges VARIABLES
    famille = "FI"
    structures_I = [
        (("iI", "iJ", "iK"), "i'k", "1j"),  # Axe i fixe
        (("iI", "iK", "iJ"), "i'k", "1j"),  # Permutation
        (("jI", "jJ", "jK"), "i'i", "1k"),  # Axe j fixe
        (("jI", "jK", "jJ"), "i'i", "1k"),  # Permutation
        (("kI", "kJ", "kK"), "i'j", "1i"),  # Axe k fixe
        (("kI", "kK", "kJ"), "i'j", "1i"),  # Permutation
    ]
    for struct, feu, eau in structures_I:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE II : ÉCHANGE FEU-EAU =====
    # Même structure que FI mais Feu ↔ Eau échangés
    famille = "FII"
    structures_II = [
        (("iI", "iJ", "iK"), "i'j", "1k"),  # Échange de FI-1
        (("iI", "iK", "iJ"), "i'j", "1k"),
        (("jI", "jJ", "jK"), "i'k", "1i"),  # Échange de FI-2
        (("jI", "jK", "jJ"), "i'k", "1i"),
        (("kI", "kJ", "kK"), "i'i", "1j"),  # Échange de FI-3
        (("kI", "kK", "kJ"), "i'i", "1j"),
    ]
    for struct, feu, eau in structures_II:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE III : DUALE - CORRIGÉE =====
    # Charge FIXE, Espaces VARIABLES + Feu/Eau en CHARGE (pas espace)
    famille = "FIII"
    structures_III = [
        (("Ii", "Ij", "Ik"), "i'K", "1J"),  # Axe I fixe, Feu/Eau en charge
        (("Ii", "Ik", "Ij"), "i'K", "1J"),  # Permutation
        (("Ji", "Jj", "Jk"), "i'I", "1K"),  # Axe J fixe
        (("Ji", "Jk", "Jj"), "i'I", "1K"),  # Permutation
        (("Ki", "Kj", "Kk"), "i'J", "1I"),  # Axe K fixe
        (("Ki", "Kk", "Kj"), "i'J", "1I"),  # Permutation
    ]
    for struct, feu, eau in structures_III:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE IV : ÉCHANGE DUAL - CORRIGÉE =====
    # Même structure que FIII mais avec échange Feu-Eau
    famille = "FIV"
    structures_IV = [
        (("Ii", "Ij", "Ik"), "1J", "i'K"),  # Échange de FIII-1
        (("Ii", "Ik", "Ij"), "1J", "i'K"),
        (("Ji", "Jj", "Jk"), "1K", "i'I"),  # Échange de FIII-2
        (("Ji", "Jk", "Jj"), "1K", "i'I"),
        (("Ki", "Kj", "Kk"), "1I", "i'J"),  # Échange de FIII-3
        (("Ki", "Kk", "Kj"), "1I", "i'J"),
    ]
    for struct, feu, eau in structures_IV:
        pentades.append(Pentade(struct, feu, eau, 1, famille))
        pentades.append(Pentade(struct, feu, eau, -1, famille))
    
    # ===== FAMILLE V : ESPACE-ESPACE (Pentades étendues) =====
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
    
    # ===== FAMILLE VI : CHARGE-CHARGE (Pentades étendues) =====
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
        print(f"⚠ {len(invalides)} pentades invalides:")
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
    for f in sorted(familles.keys()):
        count = familles[f]
        print(f"  {f}: {count} pentades ({count//2} Yang + {count//2} Yin)")
        assert count == 12, f"{f} a {count} pentades (devrait être 12)"

def test_dualite_rowlands(pentades):
    """Vérifie que FIII est bien le dual de FI avec inversion complète"""
    fi = [p for p in pentades if p.famille == "FI" and p.signe == 1]
    fiii = [p for p in pentades if p.famille == "FIII" and p.signe == 1]
    
    print("\n🔄 VÉRIFICATION DUALITÉ ROWLANDS:")
    print(f"  FI-1 : {fi[0].structure} | Feu={fi[0].feu} | Eau={fi[0].eau}")
    print(f"  FIII-1 : {fiii[0].structure} | Feu={fiii[0].feu} | Eau={fiii[0].eau}")
    
    # FI a espace dans Feu/Eau, FIII doit avoir charge
    fi_feu_espace = any(g in fi[0].feu for g in ['i', 'j', 'k'])
    fiii_feu_charge = any(g in fiii[0].feu for g in ['I', 'J', 'K'])
    
    print(f"  FI Feu contient espace : {fi_feu_espace}")
    print(f"  FIII Feu contient charge : {fiii_feu_charge}")
    
    assert fi_feu_espace and fiii_feu_charge, "DUALITÉ FEU/EAU NON RESPECTÉE !"
    print("  ✅ Dualité Rowlands correctement implémentée")

def test_generateurs(pentades):
    print("\n🔍 VÉRIFICATION DES 6 GÉNÉRATEURS (premières de chaque famille):")
    for famille in ["FI", "FII", "FIII", "FIV", "FV", "FVI"]:
        p = next(p for p in pentades if p.famille == famille and p.signe == 1)
        print(f"  {famille}: {p}")
        print(f"     Générateurs: {sorted(p.generateurs_presents())}")

def exporter_pentades(pentades, fichier="pentades_72_finales.json"):
    data = [p.to_dict() for p in pentades]
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Exporté dans {fichier}")

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("="*70)
    print("CONSTRUCTION DES 72 PENTADES - VERSION FINALE CORRIGÉE")
    print("Correction : FIII/FIV avec dualité complète (Feu/Eau en charge)")
    print("="*70)
    
    pentades = construire_toutes_pentades()
    
    print("\n🔍 TESTS DE VALIDATION:")
    print("-"*70)
    test_comptage(pentades)
    test_validite(pentades)
    test_equilibre_yang_yin(pentades)
    test_repartition_familles(pentades)
    test_generateurs(pentades)
    test_dualite_rowlands(pentades)
    
    exporter_pentades(pentades)
    
    print("\n" + "="*70)
    print("✅ CONSTRUCTION TERMINÉE AVEC SUCCÈS")
    print("✅ Toutes les validations passent")
    print("✅ Dualité Rowlands complète implémentée")
    print("="*70)