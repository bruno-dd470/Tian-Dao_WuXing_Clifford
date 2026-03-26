#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIMENSION SPECTRALE EN ALGÈBRE GÉOMÉTRIQUE PURE
Version corrigée : plus de clé Multivector non hashable
"""
import numpy as np
import json
import matplotlib.pyplot as plt
from clifford import Cl
from scipy.signal import savgol_filter
from tqdm import tqdm
import concurrent.futures
import multiprocessing
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

class ConfigSpectralAG:
    P = 6
    Q = 6
    N_SAMPLES = 10
    N_T_VALUES = 100
    T_MIN = 1e-3
    T_MAX = 1e2
    CIBLE_D_UV = 10.0
    CIBLE_D_INTERMEDIAIRE = 72.0
    CIBLE_D_IR = 4.0
    TOLERANCE_UV = 5.0
    TOLERANCE_INTERMEDIAIRE = 50.0
    TOLERANCE_IR = 1.0
    NUM_WORKERS = multiprocessing.cpu_count()

# ============================================================================
# ALGÈBRE DE CLIFFORD Cl(6,6)
# ============================================================================

class AlgebreClifford:
    def __init__(self):
        self.layout, self.blades = Cl(ConfigSpectralAG.P, ConfigSpectralAG.Q)
        self.dim = 2**(ConfigSpectralAG.P + ConfigSpectralAG.Q)  # 4096
        self.base = list(self.blades.values())
        # Construction de l'index inversé : pour chaque grade, liste des indices des blades
        self.indices_par_grade = {k: [] for k in range(13)}
        for i, blade in enumerate(self.base):
            # blade.grades() retourne un set, on prend le premier (et unique) élément
            g = next(iter(blade.grades()))
            self.indices_par_grade[g].append(i)
        print(f"✅ Algèbre Cl({ConfigSpectralAG.P},{ConfigSpectralAG.Q}) initialisée")
        print(f"   Dimension : {self.dim}")
        print(f"   Grades disponibles : {list(self.indices_par_grade.keys())}")

    def vecteur_base(self, i):
        return self.base[i]

    def produit_scalaire(self, a, b):
        return (a * ~b).value[0]

# ============================================================================
# OPÉRATEUR DE DIRAC
# ============================================================================

class OperateurDirac:
    def __init__(self, algebre, momentum=None):
        self.algebre = algebre
        if momentum is None:
            momentum = np.random.randn(12) * 0.5
        self.momentum = momentum
        self.D = algebre.layout.scalar(0)
        for i, p in enumerate(momentum):
            self.D += p * algebre.blades[f'e{i+1}']
        self.D2_scalar = (self.D * self.D).value[0]

    def matrice_D2(self):
        return self.D2_scalar * np.eye(self.algebre.dim)

    def matrice_D2_generale(self):
        dim = self.algebre.dim
        M = np.zeros((dim, dim))
        D2 = self.D * self.D
        for j, blade_j in enumerate(self.algebre.base):
            res = D2 * blade_j
            for i, blade_i in enumerate(self.algebre.base):
                coeff = self.algebre.produit_scalaire(blade_i, res)
                if abs(coeff) > 1e-12:
                    M[i, j] = coeff
        return M

# ============================================================================
# FONCTION AUXILIAIRE POUR LE CALCUL PARALLÈLE
# ============================================================================

def _compute_trace_sample(args):
    seed, t_values = args
    np.random.seed(seed)
    algebre = AlgebreClifford()
    dirac = OperateurDirac(algebre)
    M = dirac.matrice_D2()
    dim = algebre.dim
    lambd = M[0, 0]
    trace = dim * np.exp(-lambd * t_values)
    return trace

# ============================================================================
# CALCUL DE LA DIMENSION SPECTRALE
# ============================================================================

class DimensionSpectrale:
    def __init__(self, algebre):
        self.algebre = algebre

    def calculer_d_t(self, n_samples):
        t_values = np.logspace(np.log10(ConfigSpectralAG.T_MIN),
                               np.log10(ConfigSpectralAG.T_MAX),
                               ConfigSpectralAG.N_T_VALUES)

        seeds = np.random.randint(0, 2**31, size=n_samples)
        args_list = [(seed, t_values) for seed in seeds]

        traces = []
        max_workers = ConfigSpectralAG.NUM_WORKERS
        print(f"\n🚀 Lancement de {n_samples} calculs sur {max_workers} processus...")

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_compute_trace_sample, args) for args in args_list]
            for future in tqdm(concurrent.futures.as_completed(futures),
                               total=n_samples,
                               desc="Échantillons",
                               unit="sample",
                               ncols=80):
                try:
                    result = future.result()
                    traces.append(result)
                except Exception as e:
                    print(f"\n❌ Erreur dans un échantillon : {e}")

        traces = np.array(traces)
        traces_moyennes = np.mean(traces, axis=0)

        log_t = np.log(t_values)
        log_trace = np.log(traces_moyennes + 1e-10)
        log_trace_lisse = savgol_filter(log_trace, window_length=11, polyorder=3)
        derivee = np.gradient(log_trace_lisse, log_t)
        d_t = -2 * derivee

        return t_values, d_t

# ============================================================================
# VALIDATION DES RÉGIMES SPECTRAUX
# ============================================================================

class ValidationRegimesSpectrauxAG:
    def __init__(self, t_values, d_t):
        self.t_values = t_values
        self.d_t = d_t

    def valider_regimes(self):
        resultats = {}

        idx_uv = min(10, len(self.t_values) // 10)
        resultats['d_UV'] = float(np.mean(self.d_t[:idx_uv]))
        resultats['d_UV_cible'] = ConfigSpectralAG.CIBLE_D_UV
        resultats['d_UV_valide'] = abs(resultats['d_UV'] - ConfigSpectralAG.CIBLE_D_UV) < ConfigSpectralAG.TOLERANCE_UV

        idx_inter = np.argmin(np.abs(self.t_values - 1.0))
        fenetre = max(5, len(self.t_values) // 20)
        idx_debut = max(0, idx_inter - fenetre)
        idx_fin = min(len(self.t_values), idx_inter + fenetre)
        resultats['d_intermediaire'] = float(np.mean(self.d_t[idx_debut:idx_fin]))
        resultats['d_intermediaire_cible'] = ConfigSpectralAG.CIBLE_D_INTERMEDIAIRE
        resultats['d_intermediaire_valide'] = abs(resultats['d_intermediaire'] - ConfigSpectralAG.CIBLE_D_INTERMEDIAIRE) < ConfigSpectralAG.TOLERANCE_INTERMEDIAIRE

        idx_ir = max(len(self.t_values) - 10, 0)
        resultats['d_IR'] = float(np.mean(self.d_t[idx_ir:]))
        resultats['d_IR_cible'] = ConfigSpectralAG.CIBLE_D_IR
        resultats['d_IR_valide'] = abs(resultats['d_IR'] - ConfigSpectralAG.CIBLE_D_IR) < ConfigSpectralAG.TOLERANCE_IR

        resultats['continuite'] = float(np.std(np.gradient(self.d_t)))
        resultats['continuite_valide'] = resultats['continuite'] < 5.0

        return resultats

    def afficher_resultats(self, resultats):
        print("\n" + "="*80)
        print("📊 RÉSULTATS DE DIMENSION SPECTRALE (AG PURE)")
        print("="*80)
        print(f"\n{'Régime':20s} | {'d(t) mesuré':15s} | {'Cible':15s} | {'Statut':10s}")
        print("-"*80)

        statut_uv = "✅" if resultats['d_UV_valide'] else "⚠️"
        print(f"{'UV (t→0)':20s} | {resultats['d_UV']:15.2f}        | {resultats['d_UV_cible']:15.1f} | {statut_uv:10s}")

        statut_inter = "✅" if resultats['d_intermediaire_valide'] else "⚠️"
        print(f"{'Intermédiaire (t≈1)':20s} | {resultats['d_intermediaire']:15.2f}        | {resultats['d_intermediaire_cible']:15.1f} | {statut_inter:10s}")

        statut_ir = "✅" if resultats['d_IR_valide'] else "⚠️"
        print(f"{'IR (t→∞)':20s} | {resultats['d_IR']:15.2f}        | {resultats['d_IR_cible']:15.1f} | {statut_ir:10s}")

        statut_cont = "✅" if resultats['continuite_valide'] else "⚠️"
        print(f"{'Continuité':20s} | {resultats['continuite']:15.4f}        | {'< 5.0':15s} | {statut_cont:10s}")

        score = sum([
            resultats['d_UV_valide'],
            resultats['d_intermediaire_valide'],
            resultats['d_IR_valide'],
            resultats['continuite_valide']
        ])

        print("\n" + "="*80)
        print(f"SCORE DIMENSION SPECTRALE (AG) : {score}/4")
        print("="*80)

        if score >= 3:
            print("\n✅ DIMENSION SPECTRALE VALIDÉE EN AG PURE")
        elif score >= 2:
            print("\n⚠️ DIMENSION SPECTRALE PARTIELLEMENT VALIDÉE")
        else:
            print("\n❌ DIMENSION SPECTRALE NON VALIDÉE")

        return score

# ============================================================================
# VISUALISATION
# ============================================================================

def visualiser_dimension_spectrale_AG(t_values, d_t, resultats):
    print("\n📊 GÉNÉRATION DES GRAPHIQUES...")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    ax1 = axes[0]
    ax1.plot(np.log10(t_values), d_t, linewidth=2, color='blue', label='d(t) calculé')
    ax1.axhline(y=ConfigSpectralAG.CIBLE_D_UV, color='red', linestyle='--', linewidth=2,
                label=f'Cible UV ({ConfigSpectralAG.CIBLE_D_UV})')
    ax1.axhline(y=ConfigSpectralAG.CIBLE_D_INTERMEDIAIRE, color='green', linestyle='--', linewidth=2,
                label=f'Cible Nebe ({ConfigSpectralAG.CIBLE_D_INTERMEDIAIRE})')
    ax1.axhline(y=ConfigSpectralAG.CIBLE_D_IR, color='orange', linestyle='--', linewidth=2,
                label=f'Cible IR ({ConfigSpectralAG.CIBLE_D_IR})')
    ax1.set_xlabel('log₁₀(t)', fontsize=12)
    ax1.set_ylabel('Dimension spectrale d(t)', fontsize=12)
    ax1.set_title('Dimension spectrale en fonction de l\'échelle (AG pure)', fontsize=14)
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.hist(d_t, bins=40, color='purple', alpha=0.7, edgecolor='black')
    ax2.axvline(x=ConfigSpectralAG.CIBLE_D_UV, color='red', linestyle='--', linewidth=2,
                label=f'UV ({ConfigSpectralAG.CIBLE_D_UV})')
    ax2.axvline(x=ConfigSpectralAG.CIBLE_D_INTERMEDIAIRE, color='green', linestyle='--', linewidth=2,
                label=f'Nebe ({ConfigSpectralAG.CIBLE_D_INTERMEDIAIRE})')
    ax2.axvline(x=ConfigSpectralAG.CIBLE_D_IR, color='orange', linestyle='--', linewidth=2,
                label=f'IR ({ConfigSpectralAG.CIBLE_D_IR})')
    ax2.set_xlabel('Dimension spectrale d(t)', fontsize=12)
    ax2.set_ylabel('Fréquence', fontsize=12)
    ax2.set_title('Distribution des valeurs de d(t)', fontsize=14)
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('dimension_spectrale_AG_resultats.png', dpi=300, bbox_inches='tight')
    print("✅ Graphique sauvegardé : dimension_spectrale_AG_resultats.png")
    plt.show()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    multiprocessing.freeze_support()

    print("="*80)
    print("🔬 DIMENSION SPECTRALE EN ALGÈBRE GÉOMÉTRIQUE PURE")
    print("   Bibliothèque `clifford` - Calcul parallélisé avec barre de progression")
    print("="*80)
    print(f"Date : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    try:
        from clifford import Cl
    except ImportError:
        print("\n❌ Bibliothèque `clifford` non installée")
        print("   Installation : pip install clifford")
        exit(1)

    print("\n📦 Initialisation de l'algèbre...")
    algebre = AlgebreClifford()

    calculateur = DimensionSpectrale(algebre)
    t_values, d_t = calculateur.calculer_d_t(ConfigSpectralAG.N_SAMPLES)

    validateur = ValidationRegimesSpectrauxAG(t_values, d_t)
    resultats = validateur.valider_regimes()
    validateur.afficher_resultats(resultats)

    visualiser_dimension_spectrale_AG(t_values, d_t, resultats)

    with open('dimension_spectrale_AG_resultats.json', 'w', encoding='utf-8') as f:
        json.dump({
            't_values': t_values.tolist(),
            'd_t': d_t.tolist(),
            'resultats': resultats,
            'config': {
                'n_samples': ConfigSpectralAG.N_SAMPLES,
                'n_t_values': ConfigSpectralAG.N_T_VALUES,
                't_min': ConfigSpectralAG.T_MIN,
                't_max': ConfigSpectralAG.T_MAX,
                'signature': f'Cl({ConfigSpectralAG.P},{ConfigSpectralAG.Q})'
            }
        }, f, indent=2, ensure_ascii=False)

    print("\n✅ Résultats sauvegardés : dimension_spectrale_AG_resultats.json")
    print("\n" + "="*80)
    print("✅ CALCUL TERMINÉ")
    print("="*80)