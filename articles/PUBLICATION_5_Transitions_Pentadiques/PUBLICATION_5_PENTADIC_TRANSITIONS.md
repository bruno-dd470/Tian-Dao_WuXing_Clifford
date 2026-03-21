---
title: “ANGULAR TRANSITIONS BETWEEN PARTICLES”
subtitle: “A geometric reinterpretation of fundamental reactions within the framework of Cl(6,6) pentads”
author: “Bruno DE DOMINICIS”
date: “March 2026”
toc: true
toc-depth: 3
abstract_fr: |
  We present a reformulation of transitions between elementary particles (beta decay, e+e- annihilation, $pp$ nuclear fusion, muon decay, neutrino oscillations, pair production) as angle rearrangements in the Ibozoo Uû lattice, where each particle is described by a pentad of the Clifford algebra $\text{Cl}(6,6)$. The generators $i,j,k,I,J,K$ are interpreted as angles. We define a transition operator $T$ acting on the Hilbert space of pentads, decomposed into structure, fire, water, and mixed parts, and we establish selection rules (conservation of generators, chirality). An angular formulation relates $T$ to rotations in 6-dimensional space. The example of $\beta$ decay is discussed in detail. This formalism offers a unified geometric view of interactions, in accordance with Ummite concepts.
abstract_en: |
  We present a reformulation of transitions between elementary particles ($\beta$ decay, $e^+e^-$ annihilation, $pp$ nuclear fusion, muon decay, neutrino oscillations, pair production) as angular rearrangements within the Ibozoo Uû network, where each particle is described by a pentad of the Clifford algebra $\text{Cl}(6,6)$. The generators $i,j,k,I,J,K$ are interpreted as angles. We define a transition operator $T$ acting on the Hilbert space of pentads, decomposed into structure, fire, water, and mixed parts, and we establish selection rules (conservation of generators, chirality). An angular formulation relates $T$ to rotations in 6-dimensional space. The example of $\beta$ decay is treated in detail. This formalism provides a unified geometric view of interactions, in agreement with Ummite concepts.
---

# ANGULAR TRANSITIONS BETWEEN PARTICLES

## Note on the pre-geometric framework

Before addressing transitions between particles, it is essential to define the framework in which they occur.
Following approaches that seek algebraic or geometric foundations for fundamental physics [1–4], we adopt as a working hypothesis the idea that elementary particles can be described as stable configurations within a pre-geometric algebraic substrate.
 
In this approach, the fundamental degrees of freedom are not quantum fields propagating over a fixed spatiotemporal background, but rather angular relations between the generators of a Clifford algebra. A useful analogy is to consider the substrate as a **“bundle of oriented axes”** whose mutual orientations encode physical information.
 
It is essential to note that an isolated generator has no direct physical meaning; it is the relational structure—**the configuration of the angles between the generators**—that defines observable quantities such as charge, mass, or flavor.

This perspective is motivated by several considerations: 

* Clifford algebras naturally encode spin, chirality, and gauge structures [1, 2]; 
* Pre-geometric approaches suggest that spacetime itself might emerge from more fundamental combinatorial or algebraic relations [3, 4];
* Representing particles as algebraic “patterns” offers a path to unify interactions through geometric rearrangements rather than through force exchanges.

**Link to our pentad model**: In this work, we use this concept to construct a geometric representation of particles. A particle is not an entity embedded in this lattice; it is a local and stable configuration of this lattice.
 

Our formalism in Cl(6,6) and our **pentads** constitute a mathematical model of this idea:
1. The six **generators** $i,j,k,I,J,K$ represent the fundamental “axes” of this algebraic substrate in our cosmos.
2. The **angles** mentioned throughout the text (for example, $\theta_1\theta_4$) are the mathematical translation of the angular relationships between these axes within the substrate.
 3. A **pentad**, this set of five elements (three structural bivectors, a “fire” axial element, a “water” polar element), is the complete angular signature that defines the quantum state and nature of a particle (its mass, charge, flavor) as a specific and coherent pattern of these angular relationships within the lattice. 

Thus, when we describe a transition $A \to B + C + \dots$ as a **"rearrangement of angles** within the **Fundamental Angular Lattice**, we mean that the configuration of angular relations that defined particle $A$ dissolves and reconfigures to form new stable configurations, those of particles $B$ and $C$. Particle physics thus becomes a **dynamic geometry of angles**.

---

## Principle of pentad coding

In our model, each elementary particle is represented by a **pentad**, that is, an ordered set of five elements of the Clifford algebra $\text{Cl}(6,6)$. These elements are interpreted as **angles** in a six-dimensional space (generators $i,j,k,I,J,K$).
 
