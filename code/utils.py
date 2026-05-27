# utils.py: Helper functions for FEM microfluidics simulations

import numpy as np
from fenics import *

# ============================================================================
# Mesh & Geometry Utilities
# ============================================================================

def create_rectangular_channel(length, height, n_x, n_y):
    """
    Create a rectangular channel mesh.
    
    Parameters
    ----------
    length : float
        Channel length (x-direction)
    height : float
        Channel height (y-direction)
    n_x, n_y : int
        Number of elements in x and y
    
    Returns
    -------
    mesh : Mesh
        FEniCS mesh object
    """
    return RectangleMesh(Point(0, -height/2), Point(length, height/2), n_x, n_y)


def refine_mesh(mesh, levels=1):
    """Uniformly refine a mesh."""
    for _ in range(levels):
        mesh = refine(mesh)
    return mesh


# ============================================================================
# Function Space Utilities
# ============================================================================

def create_stokes_spaces(mesh, u_degree=2, p_degree=1):
    """
    Create mixed function spaces for Stokes equations (P2-P1).
    
    Returns
    -------
    V : VectorFunctionSpace
        Velocity space
    Q : FunctionSpace
        Pressure space
    W : FunctionSpace
        Mixed space
    """
    V = VectorFunctionSpace(mesh, "P", u_degree)
    Q = FunctionSpace(mesh, "P", p_degree)
    W = V * Q
    return V, Q, W


def create_scalar_spaces(mesh, degree=1):
    """
    Create a scalar function space (for concentrations, etc.).
    
    Returns
    -------
    S : FunctionSpace
        Scalar function space
    """
    return FunctionSpace(mesh, "P", degree)


# ============================================================================
# Boundary Condition Utilities
# ============================================================================

def define_boundary_subdomains(mesh, tol=1e-10):
    """
    Mark boundary subdomains for a rectangular channel:
    - 1: left (inlet)
    - 2: right (outlet)
    - 3: top wall
    - 4: bottom wall
    
    Returns
    -------
    boundaries : MeshFunction
        Boundary markers
    """
    boundaries = MeshFunction("size_t", mesh, 1)
    boundaries.set_all(0)
    
    class LeftBoundary(SubDomain):
        def inside(self, x, on_boundary):
            return on_boundary and abs(x[0]) < tol
    
    class RightBoundary(SubDomain):
        def inside(self, x, on_boundary):
            return on_boundary and abs(x[0] - mesh.coordinates()[:, 0].max()) < tol
    
    class TopBoundary(SubDomain):
        def inside(self, x, on_boundary):
            return on_boundary and x[1] > 0.5 * mesh.coordinates()[:, 1].max()
    
    class BottomBoundary(SubDomain):
        def inside(self, x, on_boundary):
            return on_boundary and x[1] < 0.5 * mesh.coordinates()[:, 1].min()
    
    LeftBoundary().mark(boundaries, 1)
    RightBoundary().mark(boundaries, 2)
    TopBoundary().mark(boundaries, 3)
    BottomBoundary().mark(boundaries, 4)
    
    return boundaries


def apply_noslip_bc(W, boundaries):
    """
    Apply no-slip boundary conditions on walls (top, bottom).
    """
    bcs = []
    u_noslip = Constant((0, 0))
    
    # Top wall
    bcs.append(DirichletBC(W.sub(0), u_noslip, boundaries, 3))
    # Bottom wall
    bcs.append(DirichletBC(W.sub(0), u_noslip, boundaries, 4))
    
    return bcs


# ============================================================================
# Analysis Utilities
# ============================================================================

