# Setup & Installation Guide

This guide will get you from zero to running your first FEM simulation in ~10 minutes.

## Prerequisites

- **OS:** macOS, Linux, or Windows (WSL2)
- **Python:** 3.9+
- **Git:** for cloning the repo
- **Conda:** recommended (Miniconda or Anaconda)

## Option 1: Conda (Recommended, but can timeout on slow networks)

Conda packages FEniCS and gmsh together, avoiding build headaches.

⚠️ **Note:** If you get timeout errors, see **Option 2 (pip)** or **Option 3 (Docker)** below.

### 1.1 Create and activate environment

```bash
# Clone the repo
git clone <this-repo>
cd fem-microfluidics-course

# Create the environment (includes FEniCS, gmsh, jupyter, matplotlib, etc.)
conda env create -f environment.yml

# Activate
conda activate fem-microfluidics

# Verify installation
python -c "import fenics; print(fenics.__version__)"
python -c "import gmsh; print(gmsh.GMSH_API_VERSION)"
```

You should see version numbers for both.

### 1.2 Start Jupyter

```bash
jupyter notebook
```

Open a notebook from the `notebooks/` directory.

---

## Option 2: pip + Manual Installation (Advanced)

If you prefer pip or need a specific version:

```bash
# Create a fresh Python 3.9+ virtual environment
python3.9 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install core packages
pip install fenics dolfin gmsh jupyter numpy scipy matplotlib sympy

# Optional: for postprocessing
pip install meshio paraview
```

**Note:** FEniCS via pip can be finicky on some systems. Conda is more reliable.

---

## Option 3: Docker

If you want a fully isolated environment:

```bash
docker build -t fem-microfluidics .
docker run -p 8888:8888 -v $(pwd):/workspace fem-microfluidics
```

⚠️ **Note:** Docker build may segfault if you're low on memory. **Increase Docker memory to 4GB or use Option 1/2 (pip) instead.** See `docs/DOCKER_TROUBLESHOOTING.md` for details.

---

## Verify Your Installation

Run this quick test to ensure everything works:

```python
# test_install.py
from dolfin import *
import gmsh

# Test 1: FEniCS
mesh = UnitSquareMesh(10, 10)
V = FunctionSpace(mesh, "P", 1)
print(f"FEniCS OK: mesh has {mesh.num_cells()} cells")

# Test 2: gmsh
gmsh.initialize()
gmsh.model.add("test")
gmsh.model.geo.addPoint(0, 0, 0, 1.0, 1)
gmsh.model.geo.addPoint(1, 0, 0, 1.0, 2)
gmsh.model.geo.addLine(1, 2, 1)
print(f"gmsh OK: initialized API version {gmsh.GMSH_API_VERSION}")
gmsh.finalize()
```

Run with:
```bash
python test_install.py
```

Expected output:
```
FEniCS OK: mesh has 200 cells
gmsh OK: initialized API version X.X.X
```

---

## Conda Environment File (`environment.yml`)

If you want to understand what's installed:

```yaml
name: fem-microfluidics
channels:
  - conda-forge
dependencies:
  - python=3.10
  - fenics::fenics
  - gmsh
  - jupyter
  - jupyterlab
  - numpy
  - scipy
  - matplotlib
  - sympy
  - meshio
  - pip
  - pip:
    - pandas
    - ipywidgets
    - tqdm
```

---

## Common Issues & Fixes

### Issue 1: "No module named 'fenics'"

**Solution:**
```bash
conda activate fem-microfluidics
python -m pip install --upgrade fenics
```

Or ensure you're using the conda-forge channel:
```bash
conda install -c conda-forge fenics
```

### Issue 2: gmsh not found in Jupyter

**Cause:** Jupyter kernel is using the wrong Python.

**Solution:**
```bash
# Register the conda env as a Jupyter kernel
conda activate fem-microfluidics
python -m ipykernel install --user --name fem-microfluidics --display-name "FEM-Microfluidics"
```

Then in Jupyter, go to **Kernel** → **Change kernel** → select `fem-microfluidics`.

### Issue 3: "Could not find Gmsh executable"

**Cause:** gmsh not in PATH.

**Solution:**
```bash
# Find it
python -c "import gmsh; print(gmsh.__file__)"

# Or reinstall
conda remove gmsh
conda install -c conda-forge gmsh
```

### Issue 4: FEniCS import succeeds, but dolfin fails

**Cause:** You're importing `dolfin` instead of `fenics`.

**Solution:**
```python
# Correct
from fenics import *
# or
import dolfin

# Not this (unless you know what you're doing)
from dolfin import *
```

### Issue 5: Jupyter kernel crashes when importing FEniCS

**Cause:** Sometimes happens with Jupyter Lab and conda-forge FEniCS.

**Solution:**
Switch to Jupyter Notebook:
```bash
jupyter notebook  # instead of jupyter lab
```

---

## Optional: ParaView for Visualization

For high-quality plots, install ParaView:

```bash
# Conda
conda install -c conda-forge paraview

# Or download from https://www.paraview.org/download/
```

Then, in your notebooks:
```python
from fenics import *
# ... run simulation ...
File("solution.pvd") << u  # Write to .pvd (ParaView format)
```

Open `solution.pvd` in ParaView GUI.

---

## Updating Your Environment

If you make changes to `environment.yml`:

```bash
conda env update --file environment.yml --prune
```

---

## Network/Timeout Issues?

If you see errors like:
```
ReadTimeoutError("HTTPSConnectionPool... Read timed out")
```

**See `docs/SETUP_ALTERNATIVES.md`** for:
- ✓ Faster pip-only installation
- ✓ Mamba (faster than conda)
- ✓ Docker (no dependency headaches)
- ✓ Google Colab (cloud, no setup)

The pip option usually works much faster!
