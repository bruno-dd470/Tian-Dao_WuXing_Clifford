---
title: "ANGULAR TRANSITIONS BETWEEN PARTICLES"
subtitle: "A geometric reinterpretation of fundamental reactions within the framework of Cl(6,6) pentads"
author: "Bruno DE DOMINICIS"
date: "March 2026"
toc: true
toc-depth: 3
abstract_fr: |
  Nous présentons une reformulation des transitions entre particules élémentaires (désintégration $\beta$, annihilation $e^+e^-$, fusion nucléaire $pp$, désintégration du muon, oscillations de neutrinos, production de paires) comme des réarrangements d'angles dans le réseau d'Ibozoo Uû, où chaque particule est décrite par une pentade de l'algèbre de Clifford $\text{Cl}(6,6)$. Les générateurs $i,j,k,I,J,K$ sont interprétés comme des angles. Nous définissons un opérateur de transition $T$ agissant sur l'espace de Hilbert des pentades, décomposé en parties structure, feu, eau et mixte, et nous établissons des règles de sélection (conservation des générateurs, chiralité). Une formulation angulaire relie $T$ à des rotations dans l'espace à 6 dimensions. L'exemple de la désintégration $\beta$ est traité en détail. Ce formalisme offre une vision géométrique unifiée des interactions, en accord avec les concepts ummites.
abstract_en: |
  We present a reformulation of transitions between elementary particles ($\beta$ decay, $e^+e^-$ annihilation, $pp$ nuclear fusion, muon decay, neutrino oscillations, pair production) as angular rearrangements within the Ibozoo Uû network, where each particle is described by a pentad of the Clifford algebra $\text{Cl}(6,6)$. The generators $i,j,k,I,J,K$ are interpreted as angles. We define a transition operator $T$ acting on the Hilbert space of pentads, decomposed into structure, fire, water and mixed parts, and we establish selection rules (conservation of generators, chirality). An angular formulation relates $T$ to rotations in 6‑dimensional space. The example of $\beta$ decay is treated in detail. This formalism provides a unified geometric view of interactions, in agreement with Ummite concepts.
---

# Note on the Pre-Geometric Framework

Before addressing transitions between particles, it is essential to define the framework in which they occur. Following approaches that seek algebraic or geometric foundations for fundamental physics [1–4], we adopt as a working hypothesis that elementary particles may be described as stable configurations within a **pre-geometric algebraic substrate**.

In this approach, the fundamental degrees of freedom are not quantum fields propagating on a fixed spacetime background, but rather *angular relations* among the generators of a Clifford algebra. A useful analogy is to view the substrate as a "bundle of oriented axes" whose mutual orientations encode physical information. Crucially, an isolated generator carries no direct physical meaning; it is the *relational structure*—the pattern of angles between generators—that defines observable quantities such as charge, mass, or flavor.

This perspective is motivated by several considerations:
*   Clifford algebras naturally encode spin, chirality, and gauge structures [1, 2];
*   Pre-geometric approaches suggest that spacetime itself may emerge from more fundamental combinatorial or algebraic relations [3, 4];
*   Representing particles as algebraic "patterns" offers a route to unify interactions through geometric rearrangements rather than force-carrying exchanges.

**Link to our pentad model:** In this work, we use this concept to build a geometric representation of particles. A particle is not an entity immersed in this network; it is a local and stable configuration of this network. Our formalism in Cl(6, 6) and our pentads are a mathematical modeling of this idea:
1.  The six generators $i, j, k, I, J, K$ represent the fundamental "axes" of this **Algebraic Substrate** in our cosmos.
2.  The angles mentioned throughout the text (for example, $\theta_1 \dots \theta_6$) are the mathematical translation of the angular relations between these axes within the substrate.
3.  A **pentad**, this set of five elements (three structure bivectors, one axial "fire" element, one polar "water" element), is the complete angular signature that defines the quantum state and nature of a particle (its mass, charge, flavor) as a specific and coherent pattern of these angular relations within the network.

