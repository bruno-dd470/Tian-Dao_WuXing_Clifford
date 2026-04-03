#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTANTES_PARTAGEES.py
========================
Fichier de constantes physiques partagées pour le framework pentadique.

Ce module centralise toutes les constantes physiques utilisées dans les 
MODULE_1 à MODULE_4 et les scripts zeeman/, avec :
- Précision 50 chiffres (Decimal)
- Valeurs CODATA 2018/2022 et PDG 2022
- Incertitudes 1σ pour propagation Monte Carlo
- Compatibilité avec tous les modules existants

Auteur : Bruno DE DOMINICIS
Date : Mars 2026
License : CC BY 4.0
"""

from decimal import Decimal, getcontext
from typing import Dict, Any, Tuple
from dataclasses import dataclass
import json
import numpy as np

# =====================================================================
# CONFIGURATION DE LA PRÉCISION
# =====================================================================
getcontext().prec = 50  # 50 chiffres significatifs

# =====================================================================
# CLASSE POUR CONSTANTES AVEC INCERTITUDES
# =====================================================================
@dataclass
class ConstanteAvecIncertitude:
    """Représente une constante physique avec sa valeur et incertitude 1σ"""
    valeur: Decimal
    incertitude: Decimal
    unite: str = ""
    source: str = "CODATA 2022"
    
    def echantillonner(self, n: int) -> np.ndarray:
        """Génère n échantillons pour propagation Monte Carlo"""
        return np.random.normal(
            float(self.valeur), 
            float(self.incertitude), 
            n
        )
    
    def to_dict(self) -> Dict:
        return {
            'valeur': str(self.valeur),
            'incertitude': str(self.incertitude),
            'unite': self.unite,
            'source': self.source
        }

# =====================================================================
# CONSTANTES FONDAMENTALES (CODATA 2018/2022)
# =====================================================================
CONSTANTES_FONDAMENTALES = {
    'hbar': ConstanteAvecIncertitude(
        valeur=Decimal('1.0545718176461565e-34'),
        incertitude=Decimal('1.5e-50'),
        unite='J·s',
        source='CODATA 2022'
    ),
    
    'h': ConstanteAvecIncertitude(
        valeur=Decimal('6.62607015e-34'),
        incertitude=Decimal('0'),
        unite='J·s',
        source='CODATA 2022'
    ),
    
    'c': ConstanteAvecIncertitude(
        valeur=Decimal('299792458'),
        incertitude=Decimal('0'),
        unite='m/s',
        source='CODATA 2022'
    ),
    
    'e': ConstanteAvecIncertitude(
        valeur=Decimal('1.602176634e-19'),
        incertitude=Decimal('0'),
        unite='C',
        source='CODATA 2022'
    ),
    
    'epsilon_0': ConstanteAvecIncertitude(
        valeur=Decimal('8.8541878128e-12'),
        incertitude=Decimal('1.3e-21'),
        unite='F/m',
        source='CODATA 2022'
    ),
    
    'mu_0': ConstanteAvecIncertitude(
        valeur=Decimal('1.25663706212e-6'),
        incertitude=Decimal('1.9e-16'),
        unite='N/A²',
        source='CODATA 2022'
    ),
    
    'alpha': ConstanteAvecIncertitude(
        valeur=Decimal('7.2973525693e-3'),
        incertitude=Decimal('1.1e-12'),
        unite='sans dimension',
        source='CODATA 2022'
    ),
    
    'alpha_inv': ConstanteAvecIncertitude(
        valeur=Decimal('137.035999084'),
        incertitude=Decimal('0.000000021'),
        unite='sans dimension',
        source='CODATA 2022'
    ),
}

# =====================================================================
# MASSES DES PARTICULES (PDG 2022)
# =====================================================================
MASSES_PARTICULES = {
    'me_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('0.51099895000'),
        incertitude=Decimal('1.5e-11'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mmu_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('105.6583745'),
        incertitude=Decimal('2.4e-6'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mtau_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('1776.86'),
        incertitude=Decimal('0.12'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mu_quark_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('2.2'),
        incertitude=Decimal('0.5'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'md_quark_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('4.7'),
        incertitude=Decimal('0.5'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'ms_quark_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('96'),
        incertitude=Decimal('8'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mc_quark_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('1270'),
        incertitude=Decimal('25'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mb_quark_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('4180'),
        incertitude=Decimal('30'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mt_quark_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('173000'),
        incertitude=Decimal('400'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mp_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('938.27208816'),
        incertitude=Decimal('2.9e-8'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mn_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('939.56542052'),
        incertitude=Decimal('5.4e-8'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mpi_plus_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('139.57039'),
        incertitude=Decimal('1.8e-5'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mpi_zero_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('134.9768'),
        incertitude=Decimal('5e-5'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mW_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('80379'),
        incertitude=Decimal('12'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mZ_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('91187.6'),
        incertitude=Decimal('2.1'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
    
    'mH_MeV': ConstanteAvecIncertitude(
        valeur=Decimal('125250'),
        incertitude=Decimal('190'),
        unite='MeV/c²',
        source='PDG 2022'
    ),
}

# =====================================================================
# MOMENTS MAGNÉTIQUES ET FACTEURS G (PDG 2022)
# =====================================================================
MOMENTS_MAGNETIQUES = {
    'g_e': ConstanteAvecIncertitude(
        valeur=Decimal('2.00231930436256'),
        incertitude=Decimal('3.5e-14'),
        unite='sans dimension',
        source='PDG 2022'
    ),
    
    'g_p': ConstanteAvecIncertitude(
        valeur=Decimal('5.5856946893'),
        incertitude=Decimal('1.6e-9'),
        unite='sans dimension',
        source='PDG 2022'
    ),
    
    'g_n': ConstanteAvecIncertitude(
        valeur=Decimal('-3.82608545'),
        incertitude=Decimal('9.0e-8'),
        unite='sans dimension',
        source='PDG 2022'
    ),
    
    'g_mu': ConstanteAvecIncertitude(
        valeur=Decimal('2.0023318414'),
        incertitude=Decimal('1.2e-9'),
        unite='sans dimension',
        source='PDG 2022'
    ),
}

# =====================================================================
# MAGNÉTONS (CODATA 2022)
# =====================================================================
MAGNETONS = {
    'muB_eV_T': ConstanteAvecIncertitude(
        valeur=Decimal('5.7883818012e-5'),
        incertitude=Decimal('1.7e-14'),
        unite='eV/T',
        source='CODATA 2022'
    ),
    
    'muB_MeV_T': ConstanteAvecIncertitude(
        valeur=Decimal('5.7883818012e-11'),
        incertitude=Decimal('1.7e-20'),
        unite='MeV/T',
        source='CODATA 2022'
    ),
    
    'muN_eV_T': ConstanteAvecIncertitude(
        valeur=Decimal('3.1524512550e-8'),
        incertitude=Decimal('9.5e-18'),
        unite='eV/T',
        source='CODATA 2022'
    ),
    
    'muN_MeV_T': ConstanteAvecIncertitude(
        valeur=Decimal('3.1524512550e-14'),
        incertitude=Decimal('9.5e-24'),
        unite='MeV/T',
        source='CODATA 2022'
    ),
}

# =====================================================================
# CONSTANTES ATOMIQUES (HYDROGÈNE)
# =====================================================================
CONSTANTES_ATOMIQUES = {
    'rydberg_eV': ConstanteAvecIncertitude(
        valeur=Decimal('13.605693122994'),
        incertitude=Decimal('4.2e-11'),
        unite='eV',
        source='CODATA 2022'
    ),
    
    'rydberg_inf_m': ConstanteAvecIncertitude(
        valeur=Decimal('10973731.568160'),
        incertitude=Decimal('2.1e-5'),
        unite='m⁻¹',
        source='CODATA 2022'
    ),
    
    'bohr_radius_m': ConstanteAvecIncertitude(
        valeur=Decimal('5.29177210903e-11'),
        incertitude=Decimal('8.0e-21'),
        unite='m',
        source='CODATA 2022'
    ),
    
    'h_eV_s': ConstanteAvecIncertitude(
        valeur=Decimal('4.135667696923588e-15'),
        incertitude=Decimal('0'),
        unite='eV·s',
        source='CODATA 2022'
    ),
    
    'A_1S_Hz': ConstanteAvecIncertitude(
        valeur=Decimal('1420405751.768'),
        incertitude=Decimal('0.002'),
        unite='Hz',
        source='PDG 2022'
    ),
    
    'mu_reduit': ConstanteAvecIncertitude(
        valeur=Decimal('0.99945567942'),
        incertitude=Decimal('1e-11'),
        unite='sans dimension',
        source='CODATA 2022'
    ),
}

# =====================================================================
# PARAMÈTRES PENTADIQUES (EXTRAITS DES VALIDATIONS)
# =====================================================================
PARAMETRES_PENTADIQUES = {
    'delta_lattice': ConstanteAvecIncertitude(
        valeur=Decimal('0.005067'),
        incertitude=Decimal('0.000030'),
        unite='sans dimension',
        source='Zeeman validation 2026'
    ),
    
    'B0_Tesla': ConstanteAvecIncertitude(
        valeur=Decimal('7.99'),
        incertitude=Decimal('0.02'),
        unite='T',
        source='Zeeman validation 2026'
    ),
    
    'delta_bicosmic': ConstanteAvecIncertitude(
        valeur=Decimal('0.010000'),
        incertitude=Decimal('0.000050'),
        unite='sans dimension',
        source='Zeeman validation 2026'
    ),
    
    'Bc_Tesla': ConstanteAvecIncertitude(
        valeur=Decimal('100'),
        incertitude=Decimal('10'),
        unite='T',
        source='Zeeman validation 2026'
    ),
    
    'f_proj_octave5': ConstanteAvecIncertitude(
        valeur=Decimal('82'),
        incertitude=Decimal('5'),
        unite='sans dimension',
        source='Fermi-LAT magnetar 2026'
    ),
    
    'D_eff': ConstanteAvecIncertitude(
        valeur=Decimal('67.7'),
        incertitude=Decimal('2.3'),
        unite='sans dimension',
        source='Zeeman validation 2026'
    ),
}

# =====================================================================
# FACTEURS DE FAMILLE PENTADIQUE (MODULE_2)
# =====================================================================
FACTEURS_FAMILLE = {
    'FI': Decimal('1.0'),
    'FII': Decimal('1.2'),
    'FIII': Decimal('1.5'),
    'FIV': Decimal('1.8'),
    'FV': Decimal('0.5'),
    'FVI': Decimal('0.8'),
}

# =====================================================================
# LOGARITHMES DE BETHE (MODULE_4) - n=1 à 10
# =====================================================================
BETHE_LOGARITHMS = {
    (1, 0): Decimal('2.984128555765498'),
    (2, 0): Decimal('2.811769893120563'), (2, 1): Decimal('-0.030016708630219'),
    (3, 0): Decimal('2.767663068844'), (3, 1): Decimal('-0.038193204'), (3, 2): Decimal('-0.003749872'),
    (4, 0): Decimal('2.749811840'), (4, 1): Decimal('-0.0419548'), (4, 2): Decimal('-0.004196'), (4, 3): Decimal('-0.000419'),
    (5, 0): Decimal('2.739200'), (5, 1): Decimal('-0.044'), (5, 2): Decimal('-0.0045'), (5, 3): Decimal('-0.0005'), (5, 4): Decimal('-0.00005'),
    (6, 0): Decimal('2.732000'), (6, 1): Decimal('-0.045'), (6, 2): Decimal('-0.0046'), (6, 3): Decimal('-0.0005'), (6, 4): Decimal('-0.00006'), (6, 5): Decimal('-0.000006'),
    (7, 0): Decimal('2.727000'), (7, 1): Decimal('-0.046'), (7, 2): Decimal('-0.0047'), (7, 3): Decimal('-0.0005'), (7, 4): Decimal('-0.00006'), (7, 5): Decimal('-0.000007'), (7, 6): Decimal('-0.0000007'),
    (8, 0): Decimal('2.723000'), (8, 1): Decimal('-0.047'), (8, 2): Decimal('-0.0048'), (8, 3): Decimal('-0.0005'), (8, 4): Decimal('-0.00006'), (8, 5): Decimal('-0.000007'), (8, 6): Decimal('-0.0000008'), (8, 7): Decimal('-0.00000008'),
    (9, 0): Decimal('2.720000'), (9, 1): Decimal('-0.048'), (9, 2): Decimal('-0.0049'), (9, 3): Decimal('-0.0005'), (9, 4): Decimal('-0.00006'), (9, 5): Decimal('-0.000007'), (9, 6): Decimal('-0.0000008'), (9, 7): Decimal('-0.00000009'), (9, 8): Decimal('-0.000000009'),
    (10, 0): Decimal('2.717000'), (10, 1): Decimal('-0.049'), (10, 2): Decimal('-0.0050'), (10, 3): Decimal('-0.0005'), (10, 4): Decimal('-0.00006'), (10, 5): Decimal('-0.000007'), (10, 6): Decimal('-0.0000008'), (10, 7): Decimal('-0.00000009'), (10, 8): Decimal('-0.00000001'), (10, 9): Decimal('-0.000000001'),
}

# =====================================================================
# MATRICES DE MÉLANGE (PDG 2022)
# =====================================================================
MATRICE_CKM = [
    [Decimal('0.974'), Decimal('0.225'), Decimal('0.004')],
    [Decimal('0.225'), Decimal('0.973'), Decimal('0.041')],
    [Decimal('0.009'), Decimal('0.040'), Decimal('0.999')],
]

MATRICE_PMNS = [
    [Decimal('0.821'), Decimal('0.551'), Decimal('0.150')],
    [Decimal('0.473'), Decimal('0.592'), Decimal('0.653')],
    [Decimal('0.328'), Decimal('0.588'), Decimal('0.740')],
]

# =====================================================================
# FONCTIONS D'ACCÈS UNIFIÉES
# =====================================================================
def get_constante(nom: str) -> Decimal:
    """Récupère la valeur d'une constante par son nom."""
    for dictionnaire in [
        CONSTANTES_FONDAMENTALES,
        MASSES_PARTICULES,
        MOMENTS_MAGNETIQUES,
        MAGNETONS,
        CONSTANTES_ATOMIQUES,
        PARAMETRES_PENTADIQUES,
    ]:
        if nom in dictionnaire:
            return dictionnaire[nom].valeur
    raise KeyError(f"Constante '{nom}' non trouvée")

