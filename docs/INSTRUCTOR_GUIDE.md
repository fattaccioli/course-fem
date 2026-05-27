# Implementation Guide for Instructors

This document provides guidance on how to deploy and customize the FEM microfluidics course for your students.

---

## Quick Overview

You now have a complete, ready-to-run course repository containing:

- **5 weeks of lecture notes** (detailed, derivations included)
- **2 fully worked notebooks** as starting examples
- **Utility library** for common FEM tasks
- **5 geometry/meshing files** as templates
- **Full documentation** on setup, troubleshooting, and the complete pipeline

**Total preparation time:** ~30 minutes to deploy; ~2 hours to customize for your context.

---

## Step 1: Deploy to Your Institution

### Option A: GitHub (Recommended)

```bash
cd /path/to/your/institution/courses
git clone <this-repo-url> fem-microfluidics
cd fem-microfluidics
# Tell students: "Clone this repo and run SETUP.md"
```

### Option B: Local Server / JupyterHub

If your institution runs a shared JupyterHub:

```bash
# On the server
git clone <this-repo-url> /opt/jupyterhub/fem-microfluidics

# Students access via browser
# http://jupyterhub.youruni.edu/user/[username]/lab/tree/fem-microfluidics
```

### Option C: Docker Container (Most Isolated)

```bash
# Build the image
docker build -t fem-microfluidics .

# Run for a student
docker run -p 8888:8888 \
  -v /path/to/fem-microfluidics:/workspace \
  fem-microfluidics
```

Students access Jupyter at `localhost:8888`.

---

## Step 2: Customize for Your Course Context

### Adjust Duration

**6-week module (30 contact hours):**
- Week 1: 4 hours lecture + 3 hours hands-on
- Week 2: 4 hours lecture + 3 hours hands-on
- Week 3: 4 hours lecture + 3 hours hands-on
- Week 4: 3 hours lecture + 2 hours hands-on
- Week 5: 2 hours lecture + 2 hours hands-on (extensions)

**4-week intensive (20 contact hours):**
- Week 1: Compress fundamentals (2 hours lecture, 2 hours exercise)
- Week 2: Stokes + EOF together (3 hours + 2 hours)
- Week 3: Geometry pipeline (2 hours + 3 hours)
- Week 4: Project work (individual)

### Assign a Project

**Option 1: Open-Ended** (Week 5)
- Design a microfluidic device (pressure-driven or electrokinetic)
- Simulate it (2D minimum, 3D bonus)
- Write a short report (3–5 pages)

**Option 2: Guided Problem Sets**
- Provide 3–4 template notebooks with missing code
- Students fill in the weak form, boundary conditions, or post-processing
- Progressive difficulty

**Option 3: Literature Review + Simulation**
- Students read a paper on microfluidics
- Reproduce one key result using FEM

### Add Your Own Physics

The repository is built to be extended. If you want to add:

**Custom boundary conditions:**
→ Edit `code/boundary_conditions.py` (placeholder file)

**New solvers:**
→ Add to `code/solvers.py`

**Additional geometries:**
→ Create new `.geo` files in `geometry/`

**New notebooks:**
→ Use `notebooks/02_poiseuille_2d.ipynb` as a template

---

## Step 3: First Run Checklist

- [ ] Clone the repo
- [ ] Run `conda env create -f environment.yml` (test on your machine first)
- [ ] Open `notebooks/01_hand_coded_poisson.ipynb` and run all cells
- [ ] Try `gmsh geometry/channels/simple_channel.geo -2 -o test.msh` (generates a mesh)
- [ ] Open `notebooks/02_poiseuille_2d.ipynb` and run all cells
- [ ] Verify no errors and all plots appear

**Troubleshooting:** See `docs/troubleshooting.md` (create if needed).

---

## Step 4: Suggested Lecture Schedule (4–6 Weeks)

### Week 1: Foundations (6 hours)

**Lecture 1a (2h):** Read `lectures/01_fem_fundamentals.md`
- Weak formulation, discretization, assembly
- Boundary conditions
- *End goal: students understand how FEM works conceptually*

