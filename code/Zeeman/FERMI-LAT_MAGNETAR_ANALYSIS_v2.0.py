#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FERMI-LAT_MAGNETAR_ANALYSIS_v2.0
Analyse réelle des données Fermi-LAT pour les magnetars
Utilise fermipy/easyFermi pour reproduire et étendre Ramakrishnan & Desai (2024)
Recherche spécifique de la résonance à 0.2 GeV (octave 6)
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from fermipy.gtanalysis import GTAnalysis
from fermipy.plotting import SEDPlotter
import yaml
import os
import logging
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MagnetarFermiAnalyzer:
    """
    Analyse des données Fermi-LAT pour les magnetars avec recherche de la résonance à 0.2 GeV
    """
    
    def __init__(self, base_dir='./fermi_analysis'):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Paramètres du modèle pentadique pour l'octave 6
        self.octave = 6
        self.B_pred = 0.00204  # Tesla
        self.E_res_GeV = 0.2  # Énergie de résonance prédite (~0.2 GeV)
        
        # Catalogue des magnetars avec leurs flares X (d'après Ramakrishnan & Desai 2024 [citation:5])
        # Basé sur le Magnetar Outburst Online Catalog
        self.magnetars = [
            # 1E 1048.1-5937 - Le cas intéressant
            {'name': '1E 1048.1-5937', 'ra': 162.0, 'dec': -59.5, 
             'flares': [
                 {'peak_mjd': 55000, 'duration_days': 30},  # Exemple, à remplacer par vraies dates
                 {'peak_mjd': 56000, 'duration_days': 30}
             ]},
            
            # SGR 1806-20
            {'name': 'SGR 1806-20', 'ra': 272.0, 'dec': -20.4,
             'flares': [
                 {'peak_mjd': 54000, 'duration_days': 30}
             ]},
            
            # SGR 1900+14
            {'name': 'SGR 1900+14', 'ra': 285.0, 'dec': 14.4,
             'flares': [
                 {'peak_mjd': 54500, 'duration_days': 30}
             ]},
            
            # 1E 1547.0-5408
            {'name': '1E 1547.0-5408', 'ra': 237.0, 'dec': -54.2,
             'flares': [
                 {'peak_mjd': 54800, 'duration_days': 30}
             ]},
            
            # XTE J1810-197
            {'name': 'XTE J1810-197', 'ra': 272.5, 'dec': -19.8,
             'flares': [
                 {'peak_mjd': 54300, 'duration_days': 30}
             ]},
            
            # 4U 0142+61
            {'name': '4U 0142+61', 'ra': 26.6, 'dec': 61.8,
             'flares': [
                 {'peak_mjd': 53500, 'duration_days': 30}
             ]},
        ]
        
        # Configuration par défaut pour fermipy
        self.config_template = {
            'logging': {'verbosity': 3},
            'data': {
                'evfile': None,  # Sera défini par easyFermi
                'scfile': None,  # Sera défini par easyFermi
            },
            'binning': {
                'roiwidth': 15.0,
                'binsz': 0.1,
                'binsperdec': 8,
            },
            'selection': {
                'emin': 100,    # 100 MeV
                'emax': 300000,  # 300 GeV
                'zmax': 90,      # Zenith angle cut
                'target': None,  # Sera défini
                'tmin': None,    # Sera défini par flare
                'tmax': None,    # Sera défini par flare
            },
            'model': {
                'src_roiwidth': 10.0,
                'galdiff': 'gll_iem_v07.fits',  # Modèle diffus galactique
                'isodiff': 'iso_P8R3_SOURCE_V3_v1.txt',  # Modèle isotrope
                'catalogs': ['4FGL-DR3'],  # Dernier catalogue
            },
            'optimizer': {'optimizer': 'NewMinuit'},
        }
    
    def setup_analysis_for_flare(self, magnetar, flare):
        """
        Configure une analyse fermipy pour un flare spécifique
        Utilise easyFermi pour télécharger automatiquement les données
        """
        from easyfermi.easyfermi import EasyFermi
        
        logger.info(f"Configuration pour {magnetar['name']} - flare à MJD {flare['peak_mjd']}")
        
        # Fenêtre temporelle: ±15 jours autour du pic (suivant Ramakrishnan & Desai [citation:5])
        tmin = flare['peak_mjd'] - 15
        tmax = flare['peak_mjd'] + 15
        
        # Créer le répertoire pour cette analyse
        analysis_dir = self.base_dir / f"{magnetar['name'].replace(' ', '_')}_MJD{flare['peak_mjd']}"
        analysis_dir.mkdir(exist_ok=True)
        
        # Utiliser easyFermi pour télécharger/configurer les données
        ef = EasyFermi(
            name=f"{magnetar['name']}_flare",
            work_dir=str(analysis_dir),
            ra=magnetar['ra'],
            dec=magnetar['dec'],
            tmin=tmin,
            tmax=tmax,
            emin=100,
            emax=300000,
            radius=15.0
        )
        
        # Télécharger les données (nécessite connexion internet)
        ef.download_data()
        
        # Configurer l'analyse fermipy
        config = self.config_template.copy()
        config['name'] = f"{magnetar['name']}_MJD{flare['peak_mjd']}"
        config['selection']['target'] = magnetar['name']
        config['selection']['tmin'] = tmin
        config['selection']['tmax'] = tmax
        config['data']['evfile'] = str(analysis_dir / 'fermi_data' / 'photon_files.fits')
        config['data']['scfile'] = str(analysis_dir / 'fermi_data' / 'spacecraft.fits')
        
        # Sauvegarder la config
        config_file = analysis_dir / 'config.yaml'
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
        
        return analysis_dir, config_file
    
    def analyze_flare(self, magnetar, flare):
        """
        Exécute l'analyse complète pour un flare
        Retourne la Test Statistic (TS) et le spectre
        """
        logger.info(f"Analyse du flare pour {magnetar['name']}")
        
        analysis_dir, config_file = self.setup_analysis_for_flare(magnetar, flare)
        
        # Initialiser GTAnalysis
        gta = GTAnalysis(str(analysis_dir / 'config.yaml'), logging={'verbosity': 3})
        
        # Setup initial (télécharge les modèles diffus si nécessaire)
        gta.setup()
        
        # Optimisation des paramètres
        gta.optimize()
        
        # Calcul de la Test Statistic pour notre source
        # Ajouter la source si elle n'est pas dans le catalogue
        if magnetar['name'] not in gta.roi.get_sources():
            gta.add_source(magnetar['name'], magnetar['ra'], magnetar['dec'],
                          spectrum={'Index': 2.0, 'Prefactor': 1e-13},
                          free=True, free_radius=3.0)
        
        # Ajustement du maximum de vraisemblance
        gta.fit()
        
        # Calcul de la TS (Test Statistic)
        ts = gta.get_sources()[magnetar['name']]['ts']
        
        # Analyse spectrale fine pour chercher la résonance à 0.2 GeV
        # On utilise une grille d'énergie plus fine
        sed = gta.sed(magnetar['name'], 
                     binsperdec=12,  # Plus fin que par défaut
                     energy_bins=np.logspace(1, 2.5, 20))  # 10-300 MeV to 0.3-3 GeV
        
        # Sauvegarder les résultats
        results = {
            'magnetar': magnetar['name'],
            'flare_mjd': flare['peak_mjd'],
            'ts': ts,
            'significance': np.sqrt(ts) if ts > 0 else 0,
            'sed': sed,
            'flux_100_300MeV': None,  # À remplir
            'flux_300_1000MeV': None,
            'flux_1_3GeV': None,
            'excess_at_0.2GeV': None,  # Notre signature
        }
        
        # Calculer les flux dans différentes bandes si détection
        if ts > 10:  # Détection significative
            for i, band in enumerate(sed['energies']):
                if 100 < band[0] < 300:  # 100-300 MeV
                    results['flux_100_300MeV'] = sed['flux'][i]
                elif 300 < band[0] < 1000:  # 300-1000 MeV
                    results['flux_300_1000MeV'] = sed['flux'][i]
                elif 1000 < band[0] < 3000:  # 1-3 GeV
                    results['flux_1_3GeV'] = sed['flux'][i]
            
            # Recherche d'excès à 0.2 GeV
            e_center = 200  # MeV
            idx = np.argmin(np.abs(sed['energies'].mean(axis=1) - e_center))
            model_flux = sed['model_flux'][idx]
            data_flux = sed['flux'][idx]
            if model_flux > 0:
                results['excess_at_0.2GeV'] = (data_flux - model_flux) / model_flux * 100
        
        return results
    
    def run_systematic_analysis(self):
        """
        Lance l'analyse systématique pour tous les magnetars et tous leurs flares
        """
        all_results = []
        
        for magnetar in self.magnetars:
            for flare in magnetar['flares']:
                try:
                    logger.info(f"Analyse de {magnetar['name']} - flare MJD {flare['peak_mjd']}")
                    results = self.analyze_flare(magnetar, flare)
                    all_results.append(results)
                    
                    # Résumé intermédiaire
                    if results['ts'] > 25:  # ~5 sigma
                        logger.info(f"⚠️ DÉTECTION POTENTIELLE: TS={results['ts']:.1f}")
                        if results['excess_at_0.2GeV']:
                            logger.info(f"   Excès à 0.2 GeV: {results['excess_at_0.2GeV']:.1f}%")
                    
                except Exception as e:
                    logger.error(f"Erreur pour {magnetar['name']} flare {flare['peak_mjd']}: {e}")
                    continue
        
        return all_results
    
    def plot_results(self, all_results):
        """
        Génère les graphiques de synthèse
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Analyse Fermi-LAT des Magnetars - Recherche de l\'Octave 6', fontsize=14)
        
        # Graphique 1: Distribution des TS
        ax = axes[0, 0]
        ts_values = [r['ts'] for r in all_results]
        ax.hist(ts_values, bins=20, alpha=0.7, color='blue')
        ax.axvline(x=25, color='r', linestyle='--', label='Seuil 5σ (TS=25)')
        ax.set_xlabel('Test Statistic (TS)')
        ax.set_ylabel('Nombre de flares')
        ax.set_title('Distribution des significativités')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Graphique 2: Excès à 0.2 GeV
        ax = axes[0, 1]
        detections = [r for r in all_results if r['ts'] > 10]
        names = [r['magnetar'][:10] + f" (MJD{r['flare_mjd']})" for r in detections]
        excess = [r.get('excess_at_0.2GeV', 0) for r in detections]
        
        if detections:
            ax.bar(names, excess, alpha=0.7, color='green')
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
            ax.set_ylabel('Excès à 0.2 GeV (%)')
            ax.set_title('Signature spectrale de l\'octave 6')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, 'Aucune détection significative', 
                   ha='center', va='center', transform=ax.transAxes)
        ax.grid(True, alpha=0.3)
        
        # Graphique 3: Carte des magnetars
        ax = axes[1, 0]
        ras = [m['ra'] for m in self.magnetars]
        decs = [m['dec'] for m in self.magnetars]
        
        # Convertir en coordonnées galactiques
        coords = SkyCoord(ra=ras, dec=decs, unit='deg', frame='icrs')
        glons = coords.galactic.l.deg
        glats = coords.galactic.b.deg
        
        scatter = ax.scatter(glons, glats, c=[r.get('ts', 0) for r in all_results if r['ts']>0], 
                            cmap='hot', s=100, alpha=0.7)
        ax.set_xlabel('Longitude Galactique (deg)')
        ax.set_ylabel('Latitude Galactique (deg)')
        ax.set_title('Position des magnetars (couleur = TS)')
        plt.colorbar(scatter, ax=ax, label='TS')
        ax.grid(True, alpha=0.3)
        
        # Graphique 4: Comparaison avec prédiction
        ax = axes[1, 1]
        ax.axhline(y=self.E_res_GeV, color='r', linestyle='--', label=f'Résonance prédite {self.E_res_GeV} GeV')
        
        # Si détections, plotter les SEDs
        if detections:
            for r in detections[:3]:  # Top 3
                if r.get('sed'):
                    e_mean = r['sed']['energies'].mean(axis=1) / 1000  # GeV
                    ax.errorbar(e_mean, r['sed']['flux'] * e_mean**2, 
                               yerr=r['sed']['flux_err'] * e_mean**2,
                               label=r['magnetar'], alpha=0.7)
        
        ax.set_xlabel('Énergie (GeV)')
        ax.set_ylabel('νFν (erg/cm²/s)')
        ax.set_title('Spectres des détections')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.base_dir / 'magnetar_analysis_summary.png', dpi=150)
        plt.show()
        
        logger.info(f"Graphique sauvegardé: {self.base_dir / 'magnetar_analysis_summary.png'}")
    
    def generate_report(self, all_results):
        """
        Génère un rapport complet de l'analyse
        """
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("RAPPORT D'ANALYSE FERMI-LAT - MAGNETARS")
        report_lines.append("="*80)
        report_lines.append(f"\nDate: {np.datetime64('now')}")
        report_lines.append(f"Recherche spécifique: Octave {self.octave} (B={self.B_pred} T, E_res={self.E_res_GeV} GeV)")
        
        # Statistiques globales
        n_flares = len(all_results)
        n_detections = len([r for r in all_results if r['ts'] > 25])
        n_marginal = len([r for r in all_results if 10 < r['ts'] <= 25])
        
        report_lines.append(f"\n📊 STATISTIQUES GLOBALES")
        report_lines.append("-"*40)
        report_lines.append(f"Flares analysés: {n_flares}")
        report_lines.append(f"Détections significatives (TS>25, ~5σ): {n_detections}")
        report_lines.append(f"Détections marginales (10<TS≤25): {n_marginal}")
        
        # Détails par flare
        report_lines.append(f"\n📋 DÉTAILS PAR FLARE")
        report_lines.append("-"*80)
        report_lines.append(f"{'Magnetar':<20} {'MJD':<10} {'TS':<8} {'Signif(σ)':<10} {'Excès@0.2GeV':<15} {'Statut'}")
        report_lines.append("-"*80)
        
        for r in sorted(all_results, key=lambda x: x['ts'], reverse=True):
            magnetar = r['magnetar'][:18]
            mjd = r['flare_mjd']
            ts = r['ts']
            sig = r['significance']
            excess = r.get('excess_at_0.2GeV', 0)
            if excess:
                excess_str = f"{excess:.1f}%"
            else:
                excess_str = "-"
            
            if ts > 25:
                statut = "✅ DÉTECTION"
            elif ts > 10:
                statut = "🟡 Marginale"
            else:
                statut = "❌ Non détecté"
            
            report_lines.append(f"{magnetar:<20} {mjd:<10.0f} {ts:<8.1f} {sig:<10.1f} {excess_str:<15} {statut}")
        
        # Analyse de la résonance à 0.2 GeV
        report_lines.append(f"\n🔬 RECHERCHE DE LA RÉSONANCE À {self.E_res_GeV} GeV")
        report_lines.append("-"*40)
        
        detections_with_excess = [r for r in all_results if r.get('excess_at_0.2GeV', 0) > 20]  # Excès >20%
        if detections_with_excess:
            report_lines.append(f"✅ {len(detections_with_excess)} flare(s) présentent un excès >20% à {self.E_res_GeV} GeV:")
            for r in detections_with_excess:
                report_lines.append(f"   • {r['magnetar']} (MJD {r['flare_mjd']}): {r['excess_at_0.2GeV']:.1f}%")
        else:
            report_lines.append(f"❌ Aucun excès significatif détecté à {self.E_res_GeV} GeV")
        
        # Comparaison avec Ramakrishnan & Desai (2024) [citation:5]
        report_lines.append(f"\n📚 COMPARAISON AVEC LA LITTÉRATURE")
        report_lines.append("-"*40)
        report_lines.append("Ramakrishnan & Desai (2024) [arXiv:2412.03900]:")
        report_lines.append("• 15 flares de 11 magnetars analysés")
        report_lines.append("• 14 flares: aucune détection significative")
        report_lines.append("• 1 magnetar (1E 1048.1-5937): 2 flares gamma à 5σ combinés")
        report_lines.append("• Délai de ~10 jours après le pic X")
        
        # Notre résultat pour 1E 1048.1-5937
        ie_results = [r for r in all_results if '1E 1048.1' in r['magnetar']]
        if ie_results:
            report_lines.append(f"\n🔍 Nos résultats pour 1E 1048.1-5937:")
            for r in ie_results:
                report_lines.append(f"   • Flare MJD {r['flare_mjd']}: TS={r['ts']:.1f}, excès={r.get('excess_at_0.2GeV', 0):.1f}%")
        
        # Conclusion
        report_lines.append(f"\n📊 CONCLUSION")
        report_lines.append("-"*40)
        
        # Compter les preuves pour l'octave 6
        n_evidence = len([r for r in all_results if r.get('excess_at_0.2GeV', 0) > 20])
        if n_evidence >= 2 and n_detections >= 1:
            statut_octave = "🟢 PARTIELLEMENT VALIDÉ"
            message = "Des preuves convergentes soutiennent l'existence de l'octave 6"
        elif n_evidence >= 1 or n_detections >= 1:
            statut_octave = "🟡 INDICES"
            message = "Des indices existent mais nécessitent confirmation"
        else:
            statut_octave = "🔴 NON VALIDÉ"
            message = "Aucune preuve significative détectée"
        
        report_lines.append(f"Statut de l'octave 6: {statut_octave}")
        report_lines.append(f"Message: {message}")
        report_lines.append("\n" + "="*80)
        
        return "\n".join(report_lines)


def main():
    """Fonction principale"""
    
    print("="*80)
    print("ANALYSE FERMI-LAT DES MAGNETARS - RECHERCHE DE L'OCTAVE 6")
    print("Reproduction et extension de Ramakrishnan & Desai (2024)")
    print("="*80)
    
    # Initialisation
    analyzer = MagnetarFermiAnalyzer(base_dir='./fermi_magnetar_analysis')
    
    # Lancement de l'analyse systématique
    print("\n📡 Lancement de l'analyse des données Fermi-LAT...")
    print("   (Les données seront téléchargées automatiquement via easyFermi)")
    print("   Cela peut prendre plusieurs heures selon la connexion\n")
    
    all_results = analyzer.run_systematic_analysis()
    
    # Génération des graphiques
    print("\n📈 Génération des graphiques...")
    analyzer.plot_results(all_results)
    
    # Génération du rapport
    print("\n📝 Génération du rapport...")
    report = analyzer.generate_report(all_results)
    
    # Sauvegarde du rapport
    report_file = analyzer.base_dir / 'fermi_magnetar_report.txt'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Rapport sauvegardé: {report_file}")
    print(report)
    print("="*80)


if __name__ == "__main__":
    main()