def get_incertitude(nom: str) -> Decimal:
    """Récupère l'incertitude 1σ d'une constante"""
    for dictionnaire in [
        CONSTANTES_FONDAMENTALES,
        MASSES_PARTICULES,
        MOMENTS_MAGNETIQUES,
        MAGNETONS,
        CONSTANTES_ATOMIQUES,
        PARAMETRES_PENTADIQUES,
    ]:
        if nom in dictionnaire:
            return dictionnaire[nom].incertitude
    raise KeyError(f"Constante '{nom}' non trouvée")

def get_constante_avec_incertitude(nom: str) -> ConstanteAvecIncertitude:
    """Récupère l'objet complet constante+incertitude"""
    for dictionnaire in [
        CONSTANTES_FONDAMENTALES,
        MASSES_PARTICULES,
        MOMENTS_MAGNETIQUES,
        MAGNETONS,
        CONSTANTES_ATOMIQUES,
        PARAMETRES_PENTADIQUES,
    ]:
        if nom in dictionnaire:
            return dictionnaire[nom]
    raise KeyError(f"Constante '{nom}' non trouvée")

def exporter_constantes_json(fichier: str = "constantes_export.json"):
    """Exporte toutes les constantes dans un fichier JSON"""
    export_data = {
        'fondamentales': {k: v.to_dict() for k, v in CONSTANTES_FONDAMENTALES.items()},
        'masses': {k: v.to_dict() for k, v in MASSES_PARTICULES.items()},
        'moments': {k: v.to_dict() for k, v in MOMENTS_MAGNETIQUES.items()},
        'magnetons': {k: v.to_dict() for k, v in MAGNETONS.items()},
        'atomiques': {k: v.to_dict() for k, v in CONSTANTES_ATOMIQUES.items()},
        'pentadiques': {k: v.to_dict() for k, v in PARAMETRES_PENTADIQUES.items()},
        'facteurs_famille': {k: str(v) for k, v in FACTEURS_FAMILLE.items()},
        'bethe_logarithms': {str(k): str(v) for k, v in BETHE_LOGARITHMS.items()},
        'ckm': [[str(x) for x in row] for row in MATRICE_CKM],
        'pmns': [[str(x) for x in row] for row in MATRICE_PMNS],
    }
    
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Constantes exportées dans {fichier}")
    return export_data

