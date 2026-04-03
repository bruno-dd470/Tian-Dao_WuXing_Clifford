# CHANGELOG.md

Toutes les modifications notables apportées au framework pentadique seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versionnement Sémantique](https://semver.org/lang/fr/).

---

## [Non publié] - En développement

### Ajouté
- **`constantes_partagees.py`** : Nouveau module centralisant toutes les constantes physiques (CODATA 2022, PDG 2022) avec précision 50 chiffres (`Decimal`)
- **`tests/test_integration.py`** : Suite de tests unitaires transversaux pour valider la cohérence entre MODULE_1, MODULE_2, MODULE_3, MODULE_4
- **Champ `masse_methode`** dans `ParticulePentadique` : Indique si la masse est "calibrée" ou "prédite" (transparence méthodologique)
- **Champ `valide_pentade`** dans `ParticulePentadique` : Validation des pentades de particules contre les 72 pentades de MODULE_1
- **Fonction `calculer_couplage_gravitationnel()`** : Calcul du couplage Janus (secteur ±) basé sur le signe de la pentade
- **Logging structuré** : Remplacement des `print()` par le module `logging` avec fichiers de log (`module2_validation.log`)
- **Configuration externe** : Fichiers YAML/JSON pour les constantes et facteurs de famille (séparation code/config)
- **Propagation d'incertitudes** : Intégration de la méthode Monte Carlo (50 000 échantillons) dans MODULE_3
- **Tables de Bethe complètes** : Logarithmes de Bethe pour n=1 à 10 dans MODULE_4
- **Compression gzip** : Export des transitions de l'hydrogène en `.json.gz` (niveau 9)

### Changé
- **MODULE_2** : Les masses des particules sont maintenant explicitement documentées comme "calibrées sur PDG" (non prédites dynamiquement)
- **MODULE_3** : Remplacement du test N-sigma par tolérance relative adaptative (1% e⁻, 5% p, 10% n)
- **MODULE_4** : Correction critique de la contrainte quantique `|ml| ≤ l` appliquée systématiquement
- **MODULE_3B** : Harmonisation complète avec MODULE_4 (classe `EtatAtomiquePentadique` unifiée)
- **MODULE_1** : Dualité Rowlands FIII/FIV corrigée (inversion complète Feu/Eau pour les familles duales)
- **Tous modules** : Import des constantes depuis `constantes_partagees.py` au lieu de définitions locales
- **Rapports** : Ajout de notes de transparence méthodologique dans tous les rapports de validation

### Corrigé
- **MODULE_2** : Incohérence entre les facteurs de famille documentés {1, 207, 3477} et implémentés {1.0, 1.2, 1.5...}
- **MODULE_3** : Erreur de conversion d'unités dans le calcul du splitting Zeeman (facteur ×1e6 supprimé)
- **MODULE_4** : États quantiques invalides générés (ml > l) maintenant rejetés par `__post_init__`
- **MODULE_3B** : Transitions vers le même état quantique maintenant interdites explicitement
- **Tous modules** : Incohérences de précision entre modules (unifiée à 50 chiffres Decimal)

### Déprécié
- **Constantes locales** : Les dictionnaires `CONSTANTES` locaux dans chaque module sont dépréciés au profit de `constantes_partagees.py`
- **`print()` pour logging** : Déprécié au profit du module `logging` standard
- **Export JSON non compressé** : Déprécié pour les fichiers de transitions >1 MB (utiliser `.json.gz`)

---

## [2.0.0] - 2026-03-15

### Ajouté
- **MODULE_4** : Modèle complet de l'atome d'hydrogène (n=1-10) avec toutes les corrections QED
- **MODULE_3B** : Règles de sélection pentadiques pour les transitions atomiques
- **Structure de tests** : Dossier `tests/` avec pytest pour validation automatique
- **Documentation** : README_modules.md mis à jour avec workflow d'exécution complet
- **Rapports de validation** : `zeeman_validation_report.txt`, `pentadic_predictions_report.txt`
- **Support Fermi-LAT** : Scripts d'analyse des magnétars dans le dossier `zeeman/`

### Changé
- **MODULE_1** : Extension de 12 à 72 pentades (6 familles × 12 éléments × 2 signes)
- **MODULE_2** : Base de données étendue à 23 particules (leptons, quarks, bosons, hadrons)
- **MODULE_3** : Propagation d'incertitudes par Monte Carlo (50 000 échantillons)
- **Précision** : Passage de float (64-bit) à Decimal (50 chiffres) pour tous les calculs physiques

### Corrigé
- **MODULE_1** : Validation stricte des 6 générateurs (i,j,k,I,J,K) dans chaque pentade
- **MODULE_2** : Correction des facteurs g pour hadrons (proton, neutron)
- **MODULE_3** : Tolérances adaptatives selon le type de particule (e⁻, p, n)

---

## [1.5.0] - 2026-02-27

### Ajouté
- **Analyse magnétar** : Détection de la résonance à 200 MeV dans 1E 1048.1-5937
- **Rapports de flare** : `report_flare_54915.txt`, `report_flare_56015.txt`, `report_flare_57515.txt`
- **Validation statistique** : Significativité combinée >1000σ sur 3 bursts indépendants
- **Périodicité de Bott** : Script `BOTT_PERIODICITY_v2.0.py` pour les octaves supérieures

### Changé
- **MODULE_3** : Intégration des données Fermi-LAT pour validation astrophysique
- **Documentation** : Ajout de PUBLICATION_3_Magnetars_en.pdf dans le dépôt

### Corrigé
- **MODULE_3** : Correction des fenêtres d'énergie pour l'analyse spectrale (25, 50, 100, 200 MeV)

---

## [1.0.0] - 2026-01-10

### Ajouté
- **MODULE_1** : Construction des 72 pentades de Cl(6,0)
- **MODULE_2** : Physique des particules dans le modèle pentadique
- **MODULE_3** : Effet Zeeman pentadique avec incertitudes
- **Export JSON** : `pentades_72_finales.json`, `particules_modele_standard.json`
- **License** : CC BY 4.0 pour tous les modules
- **README** : Documentation initiale du framework

---

## [0.5.0] - 2025-12-01

### Ajouté
- **Prototype MODULE_1** : Construction initiale de 12 pentades (Rowlands original)
- **Tests de validation** : Comptage, validité, équilibre Yang/Yin
- **Documentation** : Notes théoriques sur Cl(6,0) et Cl(6,6)

---

## Notes de Version

### Version 2.0.0 - Changements Majeurs
- **Breaking Change** : Les constantes locales sont dépréciées. Migrer vers `constantes_partagees.py`.
- **Breaking Change** : Le champ `masse_methode` est maintenant requis dans `ParticulePentadique`.
- **Performance** : Compression gzip réduit la taille des fichiers de transitions de ~5 MB à ~1 MB.

### Version 1.5.0 - Validation Astrophysique
- Première validation expérimentale du modèle via les données Fermi-LAT.
- La résonance à 200 MeV constitue la première preuve observationnelle des octaves de Bott.

### Version 1.0.0 - Release Initiale
- Framework complet fonctionnel avec 4 modules principaux.
- Toutes les validations de laboratoire (Zeeman, hydrogène) passent avec succès.

---

## Roadmap Future

### [2.1.0] - Prévu Q2 2026
- [ ] Formule de masse first-principles (facteurs {1, 207, 3477} dérivés de Cl(6,0))
- [ ] Intégration complète du couplage Janus dans MODULE_2
- [ ] Tests unitaires pour MODULE_3 et MODULE_4
- [ ] Interface CLI pour interrogation des modules

### [2.2.0] - Prévu Q3 2026
- [ ] Extension aux ions hydrogénoïdes (He⁺, Li²⁺)
- [ ] Module de calcul des sections efficaces de transition
- [ ] Visualisation interactive des pentades (Dash/Plotly)
- [ ] Intégration continue (GitHub Actions)

### [3.0.0] - Prévu Q4 2026
- [ ] Dérivation complète des masses depuis les angles de Cl(6,0)
- [ ] Validation expérimentale indépendante (collaborations externes)
- [ ] Publication des règles de Feynman pentadiques complètes
- [ ] Extension au Modèle Standard complet (génération 3 complète)

---

## Auteurs

- **Bruno DE DOMINICIS** - Auteur principal et mainteneur
- **Contributeurs** : Assistant IA (support computationnel), Jean-Pierre Petit (modèle Janus), Peter Rowlands (pentades), Gabriele Nebe (réseau 72D)

---

## License

© 2025-2026 Bruno De Dominicis. Tous les modules sont licenciés sous Creative Commons Attribution 4.0 International (CC BY 4.0).

---

*Pour plus d'informations sur le format, consultez [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).*
