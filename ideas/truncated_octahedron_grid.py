import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# -------------------------------------------------
# Canonical truncated octahedron vertices
# -------------------------------------------------
V = np.array([
    [ 2,  0,  1], [ 2,  0, -1], [-2,  0,  1], [-2,  0, -1],
    [ 1,  2,  0], [-1,  2,  0], [ 1, -2,  0], [-1, -2,  0],
    [ 0,  1,  2], [ 0, -1,  2], [ 0,  1, -2], [ 0, -1, -2],
    [ 1,  0,  2], [-1,  0,  2], [ 1,  0, -2], [-1,  0, -2],
    [ 0,  2,  1], [ 0,  2, -1], [ 0, -2,  1], [ 0, -2, -1],
    [ 2,  1,  0], [ 2, -1,  0], [-2,  1,  0], [-2, -1,  0],
], dtype=float)

# -------------------------------------------------
# Triangles (pre-validated)
# -------------------------------------------------
# Each face is triangulated explicitly.
# Squares → 2 triangles
# Hexagons → 4 triangles

TRIS = [
    # Square faces
    [0,20,16],[0,16,12],
    [1,21,17],[1,17,14],
    [2,22,16],[2,16,13],
    [3,23,17],[3,17,15],
    [4,16,20],[4,20,5],
    [6,21,17],[6,17,7],

    # Hex faces
    [0,12,8],[0,8,16],[16,8,5],[5,8,4],
    [2,13,9],[2,9,16],[16,9,4],[4,9,5],
    [1,14,11],[1,11,17],[17,11,7],[7,11,6],
    [3,15,10],[3,10,17],[17,10,6],[6,10,7],
    [4,8,12],[4,12,20],[20,12,0],[0,12,4],
    [5,8,12],[5,12,16],[16,12,0],[0,12,5],
]

# -------------------------------------------------
# BCC lattice offsets
# -------------------------------------------------
OFFSETS = []

rng = range(-1, 2)
for x in rng:
    for y in rng:
        for z in rng:
            OFFSETS.append([4*x, 4*y, 4*z])
            OFFSETS.append([4*x+2, 4*y+2, 4*z+2])

# -------------------------------------------------
# Build mesh
# -------------------------------------------------
polys = []

for o in OFFSETS:
    cell = V + np.array(o)
    for t in TRIS:
        polys.append(cell[t])

# -------------------------------------------------
# Render
# -------------------------------------------------
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

mesh = Poly3DCollection(
    polys,
    facecolor='lightblue',
    edgecolor='black',
    linewidth=0.3,
    alpha=0.85
)

ax.add_collection3d(mesh)
ax.set_box_aspect([1,1,1])
ax.axis('off')

pts = np.vstack(polys)
ax.auto_scale_xyz(pts[:,0], pts[:,1], pts[:,2])

plt.show()
