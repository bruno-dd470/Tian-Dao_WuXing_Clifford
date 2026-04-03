#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 3B : RÈGLES DE SÉLECTION POUR LES TRANSITIONS ATOMIQUES PENTADIQUES
Version corrigée - harmonisée avec MODULE_4
Basé sur les 72 pentades de Cl(6,0) et extension Cl(6,6)
"""
import json
import math
import os
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import Counter

# =====================================================================
# IMPORT DES MODULES EXISTANTS
# =====================================================================
try:
    from MODULE_1_72_pentades import Pentade
except ImportError:
    print("⚠️  MODULE_1 non trouvé - utilisation de la classe locale")
    @dataclass
    class Pentade:
        structure: Tuple[str, str, str]
        feu: str
        eau: str
        signe: int = 1
        famille: str = ""
        
        def generateurs_presents(self) -> Set[str]:
            presents = set()
            elements = list(self.structure) + [self.feu, self.eau]
            for e in elements:
                e_str = str(e).replace('-', '').replace("'", '')
                for gen in ['i', 'j', 'k', 'I', 'J', 'K']:
                    if gen in e_str:
                        presents.add(gen)
            return presents
        
        def est_valide(self) -> bool:
            return len(self.generateurs_presents()) == 6

# =====================================================================
# CONSTANTES PHYSIQUES
# =====================================================================
CONSTANTES = {
    'hbar': 1.054571817e-34,
    'me': 9.10938356e-31,
    'e': 1.602176634e-19,
    'c': 299792458,
    'muB_eV_T': 5.7883818060e-5,
    'alpha': 1/137.036,
    'me_MeV': 0.511,
    'rydberg_eV': 13.605693122994,
}

# =====================================================================
# CLASSE : ÉTAT ATOMIQUE PENTADIQUE (HARMONISÉ AVEC MODULE_4)
# =====================================================================
@dataclass
class EtatAtomiquePentadique:
    """État atomique décrit par une pentade + nombres quantiques émergents"""
    pentade: Pentade
    n: int
    l: int
    ml: int
    energie_eV: float
    particule: str = "electron"
    
    def __post_init__(self):
        """CORRECTION : Validation des contraintes quantiques"""
        if abs(self.ml) > self.l:
            raise ValueError(f"ml={self.ml} invalide pour l={self.l} (doit satisfaire |ml| ≤ l)")
    
    def __repr__(self):
        return f"|{self.particule}, n={self.n}, l={self.l}, ml={self.ml}, E={self.energie_eV:.4f} eV>"

# =====================================================================
# RÈGLES DE CONSERVATION FONDAMENTALES
# =====================================================================
class ReglesConservation:
    """Gère les lois de conservation pour les transitions pentadiques"""
    
    @staticmethod
    def conservation_generateurs(p1: Pentade, p2: Pentade) -> bool:
        gen1 = p1.generateurs_presents()
        gen2 = p2.generateurs_presents()
        return gen1 == gen2
    
    @staticmethod
    def conservation_charge(p1: Pentade, p2: Pentade, photon: Optional[Pentade] = None) -> bool:
        def count_charge(p: Pentade) -> int:
            count = 0
            elements = list(p.structure) + [p.feu, p.eau]
            for e in elements:
                e_str = str(e).replace('-', '').replace("'", '')
                for gen in ['I', 'J', 'K']:
                    if gen in e_str:
                        count += 1
            return count
        
        q1 = count_charge(p1)
        q2 = count_charge(p2)
        q_photon = count_charge(photon) if photon else 0
        return q1 == q2 + q_photon
    
    @staticmethod
    def conservation_moment_angulaire(etat1: EtatAtomiquePentadique,
                                       etat2: EtatAtomiquePentadique,
                                       photon_type: str = "dipole") -> bool:
        delta_l = abs(etat1.l - etat2.l)
        delta_ml = abs(etat1.ml - etat2.ml)
        
        if photon_type == "dipole":
            if delta_l != 1:
                return False
            if delta_ml > 1:
                return False
        elif photon_type == "magnetic":
            if delta_l != 0:
                return False
            if delta_ml > 1:
                return False
        elif photon_type == "quadrupole":
            if delta_l > 2 or delta_l == 1:
                return False
            if delta_ml > 2:
                return False
        return True
    
    @staticmethod
    def conservation_parite(etat1: EtatAtomiquePentadique,
                             etat2: EtatAtomiquePentadique,
                             photon_type: str = "dipole") -> bool:
        parite1 = (-1) ** etat1.l
        parite2 = (-1) ** etat2.l
        
        if photon_type == "dipole":
            return parite1 == -parite2
        elif photon_type == "magnetic":
            return parite1 == parite2
        elif photon_type == "quadrupole":
            return parite1 == parite2
        return True

# =====================================================================
# RÈGLES DE SÉLECTION PENTADIQUES SPÉCIFIQUES
# =====================================================================
class ReglesSelectionPentadiques:
    """Règles de sélection spécifiques au modèle pentadique"""
    
    @staticmethod
    def nombre_bivecteurs_changes(p1: Pentade, p2: Pentade) -> int:
        changes = 0
        for b1, b2 in zip(p1.structure, p2.structure):
            if b1 != b2:
                changes += 1
        return changes
    
    @staticmethod
    def regle_changement_minimal(p1: Pentade, p2: Pentade, max_changes: int = 1) -> bool:
        changes = ReglesSelectionPentadiques.nombre_bivecteurs_changes(p1, p2)
        return changes <= max_changes
    
    @staticmethod
    def transition_permise(p1: Pentade, p2: Pentade,
                           etat1: Optional[EtatAtomiquePentadique] = None,
                           etat2: Optional[EtatAtomiquePentadique] = None,
                           B_champ: float = 0) -> Dict:
        result = {
            'permise': False,
            'type': None,
            'intensite_relative': 0.0,
            'regles_violées': []
        }
        
        # CORRECTION : Interdire transitions vers même état
        if etat1 and etat2:
            if (etat1.n == etat2.n and etat1.l == etat2.l and etat1.ml == etat2.ml):
                result['regles_violées'].append('même_état')
                return result
        
        if not ReglesConservation.conservation_generateurs(p1, p2):
            result['regles_violées'].append('generateurs')
        
        if not ReglesConservation.conservation_charge(p1, p2):
            result['regles_violées'].append('charge')
        
        if not ReglesSelectionPentadiques.regle_changement_minimal(p1, p2, max_changes=2):
            result['regles_violées'].append('changement_minimal')
        
        if etat1 and etat2:
            if ReglesConservation.conservation_moment_angulaire(etat1, etat2, "dipole"):
                if ReglesConservation.conservation_parite(etat1, etat2, "dipole"):
                    result['permise'] = True
                    result['type'] = 'E1'
                    result['intensite_relative'] = 1.0
            elif ReglesConservation.conservation_moment_angulaire(etat1, etat2, "magnetic"):
                if ReglesConservation.conservation_parite(etat1, etat2, "magnetic"):
                    result['permise'] = True
                    result['type'] = 'M1'
                    result['intensite_relative'] = 0.01
            elif ReglesConservation.conservation_moment_angulaire(etat1, etat2, "quadrupole"):
                if ReglesConservation.conservation_parite(etat1, etat2, "quadrupole"):
                    result['permise'] = True
                    result['type'] = 'E2'
                    result['intensite_relative'] = 0.001
            else:
                result['regles_violées'].append('moment_angulaire')
        else:
            if len(result['regles_violées']) == 0:
                result['permise'] = True
                result['type'] = 'E1'
                result['intensite_relative'] = 1.0
        
        return result

# =====================================================================
# EFFET ZEEMAN PENTADIQUE AVEC RÈGLES DE SÉLECTION
# =====================================================================
class ZeemanPentadique:
    """Implémente l'effet Zeeman avec les règles de sélection pentadiques"""
    
    @staticmethod
    def splitting_niveaux(etat: EtatAtomiquePentadique, B_Tesla: float):
        niveaux_splites = []
        
        muB_eV_T = 5.7883818060e-5
        g_s = 2.00231930436256
        delta_E_spin = g_s * muB_eV_T * B_Tesla
        delta_E_orbital = muB_eV_T * B_Tesla
        
        if etat.l == 0:
            for ms in [-0.5, 0.5]:
                etat_split = EtatAtomiquePentadique(
                    pentade=etat.pentade,
                    n=etat.n, l=etat.l, ml=0,
                    energie_eV=etat.energie_eV + ms * delta_E_spin,
                    particule=etat.particule
                )
                niveaux_splites.append(etat_split)
        elif etat.l == 1:
            for ml in [-1, 0, 1]:
                for ms in [-0.5, 0.5]:
                    energie = etat.energie_eV + ml * delta_E_orbital + ms * delta_E_spin
                    etat_split = EtatAtomiquePentadique(
                        pentade=etat.pentade,
                        n=etat.n, l=etat.l, ml=ml,
                        energie_eV=energie,
                        particule=etat.particule
                    )
                    niveaux_splites.append(etat_split)
        return niveaux_splites
    
    @staticmethod
    def transitions_zeeman_permises(etat_initial: EtatAtomiquePentadique,
                                     etat_final: EtatAtomiquePentadique,
                                     B_Tesla: float) -> List[Dict]:
        """Liste toutes les transitions Zeeman permises"""
        niveaux_init = ZeemanPentadique.splitting_niveaux(etat_initial, B_Tesla)
        niveaux_final = ZeemanPentadique.splitting_niveaux(etat_final, B_Tesla)
        transitions = []
        
        for ei in niveaux_init:
            for ef in niveaux_final:
                delta_ml = ei.ml - ef.ml
                if abs(delta_ml) <= 1:
                    if ei.ml == ef.ml:
                        polarisation = 'π'
                    elif ei.ml > ef.ml:
                        polarisation = 'σ⁺'
                    else:
                        polarisation = 'σ⁻'
                    
                    intensite = abs(ei.energie_eV - ef.energie_eV) ** 3
                    transitions.append({
                        'initial_ml': ei.ml,
                        'final_ml': ef.ml,
                        'delta_ml': delta_ml,
                        'polarisation': polarisation,
                        'energie_photon_eV': ei.energie_eV - ef.energie_eV,
                        'intensite_relative': intensite,
                        'permise': True
                    })
        
        if transitions:
            somme = sum(t['intensite_relative'] for t in transitions)
            if somme > 0:
                for t in transitions:
                    t['intensite_relative'] /= somme
                    t['intensite_pct'] = t['intensite_relative'] * 100
        
        return transitions

