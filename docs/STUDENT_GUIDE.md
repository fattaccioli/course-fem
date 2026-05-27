# Student Quick-Start Guide

Welcome to the FEM for Microfluidics course! This guide will get you up and running in **10 minutes**.

---

## 1. Clone the Repository

```bash
git clone <course-repo-url>
cd fem-microfluidics-course
```

Or download the ZIP from GitHub and extract it.

---

## 2. Install Dependencies (Choose One)

### Option A: Conda (Recommended, 5 min)

```bash
# Create environment
conda env create -f environment.yml

# Activate
conda activate fem-microfluidics

# Verify
python -c "import fenics; import gmsh; print('✓ Ready!')"
```

### Option B: Docker (If you prefer isolation)

```bash
docker build -t fem-microfluidics .
docker run -p 8888:8888 -v $(pwd):/workspace fem-microfluidics
# Open http://localhost:8888 in browser
```

### Option C: Ask Your Instructor

If you're on a university JupyterHub or shared server, your instructor may have already set this up. Just ask for the link!

---

## 3. Start Jupyter

```bash
jupyter notebook
```

Your browser should open. If not, go to `http://localhost:8888`.

---

## 4. Open Your First Notebook

In Jupyter, navigate to:
```
notebooks/ → 01_hand_coded_poisson.ipynb
```

Click it. Read the instructions. Run the cells (Shift+Enter).

**Expected result:** You should see plots of a 1D solution and convergence study.

---

## 5. Do the Checklist

- [ ] Jupyter is running
- [ ] Can open a notebook
- [ ] Can run a cell (no errors)
- [ ] See plots
- [ ] Understand what the code is doing

If any step fails, see **Troubleshooting** below.

---

## Troubleshooting

### "No module named 'fenics'"

```bash
# Check you activated the environment
conda activate fem-microfluidics

# Or reinstall
conda install -c conda-forge fenics
```

### Jupyter kernel crashes

In Jupyter, go to **Kernel** → **Change kernel** → select `fem-microfluidics`.

Or restart: **Kernel** → **Restart Kernel**.

### gmsh not found

```bash
conda install -c conda-forge gmsh
```

### My plots aren't showing

In Jupyter, add this to the first cell:
```python
%matplotlib inline
```

### Conda takes forever / fails

Try the pip approach:
```bash
pip install fenics gmsh jupyter numpy scipy matplotlib
```

### Still stuck?

1. Check `docs/troubleshooting.md` (more detail)
2. Ask a classmate
3. Ask your instructor

---

## Course Overview

### What You'll Learn (5 Weeks)

| Week | Topic | Notebooks |
|------|-------|-----------|
| 1 | FEM Fundamentals | Hand-code 1D Poisson |
| 2 | Stokes Flow | Solve 2D Poiseuille |
| 3 | Transport & EOF | Mixing, diffusion |
| 4 | Design Pipeline | KLayout → gmsh → FEniCS |
| 5 | Extensions | 3D, reactions, droplets |

### Key Files

- `lectures/` — Detailed notes (read these!)
- `notebooks/` — Hands-on exercises
- `code/utils.py` — Helper functions (you'll use these)
- `geometry/` — Example meshes and designs
- `docs/` — Technical references

---

## Workflow for Each Week

1. **Read the lecture** (`lectures/0X_*.md`)
   - ~30 minutes, grab coffee
2. **Open the notebook** (`notebooks/0X_*.ipynb`)
   - Read the explanations
   - Run the cells
   - Try modifying the code
3. **Experiment**
   - Change parameters (mesh size, inlet pressure, etc.)
   - Plot results
   - Ask: "What happens if…?"
4. **Deliverable** (if assigned)
   - Submit modified notebook or short report

---

## Getting Help

### Before You Ask

1. **Re-read the lecture** — Often the answer is there
2. **Check your code** — Print intermediate results
3. **Search online** — Stack Overflow, FEniCS docs
4. **Try a simpler example** — Debug step-by-step

### When You Ask

1. **Be specific** — "I get an error" is less useful than the actual error message
2. **Show your code** — Paste the relevant lines
3. **Explain what you tried** — Helps us help you faster
4. **Ask in writing** — Email or discussion forum (so others see the answer)

---

## Tips for Success

### Code Style

- **Comment your code** — Future you will thank you
- **Use descriptive names** — `u_solution` not `u`
- **Test incrementally** — Run one cell at a time

### Visualization

- **Always plot results** — A picture is worth 1000 error messages
- **Label axes** — Include units, titles
- **Compare to theory** — Plot analytical solution alongside FEM

### Validation

- **Start coarse, go fine** — Build confidence with a cheap mesh first
- **Check convergence** — Refine mesh, does error shrink as expected?
- **Conserve quantities** — Does divergence of velocity vanish? Is total flux constant?

---

## Keyboard Shortcuts (Jupyter)

| Action | Shortcut |
|--------|----------|
| Run cell | Shift + Enter |
| New cell below | Ctrl + M, B |
| Delete cell | Ctrl + M, X |
| Undo | Ctrl + Z |
| Find/replace | Ctrl + H |

---

## Next Steps

1. **Right now:** Run Notebook 1 (Poisson). You'll get it immediately.
2. **This week:** Finish Notebook 2 (Poiseuille). Understand Stokes.
3. **By end of course:** Design and simulate your own device.

---

## Questions?

- **How long will this take?** 4–6 weeks, ~5 hours/week if you engage
- **Do I need prior FEM experience?** No. We start from scratch.
- **Will there be exams?** No. Focus is on learning and projects.
- **Can I use this for my research?** Yes! That's the whole point.

---

## One More Thing

**Be patient with yourself.** FEM is a different way of thinking about PDEs. It takes time. 

By week 3, you'll realize you're thinking in terms of weak forms and function spaces. That's the payoff.

Good luck, and enjoy! 🚀