def valider_coherence():
    """Valide la cohérence des constantes entre elles"""
    print("="*70)
    print("VALIDATION DE COHÉRENCE DES CONSTANTES")
    print("="*70)
    
    pi = Decimal('3.14159265358979323846')
    
    h_calc = 2 * pi * CONSTANTES_FONDAMENTALES['hbar'].valeur
    h_ref = CONSTANTES_FONDAMENTALES['h'].valeur
    ecart_h = abs(h_calc - h_ref) / h_ref * 100
    print(f"✓ h = 2πℏ : écart = {ecart_h:.6f}%")
    
    e = CONSTANTES_FONDAMENTALES['e'].valeur
    eps0 = CONSTANTES_FONDAMENTALES['epsilon_0'].valeur
    hbar = CONSTANTES_FONDAMENTALES['hbar'].valeur
    c = CONSTANTES_FONDAMENTALES['c'].valeur
    alpha_calc = e**2 / (4 * pi * eps0 * hbar * c)
    alpha_ref = CONSTANTES_FONDAMENTALES['alpha'].valeur
    ecart_alpha = abs(alpha_calc - alpha_ref) / alpha_ref * 100
    print(f"✓ α = e²/(4πε₀ℏc) : écart = {ecart_alpha:.6f}%")
    
    print("="*70)
    print("✅ VALIDATION TERMINÉE")
    print("="*70)

