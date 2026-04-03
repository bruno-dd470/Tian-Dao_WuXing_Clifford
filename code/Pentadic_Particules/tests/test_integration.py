#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_integration.py
==========================
Tests unitaires transversaux pour le framework pentadique.

Valide la cohérence entre MODULE_1, MODULE_2, MODULE_3, MODULE_4
et constantes_partagees.py

Auteur : Bruno DE DOMINICIS
Date : Mars 2026
License : CC BY 4.0
"""
import pytest
import json
import os
from decimal import Decimal

# =====================================================================
# FIXTURES
# =====================================================================
@pytest.fixture
def constantes():
    """Charge les constantes partagées"""
    from constantes_partagees import CONSTANTES, MASSES_PARTICULES
    return {'CONSTANTES': CONSTANTES, 'MASSES': MASSES_PARTICULES}

@pytest.fixture
def pentades_valides():
    """Charge les 72 pentades de MODULE_1"""
    if not os.path.exists('pentades_72_finales.json'):
        pytest.skip("pentades_72_finales.json non trouvé")
    
    with open('pentades_72_finales.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def particules():
    """Charge les particules de MODULE_2"""
    if not os.path.exists('particules_modele_standard.json'):
        pytest.skip("particules_modele_standard.json non trouvé")
    
    with open('particules_modele_standard.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# =====================================================================
# TESTS DE COHÉRENCE DES CONSTANTES
# =====================================================================
class TestConstantes:
    
    def test_precision_decimal(self, constantes):
        """Vérifie que les constantes ont une précision suffisante"""
        me = constantes['MASSES']['me_MeV']
        assert len(str(me.valeur)) > 10, "Précision insuffisante pour me_MeV"
    
    def test_coherence_h_hbar(self, constantes):
        """Vérifie h = 2πℏ"""
        from constantes_partagees import CONSTANTES_FONDAMENTALES
        import math
        
        pi = Decimal('3.14159265358979323846')
        h_calc = 2 * pi * CONSTANTES_FONDAMENTALES['hbar'].valeur
        h_ref = CONSTANTES_FONDAMENTALES['h'].valeur
        
        ecart = abs(h_calc - h_ref) / h_ref
        assert ecart < Decimal('1e-10'), f"Écart h vs 2πℏ : {ecart}"
    
    def test_incertitudes_presentes(self, constantes):
        """Vérifie que toutes les constantes ont des incertitudes"""
        for nom, const in constantes['MASSES'].items():
            assert const.incertitude >= 0, f"Incertitude manquante pour {nom}"

# =====================================================================
# TESTS DE COHÉRENCE MODULE_1 ↔ MODULE_2
# =====================================================================
class TestModule1_Module2:
    
    def test_toutes_pentades_valides(self, pentades_valides, particules):
        """Vérifie que toutes les pentades de MODULE_2 existent dans MODULE_1"""
        if not pentades_valides:
            pytest.skip("MODULE_1 non disponible")
        
        for p in particules:
            structure_str = str(p['structure'])
            trouve = False
            for pv in pentades_valides:
                if str(pv['structure']) == structure_str and pv['famille'] == p['famille']:
                    trouve = True
                    break
            assert trouve, f"Pentade de {p['nom']} non trouvée dans MODULE_1"
    
    def test_72_pentades_completes(self, pentades_valides):
        """Vérifie que MODULE_1 a exactement 72 pentades"""
        assert len(pentades_valides) == 72, f"Attendu 72 pentades, obtenu {len(pentades_valides)}"
    
    def test_equilibre_yang_yin(self, pentades_valides):
        """Vérifie l'équilibre Yang/Yin (36/36)"""
        yang = len([p for p in pentades_valides if p['signe'] == 1])
        yin = len([p for p in pentades_valides if p['signe'] == -1])
        assert yang == 36, f"Yang : {yang} au lieu de 36"
        assert yin == 36, f"Yin : {yin} au lieu de 36"

