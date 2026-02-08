import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# -------------------------
# Constants
# -------------------------
phi = (1 + 5 ** 0.5) / 2
TWIST = np.pi / 5  # 36 degrees

# -------------------------
# Base dodecahedron vertices (exact, symmetric)
# -------------------------
base_verts = np.array([
    [+1, +1, +1], [+1, +1, -1], [+1, -1, +1], [+1, -1, -1],
    [-1, +1, +1], [-1, +1, -1], [-1, -1, +1], [-1, -1, -1],

    [0, +1/phi, +phi], [0, +1/phi, -phi],
    [0, -1/phi, +phi], [0, -1/phi, -phi],

    [+1/phi, +phi, 0], [+1/phi, -phi, 0],
    [-1/phi, +phi, 0], [-1/phi, -phi, 0],

    [+phi, 0, +1/phi], [+phi, 0, -1/phi],
    [-phi, 0, +1/phi], [-phi, 0, -1/phi],
], dtype=float)

# Normalize to unit radius
base_verts /= np.linalg.norm(base_verts, axis=1).max()

# -------------------------
# Faces (pentagons)
# -------------------------
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
    [5, 9, 11, 7, 19],
]

# -------------------------
# Triangulate a dodecahedron
# -------------------------
def triangulate(verts):
    tris = []
    for face in faces:
        pts = verts[face]
        center = pts.mean(axis=0)
        for i in range(5):
            tris.append([pts[i], pts[(i + 1) % 5], center])
    return tris

# -------------------------
# Rotation about arbitrary axis
# -------------------------
def rotate_about_axis(points, axis, angle):
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    x, y, z = axis

    R = np.array([
        [c + x*x*(1-c),     x*y*(1-c) - z*s, x*z*(1-c) + y*s],
        [y*x*(1-c) + z*s,   c + y*y*(1-c),   y*z*(1-c) - x*s],
        [z*x*(1-c) - y*s,   z*y*(1-c) + x*s, c + z*z*(1-c)]
    ])

    return points @ R.T

# -------------------------
# Attach neighbor EXACTLY to a face
# -------------------------
# def attach_neighbor(base_verts, face_indices):
#     face_pts = base_verts[face_indices]
#     face_center = face_pts.mean(axis=0)

#     # Exact outward normal (for centered dodecahedron)
#     normal = face_center / np.linalg.norm(face_center)

#     # Rotate by π/5 about face normal
#     rotated = rotate_about_axis(base_verts, normal, TWIST)

#     # Translate so faces coincide
#     translated = rotated + 2 * face_center

#     return translated

def attach_neighbor(base_verts, face_indices):
    face_pts = base_verts[face_indices]
    face_center = face_pts.mean(axis=0)

    # Unit face normal (exact for centered dodecahedron)
    normal = face_center / np.linalg.norm(face_center)

    # Rotate by π/5 about face normal
    rotated = rotate_about_axis(base_verts, normal, TWIST)

    # --- CORRECT plane-based translation ---
    d = np.dot(face_center, normal)
    translated = rotated + 2 * d * normal

    return translated

# -------------------------
# Build scene
# -------------------------
all_tris = []

# Central solid
all_tris += triangulate(base_verts)

# Add 5 neighbors
for i in range(5):
    neighbor_verts = attach_neighbor(base_verts, faces[i])
    all_tris += triangulate(neighbor_verts)

# -------------------------
# Render
# -------------------------
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

mesh = Poly3DCollection(
    all_tris,
    facecolor="lightblue",
    edgecolor="black",
    linewidth=0.4,
    alpha=0.75
)

ax.add_collection3d(mesh)

ax.set_box_aspect([1, 1, 1])
ax.axis("off")

pts = np.vstack(all_tris)
ax.auto_scale_xyz(pts[:,0], pts[:,1], pts[:,2])

plt.show()
