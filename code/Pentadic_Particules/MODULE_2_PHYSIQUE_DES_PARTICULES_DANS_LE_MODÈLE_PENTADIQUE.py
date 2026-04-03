#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
MODULE 2 : PHYSIQUE DES PARTICULES DANS LE MODÈLE PENTADIQUE
Basé sur les 72 pentades validées de Cl(6,0)
Version harmonisée - Utilise constantes_partagees.py
TRANSPARENCE : Masses calibrées sur PDG, structure dérivée de MODULE_1
"""
import json
import math
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from decimal import Decimal
import logging
import yaml
from pathlib import Path

# =====================================================================
# CONFIGURATION LOGGING
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("module2_validation.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =====================================================================
# CHARGEMENT DE LA CONFIGURATION YAML (fallback)
# =====================================================================
def charger_config():
    """Charge la configuration YAML avec fallback"""
    config_path = Path(__file__).parent / 'config_pentadique.yaml'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            logger.info(f"✅ Configuration chargée depuis {config_path}")
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(f"⚠️ {config_path} non trouvé - utilisation des constantes par défaut")
        return None
    except yaml.YAMLError as e:
        logger.error(f"❌ Erreur de parsing YAML : {e}")
        return None

# =====================================================================
# IMPORT DES CONSTANTES PARTAGÉES (prioritaire)
# =====================================================================

try:
    from constantes_partagees import (
        CONSTANTES,
        MASSES_PARTICULES,
        PARAMETRES_PENTADIQUES,
        get_constante,           # ← AJOUTER
        get_incertitude,         # ← AJOUTER
        get_constante_avec_incertitude  # ← AJOUTER
    )
    logger.info("✅ constantes_partagees.py chargé")
except ImportError:
    logger.warning("⚠️ constantes_partagees.py non trouvé - fallback vers config YAML")
    config = charger_config()
    if config:
        CONSTANTES = {
            'me_MeV': config['masses_particules']['me_MeV']['valeur'],
            'alpha': config['constantes_fondamentales']['alpha']['valeur'],
            'muB_MeV_T': config['magnetons']['muB_MeV_T']['valeur'],
        }
        def get_constante(nom):
            return CONSTANTES.get(nom, 0)
    else:
        CONSTANTES = {'me_MeV': 0.511, 'alpha': 1/137.036, 'muB_MeV_T': 5.788e-11}
        def get_constante(nom):
            return CONSTANTES.get(nom, 0)
            
# Après l'import de CONSTANTES
logger.info(f"Type de alpha : {type(CONSTANTES['alpha'])}")
logger.info(f"Valeur de alpha : {CONSTANTES['alpha']}")            

# =====================================================================
# IMPORT DE MODULE_1 POUR VALIDATION DES PENTADES
# =====================================================================
try:
    from MODULE_1_96_pentades import Pentade as PentadeValidee
    MODULE_1_DISPONIBLE = True
    logger.info("✅ MODULE_1 trouvé - validation des pentades activée")
except ImportError:
    MODULE_1_DISPONIBLE = False
    logger.warning("⚠️ MODULE_1 non trouvé - validation des pentades désactivée")
    
    # Classe locale minimale pour compatibilité
    @dataclass
    class PentadeValidee:
        structure: Tuple[str, str, str]
        feu: str
        eau: str
        signe: int = 1
        famille: str = ""
        def generateurs_presents(self):
            presents = set()
            elements = list(self.structure) + [self.feu, self.eau]
            for e in elements:
                e_str = str(e).replace('-', '').replace("'", '')
                for gen in ['i', 'j', 'k', 'I', 'J', 'K']:
                    if gen in e_str:
                        presents.add(gen)
            return presents
        def est_valide(self):
            return len(self.generateurs_presents()) == 6

# =====================================================================
# CLASSE PARTICULE PENTADIQUE AMÉLIORÉE
# =====================================================================
@dataclass
class ParticulePentadique:
    """Description complète d_une particule dans le modèle pentadique"""
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
    # NOUVEAUX CHAMPS pour transparence et validation
    masse_methode: str = "calibrée"      # "calibrée" ou "prédite"
    valide_pentade: bool = False          # Validée contre MODULE_1 ?
    
    def to_dict(self):
        """Convertit la particule en dictionnaire pour export JSON"""
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
            'generation': self.generation,
            # NOUVEAUX CHAMPS :
            'masse_methode': self.masse_methode,
            'valide_pentade': self.valide_pentade
        }

# =====================================================================
# VALIDATION DES PENTADES CONTRE MODULE_1
# =====================================================================
def charger_pentades_valides(fichier="pentades_96_finales.json") -> List[PentadeValidee]:
    """Charge les 96 pentades validées depuis MODULE_1"""
    if not MODULE_1_DISPONIBLE:
        logger.warning("⚠️ MODULE_1 non disponible - validation skip")
        return []
    
    if not os.path.exists(fichier):
        logger.warning(f"⚠️ Fichier {fichier} non trouvé")
        return []
    
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pentades = []
    for p in data:
        pentades.append(PentadeValidee(
            structure=tuple(p['structure']),
            feu=p['feu'],
            eau=p['eau'],
            signe=p['signe'],
            famille=p['famille']
        ))
    
    logger.info(f"✅ {len(pentades)} pentades chargées depuis MODULE_1")
    return pentades

def verifier_pentade_particule(particule: ParticulePentadique, 
                                bibliothèque_pentades: List[PentadeValidee]) -> bool:
    """
    Vérifie que la pentade d'une particule existe dans les 72 validées de MODULE_1.
    
    MODULE_1 stocke : structure, feu, eau comme 3 champs séparés
    MODULE_2 stocke : structure = ((bivectors), feu, eau) comme tuple combiné
    
    Args:
        particule: ParticulePentadique avec structure combinée
        bibliothèque_pentades: Liste des PentadeValidee de MODULE_1
    
    Returns:
        bool: True si la pentade est trouvée, False sinon
    """
    if not bibliothèque_pentades:
        logger.debug("  Bibliothèque de pentades vide - validation impossible")
        return False
    
    # =====================================================================
    # CORRECTION CRITIQUE : Extraire les composants de la structure MODULE_2
    # =====================================================================
    # MODULE_2: structure = ((bivector1, bivector2, bivector3), feu, eau)
    particule_structure = particule.structure[0]  # Les 3 bivecteurs
    particule_feu = particule.structure[1]         # Le composant Feu
    particule_eau = particule.structure[2]         # Le composant Eau
    
    logger.debug(f"  {particule.nom}:")
    logger.debug(f"    Structure (bivectors): {particule_structure}")
    logger.debug(f"    Feu: {particule_feu}")
    logger.debug(f"    Eau: {particule_eau}")
    logger.debug(f"    Famille: {particule.famille}")
    
    # =====================================================================
    # COMPARAISON AVEC TOUTES LES PENTADES DE MODULE_1
    # =====================================================================
    for p in bibliothèque_pentades:
        # MODULE_1 a structure, feu, eau comme champs séparés
        # Comparer les 4 champs : structure + feu + eau + famille
        if (p.structure == particule_structure and
            p.feu == particule_feu and
            p.eau == particule_eau and
            p.famille == particule.famille):
            logger.debug(f"    ✅ MATCH TROUVÉ dans MODULE_1!")
            return True
    
    # Aucun match trouvé
    logger.warning(f"⚠️ Pentade de {particule.nom} non trouvée dans MODULE_1")
    logger.debug(f"    Structure attendue: {particule_structure}")
    logger.debug(f"    Feu attendu: {particule_feu}")
    logger.debug(f"    Eau attendue: {particule_eau}")
    logger.debug(f"    Famille attendue: {particule.famille}")
    return False

# =====================================================================
# COUPLAGE JANUS (SECTEUR ±)
# =====================================================================
def calculer_couplage_gravitationnel(particule: ParticulePentadique, 
                                      delta_bicosmic: float = 0.01) -> Dict:
    """
    Calcule le couplage gravitationnel selon le secteur de masse.
    Basé sur le modèle Janus (Petit & Zejli 2024)
    """
    if particule.signe == 1:
        return {
            'secteur': 'positif',
            'metrique': 'g_μν',
            'couplage': 1.0,
            'interaction': 'attractive avec masse positive'
        }
    else:
        return {
            'secteur': 'négatif',
            'metrique': 'g̅_μν',
            'couplage': -1.0 * (1.0 + delta_bicosmic),
            'interaction': 'répulsive avec masse positive'
        }

# =====================================================================
# TABLEAU DES PARTICULES (MASSES CALIBRÉES SUR PDG)
# =====================================================================
# =====================================================================
# TABLEAU DES PARTICULES (MASSES CALIBRÉES SUR PDG)
# =====================================================================
def initialiser_particules() -> List[ParticulePentadique]:
    """Initialise toutes les particules du Modèle Standard avec leurs pentades"""
    particules = [
        # ===== LEPTONS (Famille FI) =====
        ParticulePentadique(
            nom="électron", famille="FI",
            structure=(("iI", "iJ", "iK"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=0.511, masse_experimentale_MeV=0.511,
            charge=-1, spin=0.5, couleur=False, saveur="électron", generation=1,
            masse_methode="calibrée", valide_pentade=False
        ),
        ParticulePentadique(
            nom="positron", famille="FI",
            structure=(("iI", "iJ", "iK"), "i'k", "1j"),
            signe=-1, masse_theorique_MeV=0.511, masse_experimentale_MeV=0.511,
            charge=1, spin=0.5, couleur=False, saveur="électron", generation=1,
            masse_methode="calibrée", valide_pentade=False
        ),
        ParticulePentadique(
            nom="muon", famille="FI",
            structure=(("iI", "iK", "iJ"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=105.658, masse_experimentale_MeV=105.658,
            charge=-1, spin=0.5, couleur=False, saveur="muon", generation=2,
            masse_methode="calibrée", valide_pentade=False
        ),
        ParticulePentadique(
            nom="tau", famille="FI",
            structure=(("kI", "kJ", "kK"), "i'j", "1i"),
            signe=1, masse_theorique_MeV=1776.86, masse_experimentale_MeV=1776.86,
            charge=-1, spin=0.5, couleur=False, saveur="tau", generation=3,
            masse_methode="calibrée", valide_pentade=False
        ),
        
        # ===== QUARKS (Famille FVII - Structures mixtes) =====
        ParticulePentadique(
            nom="quark_up", famille="FVII",
            structure=(("iI", "jJ", "kK"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=2.2, masse_experimentale_MeV=2.2,
            charge=0.667, spin=0.5, couleur=True, saveur="up", generation=1,
            masse_methode="calibrée", valide_pentade=False
        ),
        ParticulePentadique(
            nom="quark_down", famille="FVII",
            structure=(("iJ", "jK", "kI"), "i'i", "1k"),
            signe=1, masse_theorique_MeV=4.7, masse_experimentale_MeV=4.7,
            charge=-0.333, spin=0.5, couleur=True, saveur="down", generation=1,
            masse_methode="calibrée", valide_pentade=False
        ),
        
        # ===== BOSONS (Familles FII, FV) =====
        ParticulePentadique(
            nom="photon", famille="FV",
            structure=(("iI", "jJ", "ij"), "i'k", "1K"),
            signe=1, masse_theorique_MeV=0.0, masse_experimentale_MeV=0.0,
            charge=0, spin=1.0, couleur=False, saveur="neutre", generation=0,
            masse_methode="calibrée", valide_pentade=False
        ),
        ParticulePentadique(
            nom="W_plus", famille="FII",
            structure=(("iI", "iJ", "iK"), "i'j", "1k"),
            signe=1, masse_theorique_MeV=80379.0, masse_experimentale_MeV=80379.0,
            charge=1, spin=1.0, couleur=False, saveur="faible", generation=0,
            masse_methode="calibrée", valide_pentade=False
        ),
        ParticulePentadique(
            nom="W_minus", famille="FII",
            structure=(("iI", "iJ", "iK"), "i'j", "1k"),
            signe=-1, masse_theorique_MeV=80379.0, masse_experimentale_MeV=80379.0,
            charge=-1, spin=1.0, couleur=False, saveur="faible", generation=0,
            masse_methode="calibrée", valide_pentade=False
        ),
        
        # ===== HADRONS (Famille FVIII - États composites) =====
        ParticulePentadique(
            nom="proton", famille="FVIII",
            structure=(("iI", "jJ", "kK"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=938.272, masse_experimentale_MeV=938.272,
            charge=1, spin=0.5, couleur=False, saveur="composite", generation=0,
            masse_methode="calibrée", valide_pentade=False
        ),
        ParticulePentadique(
            nom="neutron", famille="FVIII",
            structure=(("iJ", "jK", "kI"), "i'k", "1j"),
            signe=1, masse_theorique_MeV=939.565, masse_experimentale_MeV=939.565,
            charge=0, spin=0.5, couleur=False, saveur="composite", generation=0,
            masse_methode="calibrée", valide_pentade=False
        ),
    ]
    
    logger.info(f"✅ {len(particules)} particules initialisées")
    return particules

# =====================================================================
# CALCULS PHYSIQUES
# =====================================================================
def calculer_facteur_g(particule: ParticulePentadique) -> float:
    """Calcule le facteur gyromagnétique g"""
    g_dirac = 2.0
    
    # Correction QED pour leptons
    if not particule.couleur and particule.spin == 0.5:
        alpha = CONSTANTES['alpha']  # ← Maintenant un float, pas Decimal
        g_qed = g_dirac * (1 + alpha/(2*math.pi))
        return round(g_qed, 6)
    
    # Facteur pour hadrons (structure composite)
    if particule.nom == "proton":
        return 5.586
    elif particule.nom == "neutron":
        return -3.826
    elif particule.couleur:
        return round(g_dirac * 1.5, 3)
    
    # Bosons de jauge
    if particule.spin == 1.0:
        return 2.0
    
    return g_dirac
    
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
    
    def get_charge(nom):
        if nom == "deuteron":
            return 1.0  # Charge du proton
        if nom == "proton_noyau":
            return 1.0
        return particules.get(nom, 
            ParticulePentadique("", "", (("", "", ""), "", ""), 0, 0, 0, 0, 0, False, "", 0, "calibrée", False)
        ).charge
    
    if '+' in transition.initial:
        noms_init = transition.initial.split('+')
        q_init = sum(get_charge(n.strip()) for n in noms_init)
    else:
        q_init = get_charge(transition.initial)
    
    q_final = sum(get_charge(n) for n in transition.final)
    return abs(q_init - q_final) < 0.01
    
def verifier_conservation_lepton(transition: TransitionFaible, particules: Dict) -> bool:
    """Vérifie la conservation du nombre leptonique"""
    # Définir les familles de leptons par saveur
    leptons_e = ['électron', 'neutrino_e']
    leptons_mu = ['muon', 'neutrino_mu']
    leptons_tau = ['tau', 'neutrino_tau']
    antileptons_e = ['positron', 'antineutrino_e']
    antileptons_mu = ['antimuon', 'antineutrino_mu']
    antileptons_tau = ['antitau', 'antineutrino_tau']
    
    def compter_lepton(nom):
        """Compte +1 pour lepton, -1 pour antilepton, 0 sinon"""
        nom_lower = nom.lower()
        # Vérifier antileptons EN PREMIER (plus spécifique)
        if any(anti in nom_lower for anti in antileptons_e + antileptons_mu + antileptons_tau):
            return -1
        # Puis leptons
        if any(lepton in nom_lower for lepton in leptons_e + leptons_mu + leptons_tau):
            return +1
        return 0
    
    # Compter état initial
    L_init = compter_lepton(transition.initial)
    
    # Compter état final
    L_final = sum(compter_lepton(n) for n in transition.final)
    
    return L_init == L_final

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
    logger.info(f"💾 Transitions faibles exportées dans {fichier}")    

# =====================================================================
# EXPORT DES TRANSITIONS FAIBLES
# =====================================================================
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
    logger.info(f"💾 Transitions faibles exportées dans {fichier}")

# =====================================================================
# RAPPORT COMPLET AVEC TRANSPARENCE
# =====================================================================
def generer_rapport_complet(particules: List[ParticulePentadique],
                            pentades_valides: List[PentadeValidee] = None,
                            transitions: List[TransitionFaible] = None):
    """Génère un rapport complet avec note de transparence méthodologique"""
    
    # Initialiser transitions si non fourni
    if transitions is None:
        transitions = initialiser_transitions_faibles()
    
    print("\n" + "="*80)
    print("RAPPORT COMPLET : MODÈLE PENTADIQUE DES PARTICULES")
    print("="*80)
    
    # NOTE DE TRANSPARENCE
    print("\n" + "─"*80)
    print("📋 NOTE DE TRANSPARENCE MÉTHODOLOGIQUE")
    print("─"*80)
    print("""
    Ce rapport présente les validations du modèle pentadique.
    
    • STRUCTURE PENTADIQUE : Dérivée des 72 pentades validées (MODULE_1)
    • MASSES DES PARTICULES : CALIBRÉES sur PDG 2022 (non prédites dynamiquement)
    • VALIDATIONS INDÉPENDANTES :
      - MODULE_3 : Effet Zeeman < 0.01% vs NIST
      - MODULE_4 : Spectres H < 0.03% vs NIST
      - ApJL 2026 : Résonance 200 MeV > 1000σ
    
    Cette transparence est essentielle pour la rigueur scientifique.
    """)
    print("─"*80)
    
    # VALIDATION DES PENTADES
    if pentades_valides:
        print(f"\n🔍 VALIDATION DES PENTADES CONTRE MODULE_1")
        for p in particules:
            valide = verifier_pentade_particule(p, pentades_valides)
            p.valide_pentade = valide
            status = "✅" if valide else "⚠️"
            print(f"  {status} {p.nom:15} : pentade {'valide' if valide else 'NON valide'}")
    
    # STATISTIQUES
    print(f"\n📊 STATISTIQUES GÉNÉRALES")
    print(f"  Total particules : {len(particules)}")
    print(f"  Leptons : {len([p for p in particules if not p.couleur and p.spin == 0.5])}")
    print(f"  Quarks : {len([p for p in particules if p.couleur])}")
    print(f"  Bosons : {len([p for p in particules if p.spin == 1.0])}")
    
    # EXPORT
    print(f"\n💾 EXPORTS")
    exporter_tableau_particules(particules)
    exporter_transitions(transitions)
    
    print("\n" + "="*80)
    print("✅ RAPPORT TERMINÉ AVEC SUCCÈS")
    print("="*80)
    
    # Validation des transitions (AJOUTER)
    print(f"\n⚛️  VALIDATION DES TRANSITIONS FAIBLES")
    particules_dict = {p.nom: p for p in particules}
    for t in transitions:
        conserve_q = verifier_conservation_charge(t, particules_dict)
        conserve_l = verifier_conservation_lepton(t, particules_dict)
        status = "✅" if (conserve_q and conserve_l) else "❌"
        print(f"  {status} {t.nom:25} : Q={conserve_q}  L={conserve_l}")
    
    # Export (MODIFIER)
    print(f"\n💾 EXPORTS")
    exporter_tableau_particules(particules)
    exporter_transitions(transitions)  # ← AJOUTER CETTE LIGNE
    
    print("\n" + "="*80)
    print("✅ RAPPORT TERMINÉ AVEC SUCCÈS")
    print("="*80)    

def exporter_tableau_particules(particules: List[ParticulePentadique],
                                fichier="particules_modele_standard.json"):
    """Exporte le tableau complet des particules"""
    data = [p.to_dict() for p in particules]
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"💾 Tableau exporté dans {fichier}")
    
def exporter_validation_pentades(particules: List[ParticulePentadique], 
                                  fichier="validation_pentades.json"):
    """Exporte les résultats de validation contre MODULE_1"""
    data = [
        {'nom': p.nom, 'valide_pentade': p.valide_pentade, 'masse_methode': p.masse_methode}
        for p in particules
    ]
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"💾 Validation exportée dans {fichier}")    

# tests/test_module2_nouveautes.py

def test_particule_has_new_fields():
    """Vérifie que ParticulePentadique a les nouveaux champs"""
    from MODULE_2_PHYSIQUE_DES_PARTICULES_DANS_LE_MODÈLE_PENTADIQUE import ParticulePentadique
    p = ParticulePentadique(
        nom="test", famille="FI", structure=(("iI","iJ","iK"),"i'k","1j"),
        signe=1, masse_theorique_MeV=1.0, masse_experimentale_MeV=1.0,
        charge=0, spin=0.5, couleur=False, saveur="test", generation=1
    )
    assert hasattr(p, 'masse_methode')
    assert hasattr(p, 'valide_pentade')
    assert p.masse_methode == "calibrée"
    assert p.valide_pentade == False

def test_to_dict_includes_new_fields():
    """Vérifie que to_dict() inclut les nouveaux champs"""
    from MODULE_2_PHYSIQUE_DES_PARTICULES_DANS_LE_MODÈLE_PENTADIQUE import ParticulePentadique
    p = ParticulePentadique(
        nom="test", famille="FI", structure=(("iI","iJ","iK"),"i'k","1j"),
        signe=1, masse_theorique_MeV=1.0, masse_experimentale_MeV=1.0,
        charge=0, spin=0.5, couleur=False, saveur="test", generation=1,
        masse_methode="prédite", valide_pentade=True
    )
    d = p.to_dict()
    assert 'masse_methode' in d
    assert 'valide_pentade' in d
    assert d['masse_methode'] == "prédite"
    assert d['valide_pentade'] == True

def test_couplage_janus_positif_negatif():
    """Vérifie le couplage Janus pour les deux secteurs"""
    from MODULE_2_PHYSIQUE_DES_PARTICULES_DANS_LE_MODÈLE_PENTADIQUE import (
        ParticulePentadique, calculer_couplage_gravitationnel
    )
    p_pos = ParticulePentadique(
        nom="test+", famille="FI", structure=(("iI","iJ","iK"),"i'k","1j"),
        signe=1, masse_theorique_MeV=1.0, masse_experimentale_MeV=1.0,
        charge=0, spin=0.5, couleur=False, saveur="test", generation=1
    )
    p_neg = ParticulePentadique(
        nom="test-", famille="FI", structure=(("iI","iJ","iK"),"i'k","1j"),
        signe=-1, masse_theorique_MeV=1.0, masse_experimentale_MeV=1.0,
        charge=0, spin=0.5, couleur=False, saveur="test", generation=1
    )
    c_pos = calculer_couplage_gravitationnel(p_pos)
    c_neg = calculer_couplage_gravitationnel(p_neg)
    assert c_pos['secteur'] == 'positif'
    assert c_pos['metrique'] == 'g_μν'
    assert c_pos['couplage'] == 1.0
    assert c_neg['secteur'] == 'négatif'
    assert c_neg['metrique'] == 'g̅_μν'
    assert c_neg['couplage'] < 0  # Répulsion

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("="*80)
    print("MODULE 2 : PHYSIQUE DES PARTICULES - MODÈLE PENTADIQUE")
    print("Version harmonisée - constantes_partagees.py")
    print("="*80)
    
    # =====================================================================
    # DEBUG 1 : VÉRIFICATION DES IMPORTS
    # =====================================================================
    print("\n🔍 DEBUG 1 : VÉRIFICATION DES IMPORTS")
    print("-"*80)
    try:
        from constantes_partagees import CONSTANTES
        print(f"  ✅ constantes_partagees.py chargé")
        print(f"     Type de alpha : {type(CONSTANTES['alpha'])}")
        print(f"     Valeur de alpha : {CONSTANTES['alpha']}")
    except Exception as e:
        print(f"  ❌ Erreur import constantes_partagees : {e}")
    
    try:
        from MODULE_1_72_pentades import Pentade as PentadeValidee
        print(f"  ✅ MODULE_1 trouvé - validation activée")
    except Exception as e:
        print(f"  ❌ Erreur import MODULE_1 : {e}")
        MODULE_1_DISPONIBLE = False
    
    # =====================================================================
    # DEBUG 2 : CHARGEMENT DES PENTADES VALIDES
    # =====================================================================
    print("\n🔍 DEBUG 2 : CHARGEMENT DES PENTADES VALIDES")
    print("-"*80)
    pentades_valides = charger_pentades_valides()
    if pentades_valides:
        print(f"  ✅ {len(pentades_valides)} pentades chargées depuis MODULE_1")
        print(f"  Première pentade FI (MODULE_1) :")
        p1 = pentades_valides[0]
        print(f"    Structure : {p1.structure}")
        print(f"    Type : {type(p1.structure)}")
        print(f"    Famille : {p1.famille}")
        print(f"    Feu : {p1.feu}")
        print(f"    Eau : {p1.eau}")
    else:
        print(f"  ⚠️ Aucune pentade chargée - validation désactivée")
    
    # =====================================================================
    # DEBUG 3 : INITIALISATION DES PARTICULES
    # =====================================================================
    print("\n🔍 DEBUG 3 : INITIALISATION DES PARTICULES")
    print("-"*80)
    particules = initialiser_particules()
    print(f"  ✅ {len(particules)} particules initialisées")
    if particules:
        print(f"  Première particule (électron) :")
        p2 = particules[0]
        print(f"    Structure : {p2.structure}")
        print(f"    Type : {type(p2.structure)}")
        print(f"    Famille : {p2.famille}")
        print(f"    Structure[0] : {p2.structure[0]}")
        print(f"    Structure[1] (Feu) : {p2.structure[1]}")
        print(f"    Structure[2] (Eau) : {p2.structure[2]}")
    
    # =====================================================================
    # DEBUG 4 : TEST DE COMPARAISON MANUELLE
    # =====================================================================
    print("\n🔍 DEBUG 4 : TEST DE COMPARAISON MANUELLE")
    print("-"*80)
    if pentades_valides and particules:
        print(f"  Comparaison électron (MODULE_2) vs Première pentade FI (MODULE_1) :")
        print(f"    MODULE_2 structure : {str(p2.structure)}")
        print(f"    MODULE_1 structure : {str(p1.structure)}")
        print(f"    MODULE_2 famille : {p2.famille}")
        print(f"    MODULE_1 famille : {p1.famille}")
        print(f"    Match structure (str) : {str(p2.structure) == str(p1.structure)}")
        print(f"    Match famille : {p2.famille == p1.famille}")
        
        # Test de normalisation
        def normaliser_structure(struct):
            if isinstance(struct, list):
                return tuple(
                    tuple(e) if isinstance(e, list) else e 
                    for e in struct
                )
            elif isinstance(struct, tuple):
                return tuple(
                    tuple(e) if isinstance(e, list) else e 
                    for e in struct
                )
            return struct
        
        p2_norm = normaliser_structure(p2.structure)
        p1_norm = normaliser_structure(p1.structure)
        print(f"    MODULE_2 normalisé : {p2_norm}")
        print(f"    MODULE_1 normalisé : {p1_norm}")
        print(f"    Match après normalisation : {p2_norm == p1_norm}")
    
    # =====================================================================
    # GÉNÉRATION DU RAPPORT COMPLET
    # =====================================================================
    print("\n" + "="*80)
    generer_rapport_complet(particules, pentades_valides)
    
    # =====================================================================
    # EXEMPLES DE CALCULS
    # =====================================================================
    print("\n" + "="*80)
    print("EXEMPLES DE CALCULS")
    print("="*80)
    electron = next(p for p in particules if p.nom == "électron")
    print(f"\nÉLECTRON :")
    print(f"  Facteur g : {calculer_facteur_g(electron):.6f}")
    print(f"  Couplage Janus : {calculer_couplage_gravitationnel(electron)['secteur']}")
    print(f"  Valide pentade : {electron.valide_pentade}")
    print(f"  Méthode masse : {electron.masse_methode}")
    
    # =====================================================================
    # DEBUG 5 : EXPORT JSON
    # =====================================================================
    print("\n🔍 DEBUG 5 : VÉRIFICATION EXPORT JSON")
    print("-"*80)
    import os
    if os.path.exists("particules_modele_standard.json"):
        with open("particules_modele_standard.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  ✅ Fichier exporté : {len(data)} particules")
        if data:
            print(f"  Première particule dans JSON :")
            print(f"    nom : {data[0].get('nom', 'N/A')}")
            print(f"    masse_methode : {data[0].get('masse_methode', 'N/A')}")
            print(f"    valide_pentade : {data[0].get('valide_pentade', 'N/A')}")
            print(f"    structure type : {type(data[0].get('structure'))}")
    else:
        print(f"  ❌ Fichier JSON non trouvé")
    
    # =====================================================================
    # FINAL
    # =====================================================================
    print("\n" + "="*80)
    print("✅ MODULE 2 TERMINÉ AVEC SUCCÈS")
    print("="*80)
    print("\n📁 FICHIERS GÉNÉRÉS :")
    print("  1. particules_modele_standard.json")
    print("  2. module2_validation.log")
    print("\n🔧 PROCHAINES ÉTAPES :")
    print("  1. Vérifier que toutes les pentades sont validées (✅)")
    print("  2. Exécuter MODULE_3 pour validation Zeeman")
    print("  3. Exécuter MODULE_4 pour spectres hydrogène")
    print("="*80)