Thus, when we describe a transition $A \to B + C$ as a "rearrangement of angles within the **Fundamental Angular Network**," we mean that the configuration of angular relations that defined particle $A$ dissolves and reconfigures to form new stable configurations, those of particles $B$ and $C$. Particle physics thus becomes a dynamic geometry of angles.

---

# Principle of Pentad Codification**

In our model, each elementary particle is represented by a pentad, i.e., an ordered set of five elements from the Clifford algebra $\mathcal{Cl}(6, 6)$. These elements are interpreted as angles in a six-dimensional space (generators $i, j, k, I, J, K$). They are divided into three roles:

*   **Structure:** three bivectors (products of two generators) that establish the deep identity of the particle. For nucleons, we choose $\{iI, jJ, kK\}$. This choice reflects the symmetry between the three spatial dimensions $(i, j, k)$ and the three charge dimensions $(I, J, K)$. It is common to the neutron and proton because they share the same valence quark composition but with different charges.
*   **Fire:** an element of the form $\omega v$, where **$\omega$ is the pseudoscalar of the algebra** (product of the 12 generators, $\omega = \gamma\_1 \dots \gamma_{12}$, often associated with chirality or the weak interaction) and $v$ is one of the six generators. For nucleons, we have $\omega k$, which represents the weak component. This element is identical for the neutron and proton because the weak interaction acts analogously on both (they can transform into each other). The anticommutation property $\{\omega, \gamma_\mu\} = 0$ naturally encodes parity violation.
*   **Water:** an element of the form $1v$, where $1$ is a scalar element and $v$ a generator, representing mass or substance along a privileged axis. It is this element that carries the difference between the neutron and proton. Electric charge is encoded by the orientation of this axis: $1i$ corresponds to a mass aligned along $i$ (neutron, zero charge), while $1j$ corresponds to an alignment along $j$ (proton, positive charge). This interpretation is consistent with the idea that charge is a directional property in angle space.

---

# Mathematical Formalization

Let $\mathcal{Cl}(6,6)$ be the Clifford algebra generated by 12 basis vectors $\{\gamma_\mu\}_{\mu=1}^{12}$ satisfying the relation:
$$ \gamma\_\mu \gamma\_\nu + \gamma\_\nu \gamma\_\mu = 2\eta\_{\mu\nu} $$
where $\eta$ is the metric of signature $(6,6)$.

## Definition of the Chiral Element
The element responsible for chiral properties is identified as the **pseudoscalar** $\omega$ of the algebra:
$$ \omega \equiv \gamma_1 \gamma_2 \dots \gamma_{12} $$
This element satisfies $\omega^2 = 1$ and anticommutes with all odd-grade elements (vectors), i.e., $\{\omega, \gamma_\mu\} = 0$. This algebraic property naturally encodes **parity violation**. The "Fire" element ($F = \omega v$) behaves as an axial vector, while the "Water" element ($W = 1 v$) behaves as a polar vector.

## Hilbert Space $\mathcal{H}$
The space of physical states $\mathcal{H}$ is constructed from the minimal left ideals of $\mathcal{Cl}(6,6)$.
*   The spinor representation of $\mathcal{Cl}(6,6)$ has dimension $2^{12/2} = 64$ complex components.
*   Imposing the pentadic constraints (3 structure bivectors + 1 fire + 1 water) and projection via chiral projectors $P_{\pm} = \frac{1 \pm \omega}{2}$ reduces the physical degrees of freedom.
*   We estimate the dimension of the physical subspace relevant for the Standard Model families to be $\dim(\mathcal{H}) \in \{72, 144\}$, accounting for flavor, color, and particle/antiparticle doubling.

A transition is defined by the matrix element of an operator $T$ between initial and final pentadic states:
$$ \mathcal{M}_{A \to B} = \langle P_B \otimes \dots | T | P_A \rangle $$

## PENTADIC TRANSITION OPERATOR

### Decomposition

