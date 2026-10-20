import math
import numpy as np
import trimesh

def create_leaf_frond(width=0.35, length=0.55, arch=0.06):
    hw = width / 2.0
    v = np.array([
        [-hw * 0.3, 0.0, 0.0],
        [ hw * 0.3, 0.0, 0.0],
        [ hw, arch, length * 0.5],
        [-hw, arch, length * 0.5],
        [ 0.0, arch * 0.2, length],
    ], dtype=np.float32)
    f = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [3, 2, 4]
    ], dtype=np.uint32)
    uv = np.array([
        [0.15, 0.05],
        [0.85, 0.05],
        [0.95, 0.65],
        [0.05, 0.65],
        [0.5, 0.98]
    ], dtype=np.float32)
    
    mesh = trimesh.Trimesh(vertices=v, faces=f, process=True)
    return v, f.flatten(), mesh.vertex_normals, uv

def generate_lush_plant_primitives(px, pz, y_base=0.0):
    # Pot
    m_pot = trimesh.creation.cylinder(radius=0.36, height=0.72, sections=20)
    m_pot.apply_translation([px, y_base + 0.36, pz])
    
    m_rim = trimesh.creation.cylinder(radius=0.39, height=0.05, sections=20)
    m_rim.apply_translation([px, y_base + 0.70, pz])
    
    m_soil = trimesh.creation.cylinder(radius=0.35, height=0.03, sections=16)
    m_soil.apply_translation([px, y_base + 0.69, pz])
    
    m_stem = trimesh.creation.cylinder(radius=0.025, height=0.85, sections=12)
    m_stem.apply_translation([px, y_base + 1.05, pz])
    
    # Leaves
    leaf_verts_all = []
    leaf_ind_all = []
    leaf_norm_all = []
    leaf_uv_all = []
    
    num_leaves = 14
    for i in range(num_leaves):
        # 3 tiers
        tier = i // 5
        if tier == 0:
            pitch = math.radians(-30.0) # drooping down
            y_off = y_base + 0.76 + i * 0.03
            l_len = 0.56
            l_w = 0.36
            rad = 0.14
        elif tier == 1:
            pitch = math.radians(-10.0) # outward
            y_off = y_base + 0.94 + (i - 5) * 0.04
            l_len = 0.52
            l_w = 0.34
            rad = 0.12
        else:
            pitch = math.radians(25.0) # upright
            y_off = y_base + 1.15 + (i - 10) * 0.05
            l_len = 0.44
            l_w = 0.30
            rad = 0.08
            
        yaw = i * (2.0 * math.pi / num_leaves) + 0.15 * math.sin(i * 1.5)
        roll = 0.12 * math.sin(i * 2.3)
        
        lv, lf, ln, luv = create_leaf_frond(width=l_w, length=l_len, arch=0.06)
        
        # Rotation: pitch (around X), then roll (around Z), then yaw (around Y)
        Rx = trimesh.transformations.rotation_matrix(pitch, [1, 0, 0])
        Rz = trimesh.transformations.rotation_matrix(roll, [0, 0, 1])
        Ry = trimesh.transformations.rotation_matrix(yaw, [0, 1, 0])
        R = Ry @ Rz @ Rx
        
        # Position at radius & height
        ox = px + rad * math.sin(yaw)
        oz = pz + rad * math.cos(yaw)
        oy = y_off
        
        T = trimesh.transformations.translation_matrix([ox, oy, oz])
        M = T @ R
        
        # Transform vertices and normals
        v_h = np.hstack([lv, np.ones((len(lv), 1), dtype=np.float32)])
        v_trans = (M @ v_h.T).T[:, :3]
        
        n_h = np.hstack([ln, np.zeros((len(ln), 1), dtype=np.float32)])
        n_trans = (R @ n_h.T).T[:, :3]
        
        offset = len(leaf_verts_all)
        leaf_verts_all.extend(v_trans)
        leaf_ind_all.extend(lf + offset)
        leaf_norm_all.extend(n_trans)
        leaf_uv_all.extend(luv)
        
    leaf_verts_all = np.array(leaf_verts_all, dtype=np.float32)
    leaf_ind_all = np.array(leaf_ind_all, dtype=np.uint32)
    leaf_norm_all = np.array(leaf_norm_all, dtype=np.float32)
    leaf_uv_all = np.array(leaf_uv_all, dtype=np.float32)
    
    print(f"Plant at ({px}, {pz}) generated: {len(leaf_verts_all)} leaf verts, {len(leaf_ind_all)//3} leaf faces.")
    return m_pot, m_rim, m_soil, m_stem, (leaf_verts_all, leaf_ind_all, leaf_norm_all, leaf_uv_all)

pot, rim, soil, stem, leaves = generate_lush_plant_primitives(-8.5, 17.0)