# =====================================================================
# TESTS DE COHÉRENCE MODULE_2 ↔ MODULE_3
# =====================================================================
class TestModule2_Module3:
    
    def test_constantes_masses_coherentes(self, constantes, particules):
        """Vérifie que MODULE_2 et MODULE_3 utilisent les mêmes masses"""
        from constantes_partagees import MASSES_PARTICULES
        
        me_module2 = next(p for p in particules if p['nom'] == 'électron')['masse_experimentale_MeV']
        me_module3 = float(MASSES_PARTICULES['me_MeV'].valeur)
        
        ecart = abs(me_module2 - me_module3) / me_module3
        assert ecart < 0.001, f"Écart masse électron : {ecart*100:.2f}%"

# =====================================================================
# TESTS DE COHÉRENCE MODULE_3 ↔ MODULE_4
# =====================================================================
class TestModule3_Module4:
    
    def test_rydberg_coherent(self, constantes):
        """Vérifie que la constante de Rydberg est cohérente"""
        from constantes_partagees import CONSTANTES_ATOMIQUES
        
        ryd = CONSTANTES_ATOMIQUES['rydberg_eV'].valeur
        assert float(ryd) > 13.6, f"Rydberg incohérent : {ryd}"
        assert float(ryd) < 13.61, f"Rydberg incohérent : {ryd}"

# =====================================================================
# TESTS DE VALIDATION PHYSIQUE
# =====================================================================
class TestValidationPhysique:
    
    def test_masses_leptons_coherentes(self, particules):
        """Vérifie que les masses des leptons sont cohérentes avec PDG"""
        leptons = {
            'électron': (0.511, 0.001),
            'muon': (105.658, 0.01),
            'tau': (1776.86, 0.2),
        }
        
        for p in particules:
            if p['nom'] in leptons:
                attendu, tolerance = leptons[p['nom']]
                ecart = abs(p['masse_experimentale_MeV'] - attendu)
                assert ecart < tolerance, f"{p['nom']} : écart {ecart} > {tolerance}"
    
    def test_charge_conservation(self, particules):
        """Vérifie la conservation de la charge matière/antimatière"""
        for p in particules:
            if p['nom'] in ['électron', 'muon', 'tau']:
                # Trouver l'antiparticule correspondante
                anti_nom = p['nom'].replace('électron', 'positron').replace('muon', 'antimuon').replace('tau', 'antitau')
                if anti_nom == p['nom']:
                    anti_nom = 'positron' if p['nom'] == 'électron' else None
                
                if anti_nom:
                    anti = next((x for x in particules if x['nom'] == anti_nom), None)
                    if anti:
                        assert p['charge'] == -anti['charge'], \
                            f"Charge non opposée : {p['nom']} vs {anti_nom}"
    
    def test_masse_nulle_bosons(self, particules):
        """Vérifie que photon et gluon ont masse nulle"""
        for p in particules:
            if p['nom'] in ['photon', 'gluon']:
                assert p['masse_experimentale_MeV'] == 0.0, \
                    f"{p['nom']} devrait avoir masse nulle"

# =====================================================================
# TESTS DE TRANSPARENCE MÉTHODOLOGIQUE
# =====================================================================
class TestTransparence:
    
    def test_masse_methode_declaree(self, particules):
        """Vérifie que le champ masse_methode est présent"""
        for p in particules:
            assert 'masse_methode' in p, f"Champ masse_methode manquant pour {p['nom']}"
            assert p['masse_methode'] in ['calibrée', 'prédite'], \
                f"Valeur invalide pour masse_methode : {p['masse_methode']}"
    
    def test_valide_pentade_declare(self, particules):
        """Vérifie que le champ valide_pentade est présent"""
        for p in particules:
            assert 'valide_pentade' in p, f"Champ valide_pentade manquant pour {p['nom']}"

# =====================================================================
# TESTS DE RÉGRESSION
# =====================================================================
class TestRegression:
    
    def test_nombre_particules_stable(self, particules):
        """Vérifie que le nombre de particules reste stable"""
        assert len(particules) >= 20, f"Trop peu de particules : {len(particules)}"
    
    def test_fichiers_exportes(self):
        """Vérifie que les fichiers de sortie sont générés"""
        fichiers_requis = [
            'pentades_72_finales.json',
            'particules_modele_standard.json',
            'zeeman_pentadique_avec_incertitudes.json',
        ]
        
        for f in fichiers_requis:
            assert os.path.exists(f), f"Fichier requis manquant : {f}"

# =====================================================================
# POINT D'ENTRÉE
# =====================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])