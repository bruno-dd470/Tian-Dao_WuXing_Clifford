#!/usr/bin/env python3
"""
CROSS-VALIDATION PENTADIQUE v1.0
Vérification de la cohérence interne des paramètres extraits
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class PentadicCrossValidator:
    def __init__(self, g0=2.003, delta_lattice=0.00507, B0=8.0, 
                 delta_bicosmic=0.01, B_bicosmic=100):
        self.g0 = g0
        self.delta_lattice = delta_lattice
        self.B0 = B0
        self.delta_bicosmic = delta_bicosmic
        self.B_bicosmic = B_bicosmic
        
    def predict_zeeman(self, B):
        """Prédiction complète du splitting Zeeman"""
        lattice_corr = self.delta_lattice * np.sin(2 * np.pi * self.B0 / (B + 0.1))
        bicosmic_corr = self.delta_bicosmic * np.tanh(B / self.B_bicosmic)
        bicosmic_corr *= (1 + 0.1 * np.log10(B/1000)) * (B > 1000)
        
        g_eff = self.g0 * (1 + lattice_corr + bicosmic_corr)
        return 0.05788 * B * g_eff  # meV
    
    def generate_figure_of_merit(self):
        """Calcule la figure de mérite pour différents types d'expériences"""
        experiments = {
            'Laboratoire (0-10 T)': {
                'B_range': (0.1, 10),
                'precision': 0.001,  # 0.1%
                'cost': 3e6,  # €
                'duration': 0.5,  # années
                'readiness': 0.9  # prêt à démarrer
            },
            'Stellaire (0.1-1 T)': {
                'B_range': (0.1, 1),
                'precision': 0.003,  # 0.3%
                'cost': 1e6,
                'duration': 1,
                'readiness': 0.95
            },
            'Pulsars X (10⁷-10⁸ T)': {
                'B_range': (1e7, 1e8),
                'precision': 0.1,  # 10%
                'cost': 50e6,  # Satellite
                'duration': 5,
                'readiness': 0.6
            },
            'Pulsars optique (10⁸-10⁹ T)': {
                'B_range': (1e8, 1e9),
                'precision': 0.05,  # 5%
                'cost': 10e6,
                'duration': 2,
                'readiness': 0.7
            },
            'Magnetars (10¹⁰-10¹¹ T)': {
                'B_range': (1e10, 1e11),
                'precision': 0.2,  # 20%
                'cost': 100e6,
                'duration': 10,
                'readiness': 0.4
            }
        }
        
        print("\n📊 FIGURE DE MÉRITE DES EXPÉRIENCES")
        print("-" * 80)
        print(f"{'Expérience':<25} {'Signal':<12} {'S/B':<10} {'Coût/efficacité':<15} {'Priorité':<10}")
        print("-" * 80)
        
        for name, params in experiments.items():
            B_min, B_max = params['B_range']
            B_test = np.sqrt(B_min * B_max)  # Moyenne géométrique
            
            # Signal prédit
            delta_E = self.predict_zeeman(B_test)
            
            # Effet pentadique (différence avec modèle standard)
            delta_std = 0.05788 * B_test * 2.0023
            delta_pent = delta_E
            effect = abs(delta_pent - delta_std) / delta_std * 100  # %
            
            # Rapport signal/bruit
            snr = effect / (params['precision'] * 100)
            
            # Coût/efficacité
            cost_effectiveness = snr / (params['cost'] * params['duration'] / 1e6)
            
            # Priorité (0-10)
            priority = min(10, max(0, snr * cost_effectiveness * params['readiness'] * 2))
            
            print(f"{name:<25} {effect:5.2f}%      {snr:5.1f}     {cost_effectiveness:6.2f}         {priority:5.1f}/10")
        
        print("-" * 80)


# Exécution
if __name__ == "__main__":
    validator = PentadicCrossValidator()
    validator.generate_figure_of_merit()
    
    # Visualisation des prédictions sur tout le spectre
    B_all = np.logspace(-1, 11, 1000)
    delta_all = validator.predict_zeeman(B_all)
    delta_std = 0.05788 * B_all * 2.0023
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Ratio pentadique/standard
    ax1.loglog(B_all, delta_all/delta_std, 'b-', linewidth=2)
    ax1.set_xlabel('Champ B (Tesla)')
    ax1.set_ylabel('Rapport ΔE_pent / ΔE_std')
    ax1.set_title('Déviation par rapport au modèle standard')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    
    # Identification des régions de validation optimale
    ax2.loglog(B_all, abs(delta_all/delta_std - 1) * 100, 'r-', linewidth=2)
    ax2.set_xlabel('Champ B (Tesla)')
    ax2.set_ylabel('Déviation (%)')
    ax2.set_title('Régions de validation optimale')
    ax2.grid(True, alpha=0.3, which='both')
    ax2.axvspan(0.1, 10, alpha=0.2, color='blue', label='Laboratoire')
    ax2.axvspan(1e7, 1e11, alpha=0.2, color='red', label='Pulsars')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('cross_validation.png', dpi=150)
    plt.show()
    
    print("\n✅ Graphique sauvegardé: cross_validation.png")