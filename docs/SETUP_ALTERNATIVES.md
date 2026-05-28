# Alternative Setup (If Conda Fails)

If `conda env create -f environment.yml` times out or fails, use these alternatives:

---

## Option A: Fresh Install with pip (Most Reliable)

```bash
# 1. Create a fresh virtual environment
python3.10 -m venv fem-microfluidics
source fem-microfluidics/bin/activate  # On Windows: venv\Scripts\activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install core packages
pip install numpy scipy matplotlib sympy jupyter jupyterlab pandas ipywidgets tqdm

# 4. Install gmsh
pip install gmsh

# 5. Install FEniCS (choose one based on your OS/architecture)

# For most users (Linux/macOS Intel):
pip install fenics-dolfinx

# For macOS ARM64 (Apple Silicon):
pip install fenicsx

# If above fails, try:
pip install --no-build-isolation fenics
```

Test with:
```bash
python -c "import fenics; import gmsh; print('✓ Success!')"
```

---

## Option B: Mamba (Faster Than Conda)

If you have `mamba` installed, use it instead:

```bash
mamba env create -f environment.yml
```

Mamba is usually much faster and more reliable. Install it with:
```bash
conda install -c conda-forge mamba
```

---

## Option C: Pre-built Docker Image

If installation is difficult, use Docker (no dependency issues):

```bash
# Build the image
docker build -t fem-microfluidics .

# Run it
docker run -p 8888:8888 -v $(pwd):/workspace fem-microfluidics
```

Then open: `http://localhost:8888`

---

## Option D: Google Colab (Cloud, No Installation)

Use Google Colab for free cloud Jupyter:

```python
# In a Colab cell, run:
!pip install fenics-dolfinx gmsh jupyter
import fenics
print("✓ Ready!")
```

Upload the `.ipynb` notebooks and run them directly.

---

## Troubleshooting Specific Errors

### "HTTPSConnectionPool timeout"
**Cause:** conda-forge server is slow  
**Solution:** Use Option B (mamba) or C/D (alternatives)

### "No module named 'fenics'"
```bash
# Try the dolfinx version explicitly
pip install fenics-dolfinx --upgrade
```

### "gmsh not found"
```bash
pip install gmsh --upgrade
# Or use conda-forge directly:
conda install -c conda-forge gmsh
```

### "ModuleNotFoundError: No module named 'dolfin'"
Use `fenics_dolfinx` (newer version):
```python
from dolfinx import *
# Instead of:
from dolfin import *
```

### macOS ARM64 (Apple Silicon) Issues
```bash
# Use native conda-forge builds
conda install -c conda-forge python=3.10 numpy scipy matplotlib
pip install fenicsx gmsh jupyter
```

---

## Minimal Working Setup

If everything fails, this bare-bones setup will work:

```bash
pip install numpy scipy matplotlib jupyter gmsh fenics-dolfinx

# That's it. You have:
# ✓ Jupyter notebooks
# ✓ FEniCS for PDE solving
# ✓ gmsh for meshing
# ✓ Plotting (matplotlib)
```

---

## Test Your Installation

Run this to verify everything works:

```python
import numpy as np
import matplotlib.pyplot as plt
from dolfinx import *
import gmsh

print("✓ numpy:", np.__version__)
print("✓ matplotlib:", plt.__version__)
print("✓ gmsh OK")
print("✓ FEniCS OK")
print("\nAll ready for the course!")
```

---

## If You're Still Stuck

1. **Check your internet:** Are you behind a proxy/firewall?
2. **Try a different network:** Use phone hotspot, university network, or coffee shop WiFi
3. **Use Docker:** Sidesteps all installation issues
4. **Use Google Colab:** No installation at all (cloud-based)
5. **Ask your IT department:** They may have pre-configured environments

---

## Contact for Help

If you can't get it working:
- Post error message + full output → someone can help
- Try on a different machine
- Use Option C (Docker) or D (Colab) as fallback

The course works with any of these setups. Pick whichever works for you.

---

**Bottom line:** If conda times out, **use `pip install` (Option A)** — it's usually faster and more reliable.