# =====================================================================
# EXEMPLES DE TRANSITIONS ATOMIQUES
# =====================================================================
def exemples_transitions_hydrogene():
    """Génère des exemples de transitions pour l'hydrogène"""
    etats = [
        EtatAtomiquePentadique(
            pentade=Pentade(("iI", "jI", "kI"), "i'i", "1j", 1, "FI"),
            n=1, l=0, ml=0, energie_eV=-13.6057
        ),
        EtatAtomiquePentadique(
            pentade=Pentade(("iI", "jI", "kI"), "i'j", "1k", 1, "FI"),
            n=2, l=0, ml=0, energie_eV=-3.4014
        ),
        EtatAtomiquePentadique(
            pentade=Pentade(("iI", "jJ", "kK"), "i'k", "1j", 1, "FI"),
            n=2, l=1, ml=-1, energie_eV=-3.4014
        ),
        EtatAtomiquePentadique(
            pentade=Pentade(("iI", "jJ", "kK"), "i'k", "1j", 1, "FI"),
            n=2, l=1, ml=0, energie_eV=-3.4014
        ),
        EtatAtomiquePentadique(
            pentade=Pentade(("iI", "jJ", "kK"), "i'k", "1j", 1, "FI"),
            n=2, l=1, ml=1, energie_eV=-3.4014
        ),
    ]
    return etats