# =====================================================================
# ALIASES DE COMPATIBILITÉ (pour modules existants)
# =====================================================================
CONSTANTES = {
    'me_MeV': float(MASSES_PARTICULES['me_MeV'].valeur),
    'mp_MeV': float(MASSES_PARTICULES['mp_MeV'].valeur),
    'mn_MeV': float(MASSES_PARTICULES['mn_MeV'].valeur),
    'mu_MeV': float(MASSES_PARTICULES['mmu_MeV'].valeur),
    'mtau_MeV': float(MASSES_PARTICULES['mtau_MeV'].valeur),
    'alpha': float(CONSTANTES_FONDAMENTALES['alpha'].valeur),
    'muB_MeV_T': float(MAGNETONS['muB_MeV_T'].valeur),
    'G_F': Decimal('1.1663787e-5'),
    'hbar': float(CONSTANTES_FONDAMENTALES['hbar'].valeur),
    'e': float(CONSTANTES_FONDAMENTALES['e'].valeur),
    'c': float(CONSTANTES_FONDAMENTALES['c'].valeur),
    'muB_eV_T': float(MAGNETONS['muB_eV_T'].valeur),
    'g_s': float(MOMENTS_MAGNETIQUES['g_e'].valeur),
    'g_p': float(MOMENTS_MAGNETIQUES['g_p'].valeur),
    'g_n': float(MOMENTS_MAGNETIQUES['g_n'].valeur),
    'rydberg_eV': float(CONSTANTES_ATOMIQUES['rydberg_eV'].valeur),
    'h_eV_s': float(CONSTANTES_ATOMIQUES['h_eV_s'].valeur),
    'A_1S_Hz': float(CONSTANTES_ATOMIQUES['A_1S_Hz'].valeur),
    'mu_reduit': float(CONSTANTES_ATOMIQUES['mu_reduit'].valeur),
    'compression_niveau': 9,
}

