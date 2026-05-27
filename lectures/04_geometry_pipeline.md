# Week 4: Geometry Pipeline & Integration

## Learning Objectives
- Understand the full workflow: KLayout → GDS → gmsh → FEniCS.
- Learn parametric mesh generation in gmsh.
- Integrate design and simulation.
- Apply FEM to custom microfluidic geometries.

---

## Lecture 4.1: The Design-to-Simulation Pipeline

### Workflow

```
┌─────────────┐
│  KLayout    │  (1) Design circuit / layout
│  (*.kly)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  GDS Export │  (2) Export to GDS format (industry standard)
│  (*.gds)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Python      │  (3) Parse GDS, extract coordinates
│ Script      │      Build gmsh geometry
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  gmsh       │  (4) Mesh parametrically
│  (*.geo)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  gmsh       │  (5) Generate mesh file
│  (*.msh)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  FEniCS     │  (6) Load, solve, visualize
│  Simulation │
└─────────────┘
```

### Why This Workflow?

- **Separation of concerns:** Design in KLayout (familiar tool), simulation in Python (reproducible).
- **Parametric:** Change dimensions → auto-regenerate mesh → re-run simulation.
- **Version control:** GDS files are vector-based and compact.

---

## Lecture 4.2: From KLayout to gmsh

### Example: T-Junction Mixer

In KLayout, you'd define:
- **Inlet 1:** top branch, width $w_1$, length $L_1$
- **Inlet 2:** bottom branch, width $w_2$, length $L_2$
- **Outlet:** merged channel, width $w_{\text{out}}$, length $L_{\text{out}}$

### Export to GDS

1. **Create cells:** Use parametric cells in KLayout (with parameters for $w$, $L$, angles).
2. **Instance cells:** Place and overlap them to build the T-junction.
3. **Export:** File → Save As → Gzip (*.gds).

The GDS file now contains all polygons and layer information.

### Parse GDS in Python

```python
from gdspy import *

# Load GDS
lib = GdsLibrary(infile="design.gds")

# Extract polygons from a specific cell
cell = lib["MixerCell"]
polygons = cell.get_polygons()

# Polygons are lists of (x, y) vertices
for poly in polygons:
    print(poly)  # e.g., [[0, 0], [10, 0], [10, 5], [0, 5]]
```

### Build gmsh Geometry from Polygons

For each polygon:
1. Create points in gmsh.
2. Create lines connecting them.
3. Create a surface.
4. Mark physical regions (inlets, outlets, walls).

---

## Lecture 4.3: Parametric Mesh Generation

### Simple Example: Parametric Channel with Constriction

```gmsh
// channel_with_constriction.geo

// Parameters
L1 = 0.3;       // Upstream length
L2 = 0.1;       // Constriction length
L3 = 0.3;       // Downstream length

w1 = 0.1;       // Upstream width
w_min = 0.05;   // Minimum (constriction) width
w3 = 0.1;       // Downstream width

lc = 0.01;      // Mesh size

// Upstream section
Point(1) = {0,     -w1/2, 0, lc};
Point(2) = {L1,    -w1/2, 0, lc};
Point(3) = {L1,     w1/2, 0, lc};
Point(4) = {0,      w1/2, 0, lc};

// Constriction section
Point(5) = {L1 + L2, -w_min/2, 0, lc};
Point(6) = {L1 + L2,  w_min/2, 0, lc};

// Downstream section
Point(7) = {L1 + L2 + L3, -w3/2, 0, lc};
Point(8) = {L1 + L2 + L3,  w3/2, 0, lc};

// Build lines and surfaces...
```

**Key idea:** All geometry is driven by parameter values. Change them, regenerate mesh.

---

## Lecture 4.4: Mesh Refinement & Convergence

### Local Refinement

For a constriction or corner, use finer mesh:

```gmsh
// Coarse mesh in upstream
lc_upstream = 0.02;

// Fine mesh in constriction
lc_constriction = 0.005;
```

### Refinement Study

1. Generate meshes with $h = \{0.02, 0.01, 0.005\}$.
2. Solve for each mesh.
3. Compute $L^2$ error (if you have a reference solution).
4. Plot error vs. $h$ → check convergence rate.

---

## Lecture 4.5: Reproducibility & Documentation

### Version Control

Your repository should contain:
- `geometry/` folder with all `.geo` files and `.gds` exports
- `notebooks/` with parameterized meshing scripts
- `code/utils.py` with helper functions

Example structure:
```
geometry/
├── channels/
│   ├── simple_channel.geo
│   ├── constriction.geo
│   └── t_junction.geo
├── klayout_designs/
│   └── mixer_v2.gds
└── exports/
    ├── mixer_v2.geo  (generated from GDS)
    └── mesh_v2.msh
```

### Documenting Assumptions

For each simulation, note:
- **Geometry parameters:** Channel dimensions, aspect ratios.
- **Mesh parameters:** Element size, refinement zones.
- **Physical parameters:** Viscosity, diffusivity, applied field.
- **Boundary conditions:** Inlets, outlets, walls.
- **Solver settings:** Time step, tolerance, solver type.

---

## Summary: Full Pipeline

| Step | Tool | Input | Output |
|------|------|-------|--------|
| 1 | KLayout | Design concept | `.kly` file |
| 2 | KLayout | Cell definitions | `.gds` file |
| 3 | Python + gdspy | `.gds` file | Polygon list |
| 4 | Python + gmsh API | Polygons + params | `.geo` file |
| 5 | gmsh | `.geo` file | `.msh` file |
| 6 | FEniCS | `.msh` file | Simulation results |
| 7 | ParaView | `.pvd` output | Publication plots |

---

## Next: Notebooks 4.1 & 4.2

- **Notebook 4.1:** Parametric mesh generation in gmsh (scripting tutorial).
- **Notebook 4.2:** Full pipeline example: Design a T-mixer in KLayout, export GDS, auto-mesh, simulate mixing.

