# Week 3: Electrokinetic Flow & Transport

## Learning Objectives
- Understand electroosmotic flow (EOF) and the Helmholtz-Smoluchowski effect.
- Learn the convection-diffusion equation for scalar transport.
- Implement EOF + tracer transport in FEniCS.
- Validate mixing and concentration profiles.

---

## Lecture 3.1: Electroosmotic Flow (EOF)

### Physical Mechanism

When an electric field $E$ is applied across a charged interface (e.g., glass wall), it induces a flow known as electroosmotic flow.

**Helmholtz-Smoluchowski slip velocity:**
$$u_{\text{slip}} = -\frac{\epsilon \zeta E}{\mu}$$

where:
- $\epsilon$ = permittivity of the fluid
- $\zeta$ = zeta potential of the wall
- $E$ = applied electric field
- $\mu$ = dynamic viscosity

### Why this is useful in microfluidics:
- **Flat velocity profile:** Unlike pressure-driven flow, EOF gives uniform velocity (no-slip at the wall, uniform in bulk).
- **Independent of geometry:** Works in channels of any cross-section.
- **Switchable:** Turn field on/off to control flow instantly.

### Boundary Condition

In the Stokes limit with thin double layer, we model EOF as a **Helmholtz-Smoluchowski slip BC**:

$$\mathbf{u} = u_{\text{slip}} \, \mathbf{t} \quad \text{on walls}$$

where $\mathbf{t}$ is the tangential direction and $u_{\text{slip}}$ is the slip velocity.

---

## Lecture 3.2: Convection-Diffusion Equation

### Transport of a Passive Scalar

Consider a dissolved species (tracer) with concentration $c(x, t)$. In a flowing fluid:

$$\frac{\partial c}{\partial t} + \mathbf{u} \cdot \nabla c = D \nabla^2 c$$

where:
- $D$ = diffusivity (m²/s)
- $\mathbf{u}$ = velocity field (already solved from Stokes)
- First term = time evolution
- Second term = advection (carried by flow)
- RHS = diffusion (spreading due to concentration gradient)

### Steady Transport

If we inject a tracer and wait for steady state:

$$\mathbf{u} \cdot \nabla c = D \nabla^2 c$$

### Peclet Number

The **Peclet number** determines the balance:

$$\text{Pe} = \frac{\text{advection}}{\text{diffusion}} = \frac{U L}{D}$$

where $U$ is typical velocity and $L$ is channel dimension.

- **Pe ≪ 1:** Diffusion dominates → uniform concentration
- **Pe ≫ 1:** Advection dominates → sharp concentration fronts
- Microfluidics: typically Pe ~ 0.1 to 100

---

## Lecture 3.3: Weak Form & FEniCS Implementation

### Variational Formulation (Unsteady)

Multiply by test function $v$, integrate by parts:

$$\int_\Omega v \frac{\partial c}{\partial t} \, dx + \int_\Omega v \mathbf{u} \cdot \nabla c \, dx + D \int_\Omega \nabla v \cdot \nabla c \, dx = 0$$

### Time Integration

Use implicit Euler or Crank-Nicolson for stability. FEniCS can handle this natively.

### Boundary Conditions

Common BCs:
- **Inlet:** $c = c_0$ (Dirichlet)
- **Walls:** $\frac{\partial c}{\partial n} = 0$ (no-flux, Neumann)
- **Outlet:** $\frac{\partial c}{\partial n} = 0$ (outflow)

---

## Lecture 3.4: Mixing Metrics

### Mixing Efficiency

Given inlet concentrations $c_1$ (top) and $c_2$ (bottom), at a cross-section we compute:

$$\text{Unmixedness} = \frac{\int |c(y) - c_{\text{ideal}}|^2 dy}{\int |c_1 - c_2|^2 dy}$$

where $c_{\text{ideal}} = (c_1 + c_2)/2$ is perfect mixing.

- Unmixedness = 1 → completely separated
- Unmixedness = 0 → perfectly mixed

### Mixing Length

How far downstream until the unmixedness falls below a threshold (e.g., 5%)?

---

## Summary

| Concept | Value |
|---------|-------|
| **EOF slip velocity** | $-\epsilon \zeta E / \mu$ |
| **Velocity profile** | Nearly uniform (flat) |
| **Transport equation** | $\frac{\partial c}{\partial t} + \mathbf{u} \cdot \nabla c = D \nabla^2 c$ |
| **Peclet number** | $\text{Pe} = U L / D$ |
| **Stability** | Use implicit time-stepping |

---

## Next: Notebooks 3.1 & 3.2

- **Notebook 3.1:** Solve EOF in a closed channel with Helmholtz-Smoluchowski BC. Compare velocity to analytical.
- **Notebook 3.2:** Solve convection-diffusion with a tracer pulse. Visualize mixing over time.
