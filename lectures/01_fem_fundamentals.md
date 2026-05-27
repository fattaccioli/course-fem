# Week 1: FEM Fundamentals

## Learning Objectives
- Understand the weak formulation of a PDE.
- Learn the finite element discretization and assembly process.
- Implement a simple FEM solver by hand (1D Poisson).
- See why FEM works and how to validate results.

---

## Lecture 1.1: From Strong to Weak Formulation

### The Strong Form

Consider a one-dimensional boundary value problem:
$$-\frac{d^2u}{dx^2} = f(x) \quad \text{in } \Omega = (0, 1)$$

with boundary conditions:
$$u(0) = 0, \quad u(1) = 0$$

The **strong form** requires $u \in C^2(\Omega)$ (twice continuously differentiable). This is restrictive.

### Motivation: Weak Form

If we multiply both sides by a test function $v$ and integrate:
$$\int_0^1 -v \frac{d^2u}{dx^2} \, dx = \int_0^1 v f(x) \, dx$$

Now, **integrate by parts** on the left:
$$\left[ -v \frac{du}{dx} \right]_0^1 + \int_0^1 \frac{dv}{dx} \frac{du}{dx} \, dx = \int_0^1 v f(x) \, dx$$

If we choose $v$ to satisfy the same Dirichlet BC ($v(0) = v(1) = 0$), the boundary term vanishes:
$$\int_0^1 \frac{dv}{dx} \frac{du}{dx} \, dx = \int_0^1 v f(x) \, dx$$

### The Weak Form

We seek $u \in V$ such that
$$a(u, v) = L(v) \quad \forall v \in V$$

where:
- **Bilinear form:** $a(u, v) = \int_0^1 \frac{du}{dx} \frac{dv}{dx} \, dx$
- **Linear functional:** $L(v) = \int_0^1 v f(x) \, dx$
- **Function space:** $V = \{ u \in H^1(0, 1) : u(0) = 0, u(1) = 0 \}$

**Key advantage:** $u \in H^1$ requires only one derivative in an integral sense. Much weaker than $C^2$.

---

## Lecture 1.2: Finite Element Discretization

### Finite-Dimensional Subspace

We can't solve the weak form exactly (infinite-dimensional space). Instead, choose a finite-dimensional subspace $V_h \subset V$ and solve:

$$a(u_h, v_h) = L(v_h) \quad \forall v_h \in V_h$$

### Basis Functions

Let $V_h = \text{span}\{ \phi_1, \phi_2, \ldots, \phi_N \}$, where $\{\phi_i\}$ are **basis functions** (e.g., piecewise linear).

Expand:
$$u_h(x) = \sum_{j=1}^N u_j \phi_j(x)$$

### The Linear System

Substitute $u_h$ into the weak form with $v_h = \phi_i$ for $i = 1, \ldots, N$:
$$\sum_{j=1}^N u_j a(\phi_j, \phi_i) = L(\phi_i)$$

In matrix form:
$$K \mathbf{u} = \mathbf{f}$$

where:
- $K_{ij} = a(\phi_j, \phi_i) = \int_0^1 \phi_j' \phi_i' \, dx$ (stiffness matrix)
- $f_i = L(\phi_i) = \int_0^1 \phi_i f(x) \, dx$ (load vector)
- $\mathbf{u} = [u_1, u_2, \ldots, u_N]^T$ (unknowns)

---

## Lecture 1.3: Assembly

### Element-by-Element Computation

In practice, we don't compute integrals over the entire domain. Instead, partition $\Omega$ into **elements** (e.g., small intervals).

For each element $e$:
1. Map it to a reference element (e.g., $[0, 1]$ in 1D).
2. Compute local basis functions.
3. Compute local stiffness matrix $K^e$ and load vector $f^e$ via quadrature.
4. Assemble into the global matrix.

### Reference Element & Mapping

For a 1D element $e = [x_k, x_{k+1}]$ of length $h_e$, the reference element is $\hat{e} = [0, 1]$.

Linear Lagrange basis functions on $\hat{e}$:
$$\hat{\phi}_1(\xi) = 1 - \xi, \quad \hat{\phi}_2(\xi) = \xi \quad (\xi \in [0, 1])$$

Affine map: $x = x_k + \xi h_e$, so $dx = h_e \, d\xi$.

### Local Stiffness Matrix (1D, P1)

For a single element with two nodes:
$$K^e_{ij} = \int_0^1 \frac{d\hat{\phi}_j}{d\xi} \frac{d\hat{\phi}_i}{d\xi} \frac{1}{h_e} \, d\xi$$

Since $\hat{\phi}_1' = -1$ and $\hat{\phi}_2' = 1$:
$$K^e = \frac{1}{h_e} \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$$

For uniform mesh with $h = 1/n$, this is $K^e = n \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$.

### Assembly

The global stiffness matrix $K$ is formed by summing contributions from all elements, respecting the global node numbering. This is the **assembly** step.

---

## Lecture 1.4: Boundary Conditions & Solving

### Dirichlet Boundary Conditions

Essential BCs (like $u(0) = 0$) are enforced by modifying the linear system:
1. Set rows corresponding to constrained DOFs to identity.
2. Adjust the RHS accordingly.

For example, if $u_1 = 0$ (node at $x=0$), row 1 becomes:
$$K_{1,:} \to [1, 0, 0, \ldots, 0], \quad f_1 \to 0$$

### Solving

Once $K$ and $\mathbf{f}$ are assembled and BCs applied, solve the linear system:
$$\mathbf{u} = K^{-1} \mathbf{f}$$

For small problems, direct solvers (LU) work fine. For large problems, iterative solvers (CG, GMRES) are needed.

---

## Lecture 1.5: Convergence & Validation

### Convergence Theory

For the 1D Poisson problem with P1 elements:
$$\|u - u_h\|_{L^2} = O(h^2), \quad \|u - u_h\|_{H^1} = O(h)$$

where $h$ is the mesh size. **This is the goal:** as we refine the mesh, the FEM solution approaches the exact solution.

### How to Validate

1. **Analytical solution:** If available, compute the $L^2$ error on a sequence of meshes. Plot error vs. $h$ on a log-log plot. Slope should be 2 for $L^2$ norm.

2. **Comparison with known results:** E.g., for Poiseuille flow, compare velocity profiles to Hagen-Poiseuille law.

3. **Conservation checks:** E.g., total flux should be conserved.

---

## Summary of Key Ideas

| Concept | Meaning |
|---------|---------|
| **Strong form** | $-u'' = f$ with $u \in C^2$ |
| **Weak form** | $a(u, v) = L(v)$ with $u \in H^1$ |
| **Finite element space** | Piecewise polynomial approximation (e.g., P1 = piecewise linear) |
| **Assembly** | Building the global stiffness matrix from element contributions |
| **Dirichlet BC** | Enforce by modifying rows of $K$ and $\mathbf{f}$ |
| **Convergence** | Error $\sim h^p$ where $p$ is the element order |

---

## Next Steps

- **Exercise 1:** Implement a 1D Poisson solver by hand (numpy). See `notebooks/01_hand_coded_poisson.ipynb`.
- **Preview:** Week 2 extends these ideas to 2D/3D and vector equations (Stokes flow).

