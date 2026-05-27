# Week 2: Stokes Flow in FEniCS

## Learning Objectives
- Understand the Stokes equations for incompressible viscous flow.
- Learn mixed finite element methods (velocity-pressure coupling).
- Implement Stokes solver in FEniCS.
- Validate against analytical solutions (Poiseuille, Hagen-Poiseuille).

---

## Lecture 2.1: The Stokes Equations

### Momentum & Continuity

For incompressible Newtonian flow at low Reynolds number:

**Momentum equation:**
$$\rho \frac{\partial \mathbf{u}}{\partial t} + \rho (\mathbf{u} \cdot \nabla) \mathbf{u} = -\nabla p + \mu \nabla^2 \mathbf{u} + \mathbf{f}$$

**Continuity (incompressibility):**
$$\nabla \cdot \mathbf{u} = 0$$

In microfluidics (low Reynolds), we assume **steady state** ($\frac{\partial \mathbf{u}}{\partial t} = 0$) and **Stokes limit** (nonlinear term $\nabla(\mathbf{u} \cdot \mathbf{u}) \ll$ viscous term):

$$-\nabla p + \mu \nabla^2 \mathbf{u} = 0$$
$$\nabla \cdot \mathbf{u} = 0$$

### Why Stokes?

- **Reynolds number:** $\text{Re} = \rho U L / \mu$. In microfluidics, $\text{Re} \ll 1$ (viscous forces dominate).
- **Linear PDEs:** No nonlinearity simplifies numerics and analysis.
- **Time-reversible:** Unique property—if you reverse the velocity field, the flow reverses exactly.

### Boundary Conditions

Common BCs for microfluidic channels:

1. **Dirichlet (no-slip):** $\mathbf{u} = \mathbf{u}_D$ on walls.
2. **Neumann (traction):** $\sigma \mathbf{n} = \mathbf{t}$ at boundaries (e.g., prescribed shear).
3. **Inlet/outlet:** Fixed velocity profile or pressure.

---

## Lecture 2.2: Weak Formulation of Stokes

### The Variational Form

Multiply momentum by test function $\mathbf{v}$, integrate by parts:

$$\int_\Omega \nabla p \cdot \mathbf{v} \, dV + \mu \int_\Omega \nabla^2 \mathbf{u} \cdot \mathbf{v} \, dV = 0$$

After integration by parts:

$$-\int_\Omega p (\nabla \cdot \mathbf{v}) \, dV + \int_\Omega \mu \nabla \mathbf{u} : \nabla \mathbf{v} \, dV + (\text{boundary}) = 0$$

The weak form is: find $(\mathbf{u}, p) \in V \times Q$ such that

$$a(\mathbf{u}, \mathbf{v}) + b(p, \mathbf{v}) = L(\mathbf{v})$$
$$b(q, \mathbf{u}) = 0$$

where:
- $a(\mathbf{u}, \mathbf{v}) = \mu \int_\Omega \nabla \mathbf{u} : \nabla \mathbf{v} \, dV$ (viscous term)
- $b(p, \mathbf{v}) = -\int_\Omega p (\nabla \cdot \mathbf{v}) \, dV$ (pressure coupling)
- $L(\mathbf{v}) = \int_\Omega \mathbf{f} \cdot \mathbf{v} \, dV + (\text{boundary terms})$ (body force, inlet/outlet)

### Mixed Function Spaces

Naively, we might discretize $\mathbf{u}$ and $p$ using the same element type. But this leads to **locking** and spurious pressure modes.

**Solution:** Use mixed elements:
- **Velocity:** higher order (P2 = quadratic on triangles)
- **Pressure:** lower order (P1 = linear on triangles)

This pair, **P2-P1**, satisfies the **LBB (Inf-Sup) stability condition** and avoids locking.

### Why P2-P1?

- P2 has enough DOFs for smooth velocity gradients.
- P1 is "coarse" enough for pressure (no oscillations).
- Roughly equal convergence rates for velocity and pressure.

---

## Lecture 2.3: 1D Poiseuille Flow (Analytical Check)

### Setup

Consider a **2D channel** of width $H$ with fixed inlet pressure $p_0$ and outlet pressure 0:
- Domain: $x \in [0, L]$, $y \in [-H/2, H/2]$
- No-slip on top and bottom: $u_y = 0$, $u_x = 0$ at $y = \pm H/2$
- Pressure gradient: $\frac{dp}{dx} = -\Delta p / L = -p_0 / L$

### Analytical Solution

By symmetry, $u_y = 0$ everywhere, and $u_x(y)$ is parabolic:

$$u_x(y) = \frac{\Delta p}{2 \mu L} \left( H^2/4 - y^2 \right)$$

Maximum velocity at center ($y=0$):
$$u_{\max} = \frac{\Delta p H^2}{8 \mu L}$$

Average velocity:
$$\bar{u} = \frac{2}{3} u_{\max}$$

Volumetric flow rate (per unit depth):
$$Q = \int_{-H/2}^{H/2} u_x(y) \, dy = \frac{\Delta p H^3}{12 \mu L}$$

---

## Lecture 2.4: Boundary Conditions in FEniCS

### No-Slip (Dirichlet)

```python
# Walls: u = 0
def walls(x, on_boundary):
    return on_boundary and (near(x[1], H/2) or near(x[1], -H/2))

bc_wall = DirichletBC(V, (0, 0), walls)
```

### Inlet Pressure (Neumann)

At the inlet, we specify the pressure (or a pressure difference). FEniCS handles this naturally through the RHS.

### Outlet Pressure

Similarly, we can fix $p = 0$ at the outlet using a point constraint or via the problem setup.

---

## Lecture 2.5: Solver Implementation

### Block Form in FEniCS

FEniCS uses block (saddle-point) solvers for mixed problems:

```python
# Define function spaces
V = VectorFunctionSpace(mesh, "P", 2)
Q = FunctionSpace(mesh, "P", 1)
W = V * Q  # Mixed space

# Test and trial
(u, p) = TrialFunctions(W)
(v, q) = TestFunctions(W)

# Bilinear form
a = inner(nabla_grad(u), nabla_grad(v))*dx - div(v)*p*dx - q*div(u)*dx

# Linear form (RHS, inlet pressure, body force, etc.)
L = ...
```

### Solvers

For the saddle-point system, **iterative solvers** like GMRES with appropriate preconditioners are efficient. FEniCS can also use direct solvers (LU) for small problems.

---

## Summary: Stokes in Microfluidics

| Property | Stokes Limit |
|----------|--------------|
| Reynolds number | $\text{Re} \ll 1$ |
| Nonlinear term | Negligible |
| Time-reversibility | Yes |
| Coupling | Velocity ↔ Pressure (saddle-point) |
| Fem choice | Mixed: P2-P1 for velocity-pressure |
| Validation | Poiseuille, Hagen-Poiseuille laws |

---

## Next: Notebooks 2.1 & 2.2

- **Notebook 2.1:** Solve 2D Poiseuille flow in a rectangular channel. Validate against analytical profile.
- **Notebook 2.2:** Add an obstacle (e.g., a cylinder) in the channel. Visualize velocity field and pressure contours.