They are divided into three roles:

- **The structure**: three bivectors (products of two generators) that define the particle’s intrinsic identity. For nucleons, we choose $\{iI, jJ, kK\} $. This choice reflects the symmetry between the three spatial dimensions ($i,j,k$) and the three charge dimensions ($I,J,K$). It is common to both the neutron and the proton because they share the same valence quark composition (two up quarks and one down quark for the proton; one up and two down for the neutron) but with different charges.
- **Fire**: an element of the form $i'v$, where $i'$ is an additional generator (often associated with chirality or the weak interaction) and $v$ is one of the six generators. For nucleons, we have $i'k$, which represents the weak component. This element is identical for the neutron and the proton because the weak interaction acts similarly on both (they can transform into one another).
- **Water**: an element of the form $1v$, where $1$ is a scalar element (or a neutral generator) and $v$ is a generator, representing the **mass** or the **substance** along a preferred axis. It is this element that accounts for the difference between the neutron and the proton. The electric charge is encoded by the orientation of this axis: $1i$ corresponds to a mass aligned along $i$ (neutron, zero charge), while $1j$ corresponds to an alignment along $j$ (proton, positive charge). This interpretation is consistent with the idea that charge is a directional property in angle space.

## β Decay: n → p + e⁻ + ν̄ₑ

Thus, β⁻ decay is viewed as an **angular rearrangement**: the neutron changes its substance angle from $i$ to $j$, which is accompanied by the emission of the electron (which has $1j$) and the antineutrino (which has $1k$). The other angles (structure and fire) recombine to form the pentads of the final particles.

### Initial and Final Pentads

**Initial State** (neutron):

