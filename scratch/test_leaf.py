import os, math
import numpy as np
import trimesh

def create_leaf_mesh(width=0.32, length=0.48, arch=0.06):
    # 6 vertices: base-left, base-right, mid-left, mid-right, tip, mid-ridge
    # Or simple 4 vertices quad with normal and UVs
    hw = width / 2.0
    # Quad with arch
    v = np.array([
        [-hw * 0.4, 0.0, 0.0],
        [ hw * 0.4, 0.0, 0.0],
        [ hw, arch, length * 0.55],
        [-hw, arch, length * 0.55],
        [ 0.0, arch * 0.3, length],
    ], dtype=np.float32)
    # 3 triangles: (0, 1, 2), (0, 2, 3), (3, 2, 4)
    f = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [3, 2, 4]
    ], dtype=np.uint32)
    
    uv = np.array([
        [0.1, 0.0],
        [0.9, 0.0],
        [0.95, 0.6],
        [0.05, 0.6],
        [0.5, 0.98]
    ], dtype=np.float32)
    
    mesh = trimesh.Trimesh(vertices=v, faces=f, process=True)
    return v, f.flatten(), mesh.vertex_normals, uv

v, f, n, uv = create_leaf_mesh()
print("Leaf verts:", len(v), "faces:", len(f)//3, "normals:", len(n), "uvs:", len(uv))
