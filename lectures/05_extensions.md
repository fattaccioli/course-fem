# Week 5: Extensions – Reaction-Diffusion, 3D Scaling, Droplet Advection

## Learning Objectives
- Extend scalar transport to coupled reaction-diffusion.
- Scale simulations from 2D to 3D and understand computational costs.
- Introduce simplified droplet advection (optional, advanced).

---

## Lecture 5.1: Reaction-Diffusion Transport

### Adding Chemistry

The convection-diffusion equation can include reactive terms:

$$\frac{\partial c}{\partial t} + \mathbf{u} \cdot \nabla c = D \nabla^2 c + R(c)$$

where $R(c)$ is a **reaction term** (sink/source).

### Examples

**First-order degradation:**
$$R(c) = -k c$$

where $k$ is the rate constant (s⁻¹). The species decays exponentially.

**Bimolecular reaction:**
$$\frac{\partial c_A}{\partial t} + \mathbf{u} \cdot \nabla c_A = D_A \nabla^2 c_A - k c_A c_B$$

$$\frac{\partial c_B}{\partial t} + \mathbf{u} \cdot \nabla c_B = D_B \nabla^2 c_B - k c_A c_B$$

Two species interact with rate constant $k$.

### Weak Form (First-Order)

$$\int_\Omega v \frac{\partial c}{\partial t} dx + \int_\Omega v \mathbf{u} \cdot \nabla c \, dx + D \int_\Omega \nabla v \cdot \nabla c \, dx + \int_\Omega v k c \, dx = 0$$

The reaction term simply adds another integral.

### Time Integration & Stability

For the ODE $\frac{dc}{dt} = -kc$ (pure decay), the analytical solution is $c(t) = c_0 e^{-kt}$.

With implicit Euler (backward difference):
$$c^{n+1} = \frac{1 + \Delta t \, k} c^n$$

This is **unconditionally stable**. Good for reaction-dominated problems.

---

## Lecture 5.2: Scaling from 2D to 3D

### Computational Cost

For a 2D problem with $n$ elements per direction:
- Total elements: $\sim n^2$
- DOFs: $\sim n^2$
- Assembly: $O(n^2)$
- Solve (direct): $O(n^6)$; (iterative): $O(n^{2.5})$ with good preconditioner

For 3D:
- Total elements: $\sim n^3$
- DOFs: $\sim n^3$
- Assembly: $O(n^3)$
- Solve: $O(n^{9})$ (direct) or $O(n^{3.5})$ (iterative)

**Example:** If a 2D problem takes 1 second, a 3D version (same relative mesh density) takes ~100× longer.

### Practical Approach

1. **Solve 2D fully** to develop and validate.
2. **Extrude to 3D** as a sanity check (coarse mesh first).
3. **Use iterative solvers** for 3D (not direct LU).
4. **Exploit symmetry:** If the problem is 2D + extrusion, maybe 2D is enough.

### Example: Hele-Shaw vs. Full 3D

For a shallow channel, the **Hele-Shaw approximation** (velocity averaged in the $z$-direction) often gives good results at 1/10 the cost of full 3D.

---

## Lecture 5.3: Mesh Extrusion

### From 2D to 3D Using gmsh

If you have a 2D mesh in gmsh:

```gmsh
// 2D mesh (channels, obstacles, etc.)
...
// After defining surfaces and meshing:

Mesh.Generate(2);  // Generate 2D mesh

// Extrude vertically
out[] = Extrude {0, 0, depth} { Surface{1}; Layers{nlayers}; };

// out[0] = extruded volume
// out[1] = top surface
// out[2:n] = side surfaces
```

**nlayers:** Number of layers in the extrusion. Use ~10–20 for adequate resolution.

### Python/FEniCS Alternative

Load a 2D mesh, extrude programmatically:

```python
from fenics import *

# Load 2D mesh
mesh_2d = Mesh("channel_2d.msh")

# Extrude (simple method)
mesh_3d = Mesh()
# ... (use specialization or manual extrusion)
```

FEniCS doesn't have built-in extrusion; gmsh is easier.

---

## Lecture 5.4: Simplified Droplet Advection (Optional)

### Motivation

In **droplet microfluidics**, solute can be transported inside a droplet via advection + diffusion. A full simulation requires:
- Interface tracking (complex)
- Two-phase Navier-Stokes (expensive)

### Simplified Model

Instead:
1. Solve Stokes for the **surrounding fluid** (external phase).
2. Assume the **droplet is a moving rigid body** (no deformation).
3. Advect the droplet interface using the external velocity.
4. Solve convection-diffusion **inside the droplet** separately.

### Implementation Steps

**Step 1:** Solve Stokes for external flow (e.g., Poiseuille).

**Step 2:** At time $t$, the droplet interface is at position $(x_0 + \int_0^t u_{ext}(x_0, s) ds, y_{\text{droplet}})$.

**Step 3:** Inside the droplet, solve:
$$\frac{\partial c}{\partial t} + \mathbf{u}_{\text{droplet}} \cdot \nabla c = D \nabla^2 c$$

where $\mathbf{u}_{\text{droplet}}$ is a Marangoni flow (shear-induced) or just internal recirculation.

**Step 4:** For a rigid sphere, the internal flow can be approximated analytically (Hill vortex).

### Limitations

- Assumes droplet doesn't deform (valid for high surface tension).
- Ignores coalescence.
- 2D droplet (circle) is unrealistic; 3D spherical droplets are better.

### When to use this model

- Quick screening of designs.
- Teaching tool (shows how to couple different physics).
- Cases where full two-phase simulation is too expensive.

---

## Lecture 5.5: Practical Advice for Extensions

### Choosing Your Extension

**If you want reaction-diffusion:**
- Good for: enzymatic assays, chemical kinetics, mixing-controlled reactions.
- Start with: first-order decay, then generalize.

**If you want 3D:**
- Good for: validating 2D assumptions, accurate volume/flux calculations.
- Start with: extrude a 2D mesh, use coarse resolution.

**If you want droplets:**
- Good for: understanding internal mixing, transport in droplet-based assays.
- Start with: simplified advection (this lecture), not full interface tracking.

### Convergence in Complex Cases

1. **Grid convergence:** Refine mesh, check if results stabilize.
2. **Time convergence (unsteady):** Halve time step, check if results change <5%.
3. **Parametric convergence:** If you added a new physics (reaction rate, droplet size), vary it and confirm sensitivity.

---

## Summary: Extension Toolkit

| Extension | Complexity | Payoff | Use When |
|-----------|------------|--------|----------|
| **Reaction-diffusion** | Low | High | Studying mixing-limited reactions |
| **3D** | Medium | Medium | Validating 2D; accurate 3D metrics |
| **Droplets (simplified)** | Medium | Medium | Quick screening; teaching |
| **Droplets (full)** | Very High | High | Production simulations (expensive) |

---

## Next: Notebooks 5.1, 5.2, 5.3

- **Notebook 5.1:** Reaction-diffusion: add first-order decay to convection-diffusion.
- **Notebook 5.2:** 2D → 3D: extrude a channel, compare computational time.
- **Notebook 5.3 (optional):** Simplified droplet advection in a pressure-driven flow.

