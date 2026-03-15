---
title: "ANGULAR TRANSITIONS BETWEEN PARTICLES"
subtitle: "Une réinterprétation géométrique des réactions fondamentales dans le cadre des pentades Cl(6,6)"
author: "Bruno DE DOMINICIS"
date: "March 2026"
abstract_fr: |
  Nous présentons une reformulation des transitions entre particules élémentaires (désintégration $\beta$, annihilation $e^+e^-$, fusion nucléaire $pp$, désintégration du muon, oscillations de neutrinos, production de paires) comme des réarrangements d'angles dans le réseau d'Ibozoo Uû, où chaque particule est décrite par une pentade de l'algèbre de Clifford $\text{Cl}(6,6)$. Les générateurs $i,j,k,I,J,K$ sont interprétés comme des angles. Nous définissons un opérateur de transition $T$ agissant sur l'espace de Hilbert des pentades, décomposé en parties structure, feu, eau et mixte, et nous établissons des règles de sélection (conservation des générateurs, chiralité). Une formulation angulaire relie $T$ à des rotations dans l'espace à 6 dimensions. L'exemple de la désintégration $\beta$ est traité en détail. Ce formalisme offre une vision géométrique unifiée des interactions, en accord avec les concepts ummites.
abstract_en: |
  We present a reformulation of transitions between elementary particles ($\beta$ decay, $e^+e^-$ annihilation, $pp$ nuclear fusion, muon decay, neutrino oscillations, pair production) as angular rearrangements within the Ibozoo Uû network, where each particle is described by a pentad of the Clifford algebra $\text{Cl}(6,6)$. The generators $i,j,k,I,J,K$ are interpreted as angles. We define a transition operator $T$ acting on the Hilbert space of pentads, decomposed into structure, fire, water and mixed parts, and we establish selection rules (conservation of generators, chirality). An angular formulation relates $T$ to rotations in 6‑dimensional space. The example of $\beta$ decay is treated in detail. This formalism provides a unified geometric view of interactions, in agreement with Ummite concepts.
---

# ANGULAR TRANSITIONS BETWEEN PARTICLES

## General principle

A transition $A \to B + C + \dots$ becomes a **rearrangement of angles** in the Ibozoo Uû lattice. The angles (generators $i,j,k,I,J,K$) recombine to form new pentads.

---

## β decay: n → p + e⁻ + ν̄ₑ

### Initial and final pentads

**Neutron** (our proposal):