# =====================================================================
# VALIDATION ET EXPORT
# =====================================================================
def valider_regles_selection():
    """Valide les règles de sélection"""
    print("="*80)
    print("VALIDATION DES RÈGLES DE SÉLECTION PENTADIQUES")
    print("="*80)
    
    etats = exemples_transitions_hydrogene()
    resultats = []
    
    for i, etat1 in enumerate(etats):
        for j, etat2 in enumerate(etats):
            if i != j:
                regle = ReglesSelectionPentadiques.transition_permise(
                    etat1.pentade, etat2.pentade, etat1, etat2
                )
                if regle['permise']:
                    resultats.append({
                        'de': f"n={etat1.n}, l={etat1.l}",
                        'vers': f"n={etat2.n}, l={etat2.l}",
                        'type': regle['type'],
                        'intensite': regle['intensite_relative']
                    })
    
    print(f"✅ {len(resultats)} transitions permises trouvées")
    return resultats

def exporter_regles_selection(fichier: str = "regles_selection_resultats.json"):
    """Exporte les résultats"""
    resultats_validation = valider_regles_selection()
    
    transitions_zeeman = ZeemanPentadique.transitions_zeeman_permises(
        exemples_transitions_hydrogene()[2],
        exemples_transitions_hydrogene()[0],
        B_Tesla=1.0
    )
    
    donnees = {
        'validation': resultats_validation,
        'zeeman_B1T': [
            {
                'polarisation': t['polarisation'],
                'energie_photon_eV': t['energie_photon_eV'],
                'intensite_relative': t['intensite_relative'],
                'intensite_pct': t.get('intensite_pct', 0)
            }
            for t in transitions_zeeman
        ],
        'regles': {
            'conservation_generateurs': True,
            'conservation_charge': True,
            'changement_minimal_bivecteurs': True,
            'moment_angulaire': True,
            'parite': True
        }
    }
    
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Résultats exportés dans {fichier}")
    return donnees

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("="*80)
    print("MODULE 3B : RÈGLES DE SÉLECTION PENTADIQUES - VERSION CORRIGÉE")
    print("CORRECTION : Harmonisation avec MODULE_4")
    print("="*80)
    
    resultats = valider_regles_selection()
    donnees = exporter_regles_selection()
    
    print("\n" + "="*80)
    print("✅ MODULE 3B TERMINÉ AVEC SUCCÈS")
    print("="*80)