$$
P(n) = \{ iI,\ jJ,\ kK,\ i'k,\ 1i \}
$$

Associated angles (with the correspondence $i \leftrightarrow \theta_1$, $j \leftrightarrow \theta_2$, $k \leftrightarrow \theta_3$, $I \leftrightarrow \theta_4$, $J \leftrightarrow \theta_5$, $K \leftrightarrow \theta_6$):
$$
\{\theta_1\theta_4,\ \theta_2\theta_5,\ \theta_3\theta_6,\ (\theta_1\theta_2\theta_3\theta_4\theta_5\theta_6)\cdot\theta_3,\ 1\cdot\theta_1\}
$$

**Final state** (proton + electron + antineutrino):

$$
P(p) = \{ iI,\ jJ,\ kK,\ i'k,\ 1j \}
$$
$$
P(e^-) = \{ iI,\ iJ,\ iK,\ i'k,\ 1j \}
$$
$$
P(\bar{\nu}_e) = \{ iK,\ iJ,\ iI,\ i'j,\ 1k \}
$$

(Note: The representation of the antineutrino is taken here to be identical to that of the electron neutrino used in the section on oscillations; a more precise convention could introduce signs to distinguish between particle and antiparticle, but this does not affect the qualitative discussion.)

### Description of the angular transition

- **Step 1**: The neutron changes its substance angle from $1i$ to $1j$ (rotation of the mass axis from $i$ to $j$). This is the transformation of the down quark into an up quark via the weak interaction.
- **Step 2**: The neutron’s structure angles $\{iI, jJ, kK\}$ reorganize to yield those of the proton (unchanged) and those of the electron (which are $\{iI, iJ, iK\}$). The electron carries away part of the structure.
- **Step 3**: The antineutrino is formed from the remaining angles, with a $1k$ component and an $i'j$ component (i.e., a permutation of the generators).

This geometric description advantageously replaces the usual picture of the emission of a $W^-$ boson: the transition is a pure rearrangement of angles, without the introduction of virtual particles.

---

## Annihilation e⁺ e⁻ → γγ

### Principle of pentad coding for leptons and photons

- **The structure**: for charged leptons, $\{iI, iJ, iK\}$; for the photon, the same but without fire or water.
- **Fire**: $i'k$ for the electron, $-i'k$ for the positron.
- **Water**: $1j$ for the electron, $-1j$ for the positron.

Photons are represented by $\{iI, iJ, iK, 0, 0\}$.

### Initial and final pentads

**Initial state**:

$$
P(e^-) = \{ iI,\ iJ,\ iK,\ i'k,\ 1j \}
$$
$$
P(e^+) = \{ -iI,\ -iJ,\ -iK,\ -i'k,\ -1j \}
$$

**Final state** (two photons):

$$
P(\gamma_1) = \{ iI,\ iJ,\ iK,\ 0,\ 0 \}
$$
$$
P(\gamma_2) = \{ iI,\ iJ,\ iK,\ 0,\ 0 \}
$$

### Description of the angular transition

Annihilation results from a **cancellation of opposite angles**: each component of the positron is the opposite of that of the electron. Their sum is zero, but energy must be conserved. The six bivectors (three of each) recombine into two sets of three, forming two photons. The fire and water components actually cancel each other out, since photons have neither mass nor weak interaction.

In terms of angles:

$$
\{iI,iJ,iK,i'k,1j\} + \{-iI,-iJ,-iK,-i'k,-1j\} \to \{iI,iJ,iK,0,0\} + \{iI,iJ,iK,0,0\}
$$

The conservation of the number of generators is respected: each photon has three bivectors (six generators), while the pair also had six (with opposite signs).

---

## Nuclear fusion: p + p → d + e⁺ + νₑ

### Pentads

**Initial state** (two protons):

$$
P(p_1) = \{ iI,\ jJ,\ kK,\ i'k,\ 1j \}
$$
$$
P(p_2) = \{ iI,\ jJ,\ kK,\ i'k,\ 1j \}
$$

**Final state** (deuteron, positron, electron neutrino):

$$
P(d) = \{ iI,\ jJ,\ kK,\ i'k,\ 1j \} \quad (\text{with binding})
$$
$$
P(e^+) = \{ -iI,\ -iJ,\ -iK,\ -i'k,\ -1j \}
$$
$$
P(\nu_e) = \{ iK,\ iJ,\ iI,\ i'j,\ 1k \}
$$

### Description

One of the protons undergoes an internal β⁺ decay: its spin changes from $1j$ to $1i$ (thus becoming a neutron), and it emits a positron (opposite configuration) and a neutrino (permutated structure) . The neutron thus formed binds with the other proton to form a deuteron. The binding is represented by an additional coupling of the angles, not detailed in the pentad itself.

The conservation of the generators is ensured by the selection rules of the weak interaction, which allow for flavor changes.

---

## Muon decay: μ⁻ → e⁻ + ν̄ₑ + νμ

### Pentads

**Muon**:

$$
P(\mu^-) = \{ jI,\ jJ,\ jK,\ i'i,\ 1k \}
$$

**Electron**:

$$
P(e^-) = \{ iI,\ iJ,\ iK,\ i'k,\ 1j \}
$$

**Electron antineutrino**:

$$
P(\bar{\nu}_e) = \{ iK,\ iJ,\ iI,\ i'j,\ 1k \}
$$

**Muon neutrino**:

$$
P(\nu_\mu) = \{ jK,\ jI,\ jJ,\ i'k,\ 1i \}
$$

(Note: The representation of antineutrinos here is modeled after that of neutrinos, which is a simplification. A more detailed description could introduce signs to distinguish between particles and antiparticles, but this does not change the geometric interpretation of the axis rotation.)

### Description

The muon has its structure along the $j$ axis, the electron along the $i$ axis. The decay corresponds to a **rotation of the flavor axis** from $j$ to $i$, accompanied by the emission of two neutrinos that carry the permutations. The fire and water elements redistribute themselves among the three final products.

---

## Neutrino oscillation: νₑ → νμ

### Pentads

**Electron neutrino**:

$$
P(\nu_e) = \{ iK,\ iJ,\ iI,\ i'j,\ 1k \}
$$

**Muon neutrino**:

$$
P(\nu_\mu) = \{ jK,\ jI,\ jJ,\ i'k,\ 1i \}
$$

### Description

Oscillation is a **continuous rotation of the angles in space**: the preferred axis of the structure gradually shifts from $i$ to $j$. The transition operator is $\exp(i\alpha L_{ji})$, where $\alpha$ is proportional to time and $\Delta m^2$. The oscillation probability is $\sin^2\alpha$, consistent with the standard formula.

---

## Pair production: γ → e⁺ + e⁻

### Pentads

**Photon** (in the presence of an external field):

$$
P(\gamma) = \{ iI,\ iJ,\ iK,\ 0,\ 0 \}
$$

**Electron-positron pair**:

$$
P(e^-) = \{ iI,\ iJ,\ iK,\ i'k,\ 1j \}
$$
$$
P(e^+) = \{ -iI,\ -iJ,\ -iK,\ -i'k,\ -1j \}
$$

### Description

A high-energy photon interacts with an external field (for example, the Coulomb field of a nucleus).
 This field provides the missing orientations (axes $j$, $k$, $i'$) that allow for the **creation of matter**: the water elements $1j$ and $-1j$ as well as the fire elements $i'k$ and $-i'k$ appear, while the photon’s structure splits into two opposing sets. This is the reverse of annihilation.

---

## Summary table of transitions

| Transition | Type | Angular transformation |
|--------------------------------|--------------------|------------------------------------------------------------|
| $n \to p + e^- + \bar{\nu}_e$ | $\beta^-$ | Rotation of the substance angle ($1i \to 1j$) + emission |
| $e^+e^- \to \gamma\gamma$ | Annihilation | Cancellation of opposite angles |
| $pp \to e^+ \nu_e$ | Fusion | Entanglement of angles (with proton transformation) |
| $\mu^- \to e^- \bar{\nu}_e\nu_\mu$ | Decay | Rotation of the flavor axis ($j \to i$) |
| $\nu_e \rightleftarrows \nu_\mu$ | Oscillation | Rotation of angles in space (time-dependent) |
| $\gamma \to e^+e^-$ | Pair production | Creation of matter (water and fire) from angles, assisted by an external field |

---

## Angular Conservation Laws

- **Conservation of the total number of generators**: each element (bivector, fire, water) has a fixed number of generators; the sum is invariant.
- **Conservation of generator type**: $i,j,k,I,J,K$ (and $i'$) are conserved individually, modulo gauge transformations.
- **Conservation of chirality**: linked to the presence of $i'$ in the fire elements.
- **Conservation of total angular momentum**: in angle space, rotations preserve the norm of the angular momentum vector.

---

## Mathematical formalization

Let $\mathcal{H}$ be the Hilbert space of pentads (dimension 72 or 144). A transition operator $T$ acts on tensor products:

$$
\langle P_B \otimes P_C \otimes \cdots | T | P_A \rangle
$$

The transition probability is given by the square of the matrix element.

---

# PENTADIC TRANSITION OPERATOR

## Decomposition

$$
T = T_{\text{structure}} + T_{\text{fire}} + T_{\text{water}} + T_{\text{mixed}}
$$

- $T_{\text{structure}}$ acts on triples of bivectors.
- $T_{\text{fire}}$ acts on the elements $i'v$.
- $T_{\text{water}}$ acts on the elements $1v$.
- $T_{\text{mixed}}$ pairs the different types.

## Compact Expression

In $\text{Cl}(6,0)$, with a basis $\{E_a\}$:

$$
T = \sum_{a,b} g_{ab} (E_a \otimes E_b^*)
$$

For a pentad $P = \{B_1,B_2,B_3,F,S\}$:

$$
|P\rangle = |B_1\rangle \wedge |B_2\rangle \wedge |B_3\rangle \wedge |F\rangle \wedge |S\rangle
$$

$$
T|P\rangle = \sum_{P'} T_{P'P} |P'\rangle,
$$

$$
T_{P'P} = \sum_{\text{cycles}} \prod_{k=1}^5 \langle e'_k | T_{\text{local}} | e_k \rangle
$$

## Selection rules

- Conservation of the number and type of generators.
- Conservation of chirality.
- Pentadic Feynman diagrams.

## Example: β decay

$$
\mathcal{M} = \langle P(p) \otimes P(e^-) \otimes P(\bar{\nu}_e) | T | P(n) \rangle = G_F \, J_{\text{had}} \cdot J_{\text{lep}}
$$

where

$$
J_{\text{had}} = \langle P(p) | T_{\text{struct}} \otimes T_{\text{fire}} | P(n) \rangle,
$$

$$
J_{\text{lep}} = \langle P(e^-) \otimes P(\bar{\nu}_e) | T_{\text{fire}} \otimes T_{\text{water}} |0\rangle.
$$

## Canonical quantization

Operators $a_P$, $a_P^\dagger$ with $[a_P, a_Q^\dagger]_{\mp} = \delta_{PQ}$. The interaction Hamiltonian is a sum of products.

## Angular formulation

The angles $\theta_\mu$ are the generators. $T$ becomes a differential operator:

$$
T = \exp\!\left( i \sum_{i,j} \omega_{ij} L_{ij} \right), \quad L_{ij} = -i(\theta_i \partial_{\theta_j} - \theta_j \partial_{\theta_i})
$$

For the decay $\mu \to e$, the probability is $\sin^2\alpha$, with $\alpha \propto t \Delta m^2/E$.

---

## Toward a complete theory

It remains to:
- Determine the coupling constants from the data.
- Derive the pentadic Feynman rules.
- Calculate the cross sections.
- Predict new processes.

## Conclusion

The operator $T$, defined by a sum over cycles of local matrix elements, provides a coherent mathematical framework for describing all particle transitions as angle rearrangements. This geometric model, inspired by Ummite concepts, unifies interactions and paves the way for a deeper understanding of particle physics.
