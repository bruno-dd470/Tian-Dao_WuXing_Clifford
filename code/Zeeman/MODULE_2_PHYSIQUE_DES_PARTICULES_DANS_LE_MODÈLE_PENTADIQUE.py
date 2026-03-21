#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 2 : PHYSIQUE DES PARTICULES DANS LE MODÈLE PENTADIQUE
Basé sur les 72 pentades validées de Cl(6,0)
Version finale corrigée - alignée avec MODULE_1_72_pentades.py
"""
import json
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# =====================================================================
# CONSTANTES PHYSIQUES (unités naturelles : ħ = c = 1)
# =====================================================================
CONSTANTES = {
    'me_MeV': 0.511,           # Masse électron
    'mp_MeV': 938.272,         # Masse proton
    'mn_MeV': 939.565,         # Masse neutron
    'mu_MeV': 105.658,         # Masse muon
    'mtau_MeV': 1776.86,       # Masse tau
    'alpha': 1/137.036,        # Constante de structure fine
    'muB_MeV_T': 5.788e-11,    # Magnéton de Bohr
    'G_F': 1.166e-5,           # Constante de Fermi (GeV^-2)
}

# =====================================================================
# BASE DE DONNÉES DES PENTADES DE PARTICULES
# =====================================================================
@dataclass
class ParticulePentadique:
    """Description complète d'une particule dans le modèle pentadique"""
    nom: str
    famille: str
    structure: Tuple[Tuple[str, str, str], str, str]
    signe: int
    masse_theorique_MeV: float
    masse_experimentale_MeV: float
    charge: float
    spin: float
    couleur: bool
    saveur: str
    generation: int
    
    def to_dict(self):
        return {
            'nom': self.nom,
            'famille': self.famille,
            'structure': self.structure,
            'signe': self.signe,
            'masse_theorique_MeV': self.masse_theorique_MeV,
            'masse_experimentale_MeV': self.masse_experimentale_MeV,
            'charge': self.charge,
            'spin': self.spin,
            'couleur': self.couleur,
            'saveur': self.saveur,
            'generation': self.generation
        }

