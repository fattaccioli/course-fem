# FEM for Microfluidics: A Comprehensive Course

A complete, open-source teaching module introducing finite element method (FEM) concepts through microfluidic applications. Students design circuits in KLayout, mesh with gmsh, and simulate using FEniCS.

## Course Overview

**Level:** Master's students with no prior FEM experience  
**Duration:** 4–6 weeks (~20–30 contact hours for lectures + computational work)  
**Language:** Python, with gmsh scripting  
**Philosophy:** Learn by doing—weak forms → hand-coded assembly → FEniCS → real geometries.

### Learning Objectives

By the end of this course, students will:
1. Understand the weak formulation and finite element discretization of PDEs.
2. Implement a simple FEM solver by hand (assembly, BCs, solving).
3. Use FEniCS to solve coupled multiphysics problems (Stokes, transport, electrokinetics).
4. Design microfluidic geometries in KLayout and translate them into simulations.
5. Visualize and interpret results in ParaView.
6. Apply FEM to pressure-driven flow, electroosmotic flow, and convective-diffusive transport.

---

## Course Structure

### Week 1: FEM Fundamentals
- Lecture 1.1: Weak formulation—from PDE to variational form
- Lecture 1.2: Finite element spaces and assembly
- Computational Exercise 1: Hand-code a 1D Poisson solver

### Week 2: Stokes Flow in FEniCS
- Lecture 2.1: Stokes equations and pressure-velocity coupling
- Lecture 2.2: Mixed finite element spaces (P2-P1)
- Notebook 2.1: Poiseuille flow (2D)
- Notebook 2.2: Flow around an obstacle

### Week 3: Electrokinetic Flow & Transport
- Lecture 3.1: Electroosmotic flow and slip boundaries
- Lecture 3.2: Convection-diffusion equation
- Notebook 3.1: EOF in a closed channel
- Notebook 3.2: Passive tracer mixing

### Week 4: Geometry Pipeline & Integration
- Lecture 4.1: Workflow—KLayout → GDS → gmsh → FEniCS
- Notebook 4.1: Parametric mesh generation (gmsh scripting)
- Notebook 4.2: Simulating a KLayout-designed T-junction

### Week 5: Extensions (Reaction-Diffusion, 3D, Droplets)
- Lecture 5.1: Reaction-diffusion and active transport
- Notebook 5.1: Coupled reaction-diffusion
- Notebook 5.2: 2D to 3D—computational cost and scaling
- [Optional] Notebook 5.3: Simplified droplet advection

---

## Repository Structure

```
fem-microfluidics-course/
├── README.md                          # This file
├── SETUP.md                           # Installation & environment
├── lectures/
│   ├── 01_fem_fundamentals.md         # Week 1 notes
│   ├── 02_stokes_flow.md              # Week 2 notes
│   ├── 03_electrokinetics.md          # Week 3 notes
│   ├── 04_geometry_pipeline.md        # Week 4 notes
│   └── 05_extensions.md               # Week 5 notes
├── notebooks/
│   ├── 01_hand_coded_poisson.ipynb    # 1D Poisson assembly
│   ├── 02_poiseuille_2d.ipynb         # 2D pressure-driven flow
│   ├── 02_obstacle_flow.ipynb         # Flow with obstacle
│   ├── 03_eof_channel.ipynb           # Electroosmotic flow
│   ├── 03_convection_diffusion.ipynb  # Tracer transport
│   ├── 04_parametric_mesh.ipynb       # gmsh scripting
│   ├── 04_klayout_to_fem.ipynb        # Full pipeline example
│   ├── 05_reaction_diffusion.ipynb    # Coupled transport
│   ├── 05_3d_scaling.ipynb            # 2D vs 3D
│   └── 05_droplet_advection.ipynb     # [Optional] Simplified droplets
├── code/
│   ├── utils.py                       # Helper functions (mesh, plotting, etc.)
│   ├── boundary_conditions.py         # Common BC implementations
│   ├── solvers.py                     # Reusable solver kernels
│   └── klayout_interface.py           # KLayout ↔ gmsh translation
├── geometry/
│   ├── channels/
│   │   ├── simple_channel.geo         # gmsh file for a basic channel
│   │   ├── t_junction.geo             # T-mixer geometry
│   │   └── constriction.geo           # Channel with constriction
│   └── examples/
│       └── klayout_export_example.gds # Example GDS from KLayout
├── data/
│   └── analytical_solutions/          # Reference solutions for validation
├── docs/
│   ├── fenics_quick_ref.md            # FEniCS API cheat sheet
│   ├── gmsh_scripting.md              # gmsh geometry scripting guide
│   └── troubleshooting.md             # Common errors & fixes
└── environment.yml                    # Conda environment file

```

---

## Quick Start

### 1. Clone and Install

