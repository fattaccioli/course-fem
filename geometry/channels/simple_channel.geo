// simple_channel.geo
// A basic rectangular microfluidic channel for FEM simulation

// ============================================================
// PARAMETERS
// ============================================================

// Physical dimensions
L = 1.0;    // Channel length (x-direction)
H = 0.1;    // Channel height (y-direction)

// Mesh parameters
lc = 0.02;  // Characteristic length (element size)

// ============================================================
// GEOMETRY
// ============================================================

// Points: corners of the rectangle
Point(1) = {0,     -H/2, 0, lc};    // Bottom-left
Point(2) = {L,     -H/2, 0, lc};    // Bottom-right
Point(3) = {L,      H/2, 0, lc};    // Top-right
Point(4) = {0,      H/2, 0, lc};    // Top-left

// Lines: edges of the rectangle
Line(1) = {1, 2};   // Bottom wall
Line(2) = {2, 3};   // Right wall (outlet)
Line(3) = {3, 4};   // Top wall
Line(4) = {4, 1};   // Left wall (inlet)

// Closed curve
Curve Loop(1) = {1, 2, 3, 4};

// Surface
Plane Surface(1) = {1};

// ============================================================
// PHYSICAL REGIONS (for boundary condition application)
// ============================================================

Physical Curve("inlet", 10) = {4};      // Left edge
Physical Curve("outlet", 20) = {2};     // Right edge
Physical Curve("walls", 30) = {1, 3};   // Top and bottom (no-slip)

Physical Surface("fluid", 100) = {1};   // Interior domain

// ============================================================
// MESHING
// ============================================================

// Optional: Set the mesh algorithm
// 6 = Delaunay (triangular)
// 8 = Delaunay (quad)
Mesh.Algorithm = 6;

// Smoothing iterations
Mesh.Smoothing = 3;
