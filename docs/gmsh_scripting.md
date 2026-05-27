# gmsh Scripting Guide

A quick reference for parametric mesh generation in gmsh.

## Basic Workflow

```
gmsh script.geo -2 -o mesh.msh    # Generate 2D mesh
gmsh script.geo -3 -o mesh.msh    # Generate 3D mesh
```

## Minimal Example: Rectangular Channel

```gmsh
// Channel.geo: Simple rectangular channel

// Parameters
lc = 0.01;      // Characteristic length (controls mesh density)
L = 1.0;        // Length
H = 0.1;        // Height

// Define corners
Point(1) = {0,    -H/2, 0, lc};    // Bottom-left
Point(2) = {L,    -H/2, 0, lc};    // Bottom-right
Point(3) = {L,     H/2, 0, lc};    // Top-right
Point(4) = {0,     H/2, 0, lc};    // Top-left

// Define edges
Line(1) = {1, 2};    // Bottom
Line(2) = {2, 3};    // Right
Line(3) = {3, 4};    // Top
Line(4) = {4, 1};    // Left

// Define surface (closed loop)
Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

// Define physical regions (for boundary conditions)
Physical Curve("inlet", 10) = {4};      // Left edge
Physical Curve("outlet", 20) = {2};     // Right edge
Physical Curve("wall", 30) = {1, 3};    // Top and bottom

Physical Surface("fluid", 100) = {1};   // Interior
```

## Key Concepts

### Points
```gmsh
Point(tag) = {x, y, z, lc};
```
- `tag`: unique identifier
- `{x, y, z}`: coordinates
- `lc`: mesh size at this point (smaller → finer mesh)

### Curves (Lines)
```gmsh
Line(tag) = {P1, P2};           // Straight line
Spline(tag) = {P1, P2, ...};    // Smooth spline
```

### Surfaces
```gmsh
Curve Loop(tag) = {L1, L2, L3, L4};  // Define boundary
Plane Surface(tag) = {Curve Loop tag};
```

**Note:** Curve signs matter: positive or negative determines orientation.

### Physical Regions (for BC application)
```gmsh
Physical Curve("name", tag) = {L1, L2, ...};
Physical Surface("name", tag) = {S1, S2, ...};
```

These allow you to tag regions for FEniCS boundary conditions.

## Parametric Geometry: T-Junction Example

```gmsh
// T_junction.geo

lc = 0.005;
w = 0.1;        // Channel width
h = 0.05;       // Branch height
L_main = 1.0;   // Main channel length
L_branch = 0.3; // Branch length

// Main channel
Point(1)  = {0,      -w/2, 0, lc};
Point(2)  = {L_main, -w/2, 0, lc};
Point(3)  = {L_main,  w/2, 0, lc};
Point(4)  = {0,       w/2, 0, lc};

// Branch junction point
x_branch = L_main / 2;

Point(5)  = {x_branch, w/2, 0, lc};          // Where branch leaves main
Point(6)  = {x_branch, w/2 + L_branch, 0, lc}; // End of branch

// Lines for main channel
Line(1) = {1, 2};  // Bottom inlet
Line(2) = {2, 3};  // Outlet
Line(3) = {3, 5};  // Top, inlet to junction
Line(4) = {5, 6};  // Branch
Line(5) = {6, 5};  // Branch return (oops, this is wrong)
...
```

**Better approach:** Use Gmsh's extrusion to build from 1D curves.

## Meshing Strategy: From Curves to Surfaces

For complex shapes, build incrementally:

1. **Define points** → corners, junctions
2. **Define curves** → boundaries
3. **Define loops** → closed regions
4. **Define surfaces** → fill regions
5. **Tag physically** → for FEniCS

Example:
```gmsh
// Build a channel with an embedded circle (obstacle)

// Outer rectangle
...
Plane Surface(1) = {Outer Loop};

// Circle at center
Point(101) = {x_center, y_center, 0, lc_fine};
Circle(101) = {P_left, P_center, P_right};
...
Plane Surface(2) = {Inner Loop};

// Subtract: Surface = outer \ inner
Plane Surface(3) = {1, -2};  // Negative sign = hole
```

## Mesh Refinement

### Uniform refinement
```gmsh
Mesh.CharacteristicLengthFactor = 2.0;  // Halve all element sizes
```

### Local refinement
```gmsh
// Refine near a point
Point(101) = {x, y, z, lc_fine};  // Small lc near this point
```

### Field-based refinement (advanced)
```gmsh
Field[1] = Distance;
Field[1].Sampling = 1000;
Field[1].VertexSemi = {102};

Field[2] = MathEval;
Field[2].F = "0.001 + 0.01 * F1";

Background Field = 2;
```

## 3D Extrusion from 2D

```gmsh
// Extrude a 2D surface to 3D
out[] = Extrude {0, 0, depth} { Surface{1}; };

// out[0] = new 3D volume
// out[1] = top surface
// out[2:5] = side surfaces
```

## Common Mistakes

1. **Inconsistent orientation:** Make sure curve loops are consistently oriented (right-hand rule).
2. **Overlapping points:** Always reuse point tags, don't create duplicates at the same location.
3. **Missing physical tags:** If you don't tag regions, FEniCS can't apply BCs there.
4. **lc too coarse:** If mesh elements are too large, numerical errors increase. Start with smaller lc.

## Checking Your Mesh

```bash
# Visualize in gmsh GUI
gmsh channel.geo

# Or convert to other formats
gmsh channel.geo -2 -format msh2 -o mesh.msh
gmsh channel.geo -2 -format vtk -o mesh.vtk
```

## FEniCS Integration

Once you have `mesh.msh`, load it in Python:

```python
from fenics import *

mesh = Mesh("mesh.msh")
boundaries = MeshFunction("size_t", mesh, 1, mesh.domains())

# Now use physical region tags:
bc = DirichletBC(V, u_val, boundaries, 10)  # Tag 10 = "inlet"
```

## Advanced: Parametric Script

```python
# channel_mesh.py: Generate mesh from Python

import gmsh

def create_channel_mesh(length, height, mesh_size, filename="channel.msh"):
    gmsh.initialize()
    gmsh.model.add("channel")
    
    # Create geometry
    lc = mesh_size
    gmsh.model.geo.addPoint(0, -height/2, 0, lc, 1)
    gmsh.model.geo.addPoint(length, -height/2, 0, lc, 2)
    gmsh.model.geo.addPoint(length, height/2, 0, lc, 3)
    gmsh.model.geo.addPoint(0, height/2, 0, lc, 4)
    
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(2, 3, 2)
    gmsh.model.geo.addLine(3, 4, 3)
    gmsh.model.geo.addLine(4, 1, 4)
    
    gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)
    
    gmsh.model.geo.synchronize()
    
    # Mesh and save
    gmsh.model.mesh.generate(2)
    gmsh.write(filename)
    gmsh.finalize()

# Usage
create_channel_mesh(length=1.0, height=0.1, mesh_size=0.01)
```

## References

- Official gmsh documentation: https://gmsh.info/doc/texinfo/gmsh.html
- Gmsh scripting API (Python): https://gmsh.info/doc/api/gmsh.html

