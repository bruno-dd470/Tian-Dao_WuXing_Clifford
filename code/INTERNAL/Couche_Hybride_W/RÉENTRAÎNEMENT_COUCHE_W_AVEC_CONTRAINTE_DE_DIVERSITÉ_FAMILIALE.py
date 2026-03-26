#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RÉENTRAÎNEMENT COUCHE W AVEC CONTRAINTE DE DIVERSITÉ FAMILIALE
Objectif : Activer les 6 familles de pentades (FI à FVI)
"""
from __future__ import annotations
import numpy as np
import torch
import torch.nn as nn
import json
from typing import Dict, Tuple, List
import math

# ============================================================================
# CHARGEMENT DES POIDS EXISTANTS
# ============================================================================
def charger_poids_W(fichier: str = 'couche_hybride_W_poids.json') -> torch.Tensor:
    """Charge les poids W existants"""
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
    W = torch.tensor(data['W'], dtype=torch.float32)
    print(f"✅ Poids chargés : shape {W.shape}")
    return W

# ============================================================================
# CLASSE : COUCHE W AVEC DIVERSITÉ FAMILIALE
# ============================================================================
class CoucheHybrideDiversite(nn.Module):
    """Couche W avec pénalité de diversité familiale"""
    
    def __init__(self, dim_cl66: int = 10, dim_nebe: int = 72):
        super().__init__()
        self.dim_cl66 = dim_cl66
        self.dim_nebe = dim_nebe
        self.W = nn.Parameter(torch.Tensor(dim_nebe, dim_cl66))
        
        # Initialisation avec poids existants + bruit
        self._initialiser_avec_poids_existants()
        
        # Poids de régularisation
        self.orthog_penalty_weight = 0.01
        self.norm_penalty_weight = 0.001
        self.rang_penalty_weight = 0.1
        self.diversite_penalty_weight = 1.0  # NOUVEAU : pénalité diversité
        
    def _initialiser_avec_poids_existants(self):
        """Initialise avec les poids existants + petit bruit"""
        try:
            W_exist = charger_poids_W('couche_hybride_W_poids.json')
            with torch.no_grad():
                # Ajout de bruit pour permettre l'apprentissage
                bruit = 0.05 * torch.randn_like(W_exist)
                self.W.data.copy_(W_exist + bruit)
            print("✅ Initialisé avec poids existants + bruit (σ=0.05)")
        except FileNotFoundError:
            print("⚠️ Poids existants non trouvés - initialisation aléatoire")
            nn.init.orthogonal_(self.W)
    
    def forward(self, v_cl66: torch.Tensor) -> torch.Tensor:
        """Projection linéaire Cl(6,6) → Nebe"""
        return v_cl66 @ self.W.T
    
    def orthogonalite_penalty(self) -> torch.Tensor:
        """Pénalité d'orthogonalité : W.T·W ≈ I_10"""
        WTW = self.W.T @ self.W
        I_10 = torch.eye(10, device=self.W.device)
        return torch.norm(WTW - I_10, p='fro')
    
    def norm_penalty(self) -> torch.Tensor:
        """Pénalité de norme : ||W||_F ≈ √72"""
        norme_F = torch.norm(self.W, p='fro')
        cible = math.sqrt(self.dim_nebe)
        return torch.abs(norme_F - cible)
    
    def rang_penalty(self) -> torch.Tensor:
        """Pénalité pour préserver le rang 10"""
        _, S, _ = torch.linalg.svd(self.W, full_matrices=False)
        seuil_min = 0.1
        return torch.sum(torch.relu(seuil_min - S) ** 2)
    
    def diversite_familiale_penalty(self, X_batch: torch.Tensor) -> torch.Tensor:
        """
        NOUVEAU : Pénalité pour encourager l'activation de toutes les familles
        Les 72 pentades sont organisées en 6 familles de 12
        """
        # Projection batch
        Y = X_batch @ self.W.T  # (batch, 72)
        
        # Calcul de l'activation par famille (6 familles × 12 pentades)
        activations_familles = []
        for fam in range(6):
            idx_debut = fam * 12
            idx_fin = (fam + 1) * 12
            # Activation moyenne de la famille
            activation_fam = torch.mean(torch.abs(Y[:, idx_debut:idx_fin]), dim=1)
            activations_familles.append(activation_fam)
        
        # Stack : (batch, 6)
        activations_familles = torch.stack(activations_familles, dim=1)
        
        # Objectif : toutes les familles également activées
        # Calcul de la variance entre familles (doit être minimale)
        variance_familles = torch.var(activations_familles, dim=1)
        
        # Pénalité : somme des variances (plus c'est bas, mieux c'est)
        penalty = torch.mean(variance_familles)
        
        return penalty
    
    def get_reg_loss(self, X_batch: torch.Tensor = None) -> torch.Tensor:
        """Calcule la perte de régularisation totale"""
        loss = torch.tensor(0.0, device=self.W.device, dtype=torch.float32)
        
        if self.orthog_penalty_weight > 0:
            loss = loss + self.orthog_penalty_weight * self.orthogonalite_penalty()
        if self.norm_penalty_weight > 0:
            loss = loss + self.norm_penalty_weight * self.norm_penalty()
        if self.rang_penalty_weight > 0:
            loss = loss + self.rang_penalty_weight * self.rang_penalty()
        if self.diversite_penalty_weight > 0 and X_batch is not None:
            loss = loss + self.diversite_penalty_weight * self.diversite_familiale_penalty(X_batch)
        
        return loss
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques de la couche"""
        W_np = self.W.detach().cpu().numpy()
        U, S, Vt = np.linalg.svd(W_np, full_matrices=False)
        norme_F = np.linalg.norm(W_np, 'fro')
        condition = S[0] / S[-1] if S[-1] > 1e-10 else float('inf')
        
        # Analyse de diversité familiale
        # Projection de vecteurs tests
        X_test = torch.randn(100, 10)
        Y_test = torch.randn(100, 10) @ self.W.T
        activations_familles = []
        for fam in range(6):
            idx_debut = fam * 12
            idx_fin = (fam + 1) * 12
            activation_fam = torch.mean(torch.abs(Y_test[:, idx_debut:idx_fin])).item()
            activations_familles.append(activation_fam)
        
        return {
            'norme_Frobenius': float(norme_F),
            'valeurs_singulieres': S.tolist(),
            'conditionnement': float(condition),
            'rang_estime': int(np.sum(S > 1e-6)),
            'activations_familles': activations_familles,
            'ratio_diversite': float(min(activations_familles) / max(activations_familles)) if max(activations_familles) > 0 else 0.0
        }

# ============================================================================
# FONCTION D'ENTRAÎNEMENT
# ============================================================================
def entrainer_W_avec_diversite(
    couche: CoucheHybrideDiversite,
    n_epochs: int = 2000,
    lr: float = 0.001,
    batch_size: int = 64
) -> Dict:
    """Entraînement avec contrainte de diversité familiale"""
    
    print("="*80)
    print("RÉENTRAÎNEMENT COUCHE W AVEC DIVERSITÉ FAMILIALE")
    print("="*80)
    
    # Génération de données d'entraînement
    n_samples = 5000
    torch.manual_seed(42)
    np.random.seed(42)
    
    # Données d'entrée (espace Cl(6,6) 10D)
    X = torch.randn(n_samples, 10, dtype=torch.float32) * 0.5
    
    # Cible physique (basée sur structure 72 pentades)
    try:
        with open('pentades_72_finales.json', 'r', encoding='utf-8') as f:
            pentades_data = json.load(f)
        W_cible = np.zeros((72, 10), dtype=np.float32)
        for idx, p in enumerate(pentades_data):
            elements = p.get('elements', [])
            signe = p.get('signe', 1)
            for i, elem in enumerate(elements[:3]):
                elem_str = str(elem).replace('-', '').replace("'", '')
                for j, gen in enumerate(['i', 'j', 'k', 'I', 'J', 'K']):
                    if gen in elem_str:
                        W_cible[idx, j] += signe * 0.5
        normes = np.linalg.norm(W_cible, axis=1, keepdims=True)
        normes = np.where(normes > 1e-8, normes, 1.0)
        W_cible = W_cible / normes
        Y_cible = X @ torch.tensor(W_cible, dtype=torch.float32).T
    except FileNotFoundError:
        print("⚠️ Fichier pentades non trouvé - cible aléatoire structurée")
        Y_cible = torch.randn(n_samples, 72) * 0.5
    
    # Ajout de bruit pour robustesse
    noise_level = 0.05
    Y = Y_cible + noise_level * torch.randn_like(Y_cible)
    
    # Optimiseur
    optimizer = torch.optim.Adam(couche.parameters(), lr=lr, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=100, min_lr=1e-7
    )
    
    # Historique
    history = {
        'loss_total': [],
        'loss_pred': [],
        'loss_diversite': [],
        'loss_reg': [],
        'ratio_diversite': [],
        'activations_familles': []
    }
    
    print(f"\n{'Époque':8s} | {'Loss Total':12s} | {'Loss Pred':12s} | "
          f"{'Loss Div':10s} | {'Ratio Div':10s} | {'Familles (6)':20s}")
    print("-"*80)
    
    best_ratio = 0.0
    patience_counter = 0
    max_patience = 300
    
    for epoch in range(n_epochs):
        couche.train()
        
        # Mini-batch
        indices = torch.randperm(n_samples)[:batch_size]
        X_batch = X[indices]
        Y_batch = Y[indices]
        
        # Forward
        optimizer.zero_grad()
        Y_pred = couche(X_batch)
        
        # Pertes
        loss_pred = torch.mean((Y_pred - Y_batch) ** 2)
        loss_diversite = couche.diversite_familiale_penalty(X_batch)
        loss_reg = couche.get_reg_loss(X_batch) - loss_diversite  # Exclude diversity from reg
        loss_total = loss_pred + loss_diversite + loss_reg
        
        # Backward
        loss_total.backward()
        torch.nn.utils.clip_grad_norm_(couche.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step(loss_total.item())
        
        # Logging every 100 epochs
        if epoch % 100 == 0 or epoch == n_epochs - 1:
            couche.eval()
            stats = couche.get_stats()
            
            history['loss_total'].append(loss_total.item())
            history['loss_pred'].append(loss_pred.item())
            history['loss_diversite'].append(loss_diversite.item())
            history['loss_reg'].append(loss_reg.item())
            history['ratio_diversite'].append(stats['ratio_diversite'])
            history['activations_familles'].append(stats['activations_familles'])
            
            fam_str = " | ".join([f"{a:.3f}" for a in stats['activations_familles']])
            print(f"{epoch:8d} | {loss_total.item():12.6f} | {loss_pred.item():12.6f} | "
                  f"{loss_diversite.item():10.6f} | {stats['ratio_diversite']:10.4f} | {fam_str}")
            
            # Early stopping sur ratio de diversité
            if stats['ratio_diversite'] > best_ratio:
                best_ratio = stats['ratio_diversite']
                patience_counter = 0
                # Sauvegarde des meilleurs poids
                torch.save(couche.state_dict(), 'couche_W_diversite_meilleur.pth')
            else:
                patience_counter += 1
            
            if patience_counter >= max_patience:
                print(f"\n⏹️ Early stopping à l'époque {epoch}")
                break
    
    # Charger les meilleurs poids
    try:
        couche.load_state_dict(torch.load('couche_W_diversite_meilleur.pth', weights_only=True))
        print("\n✅ Meilleurs poids restaurés")
    except Exception as e:
        print(f"\n⚠️ Impossible de restaurer: {e}")
    
    # Export JSON
    with open('couche_hybride_W_poids.json', 'w', encoding='utf-8') as f:
        etat = couche.state_dict()
        etat_python = {k: v.detach().cpu().numpy().tolist() for k, v in etat.items()}
        json.dump(etat_python, f, indent=2)
    print("✅ Poids exportés: couche_hybride_W_poids.json")
    
    # Statistiques finales
    stats_final = couche.get_stats()
    print("\n" + "="*80)
    print("STATISTIQUES FINALES")
    print("="*80)
    print(f"   Norme Frobenius : {stats_final['norme_Frobenius']:.4f} (cible: {math.sqrt(72):.4f})")
    print(f"   Conditionnement : {stats_final['conditionnement']:.2f} (cible: < 20)")
    print(f"   Rang estimé     : {stats_final['rang_estime']}/10")
    print(f"   Ratio diversité : {stats_final['ratio_diversite']:.4f} (1.0 = parfait)")
    print(f"\n   Activations par famille:")
    familles = ['FI', 'FII', 'FIII', 'FIV', 'FV', 'FVI']
    for i, (fam, act) in enumerate(zip(familles, stats_final['activations_familles'])):
        print(f"      {fam:4s} : {act:.4f}")
    
    return history

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    # Initialiser la couche
    couche = CoucheHybrideDiversite(dim_cl66=10, dim_nebe=72)
    
    # Stats initiales
    stats_init = couche.get_stats()
    print("\n📊 STATISTIQUES INITIALES (AVANT RÉENTRAÎNEMENT)")
    print("-"*80)
    print(f"   Ratio diversité : {stats_init['ratio_diversite']:.4f}")
    print(f"   Activations familles : {stats_init['activations_familles']}")
    
    # Entraînement
    history = entrainer_W_avec_diversite(couche, n_epochs=2000, lr=0.001)
    
    # Stats finales
    stats_final = couche.get_stats()
    print("\n📊 COMPARAISON AVANT / APRÈS")
    print("-"*80)
    print(f"   Ratio diversité : {stats_init['ratio_diversite']:.4f} → {stats_final['ratio_diversite']:.4f}")
    print(f"   Amélioration    : ×{stats_final['ratio_diversite']/max(stats_init['ratio_diversite'], 0.01):.2f}")
    
    print("\n" + "="*80)
    print("✅ RÉENTRAÎNEMENT TERMINÉ")
    print("="*80)
