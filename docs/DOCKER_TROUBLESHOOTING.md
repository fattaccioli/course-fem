# Docker Issues & Solutions

## "Segmentation Fault" During Build

This typically means Docker ran out of memory or hit a resource limit.

### Quick Fixes (Try in Order)

#### 1. Increase Docker Memory (BEST FIX)

**macOS (Docker Desktop):**
```
Docker Desktop → Preferences → Resources → Memory
Increase to at least 4GB (8GB recommended)
```

**Linux:**
```bash
# Check current memory
docker info | grep Memory

# Build with memory limit (if too low)
docker build --memory=4g -t fem-microfluidics .
```

**Windows (Docker Desktop):**
```
Settings → Resources → Memory
Increase to at least 4GB
```

#### 2. Use the Updated Lightweight Dockerfile

The new Dockerfile is much simpler and uses less memory:

```bash
docker build -t fem-microfluidics .
```

If it still fails, try with explicit memory:
```bash
docker build --memory=4g -t fem-microfluidics .
```

#### 3. Clean Docker Cache

```bash
# Remove unused images/containers
docker system prune -a --volumes

# Then rebuild
docker build -t fem-microfluidics .
```

#### 4. Build with Verbose Output

```bash
docker build --progress=plain -t fem-microfluidics . 2>&1 | tail -50
```

This shows exactly where it fails.

---

## If Docker Still Doesn't Work

**Use pip instead** (recommended):

```bash
python3 -m venv fem-microfluidics
source fem-microfluidics/bin/activate
pip install numpy scipy matplotlib jupyter gmsh fenics-dolfinx
jupyter notebook
```

This is faster, simpler, and avoids all Docker issues.

---

## Running Docker (If Build Succeeds)

```bash
# Run the container
docker run -p 8888:8888 -v $(pwd):/workspace fem-microfluidics

# On Windows, use:
docker run -p 8888:8888 -v %cd%:/workspace fem-microfluidics

# Then open: http://localhost:8888
```

Get the Jupyter token from the console output and paste it.

---

## Docker Resource Limits

### Check Your System

```bash
# macOS/Linux
docker stats

# Windows (in PowerShell)
docker stats
```

Watch the memory usage. If it spikes and crashes, you hit the limit.

### Recommended Resources for Docker

| Component | Minimum | Recommended |
|-----------|---------|------------|
| Memory | 2 GB | 4-8 GB |
| Disk | 5 GB | 20 GB |
| CPU Cores | 2 | 4+ |

---

## Alternative: Use Pre-built Image

If you have internet access, use a pre-built Docker image:

```bash
# Instead of building, use existing image
docker run -p 8888:8888 -v $(pwd):/workspace \
  --name fem-jupyter \
  jupyter/scipy-notebook

# Then install FEniCS manually inside:
# docker exec fem-jupyter pip install fenics-dolfinx gmsh
```

---

## Still Stuck?

### Option 1: Use pip (Easiest)
```bash
python3 -m venv fem-microfluidics
source fem-microfluidics/bin/activate
pip install numpy scipy matplotlib jupyter gmsh fenics-dolfinx
jupyter notebook
```

### Option 2: Use Google Colab (No Installation)
```
1. Go to https://colab.research.google.com
2. Create new notebook
3. Run: !pip install fenics-dolfinx gmsh
4. Upload the course notebooks
5. Run them in the cloud
```

### Option 3: Use University JupyterHub
Ask your IT department if they have a shared JupyterHub—it may already have everything installed.

---

## Key Takeaway

**Docker can have resource issues. If it segfaults:**
1. ✓ Increase memory (most common fix)
2. ✓ Try pip instead (faster, simpler)
3. ✓ Use Colab (cloud, no setup)

The course works with any installation method. Pick what works best for your system.

---

## Questions?

See the main guides:
- `SETUP.md` — Installation overview
- `SETUP_ALTERNATIVES.md` — All options
- `CONDA_TIMEOUT_FIX.md` — Network issues

Or try pip—it almost always works. 🚀