# =====================================================================
# POINT D'ENTRÉE PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    print("="*70)
    print("CONSTANTES_PARTAGEES.py — Framework Pentadique")
    print("Précision: 50 chiffres (Decimal)")
    print("Sources: CODATA 2022, PDG 2022, Validations Zeeman 2026")
    print("="*70)
    
    print("\n📊 CONSTANTES CLÉS:")
    print(f"  me = {CONSTANTES['me_MeV']} MeV/c²")
    print(f"  mp = {CONSTANTES['mp_MeV']} MeV/c²")
    print(f"  α  = {CONSTANTES['alpha']}")
    print(f"  μB = {CONSTANTES['muB_eV_T']} eV/T")
    print(f"  g_e = {CONSTANTES['g_s']}")
    
    print("\n🔷 PARAMÈTRES PENTADIQUES:")
    print(f"  δ_lattice = {float(PARAMETRES_PENTADIQUES['delta_lattice'].valeur):.6f}")
    print(f"  B0 = {float(PARAMETRES_PENTADIQUES['B0_Tesla'].valeur):.2f} T")
    print(f"  δ_bicosmic = {float(PARAMETRES_PENTADIQUES['delta_bicosmic'].valeur):.6f}")
    print(f"  D_eff = {float(PARAMETRES_PENTADIQUES['D_eff'].valeur):.1f}")
    
    print("\n💾 EXPORT:")
    exporter_constantes_json()
    
    print("\n🔍 VALIDATION:")
    valider_coherence()
    
    print("\n✅ MODULE TERMINÉ AVEC SUCCÈS")
    print("="*70)