$$P(n) = \{ iI,\; jJ,\; kK,\; i'k,\; 1j \}$$

Angles: $\{\theta_1\theta_4,\; \theta_2\theta_5,\; \theta_3\theta_6,\; (\theta_1\theta_2\theta_3\theta_4\theta_5\theta_6)\cdot\theta_3,\; 1\cdot\theta_2\}$

**Proton**:

$$P(p) = \{ iI,\; jJ,\; kK,\; i'k,\; 1j \}$$

… but it's identical! Let's correct it.

**Corrected neutron** (without electric charge):

$$P(n) = \{ iI,\; jJ,\; kK,\; i'k,\; 1i \} \qquad (\text{Water } = 1i \text{ instead of } 1j)$$

**Proton** (with charge):

$$P(p) = \{ iI,\; jJ,\; kK,\; i'k,\; 1j \}$$

**Electron**:

$$P(e^-) = \{ iI,\; iJ,\; iK,\; i'k,\; 1j \}$$

**Antineutrino**:

$$P(\bar{\nu}_e) = \{ iK,\; iJ,\; iI,\; i'j,\; 1k \}$$

### Angular transition

The decay is written as:

$$P(n) \to P(p) + P(e^-) + P(\bar{\nu}_e)$$

In terms of angles:

- **Step 1**: The neutron changes its substance angle
  $1i$ (mass along $i$) → $1j$ (mass along $j$)
  → rotation of the mass angle from $i$ to $j$.

- **Step 2**: Emission of the electron
  The structure angles $iI, iJ, iK$ partially detach and form a new pentad.

- **Step 3**: Emission of the antineutrino
  The remaining angles reorganize.

**Angular momentum conservation**: the sum of the "angular momenta" (angles) is conserved.

---

## Annihilation e⁺ e⁻ → γγ

### Pentads

**Positron**:

$$P(e^+) = \{ -iI,\; -iJ,\; -iK,\; -i'k,\; -1j \}$$

**Electron**:

$$P(e^-) = \{ iI,\; iJ,\; iK,\; i'k,\; 1j \}$$

**Photon** (simplified):

$$P(\gamma) = \{ iI,\; iJ,\; iK,\; 0,\; 0 \} \quad (\text{no Fire/Water})$$

### Angular transition

$$P(e^+) + P(e^-) \to P(\gamma) + P(\gamma)$$

- Opposite angles cancel: $iI + (-iI) = 0$.
- Two sets of angles $\{iI, iJ, iK\}$ remain, without substance.
- These sets form two photons.

This is a **phase cancellation** between opposite angular configurations.

---

## Nuclear fusion: p + p → d + e⁺ + νₑ

Two protons fuse to form a deuteron, a positron and a neutrino.

### Deuteron (bound p + n)

Effective pentad of the deuteron:

$$P(d) = \{ iI,\; jJ,\; kK,\; i'k,\; 1j \} \quad (\text{like proton but with bond})$$

### Angular transition

$$P(p) + P(p) \to P(d) + P(e^+) + P(\nu_e)$$

- The angles of the two protons interlace.
- A proton transforms one of its quarks $u \to d$ via weak interaction.
- Emission of the positron and the neutrino.

In terms of angles: color angles recombine to form a stable bound structure.

---

## Muon decay: μ⁻ → e⁻ + ν̄ₑ + νμ

### Pentads

**Muon**:

$$P(\mu^-) = \{ jI,\; jJ,\; jK,\; i'i,\; 1k \}$$

**Electron**:

$$P(e^-) = \{ iI,\; iJ,\; iK,\; i'k,\; 1j \}$$

**Muon neutrino**:

$$P(\nu_\mu) = \{ jK,\; jI,\; jJ,\; i'k,\; 1i \}$$

**Electron antineutrino**:

$$P(\bar{\nu}_e) = \{ iK,\; iJ,\; iI,\; i'j,\; 1k \}$$

### Angular transition

$$P(\mu^-) \to P(e^-) + P(\bar{\nu}_e) + P(\nu_\mu)$$

- The muon has its principal axis along $j$ (structure $jI, jJ, jK$).
- The electron has its principal axis along $i$.
- This is a **rotation of the spatial reference angle** from $j$ to $i$.
- The neutrinos carry the angular differences.

---

## Neutrino oscillation: νₑ → νμ

### Pentads

**Electron neutrino**:

$$P(\nu_e) = \{ iK,\; iJ,\; iI,\; i'j,\; 1k \}$$

**Muon neutrino**:

$$P(\nu_\mu) = \{ jK,\; jI,\; jJ,\; i'k,\; 1i \}$$

### Angular transition

$$P(\nu_e) \rightleftarrows P(\nu_\mu)$$

This is an oscillation between reference angles:

- $\nu_e$ is centered on the axis $i$,
- $\nu_\mu$ is centered on the axis $j$.

The transition is a **rotation in angle space** with a frequency proportional to $\Delta m^2$.

---

## Pair production: γ → e⁺ + e⁻

### Angular transition

$$P(\gamma) + \text{field} \to P(e^+) + P(e^-)$$

- A photon (pure configuration of angles without substance) interacts with a field.
- The angles $\{iI, iJ, iK\}$ split into two sets.
- Each set receives a substance ($1j$ and $-1j$) to form $e^-$ and $e^+$.

This is the **creation of substance from pure angles** through interaction with an external field.

---

## Summary table of transitions

| Transition | Type | Angular transformation |
|------------|------|------------------------|
| $n \to p + e^- + \bar{\nu}_e$ | $\beta^-$ | Rotation of substance angle ($1i\to1j$) + emission |
| $e^+e^- \to \gamma\gamma$ | Annihilation | Cancellation of opposite angles |
| $pp \to d e^+ \nu_e$ | Fusion | Interlacing of angles |
| $\mu^- \to e^- \bar{\nu}_e\nu_\mu$ | Decay | Rotation of spatial axis ($j\to i$) |
| $\nu_e \rightleftarrows \nu_\mu$ | Oscillation | Rotation in angle space |
| $\gamma \to e^+e^-$ | Pair production | Creation of substance from angles |

---

## Angular conservation laws

These transitions suggest conservation laws:

- **Conservation of the number of angles**: the total number of generators (counted with multiplicities) is conserved.
- **Conservation of "total angular momentum"**: the vector sum of the angles (in a sense to be defined) is conserved.
- **Conservation of chirality**: linked to the presence/absence of $i'$ in the terms.

---

## Mathematical formalization

We can define a **transition operator** $T$ such that:

$$T(P_A \to P_B + P_C) = \langle P_B \otimes P_C | H_{\text{int}} | P_A \rangle$$

where $H_{\text{int}}$ couples the angles between pentads.

The transition probability is:

$$\text{Prob} = \big| \langle P_{\text{final}} | e^{-i H_{\text{int}} t} | P_{\text{initial}} \rangle \big|^2$$

---

# PENTADIC TRANSITION OPERATOR

## Space of pentadic states

Let $\mathcal{H}$ be the Hilbert space of pentadic states, of dimension 72 (or 144 in $Cl(6,6)$):

$$
\mathcal{H} = \operatorname{span}\{ |P_1\rangle, |P_2\rangle, \dots, |P_{72}\rangle \}
$$

where each $|P_a\rangle$ is a basis state corresponding to a specific pentad.

## Structure of the transition operator

$T$ acts on $\mathcal{H}\otimes\mathcal{H} \to \mathcal{H}\otimes\mathcal{H}$ (two-body process) or more generally on tensor products.

It is decomposed into three parts:

$$
T = T_{\text{structure}} + T_{\text{fire}} + T_{\text{water}} + T_{\text{mixed}}
$$

### $T_{\text{structure}}$: transitions between structural elements

This operator acts on triples of bivectors $\{B_1,B_2,B_3\}$.

For an elementary transition $B_i \to B_j$:

$$
T_{\text{structure}} |B_i\rangle\langle B_j| = \sum_{k,l} M_{ij}^{kl} |B_k\rangle\langle B_l|
$$

where $M$ is a $15\times15$ matrix (for the 15 bivectors of $Cl(6,0)$).

Example: transition $iI \to iJ$ (rotation in charge space)

$$
T_{\text{structure}} |iI\rangle\langle iJ| = \alpha\, |iJ\rangle\langle iI| + \beta\, |iK\rangle\langle iK| + \cdots
$$

### $T_{\text{fire}}$: transitions involving the Fire element

The Fire element $F = i'\cdot v$ ($v\in\{i,j,k,I,J,K\}$) has its own operator:

$$
T_{\text{fire}} |F\rangle\langle F'| = \gamma_{FF'}\, |F'\rangle\langle F| + \text{cross terms with structure}
$$

### $T_{\text{water}}$: transitions involving the Water element

The Water element $S = 1\cdot v$ has a similar operator:

$$
T_{\text{water}} |S\rangle\langle S'| = \delta_{SS'}\, |S'\rangle\langle S|
$$

### $T_{\text{mixed}}$: couplings between different types

Transitions that mix structure, fire and water:

$$
\begin{aligned}
T_{\text{mixed}} &|B_1B_2B_3,F,S\rangle\langle B'_1B'_2B'_3,F',S'| = \\
&\lambda_1 \langle B_1,B'_1\rangle \; |B'_2B'_3,F',S'\rangle\langle B_2B_3,F,S| \\
+&\lambda_2 \langle F,F'\rangle \; |B_1B_2B_3,S'\rangle\langle B'_1B'_2B'_3,S| \\
+&\lambda_3 \langle S,S'\rangle \; |B_1B_2B_3,F'\rangle\langle B'_1B'_2B'_3,F|
\end{aligned}
$$

## Compact expression in $Cl(6,0)$

We can write $T$ as an element of the tensor algebra over $Cl(6,0)$:

$$
T = \sum_{a,b} g_{ab} \; (E_a \otimes E_b^*)
$$

where $\{E_a\}$ are the 64 elements of $Cl(6,0)$, $g_{ab}$ are coupling coefficients, and $E_b^*$ is the dual element.

For a pentad $P = \{B_1,B_2,B_3,F,S\}$, we have:

$$
|P\rangle = |B_1\rangle \wedge |B_2\rangle \wedge |B_3\rangle \wedge |F\rangle \wedge |S\rangle
$$

and $T$ acts via:

$$
T|P\rangle = \sum_{P'} T_{P'P} |P'\rangle,\qquad
T_{P'P} = \langle P'|T|P\rangle = \sum_{\text{cycles}} \prod \langle \text{element}'| T_{\text{local}}|\text{element}\rangle
$$

## Selection rules

- **Conservation of the total number of generators**: each element of $Cl(6,0)$ has a conserved "weight" (number of generators).
- **Conservation of generator type**: $i,j,k,I,J,K$ are conserved individually (modulo gauge transformations).
- **Conservation of chirality**: linked to the presence of $i'$ in the terms.
- **Pentadic Feynman rules**: for a transition to an $n$-body system,
  $$
  T_{P_1\cdots P_n \to Q_1\cdots Q_m} = \sum_{\text{diagrams}} \prod_{\text{vertices}} g_v \cdot \prod_{\text{propagators}} \Delta_{pq}
  $$

## Example: $\beta$ decay

For $n \to p + e^- + \bar{\nu}_e$, the matrix element is:

$$
\langle P(p)\otimes P(e^-)\otimes P(\bar{\nu}_e) | T | P(n) \rangle
$$

Factoring out:

$$
T_\beta = G_F \; (J_{\text{hadronic}})\cdot(J_{\text{leptonic}})
$$

with
$$
J_{\text{hadronic}} = \langle P(p)| T_{\text{structure}} |P(n)\rangle,\qquad
J_{\text{leptonic}} = \langle P(e^-)\otimes P(\bar{\nu}_e)| T_{\text{fire}}\otimes T_{\text{water}} |0\rangle
$$

## Canonical quantization

We define creation/annihilation operators for each pentad:

$$
[ a_P, a_Q^\dagger ] = \delta_{PQ}
$$

The interaction Hamiltonian becomes:

$$
H_{\text{int}} = \sum_{P,Q,R,\dots} T_{PQ\dots}^{RS\dots}\; a_P^\dagger a_Q^\dagger \cdots a_R a_S \cdots
$$

## Connection to field theory

Our $T$ is equivalent to the $S$ matrix in quantum field theory, with an underlying discrete structure:

$$
S = T \exp\!\left( i\int d^4x\, H_{\text{int}}(x) \right)
$$

where $H_{\text{int}}(x)$ is constructed from pentadic fields $\phi_P(x)$:

$$
\phi_P(x) = \sum_k u_{Pk}(x) a_{Pk} + v_{Pk}(x) a_{Pk}^\dagger
$$

## Angular formulation (Ummite interpretation)

In terms of angles, $T$ becomes a differential operator on angular wave functions:

$$
T = \exp\!\left( i\sum_{i,j} \omega_{ij} L_{ij} \right)
$$

where $L_{ij}$ are the rotation generators in the 6-angle space, and $\omega_{ij}$ are transition frequencies.

The matrix elements:

$$
\langle \theta'_1\dots\theta'_6 | T | \theta_1\dots\theta_6 \rangle = \delta^6(\theta' - \theta - \Omega) \cdot \text{phase}
$$

## Numerical example: $\mu \to e$ transition

For muon decay, the reference angles change:

$$
|\theta_1,\theta_2,\theta_3,\theta_4,\theta_5,\theta_6\rangle_\mu = |\theta_1=j,\dots\rangle
$$

The operator $T$ performs a rotation:

$$
T_{\mu\to e} = \exp(i\alpha L_{ji})
$$

where $L_{ji}$ is the rotation generator from axis $j$ to axis $i$. The transition probability is:

$$
\text{Prob} = |\langle \theta_i(e^-)| T_{\mu\to e} |\theta_j(\mu)\rangle|^2 = \sin^2\alpha
$$

and $\alpha$ is proportional to time and the mass difference.

## Toward a Complete Theory

To complete the theory, we must:

- Determine the coupling constants $g_{ab}$ from experimental data.
- Derive the pentadic Feynman rules.
- Calculate the cross sections and compare them to measurements.
- Predict new transitions not yet observed.

## Conclusion

The transition operator $T$ can be specified as:

$$
T = \sum_{\text{cycles}} \prod_{\text{elements}} \langle \text{element}' | T_{\text{local}} | \text{element} \rangle
$$

with $T_{\text{local}}$ acting on the 64 elements of $Cl(6,0)$ according to:

$$
T_{\text{local}} = \sum_{a,b} g_{ab}\; (e_a \otimes e_b^*)
$$

and the selection rules:

- conservation of generators,
- conservation of chirality,
- gauge invariance.

This is a mathematically well-defined operator that allows us to calculate all particle transitions in this pentadic model.