**Exercise 1 (2h, hands-on):** Open `notebooks/01_hand_coded_poisson.ipynb`
- Walk through hand-coded 1D Poisson
- Students modify the source function, observe convergence
- **Deliverable:** convergence plot (email or submit)

**Lecture 1b (1h):** Numerical validation
- Error metrics, convergence rates
- When to trust FEM results

**Homework (1h):** Reading
- Optional: Logg et al. FEniCS book, Chapter 1 (available free online)

---

### Week 2: Stokes Flow (6 hours)

**Lecture 2a (2h):** `lectures/02_stokes_flow.md`
- Stokes equations for low-Re flow
- Mixed FEM (P2-P1), why it matters
- Boundary conditions for microfluidics

**Exercise 2a (1.5h):** `notebooks/02_poiseuille_2d.ipynb`
- Students run the Poiseuille solver
- Modify inlet pressure, measure flow rate change
- Compare velocity profiles to analytical formula

**Lecture 2b (1.5h):** Advanced BC
- Pressure inlets/outlets
- Slip boundary conditions (preview for EOF)

**Exercise 2b (1h):** Extend Poiseuille
- Add a cylindrical obstacle in the channel
- Visualize velocity around the obstacle
- (Notebook template: `02_obstacle_flow.ipynb` — you'll write this)

---

### Week 3: Electrokinetics & Transport (6 hours)

**Lecture 3a (1.5h):** `lectures/03_electrokinetics.md`
- Electroosmotic flow physics
- Helmholtz-Smoluchowski BC

**Exercise 3a (1.5h):** EOF simulation
- Set up EOF in a channel
- Compare velocity profile to analytical (should be flat!)
- (Notebook: `03_eof_channel.ipynb` — you'll write this)

**Lecture 3b (1.5h):** Convection-diffusion
- Transport equation, Peclet number
- Time-stepping, stability

**Exercise 3b (1.5h):** Mixing simulation
- Inject tracer at inlet, watch it spread
- Measure mixing efficiency
- (Notebook: `03_convection_diffusion.ipynb` — you'll write this)

---

### Week 4: Integration & Design (5 hours)

**Lecture 4 (2h):** `lectures/04_geometry_pipeline.md`
- KLayout → GDS → gmsh → FEniCS workflow
- Parametric geometry in gmsh

**Exercise 4 (2h):** Design your own
- Students sketch a simple device in KLayout (or use template)
- Export to GDS
- Write a Python script to convert GDS → gmsh geometry
- Mesh and load in FEniCS
- (Notebook: `04_klayout_to_fem.ipynb` — you'll provide template)

**Wrap-up (1h):** Project assignment
- Hand out project specification
- Answer questions

---

### Week 5: Extensions & Projects (Varies)

**Lecture 5a (1h, optional):** `lectures/05_extensions.md`
- Reaction-diffusion, 3D scaling, droplets

**Exercise 5a (1.5h, optional):** Advanced
- First-order decay in transport
- (Notebook: `05_reaction_diffusion.ipynb`)

**Project Work (2–3h):** Students work on final project
- May be individual or pairs
- Instructor available for questions

**Presentations (1–2h, if graded):** Final presentations or written reports

---

## Step 5: Notebooks You'll Need to Write

The repository includes 2 complete notebooks. For a full course, you'll want to add:

- [ ] `03_eof_channel.ipynb` — EOF simulation (copy/modify `02_poiseuille_2d.ipynb`, change BC)
- [ ] `03_convection_diffusion.ipynb` — Tracer transport (new weak form, time-stepping)
- [ ] `04_parametric_mesh.ipynb` — gmsh scripting tutorial
- [ ] `04_klayout_to_fem.ipynb` — Full pipeline example
- [ ] `05_reaction_diffusion.ipynb` — Coupled transport with decay
- [ ] `05_3d_scaling.ipynb` — Extrude 2D mesh to 3D
- [ ] `05_droplet_advection.ipynb` (optional) — Simplified droplet mixing

**Time to write:** ~2–3 hours per notebook (use templates).

---

## Step 6: Assessment Options

### Formative (No Grades, Feedback Only)

Students submit notebooks with:
- Code (clean, commented)
- Results (plots, error metrics)
- Short explanation (1 paragraph)

**Feedback:** "Good convergence study! Next time, try refining the mesh further."

### Summative (Graded)

**Project rubric (100 points):**
- Correct physics (30): PDE, BCs, parameters properly set
- Code quality (20): Clean, documented, reproducible
- Validation (20): Comparison to theory, error analysis, or sensitivity study
- Visualization (15): Clear plots, proper labels
- Report (15): Concise explanation of problem, method, results

---

## Step 7: Supporting Materials to Create

For maximum effectiveness, add:

### For Students:
- [ ] **Quick Start Guide** (1 page): "Clone repo → conda activate → jupyter notebook"
- [ ] **Glossary** (1 page): FEM terminology (weak form, assembly, Peclet, zeta potential, etc.)
- [ ] **Troubleshooting FAQ** (2 pages): Common errors and fixes

### For You:
- [ ] **Solutions notebook** (private): Completed versions of all notebooks for reference
- [ ] **Grading rubric** (detailed): Specific criteria for each project
- [ ] **Time log**: Track how long each activity takes; adjust next year

---

## Step 8: Making It Your Own

### Customize Geometries

Add microfluidic devices relevant to your lab:

```bash
geometry/
├── channels/
│   ├── simple_channel.geo          # Already here
│   ├── flow_focus_device.geo       # Add this
│   ├── serpentine_mixer.geo        # Add this
│   └── gradient_generator.geo      # Add this
```

Each `.geo` file becomes a homework exercise.

### Include Your Research

If your lab studies:
- **Electrophoresis:** Add EOF examples + electric double layer
- **Droplet microfluidics:** Expand `05_droplet_advection.ipynb`
- **Thermal convection:** Add heat equation notebook
- **Bioparticles:** Couple to electrokinetic mobility

### Invite Guest Experts

Week 5 could include a 1-hour Zoom seminar:
- Practitioner from industry (FEM in device design)
- Senior PhD student presenting their simulation results
- Microfluidics expert discussing numerical best practices

---

## Maintenance & Updates

### After First Run

- Collect student feedback (short survey)
- Fix broken notebook cells
- Update lecture notes with clarifications
- Add 1–2 new example geometries based on student questions

### Annually

- Update gmsh syntax (versions change)
- Verify conda environment still works (package updates)
- Prune unused files
- Add one new advanced topic (e.g., adjoint-based optimization)

### Git Workflow

```bash
# After each semester
git tag -a v2024_fall -m "Version after fall 2024 teaching"
git push origin v2024_fall

# For bug fixes
git checkout -b fix/poisson-convergence
# ... fix ...
git commit -m "Fix: Poisson convergence plot axes"
git push origin fix/poisson-convergence
# Create pull request, merge to main
```

---

## References for You (Instructor)

### FEniCS
- **FEniCS Book** (free online): https://fenicsproject.org/pub/documents/book/
- **FEniCS API docs**: https://fenics.readthedocs.io/

### gmsh
- **gmsh Manual**: https://gmsh.info/doc/texinfo/gmsh.html
- **gmsh Python API**: https://gmsh.info/doc/api/gmsh.html

### Microfluidics & Electrokinetics
- **Squires & Quake (2005)**: "Microfluidics: Fluid physics at the nanoliter scale" — essential reading
- **Stone, Stroock, Ajdari (2004)**: "Engineering flows in small devices" — comprehensive review

### Numerical Methods
- **Brenner & Scott**: "The Mathematical Theory of Finite Element Methods" — rigorous FEM theory
- **Persson & Strang (2004)**: "A Simple Mesh Generator in MATLAB" — clear explanation of unstructured meshing

---

## Closing Remarks

This course teaches **computational thinking in microfluidics**. Students will learn:
- **What** FEM is and why it matters
- **How** to implement it (hand-coding + libraries)
- **When** to use it (and when not to)
- **How** to validate results

By the end, they'll be able to:
- Design a microfluidic device
- Simulate its behavior
- Validate against theory or experiments
- Present results

This is **directly applicable** to research labs and industry.

Good luck, and feel free to adapt this course to your context. The modular structure makes it easy to swap, extend, or simplify.

---

**Questions or feedback?** File an issue on the repository, or reach out to the course maintainer.

Happy teaching!