The transition operator $T$ acts on the tensor product of pentadic states. It is decomposed according to the geometric roles of the pentad elements:
$$ T = T_{\text{struct}} + T_{\text{fire}} + T_{\text{water}} + T_{\text{mix}} $$
*   **$T_{\text{struct}}$**: Acts on the triplet of bivectors defining the particle's identity.
*   **$T_{\text{fire}}$**: Acts on the axial component $F = \omega v$. It is responsible for chiral transitions (Weak interaction).
*   **$T_{\text{water}}$**: Acts on the polar component $W = v$. It governs mass/charge orientation changes.
*   **$T_{\text{mix}}$**: Couples the sectors, allowing for processes where structure converts into substance.

### Compact Expression

In the full $\mathcal{Cl}(6,6)$ basis $\{E_a\}$, the operator can be expressed as a sum over basis elements:
$$ T = \sum_{a,b} g_{ab} (E_a \otimes E_b^\dagger) $$
For a pentad state $|P\rangle = |B_1\rangle \wedge |B_2\rangle \wedge |B_3\rangle \wedge |F\rangle \wedge |W\rangle$, the action of $T$ is:
$$ T |P\rangle = \sum_{P'} \mathcal{T}_{P'P} |P'\rangle $$
where the coefficient $\mathcal{T}_{P'P}$ is computed as a cycle product of local transitions between the 5 components.

### Angular Formulation

The generators $\gamma_\mu$ are associated with angular coordinates $\theta_\mu$ in the pre-geometric network. The operator $T$ acts as a rotation operator in this space:
$$ T = \exp\left( i \sum_{\mu < \nu} \omega_{\mu\nu} L_{\mu\nu} \right) $$
where $L_{\mu\nu}$ are the generators of rotations in the 12-dimensional space. For neutrino oscillations ($\nu_e \to \nu_\mu$), this reduces to a rotation in the $(i, j)$ plane with angle $\alpha(t)$:
$$ P(\nu_e \to \nu_\mu) = \sin^2(\alpha(t)), \quad \text{with } \alpha(t) \propto \frac{\Delta m^2 L}{E} $$
This recovers the standard phenomenological formula from pure geometry.

### Conclusion

The operator $T$, defined as a geometric rearrangement within $\mathcal{Cl}(6,6)$, provides a unified mathematical framework for particle transitions. By identifying the chiral element as the algebraic pseudoscalar, we ground the Weak interaction in the fundamental parity properties of the space itself. This geometric model stands on rigorous algebraic footing and offers a promising path toward unifying quantum mechanics and geometry.

---

# β Decay: $n \to p + e^- + \bar{\nu}_e$

## Principle of Pentad Codification

In our model, each elementary particle is represented by a pentad, i.e., an ordered set of five elements from the Clifford algebra $\mathcal{Cl}(6, 6)$. These elements are interpreted as angles in a six-dimensional space (generators $i, j, k, I, J, K$). They are divided into three roles:

*   **Structure:** three bivectors (products of two generators) that establish the deep identity of the particle. For nucleons, we choose $\{iI, jJ, kK\}$. This choice reflects the symmetry between the three spatial dimensions $(i, j, k)$ and the three charge dimensions $(I, J, K)$. It is common to the neutron and proton because they share the same valence quark composition but with different charges.
*   **Fire:** an element of the form $\omega v$, where **$\omega$ is the pseudoscalar of the algebra** ($\omega = \gamma_1 \dots \gamma_{12}$, associated with chirality and the weak interaction) and $v$ is one of the six generators. For nucleons, we have $\omega k$, which represents the weak component. This element is identical for the neutron and proton because the weak interaction acts analogously on both. The anticommutation property $\{\omega, \gamma_\mu\} = 0$ naturally encodes parity violation.
*   **Water:** an element of the form $1v$, where $1$ is a scalar element and $v$ a generator, representing mass or substance along a privileged axis. It is this element that carries the difference between the neutron and proton. Electric charge is encoded by the orientation of this axis: $1i$ corresponds to a mass aligned along $i$ (neutron, zero charge), while $1j$ corresponds to an alignment along $j$ (proton, positive charge). This interpretation is consistent with the idea that charge is a directional property in angle space.

Thus, $\beta^-$ decay is seen as an angular rearrangement: the neutron changes its substance angle from $1i$ to $1j$, accompanied by the emission of the electron (which possesses $1j$) and the antineutrino (which possesses $1k$). The other angles (structure and fire) recombine to form the pentads of the final particles.

## Initial and Final Pentads

**Initial state (neutron):**
$$ P(n) = \{iI, jJ, kK, \omega k, 1i\} $$
Associated angles (with the correspondence $i \leftrightarrow \theta_1, j \leftrightarrow \theta_2, k \leftrightarrow \theta_3, I \leftrightarrow \theta_4, J \leftrightarrow \theta_5, K \leftrightarrow \theta_6$):
$$ \{\theta_1\theta_4, \theta_2\theta_5, \theta_3\theta_6, \omega \cdot \theta_3, 1 \cdot \theta_1\} $$

**Final state (proton + electron + antineutrino):**
$$
\begin{aligned}
P(p) &= \{iI, jJ, kK, \omega k, 1j\} \\
P(e^-) &= \{iI, iJ, iK, \omega k, 1j\} \\
P(\bar{\nu}_e) &= \{iK, iJ, iI, \omega j, 1k\}
\end{aligned}
$$
*(Note: The representation of the antineutrino here follows the neutrino convention; a more refined description could introduce charge conjugation signs to distinguish particle and antiparticle explicitly.)*

## Description of the Angular Transition

*   **Step 1:** The neutron changes its substance angle $1i \to 1j$ (rotation of the mass axis from $i$ to $j$). This corresponds to the transformation of a down quark into an up quark via the weak interaction.
*   **Step 2:** The structure angles of the neutron $\{iI, jJ, kK\}$ reorganize to give those of the proton (unchanged) and those of the electron (which are $\{iI, iJ, iK\}$). The electron carries away part of the structure.
*   **Step 3:** The antineutrino is formed from the remaining angles, with a substance $1k$ and a fire $\omega j$ (a permutation of generators).

This geometric description replaces the usual picture of $W^-$ boson emission: the transition is a pure rearrangement of angles within the algebraic substrate, without the introduction of virtual gauge bosons. The effective Fermi coupling $G_F$ emerges from the geometric overlap of the initial and final pentadic configurations.

---

# Annihilation $e^+ e^- \to \gamma\gamma$

## Principle of Pentad Codification for Leptons and Photons

*   **Structure:** for charged leptons, $\{iI, iJ, iK\}$; for the photon, the same structure but without fire or water components.
*   **Fire:** $\omega k$ for the electron, $-\omega k$ for the positron (opposite chirality projection).
*   **Water:** $1j$ for the electron, $-1j$ for the positron (opposite mass/charge orientation).

Photons are represented by $\{iI, iJ, iK, 0, 0\}$, reflecting their lack of rest mass and weak charge.

## Initial and Final Pentads

**Initial state:**
$$
\begin{aligned}
P(e^-) &= \{iI, iJ, iK, \omega k, 1j\} \\
P(e^+) &= \{-iI, -iJ, -iK, -\omega k, -1j\}
\end{aligned}
$$

**Final state (two photons):**
$$
\begin{aligned}
P(\gamma_1) &= \{iI, iJ, iK, 0, 0\} \\
P(\gamma_2) &= \{iI, iJ, iK, 0, 0\}
\end{aligned}
$$

## Description of the Angular Transition

Annihilation results from a cancellation of opposite algebraic elements: each element of the positron pentad is the negative of the corresponding electron element. Their algebraic sum gives zero for the fire and water sectors, but the structure bivectors must be conserved.

In terms of generators:
$$ \{iI, iJ, iK, \omega k, 1j\} + \{-iI, -iJ, -iK, -\omega k, -1j\} \to \{iI, iJ, iK, 0, 0\} + \{iI, iJ, iK, 0, 0\} $$

The six bivectors (three from each lepton) recombine into two sets of three, forming two photons. The fire and water elements cancel completely, consistent with photons having neither rest mass nor weak interaction. Conservation of the total number of generators is respected: each photon possesses three bivectors (six generators), while the lepton pair also contained six generators (with opposite signs).

The energy released corresponds to the "liberation" of the angular constraints that defined the massive state (water element), now converted into propagating structural modes (photons).

---

# Nuclear Fusion: $p + p \to d + e^+ + \nu_e$

## Pentads

**Initial state (two protons):**
$$
\begin{aligned}
P(p_1) &= \{iI, jJ, kK, \omega k, 1j\} \\
P(p_2) &= \{iI, jJ, kK, \omega k, 1j\}
\end{aligned}
$$

**Final state (deuteron, positron, electron neutrino):**
$$
\begin{aligned}
P(d) &= \{iI, jJ, kK, \omega k, 1j\} \quad \text{(with binding coupling)} \\
P(e^+) &= \{-iI, -iJ, -iK, -\omega k, -1j\} \\
P(\nu_e) &= \{iK, iJ, iI, \omega j, 1k\}
\end{aligned}
$$

## Description

One of the protons undergoes an internal $\beta^+$ transformation: its water element changes from $1j \to 1i$ (thus becoming a neutron internally), and it emits a positron (opposite pentadic configuration) and a neutrino (permuted structure). The neutron thus formed binds with the other proton to give a deuteron.

The binding is represented by an additional coupling of angles between the nucleon pentads, not detailed in the single-particle pentad itself. This coupling corresponds to the residual strong interaction, modeled as a sharing of structure bivectors between the two nucleons.

Conservation of generators is ensured by the selection rules of the weak interaction, which allow flavor changes (rotation in the $(i, j)$ plane) while preserving the total count of each generator type across the full reaction.

---

# Muon Decay: $\mu^- \to e^- + \bar{\nu}_e + \nu_\mu$

## Pentads

**Muon:**
$$ P(\mu^-) = \{jI, jJ, jK, \omega i, 1k\} $$

**Electron:**
$$ P(e^-) = \{iI, iJ, iK, \omega k, 1j\} $$

**Electron antineutrino:**
$$ P(\bar{\nu}_e) = \{iK, iJ, iI, \omega j, 1k\} $$

**Muon neutrino:**
$$ P(\nu_\mu) = \{jK, jI, jJ, \omega k, 1i\} $$

*(Remark: The representation of antineutrinos here follows the neutrino convention; a finer description could introduce charge conjugation signs to distinguish particle and antiparticle explicitly.)*

## Description

The muon has its structure aligned along the $j$ axis, while the electron has its structure along $i$. The decay corresponds to a **rotation of the flavor axis from $j$ to $i$**, accompanied by the emission of two neutrinos that carry away the angular permutations required to conserve generators.

The fire and water elements are redistributed among the three final products:
*   The electron takes the water $1j$ (charge) and fire $\omega k$.
*   The antineutrino carries water $1k$ and fire $\omega j$.
*   The muon neutrino carries water $1i$ and fire $\omega k$.

This process illustrates how **lepton flavor** is encoded in the orientation of the structure bivectors: muon family along $j$, electron family along $i$, tau family along $k$ (by extension).

---

# Neutrino Oscillation: $\nu_e \leftrightarrow \nu_\mu$

## Pentads

**Electron neutrino:**
$$ P(\nu_e) = \{iK, iJ, iI, \omega j, 1k\} $$

**Muon neutrino:**
$$ P(\nu_\mu) = \{jK, jI, jJ, \omega k, 1i\} $$

## Description

Oscillation is modeled as a **continuous rotation in angle space**: the privileged axis of the structure gradually passes from $i$ to $j$. The transition operator is:
$$ T_{\text{osc}} = \exp(i \alpha L_{ji}) $$
where $L_{ji}$ is the generator of rotations in the $(j, i)$ plane, and $\alpha$ is a time-dependent angle.

The oscillation probability is:
$$ P(\nu_e \to \nu_\mu) = \sin^2 \alpha, \quad \text{with } \alpha \propto \frac{\Delta m^2 L}{E} $$

This recovers the standard phenomenological formula from pure geometry. The mass-squared difference $\Delta m^2$ is interpreted as a difference in the angular velocity of rotation between the two flavor eigenstates within the algebraic substrate.

---

# Pair Production: $\gamma \to e^+ + e^-$

## Pentads

**Photon (in the presence of an external field):**
$$ P(\gamma) = \{iI, iJ, iK, 0, 0\} $$

**Electron-positron pair:**
$$
\begin{aligned}
P(e^-) &= \{iI, iJ, iK, \omega k, 1j\} \\
P(e^+) &= \{-iI, -iJ, -iK, -\omega k, -1j\}
\end{aligned}
$$

## Description

A high-energy photon interacts with an external field (e.g., the Coulomb field of a nucleus). This field provides the missing orientations (axes $j, k, \omega$) which allow the creation of substance: the water elements $1j$ and $-1j$ as well as the fire elements $\omega k$ and $-\omega k$ appear, while the photon's structure splits into two opposite sets.

This is the **inverse of annihilation**:
*   **Annihilation:** Massive pentads $\to$ massless structure (photons).
*   **Pair production:** Massless structure + external field $\to$ massive pentads.

The external field is necessary to satisfy conservation of momentum and to provide the angular "catalyst" that allows the water and fire elements to emerge from the algebraic vacuum. The threshold energy $E_\gamma \geq 2m_e c^2$ corresponds to the minimum angular excitation required to create the water elements (mass) of both particles.

---

# Summary Table of Transitions

| Transition Type | Angular Transformation | Conserved Quantities |
|-----------------|------------------------|----------------------|
| $n \to p + e^- + \bar{\nu}_e$ ($\beta^-$) | Rotation of substance angle ($1i \to 1j$) + emission | Generators, chirality |
| $e^+ e^- \to \gamma\gamma$ (Annihilation) | Cancellation of opposite fire/water angles | Total bivector count |
| $p + p \to d + e^+ + \nu_e$ (Fusion) | Interlacing of angles (with $\beta^+$ on one proton) | Generators, baryon number |
| $\mu^- \to e^- + \bar{\nu}_e + \nu_\mu$ (Decay) | Rotation of flavor axis ($j \to i$) | Generators, lepton number |
| $\nu_e \leftrightarrow \nu_\mu$ (Oscillation) | Continuous rotation in angle space (time-dependent) | Total probability norm |
| $\gamma \to e^+ + e^-$ (Pair production) | Creation of substance (water and fire) from structure + field | Energy-momentum, generators |

---

# Angular Conservation Laws

The pentadic formalism imposes the following conservation laws on all transitions:

1.  **Conservation of the total number of generators:** Each element (bivector, fire, water) contains a fixed number of generators; the sum across initial and final states is invariant.
2.  **Conservation of generator type:** The generators $i, j, k, I, J, K$ are conserved individually, modulo gauge transformations (rotations in generator space).
3.  **Conservation of chirality:** Linked to the presence of $\omega$ in fire elements. Chirality is conserved in electromagnetic and strong processes but can be flipped by $T_{\text{fire}}$ in weak processes (via projection $P_L = \frac{1 - \omega}{2}$).
4.  **Conservation of total angular momentum:** In angle space, rotations conserve the norm of the angular vector. This corresponds to standard angular momentum conservation in physical space.
5.  **Pentadic closure:** Valid transitions must map a valid pentad to a tensor product of valid pentads. This forbids certain decays that would violate the bivector structure (e.g., proton stability is ensured because no valid pentadic rearrangement allows $p \to \text{mesons}$ without violating generator conservation).

---

# BIBLIOGRAPHIE SUGGÉRÉE 

Pour étayer la section 1.1.1 et donner du poids académique, ajoutez ces références standards :

1.  Hestenes, D. (1984). *Clifford Algebra to Geometric Calculus*. D. Reidel Publishing. (Pour l'usage des algèbres de Clifford en physique).
2.  Connes, A. (1994). *Noncommutative Geometry*. Academic Press. (Pour le concept de géométrie pré-géométrique algébrique).
3.  Furey, C. (2016). "Standard Model Physics from an Algebra?". *Journal of Mathematical Physics*. (Pour la codification des particules via algèbre).
4.  Rovelli, C. (2004). *Quantum Gravity*. Cambridge University Press. (Pour l'idée de réseau de spins/pré-géométrie).
5.  Wheeler, J. A. (1962). *Geometrodynamics*. Academic Press. (Pour le concept historique de "pregeometry").