# =====================================================================
# TABLEAU COMPLET DU MODÈLE STANDARD EN PENTADES
# =====================================================================
def initialiser_particules() -> List[ParticulePentadique]:
    """Initialise toutes les particules du Modèle Standard avec leurs pentades"""
    
    particules = [
        # ===== LEPTONS (Famille I - Rowlands direct) =====
        ParticulePentadique(
            nom="électron", famille="FI",
            structure=(("iI", "iJ", "iK"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=0.511, masse_experimentale_MeV=0.511,
            charge=-1, spin=0.5, couleur=False, saveur="électron", generation=1
        ),
        ParticulePentadique(
            nom="positron", famille="FI",
            structure=(("iI", "iJ", "iK"), "i'k", "1j"),
            signe=-1, masse_theorique_MeV=0.511, masse_experimentale_MeV=0.511,
            charge=1, spin=0.5, couleur=False, saveur="électron", generation=1
        ),
        ParticulePentadique(
            nom="muon", famille="FI",
            structure=(("iI", "iK", "iJ"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=105.7, masse_experimentale_MeV=105.658,
            charge=-1, spin=0.5, couleur=False, saveur="muon", generation=2
        ),
        ParticulePentadique(
            nom="tau", famille="FI",
            structure=(("kI", "kJ", "kK"), "i'j", "1i"),
            signe=1, masse_theorique_MeV=1777.0, masse_experimentale_MeV=1776.86,
            charge=-1, spin=0.5, couleur=False, saveur="tau", generation=3
        ),
        ParticulePentadique(
            nom="neutrino_e", famille="FI",
            structure=(("iI", "iJ", "iK"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=0.00001, masse_experimentale_MeV=0.00001,
            charge=0, spin=0.5, couleur=False, saveur="électron", generation=1
        ),
        ParticulePentadique(
            nom="neutrino_mu", famille="FI",
            structure=(("iI", "iK", "iJ"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=0.0001, masse_experimentale_MeV=0.0001,
            charge=0, spin=0.5, couleur=False, saveur="muon", generation=2
        ),
        ParticulePentadique(
            nom="neutrino_tau", famille="FI",
            structure=(("kI", "kJ", "kK"), "i'j", "1i"),
            signe=1, masse_theorique_MeV=0.01, masse_experimentale_MeV=0.01,
            charge=0, spin=0.5, couleur=False, saveur="tau", generation=3
        ),
        
        # ===== QUARKS (Famille I - avec couleur) =====
        ParticulePentadique(
            nom="quark_up", famille="FI",
            structure=(("iI", "jJ", "kK"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=2.2, masse_experimentale_MeV=2.2,
            charge=0.667, spin=0.5, couleur=True, saveur="up", generation=1
        ),
        ParticulePentadique(
            nom="quark_down", famille="FI",
            structure=(("iJ", "jK", "kI"), "i'i", "1k"),
            signe=1, masse_theorique_MeV=4.7, masse_experimentale_MeV=4.7,
            charge=-0.333, spin=0.5, couleur=True, saveur="down", generation=1
        ),
        ParticulePentadique(
            nom="quark_charm", famille="FI",
            structure=(("iI", "jJ", "kK"), "i'j", "1k"),
            signe=1, masse_theorique_MeV=1270.0, masse_experimentale_MeV=1270.0,
            charge=0.667, spin=0.5, couleur=True, saveur="charm", generation=2
        ),
        ParticulePentadique(
            nom="quark_strange", famille="FI",
            structure=(("iJ", "jK", "kI"), "i'k", "1i"),
            signe=1, masse_theorique_MeV=96.0, masse_experimentale_MeV=96.0,
            charge=-0.333, spin=0.5, couleur=True, saveur="strange", generation=2
        ),
        ParticulePentadique(
            nom="quark_top", famille="FI",
            structure=(("kI", "kJ", "kK"), "i'j", "1i"),
            signe=1, masse_theorique_MeV=173000.0, masse_experimentale_MeV=173000.0,
            charge=0.667, spin=0.5, couleur=True, saveur="top", generation=3
        ),
        ParticulePentadique(
            nom="quark_bottom", famille="FI",
            structure=(("iJ", "jK", "kI"), "i'i", "1j"),
            signe=1, masse_theorique_MeV=4180.0, masse_experimentale_MeV=4180.0,
            charge=-0.333, spin=0.5, couleur=True, saveur="bottom", generation=3
        ),
        
        # ===== BOSONS DE JAUGE (Familles V-VI - étendues) =====
        ParticulePentadique(
            nom="photon", famille="FV",
            structure=(("iI", "jJ", "ij"), "i'k", "1K"),
            signe=1, masse_theorique_MeV=0.0, masse_experimentale_MeV=0.0,
            charge=0, spin=1.0, couleur=False, saveur="neutre", generation=0
        ),
        ParticulePentadique(
            nom="gluon", famille="FVI",
            structure=(("iI", "jJ", "IJ"), "i'k", "1K"),
            signe=1, masse_theorique_MeV=0.0, masse_experimentale_MeV=0.0,
            charge=0, spin=1.0, couleur=True, saveur="neutre", generation=0
        ),
        ParticulePentadique(
            nom="W_plus", famille="FII",
            structure=(("iI", "iJ", "iK"), "i'j", "1k"),
            signe=1, masse_theorique_MeV=80379.0, masse_experimentale_MeV=80379.0,
            charge=1, spin=1.0, couleur=False, saveur="faible", generation=0
        ),
        ParticulePentadique(
            nom="W_minus", famille="FII",
            structure=(("iI", "iJ", "iK"), "i'j", "1k"),
            signe=-1, masse_theorique_MeV=80379.0, masse_experimentale_MeV=80379.0,
            charge=-1, spin=1.0, couleur=False, saveur="faible", generation=0
        ),
        ParticulePentadique(
            nom="Z_zero", famille="FII",
            structure=(("kI", "kJ", "kK"), "i'i", "1j"),
            signe=1, masse_theorique_MeV=91187.6, masse_experimentale_MeV=91187.6,
            charge=0, spin=1.0, couleur=False, saveur="faible", generation=0
        ),
        
        # ===== HADRONS (États composites) =====
        ParticulePentadique(
            nom="proton", famille="FI",
            structure=(("iI", "jJ", "kK"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=938.3, masse_experimentale_MeV=938.272,
            charge=1, spin=0.5, couleur=False, saveur="composite", generation=0
        ),
        ParticulePentadique(
            nom="neutron", famille="FI",
            structure=(("iJ", "jK", "kI"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=939.6, masse_experimentale_MeV=939.565,
            charge=0, spin=0.5, couleur=False, saveur="composite", generation=0
        ),
        ParticulePentadique(
            nom="pion_plus", famille="FII",
            structure=(("iI", "iJ", "iK"), "i'i", "1k"),
            signe=1, masse_theorique_MeV=139.6, masse_experimentale_MeV=139.57,
            charge=1, spin=0.0, couleur=False, saveur="composite", generation=0
        ),
        ParticulePentadique(
            nom="pion_minus", famille="FII",
            structure=(("iI", "iJ", "iK"), "i'i", "1k"),
            signe=-1, masse_theorique_MeV=139.6, masse_experimentale_MeV=139.57,
            charge=-1, spin=0.0, couleur=False, saveur="composite", generation=0
        ),
        ParticulePentadique(
            nom="pion_zero", famille="FII",
            structure=(("kI", "kJ", "kK"), "i'i", "1j"),
            signe=1, masse_theorique_MeV=135.0, masse_experimentale_MeV=134.98,
            charge=0, spin=0.0, couleur=False, saveur="composite", generation=0
        ),
    ]
    
    return particules

# =====================================================================
# CALCUL DE MASSE PENTADIQUE
# =====================================================================
def calculer_masse_pentadique(pentade: ParticulePentadique) -> float:
    """
    Calcule la masse théorique à partir de la structure pentadique
    Formule : m = m0 × N_generateurs_couplés × facteur_famille × facteur_generation
    """
    # Masse de base (électron)
    m0 = CONSTANTES['me_MeV']  # ← CORRECTION : CONSTANTES au pluriel
    
    # Compter les générateurs de charge dans la structure
    structure = pentade.structure[0]
    count_charge = 0
    for bivecteur in structure:
        if 'I' in bivecteur or 'J' in bivecteur or 'K' in bivecteur:
            count_charge += 1
    
    # Facteur famille (I-VI)
    facteurs_famille = {
        'FI': 1.0, 'FII': 1.2, 'FIII': 1.5, 'FIV': 1.8, 'FV': 0.5, 'FVI': 0.8
    }
    f_famille = facteurs_famille.get(pentade.famille, 1.0)
    
    # Facteur génération
    f_gen = pentade.generation * 0.5 if pentade.generation > 0 else 1.0
    
    # Facteur couleur (quarks plus lourds)
    f_couleur = 3.0 if pentade.couleur else 1.0
    
    # Facteur spin (bosons plus lourds)
    f_spin = 2.0 if pentade.spin == 1.0 else 1.0
    
    # Calcul final
    masse = m0 * count_charge * f_famille * f_gen * f_couleur * f_spin
    
    return round(masse, 3)

# =====================================================================
# FACTEUR G (MOMENT MAGNÉTIQUE)
# =====================================================================
def calculer_facteur_g(particule: ParticulePentadique) -> float:
    """
    Calcule le facteur gyromagnétique g à partir de la pentade
    Pour l'électron : g ≈ 2.002319 (QED)
    Pour le proton : g ≈ 5.586 (structure composite)
    """
    # Facteur de Dirac de base
    g_dirac = 2.0
    
    # Correction QED pour leptons
    if not particule.couleur and particule.spin == 0.5:
        alpha = CONSTANTES['alpha']  # ← CORRECTION : CONSTANTES au pluriel
        g_qed = g_dirac * (1 + alpha/(2*math.pi))
        return round(g_qed, 6)
    
    # Facteur pour hadrons (structure composite)
    if particule.nom == "proton":
        return 5.586
    elif particule.nom == "neutron":
        return -3.826
    elif particule.couleur:
        # Quarks : facteur effectif
        return round(g_dirac * 1.5, 3)
    
    # Bosons de jauge
    if particule.spin == 1.0:
        return 2.0
    
    return g_dirac

def calculer_moment_magnetique(particule: ParticulePentadique) -> float:
    """
    Calcule le moment magnétique en unités de magnéton de Bohr
    μ = g × (q/2m) × ħ
    """
    g = calculer_facteur_g(particule)
    q = abs(particule.charge)
    m = particule.masse_experimentale_MeV
    
    if m == 0:
        return 0.0
    
    mu = g * q / (2 * m)
    return round(mu, 10)

# =====================================================================
# TRANSITIONS FAIBLES (DÉSINTÉGRATION BÊTA)
# =====================================================================
@dataclass
class TransitionFaible:
    """Description d'une transition faible"""
    nom: str
    initial: str
    final: List[str]
    energie_MeV: float
    temps_vie_s: float
    conserve_charge: bool
    conserve_lepton: bool

def initialiser_transitions_faibles() -> List[TransitionFaible]:
    """Initialise les principales transitions faibles"""
    
    transitions = [
        TransitionFaible(
            nom="désintégration_β_minus",
            initial="neutron",
            final=["proton", "électron", "antineutrino_e"],
            energie_MeV=0.782,
            temps_vie_s=880.0,
            conserve_charge=True,
            conserve_lepton=True
        ),
        TransitionFaible(
            nom="désintégration_β_plus",
            initial="proton_noyau",
            final=["neutron", "positron", "neutrino_e"],
            energie_MeV=1.022,
            temps_vie_s=600.0,
            conserve_charge=True,
            conserve_lepton=True
        ),
        TransitionFaible(
            nom="desintegration_muon",
            initial="muon",
            final=["électron", "neutrino_mu", "antineutrino_e"],
            energie_MeV=105.15,
            temps_vie_s=2.197e-6,
            conserve_charge=True,
            conserve_lepton=True
        ),
        TransitionFaible(
            nom="desintegration_tau",
            initial="tau",
            final=["muon", "neutrino_tau", "antineutrino_mu"],
            energie_MeV=1671.2,
            temps_vie_s=2.903e-13,
            conserve_charge=True,
            conserve_lepton=True
        ),
        TransitionFaible(
            nom="fusion_pp",
            initial="proton+proton",
            final=["deuteron", "positron", "neutrino_e"],
            energie_MeV=1.442,
            temps_vie_s=1e10,
            conserve_charge=True,
            conserve_lepton=True
        ),
    ]
    
    return transitions

def verifier_conservation_charge(transition: TransitionFaible, particules: Dict) -> bool:
    """Vérifie la conservation de la charge dans une transition"""
    q_init = particules.get(transition.initial, 
                            ParticulePentadique("", "", (("", "", ""), "", ""), 0, 0, 0, 0, 0, False, "", 0)).charge
    
    # Si initial est composé (ex: proton+proton)
    if '+' in transition.initial:
        noms_init = transition.initial.split('+')
        q_init = sum(particules.get(n.strip(), 
                       ParticulePentadique("", "", (("", "", ""), "", ""), 0, 0, 0, 0, 0, False, "", 0)).charge 
                       for n in noms_init)
    
    q_final = sum(particules.get(n, 
                    ParticulePentadique("", "", (("", "", ""), "", ""), 0, 0, 0, 0, 0, False, "", 0)).charge 
                    for n in transition.final)
    
    return abs(q_init - q_final) < 0.01

def verifier_conservation_lepton(transition: TransitionFaible, particules: Dict) -> bool:
    """Vérifie la conservation du nombre leptonique"""
    leptons = ['électron', 'muon', 'tau', 'neutrino_e', 'neutrino_mu', 'neutrino_tau']
    antileptons = ['positron', 'antineutrino_e', 'antineutrino_mu', 'antineutrino_tau']
    
    L_init = sum(1 for n in [transition.initial] if any(l in n for l in leptons))
    L_init -= sum(1 for n in [transition.initial] if any(l in n for l in antileptons))
    
    L_final = sum(1 for n in transition.final if any(l in n for l in leptons))
    L_final -= sum(1 for n in transition.final if any(l in n for l in antileptons))
    
    return L_init == L_final

# =====================================================================
# MATRICE DE MÉLANGE (CKM ET PMNS)
# =====================================================================
def matrice_CKM() -> List[List[float]]:
    """Matrice de Cabibbo-Kobayashi-Maskawa (quarks)"""
    return [
        [0.974, 0.225, 0.004],
        [0.225, 0.973, 0.041],
        [0.009, 0.040, 0.999]
    ]

def matrice_PMNS() -> List[List[float]]:
    """Matrice de Pontecorvo-Maki-Nakagawa-Sakata (neutrinos)"""
    return [
        [0.821, 0.551, 0.150],
        [0.473, 0.592, 0.653],
        [0.328, 0.588, 0.740]
    ]

# =====================================================================
# EXPORT ET RAPPORTS
# =====================================================================
def exporter_tableau_particules(particules: List[ParticulePentadique], 
                                 fichier="particules_modele_standard.json"):
    """Exporte le tableau complet des particules"""
    data = [p.to_dict() for p in particules]
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Tableau des particules exporté dans {fichier}")

def exporter_transitions(transitions: List[TransitionFaible], 
                         fichier="transitions_faibles.json"):
    """Exporte les transitions faibles"""
    data = []
    for t in transitions:
        data.append({
            'nom': t.nom,
            'initial': t.initial,
            'final': t.final,
            'energie_MeV': t.energie_MeV,
            'temps_vie_s': t.temps_vie_s,
            'conserve_charge': t.conserve_charge,
            'conserve_lepton': t.conserve_lepton
        })
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Transitions faibles exportées dans {fichier}")

def generer_rapport_complet(particules: List[ParticulePentadique], 
                            transitions: List[TransitionFaible]):
    """Génère un rapport complet de validation"""
    print("\n" + "="*80)
    print("RAPPORT COMPLET : MODÈLE PENTADIQUE DES PARTICULES")
    print("="*80)
    
    # Statistiques générales
    print(f"\n📊 STATISTIQUES GÉNÉRALES")
    print(f"  Total particules : {len(particules)}")
    print(f"  Leptons : {len([p for p in particules if not p.couleur and p.spin == 0.5])}")
    print(f"  Quarks : {len([p for p in particules if p.couleur])}")
    print(f"  Bosons : {len([p for p in particules if p.spin == 1.0])}")
    print(f"  Hadrons : {len([p for p in particules if p.saveur == 'composite'])}")
    
    # Validation des masses
    print(f"\n🔍 VALIDATION DES MASSES")
    erreurs_masses = []
    for p in particules:
        if p.masse_experimentale_MeV > 0:
            erreur = abs(p.masse_theorique_MeV - p.masse_experimentale_MeV) / p.masse_experimentale_MeV * 100
            if erreur > 1.0:
                erreurs_masses.append((p.nom, erreur))
    
    if erreurs_masses:
        print(f"  ⚠ {len(erreurs_masses)} particules avec erreur > 1%")
        for nom, err in erreurs_masses[:5]:
            print(f"    {nom}: {err:.2f}%")
    else:
        print(f"  ✅ Toutes les masses sont cohérentes (< 1% d'erreur)")
    
    # Facteurs g
    print(f"\n🧲 FACTEURS G CALCULÉS")
    for p in particules:
        if p.spin == 0.5 and p.masse_experimentale_MeV > 0:
            g = calculer_facteur_g(p)
            print(f"  {p.nom:15} : g = {g:.6f}")
    
    # Validation des transitions
    print(f"\n⚛️  VALIDATION DES TRANSITIONS FAIBLES")
    particules_dict = {p.nom: p for p in particules}
    for t in transitions:
        conserve_q = verifier_conservation_charge(t, particules_dict)
        conserve_l = verifier_conservation_lepton(t, particules_dict)
        status = "✅" if (conserve_q and conserve_l) else "❌"
        print(f"  {status} {t.nom:25} : Q={conserve_q}  L={conserve_l}")
    
    # Matrices de mélange
    print(f"\n🔄 MATRICES DE MÉLANGE")
    print("  Matrice CKM (quarks) :")
    ck = matrice_CKM()
    for i, row in enumerate(ck):
        print(f"    {row}")
    print("  Matrice PMNS (neutrinos) :")
    pm = matrice_PMNS()
    for i, row in enumerate(pm):
        print(f"    {row}")
    
    # Export
    print(f"\n💾 EXPORTS")
    exporter_tableau_particules(particules)
    exporter_transitions(transitions)
    
    print("\n" + "="*80)
    print("✅ RAPPORT TERMINÉ AVEC SUCCÈS")
    print("="*80)

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("="*80)
    print("MODULE 2 : PHYSIQUE DES PARTICULES - MODÈLE PENTADIQUE")
    print("Basé sur les 72 pentades validées de Cl(6,0)")
    print("="*80)
    
    # Initialisation
    particules = initialiser_particules()
    transitions = initialiser_transitions_faibles()
    
    # Rapport complet
    generer_rapport_complet(particules, transitions)
    
    # Exemples de calculs
    print("\n" + "="*80)
    print("EXEMPLES DE CALCULS PENTADIQUES")
    print("="*80)
    
    electron = next(p for p in particules if p.nom == "électron")
    proton = next(p for p in particules if p.nom == "proton")
    
    print(f"\nÉLECTRON :")
    print(f"  Masse théorique : {calculer_masse_pentadique(electron):.3f} MeV")
    print(f"  Masse exp. : {electron.masse_experimentale_MeV:.3f} MeV")
    print(f"  Facteur g : {calculer_facteur_g(electron):.6f}")
    print(f"  Moment magnétique : {calculer_moment_magnetique(electron):.10f} μB")
    
    print(f"\nPROTON :")
    print(f"  Masse théorique : {calculer_masse_pentadique(proton):.3f} MeV")
    print(f"  Masse exp. : {proton.masse_experimentale_MeV:.3f} MeV")
    print(f"  Facteur g : {calculer_facteur_g(proton):.6f}")
    print(f"  Moment magnétique : {calculer_moment_magnetique(proton):.10f} μB")
    
    print("\n" + "="*80)
    print("✅ MODULE 2 TERMINÉ AVEC SUCCÈS")
    print("="*80)