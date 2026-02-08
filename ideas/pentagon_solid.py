import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

# Golden ratio
phi = (1 + 5 ** 0.5) / 2

# Dodecahedron vertices
verts = np.array([
    [+1, +1, +1],
    [+1, +1, -1],
    [+1, -1, +1],
    [+1, -1, -1],
    [-1, +1, +1],
    [-1, +1, -1],
    [-1, -1, +1],
    [-1, -1, -1],

    [0, +1/phi, +phi],
    [0, +1/phi, -phi],
    [0, -1/phi, +phi],
    [0, -1/phi, -phi],

    [+1/phi, +phi, 0],
    [+1/phi, -phi, 0],
    [-1/phi, +phi, 0],
    [-1/phi, -phi, 0],

    [+phi, 0, +1/phi],
    [+phi, 0, -1/phi],
    [-phi, 0, +1/phi],
    [-phi, 0, -1/phi],
])

# Normalize for nicer viewing
verts /= np.linalg.norm(verts, axis=1).max()

# Pentagon faces (vertex indices)
faces = [
    [0, 8, 10, 2, 16],
    [0, 16, 17, 1, 12],
    [0, 12, 14, 4, 8],
    [8, 4, 18, 6, 10],
    [10, 6, 15, 13, 2],
    [2, 13, 3, 17, 16],
    [1, 9, 5, 14, 12],
    [4, 14, 5, 19, 18],
    [6, 18, 19, 7, 15],
    [3, 13, 15, 7, 11],
    [1, 17, 3, 11, 9],
    [5, 9, 11, 7, 19]
]

triangles = []

# Triangulate each pentagon via center point
for face in faces:
    pts = verts[face]
    center = pts.mean(axis=0)

    for i in range(len(face)):
        a = pts[i]
        b = pts[(i + 1) % len(face)]
        triangles.append([a, b, center])

# Plot
fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection='3d')

# --- TRIANGLES (implementation layer) ---
tri_mesh = Poly3DCollection(
    triangles,
    facecolor="lightblue",
    edgecolor="black",
    linewidth=0.4,
    alpha=0.6
)
ax.add_collection3d(tri_mesh)

# --- PENTAGON OUTLINES (semantic layer, robust) ---
pentagon_edges = []

for face in faces:
    pts = verts[face]
    for i in range(len(pts)):
        a = pts[i]
        b = pts[(i + 1) % len(pts)]
        pentagon_edges.append([a, b])

pent_lines = Line3DCollection(
    pentagon_edges,
    colors="darkblue",
    linewidths=2.2
)

ax.add_collection3d(pent_lines)

# View settings
ax.set_box_aspect([1, 1, 1])
ax.axis("off")

all_pts = np.vstack(verts)
ax.auto_scale_xyz(all_pts[:,0], all_pts[:,1], all_pts[:,2])

plt.show()
