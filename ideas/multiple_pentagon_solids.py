import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def rotate_about_axis(points, axis, angle):
    axis = axis / np.linalg.norm(axis)
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    R = np.array([
        [
            cos_a + axis[0]*axis[0]*(1-cos_a),
            axis[0]*axis[1]*(1-cos_a) - axis[2]*sin_a,
            axis[0]*axis[2]*(1-cos_a) + axis[1]*sin_a
        ],
        [
            axis[1]*axis[0]*(1-cos_a) + axis[2]*sin_a,
            cos_a + axis[1]*axis[1]*(1-cos_a),
            axis[1]*axis[2]*(1-cos_a) - axis[0]*sin_a
        ],
        [
            axis[2]*axis[0]*(1-cos_a) - axis[1]*sin_a,
            axis[2]*axis[1]*(1-cos_a) + axis[0]*sin_a,
            cos_a + axis[2]*axis[2]*(1-cos_a)
        ]
    ])

    return points @ R.T


phi = (1 + 5 ** 0.5) / 2

# Base dodecahedron vertices
base_verts = np.array([
    [+1, +1, +1], [+1, +1, -1], [+1, -1, +1], [+1, -1, -1],
    [-1, +1, +1], [-1, +1, -1], [-1, -1, +1], [-1, -1, -1],
    [0, +1/phi, +phi], [0, +1/phi, -phi],
    [0, -1/phi, +phi], [0, -1/phi, -phi],
    [+1/phi, +phi, 0], [+1/phi, -phi, 0],
    [-1/phi, +phi, 0], [-1/phi, -phi, 0],
    [+phi, 0, +1/phi], [+phi, 0, -1/phi],
    [-phi, 0, +1/phi], [-phi, 0, -1/phi],
])

base_verts /= np.linalg.norm(base_verts, axis=1).max()

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

def triangulated_mesh(verts):
    triangles = []
    for face in faces:
        pts = verts[face]
        center = pts.mean(axis=0)
        for i in range(len(pts)):
            triangles.append([pts[i], pts[(i+1)%5], center])
    return triangles

# Compute face normals and centers
face_centers = []
face_normals = []

for face in faces:
    pts = base_verts[face]
    center = pts.mean(axis=0)
    normal = np.cross(pts[1] - pts[0], pts[2] - pts[0])
    normal /= np.linalg.norm(normal)
    face_centers.append(center)
    face_normals.append(normal)

# Build solids
all_triangles = []

# Center solid
all_triangles += triangulated_mesh(base_verts)

# Add neighbors (touching faces)
offset_dist = np.linalg.norm(face_centers[0]) * 2

angle = np.pi / 5  # 36 degrees

for i in range(5):
    normal = face_normals[i]

    # Rotate solid around the face normal
    rotated = rotate_about_axis(base_verts, normal, angle)

    # Translate to touch face
    offset = normal * offset_dist
    new_verts = rotated + offset

    all_triangles += triangulated_mesh(new_verts)


# Plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

mesh = Poly3DCollection(
    all_triangles,
    facecolor="lightblue",
    edgecolor="black",
    linewidth=0.4,
    # alpha=0.7
)

ax.add_collection3d(mesh)
ax.set_box_aspect([1,1,1])
ax.axis("off")

pts = np.vstack(all_triangles)
ax.auto_scale_xyz(pts[:,0], pts[:,1], pts[:,2])

plt.show()