def velocity_profile_along_line(u_solution, x_pos, y_min, y_max, n_points=50):
    """
    Extract velocity along a vertical line at x = x_pos.
    
    Parameters
    ----------
    u_solution : Function
        Velocity solution
    x_pos : float
        x-coordinate of the line
    y_min, y_max : float
        y-range
    n_points : int
        Number of points to evaluate
    
    Returns
    -------
    y_vals : ndarray
        y-coordinates
    u_x_vals : ndarray
        x-component of velocity
    u_y_vals : ndarray
        y-component of velocity
    """
    y_vals = np.linspace(y_min, y_max, n_points)
    u_x_vals = []
    u_y_vals = []
    
    for y in y_vals:
        point = Point(x_pos, y)
        try:
            u_val = u_solution(point)
            u_x_vals.append(u_val[0])
            u_y_vals.append(u_val[1])
        except:
            u_x_vals.append(np.nan)
            u_y_vals.append(np.nan)
    
    return y_vals, np.array(u_x_vals), np.array(u_y_vals)


def compute_l2_error(u_fem, u_exact, mesh):
    """
    Compute L2 error between FEM solution and exact solution.
    
    Parameters
    ----------
    u_fem : Function
        FEM solution
    u_exact : Function or Expression
        Exact solution
    mesh : Mesh
        Domain
    
    Returns
    -------
    error : float
        L2 norm of the error
    """
    V = u_fem.function_space()
    error_func = project(u_fem - u_exact, V)
    return norm(error_func, 'L2')


def compute_flow_rate(u_solution, y_min, y_max, x_pos, n_points=100):
    """
    Compute volumetric flow rate (per unit depth) by integration.
    
    Q = ∫ u_x dy
    
    Parameters
    ----------
    u_solution : Function
        Velocity solution
    y_min, y_max : float
        Integration bounds (y-range of channel)
    x_pos : float
        x-coordinate at which to evaluate
    n_points : int
        Number of quadrature points
    
    Returns
    -------
    Q : float
        Flow rate
    """
    y_vals, u_x_vals, _ = velocity_profile_along_line(
        u_solution, x_pos, y_min, y_max, n_points
    )
    # Trapezoid rule integration
    Q = np.trapz(u_x_vals, y_vals)
    return Q


def evaluate_at_points(function, points):
    """
    Evaluate a function at multiple points.
    
    Parameters
    ----------
    function : Function
        FEniCS function
    points : list of tuples
        Points to evaluate at: [(x1, y1), (x2, y2), ...]
    
    Returns
    -------
    values : list
        Function values at points
    """
    values = []
    for x, y in points:
        try:
            point = Point(x, y)
            val = function(point)
            values.append(val)
        except:
            values.append(np.nan)
    return values


# ============================================================================
# Output & Visualization Utilities
# ============================================================================

def save_solution_pvd(u, p, filename_prefix):
    """
    Save velocity and pressure to ParaView .pvd files.
    
    Parameters
    ----------
    u : Function
        Velocity solution
    p : Function
        Pressure solution
    filename_prefix : str
        Prefix for output files (e.g., "solution")
    """
    File(filename_prefix + "_velocity.pvd") << u
    File(filename_prefix + "_pressure.pvd") << p
    print(f"Solutions saved to {filename_prefix}_*.pvd")


def summary_stats(u_solution, p_solution, channel_height):
    """
    Print summary statistics of a flow solution.
    
    Parameters
    ----------
    u_solution : Function
        Velocity field
    p_solution : Function
        Pressure field
    channel_height : float
        Channel height (for context)
    """
    # Velocity stats
    u_mag = project(sqrt(u_solution[0]**2 + u_solution[1]**2), p_solution.function_space())
    u_max = u_mag.vector().max()
    
    # Pressure stats
    p_max = p_solution.vector().max()
    p_min = p_solution.vector().min()
    
    # Divergence check
    div_u = project(div(u_solution), p_solution.function_space())
    div_u_max = np.max(np.abs(div_u.vector().get_local()))
    
    print("\n" + "="*60)
    print("FLOW SOLUTION SUMMARY")
    print("="*60)
    print(f"Max velocity:           {u_max:.6e}")
    print(f"Max pressure:           {p_max:.6e}")
    print(f"Min pressure:           {p_min:.6e}")
    print(f"Max |∇·u| (divg check): {div_u_max:.6e}")
    print("="*60 + "\n")