```bash
git clone <this-repo>
cd fem-microfluidics-course
conda env create -f environment.yml
conda activate fem-microfluidics
```

### 2. Run Your First Simulation

```bash
jupyter notebook notebooks/02_poiseuille_2d.ipynb
```

This will solve 2D Poiseuille flow, plot the velocity field, and compare to analytical solution.

### 3. Create a Mesh

```bash
gmsh geometry/channels/simple_channel.geo -2 -o geometry/channels/simple_channel.msh
```

Then load it in a notebook and simulate.

---

## Key Technologies

| Tool | Purpose | Why |
|------|---------|-----|
| **FEniCS** | PDE solver | Python, clean syntax, great for teaching |
| **gmsh** | Mesh generation | Open-source, scriptable, handles 2D→3D |
| **KLayout** | Circuit design | Standard in microfluidics labs, parametric cells |
| **ParaView** | Visualization | Free, publication-quality plots |
| **Jupyter** | Interactive computing | Narrative + code + results in one place |

---

## Learning Path by Week

### Week 1: Foundation
- **Key concept:** Weak formulation (integration by parts) turns a PDE into a solvable linear system.
- **Exercise:** Assemble the stiffness matrix for 1D Poisson by hand (numpy), solve, validate.
- **Time:** ~5 hours (lecture + hands-on).

### Week 2: Stokes Flow
- **Key concept:** Mixed FEM (velocity + pressure) avoids locking in incompressible flow.
- **Exercise:** Solve 2D Poiseuille, then modify BCs or add an obstacle.
- **Validation:** Compare velocity profiles to Hagen-Poiseuille law.
- **Time:** ~6–8 hours.

### Week 3: Electrokinetics & Transport
- **Key concept:** Helmholtz-Smoluchowski slip makes EOF tractable; transport is decoupled once velocity is known.
- **Exercise:** Solve EOF with a tracer pulse. Watch diffusion smooth the concentration profile.
- **Validation:** Mixing efficiency (concentration variance) as a function of Reynolds number.
- **Time:** ~6–8 hours.

### Week 4: Integration
- **Key concept:** The full pipeline—design in KLayout, mesh parametrically, simulate, visualize.
- **Exercise:** Design a T-mixer in KLayout (or use a template). Export coordinates. Auto-mesh. Simulate mixing.
- **Deliverable:** Jupyter notebook with the full pipeline.
- **Time:** ~4–6 hours.

### Week 5: Extensions
- **Reaction-diffusion:** Add a chemical sink or source term.
- **3D:** Extrude a 2D mesh, compare computational cost.
- **Droplets (optional):** Simplified advection—move a "droplet" interface and solve transport inside/outside.
- **Time:** ~4–8 hours (depending on depth).

---

## Assessment

Students are expected to:
1. **Participate in computational exercises** (formative, no grades).
2. **Complete one full pipeline project** (design → mesh → simulate → report).
3. **Submit a Jupyter notebook** documenting their chosen microfluidic problem.

**Grading rubric (if needed):**
- Correct physics (correct PDE, BCs, parameters).
- Code quality and comments.
- Validation against analytical or published results.
- Clarity of results and interpretation.
- Use of the full pipeline (KLayout or parametric gmsh → FEniCS → ParaView).

---

## Troubleshooting & FAQ

See `docs/troubleshooting.md` for common issues:
- FEniCS import errors
- gmsh meshing fails
- Visualization in ParaView
- Numerical instabilities (Péclet number, CFL condition)

---

## References & Further Reading

### Foundational FEM
- Logg, Mardal, Wells. *Automated Solution of Differential Equations by the Finite Element Method* (FEniCS book, freely available).
- Brenner & Scott. *The Mathematical Theory of Finite Element Methods*.

### Microfluidics & Electrokinetics
- Squires & Quake. "Microfluidics: Fluid physics at the nanoliter scale" (*Rev. Mod. Phys.*, 2005).
- Stone, Stroock, Ajdari. "Engineering flows in small devices: Microfluidics toward a lab-on-a-chip" (*Annu. Rev. Fluid Mech.*, 2004).

### gmsh & Meshing
- gmsh documentation: https://gmsh.info/
- Persson & Strang. "A simple mesh generator in MATLAB" (*SIAM Review*, 2004).

### ParaView
- ParaView user guide: https://www.paraview.org/Wiki/ParaView

---

## Contributing & Feedback

This course is a living document. If you improve a notebook, add an example, or spot an error, please contribute back via pull request or issue.

---

## License

All materials are released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (lectures, notebooks) and [GNU GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html) (code).

---

## Contact & Attribution

**Course design and materials:** [Your name / Lab]  
**Last updated:** [Date]  
**FEniCS:** https://fenicsproject.org/  
**gmsh:** https://gmsh.info/  

---

Enjoy, and happy simulating!
