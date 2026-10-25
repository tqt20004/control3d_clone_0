import bpy
import math

# ==============================================================================
# BẢN VẼ 3D NHÀ PHỐ 50m2 HIỆN ĐẠI (4.5m x 11.2m)
# - Trệt: Sân trước, Khách, Cầu thang, Bếp & Bàn ăn, WC
# - Tầng 2: 2 Phòng ngủ (Master trước + Balcony, PN 2 sau), WC
# - Tầng 3: 3 Phòng ngủ (PN 3 trước, PN 4 giữa, PN 5 sau), WC
# - Tầng 4: Tum thang, Phòng thờ/giặt, Sân thượng Pergola bàn trà cây xanh
# ==============================================================================

# 1. DỌN SẠCH SCENE CŨ
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in bpy.data.meshes:
    if block.users == 0: bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if block.users == 0: bpy.data.materials.remove(block)

# 2. HỆ THỐNG VẬT LIỆU (Tương thích 100% Blender 3.x đến 4.x)
def create_material(name, base_color, roughness=0.5, metallic=0.0, transmission=0.0, emission=None, alpha=1.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Base Color
    if 'Base Color' in bsdf.inputs:
        bsdf.inputs['Base Color'].default_value = (*base_color[:3], 1.0)
    # Roughness
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = roughness
    # Metallic
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metallic
    # Transmission (Kính)
    for trans_key in ['Transmission Weight', 'Transmission']:
        if trans_key in bsdf.inputs:
            bsdf.inputs[trans_key].default_value = transmission
            break
    # Alpha
    if 'Alpha' in bsdf.inputs:
        bsdf.inputs['Alpha'].default_value = alpha
        if alpha < 1.0 or transmission > 0:
            mat.blend_method = 'BLEND'
    # Emission (Đèn)
    if emission:
        for em_key in ['Emission Color', 'Emission']:
            if em_key in bsdf.inputs:
                bsdf.inputs[em_key].default_value = (*emission[:3], 1.0)
                break
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = 4.0
            
    return mat

mat_wall_white   = create_material("M_WallWhite",   (0.95, 0.95, 0.95), roughness=0.6)
mat_wall_dark    = create_material("M_WallDark",    (0.22, 0.23, 0.25), roughness=0.5)
mat_floor_tile   = create_material("M_FloorTile",   (0.88, 0.88, 0.90), roughness=0.2)
mat_floor_wood   = create_material("M_FloorWood",   (0.55, 0.35, 0.20), roughness=0.4)
mat_wood_furn    = create_material("M_WoodFurn",    (0.40, 0.25, 0.15), roughness=0.3)
mat_sofa         = create_material("M_SofaFabric",  (0.20, 0.35, 0.45), roughness=0.8)
mat_bed_sheet    = create_material("M_BedSheet",    (0.92, 0.90, 0.85), roughness=0.7)
mat_bed_pillow   = create_material("M_BedPillow",   (0.85, 0.40, 0.35), roughness=0.6)
mat_kitchen      = create_material("M_KitchenCounter",(0.15, 0.15, 0.18), roughness=0.2)
mat_metal_black  = create_material("M_MetalBlack",  (0.08, 0.08, 0.08), roughness=0.3, metallic=0.9)
mat_glass        = create_material("M_Glass",       (0.85, 0.92, 0.95), roughness=0.05, transmission=0.85, alpha=0.3)
mat_lamp         = create_material("M_LampWarm",    (1.0, 0.85, 0.6),   emission=(1.0, 0.85, 0.6))
mat_plant        = create_material("M_PlantLeaf",   (0.18, 0.48, 0.20), roughness=0.5)
mat_terrace_tile = create_material("M_TerraceTile", (0.45, 0.45, 0.48), roughness=0.6)

# 3. HÀM TẠO HÌNH CƠ BẢN
def add_box(name, loc, size, mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    return obj

# THÔNG SỐ NHÀ 50m2 (Rộng 4.5m x Dài 11.2m = 50.4 m2)
W = 4.5       # Chiều rộng (X: từ -2.25 đến 2.25)
L = 11.2      # Chiều dài (Y: từ 0 đến 11.2)
H_G = 3.6     # Cao tầng trệt
H_2 = 3.2     # Cao tầng 2
H_3 = 3.2     # Cao tầng 3
H_4 = 2.8     # Cao tầng tum / sân thượng
SLAB_THICK = 0.22

# ==============================================================================
# HÀM DỰNG SÀN VÀ DẦM KẾT CẤU
# ==============================================================================
def build_floor_slab(floor_idx, z_level, mat_floor, has_front_balcony=False, balcony_depth=1.2):
    # Sàn bê tông
    slab_y_len = L + (balcony_depth if has_front_balcony else 0)
    slab_y_center = (L / 2) - (balcony_depth / 2 if has_front_balcony else 0)
    slab = add_box(f"FloorSlab_{floor_idx}", (0, slab_y_center, z_level - SLAB_THICK / 2), (W, slab_y_len, SLAB_THICK), mat_wall_dark)
    
    # Lớp hoàn thiện sàn (gạch/gỗ)
    finish = add_box(f"FloorFinish_{floor_idx}", (0, L / 2, z_level + 0.01), (W - 0.2, L - 0.2, 0.02), mat_floor)
    
    # Lan can ban công nếu có
    if has_front_balcony:
        bal_y = -balcony_depth
        # Sàn ban công gạch ngoài trời
        add_box(f"BalconyFloor_{floor_idx}", (0, bal_y / 2, z_level + 0.01), (W, balcony_depth, 0.02), mat_terrace_tile)
        # Lan can kính mặt trước
        add_box(f"BalconyGlass_{floor_idx}", (0, bal_y, z_level + 0.55), (W, 0.04, 1.0), mat_glass)
        # Tay vịn inox đen
        add_box(f"BalconyRail_{floor_idx}", (0, bal_y, z_level + 1.07), (W, 0.08, 0.05), mat_metal_black)

# ==============================================================================
# NỘI THẤT DÙNG CHUNG (Cầu thang, Giường, Tủ, Sofa)
# ==============================================================================
def add_staircase(base_z, height, start_y=4.8):
    # Cầu thang 15 bậc ziczac ở giữa nhà (Y từ 4.8 đến 7.2)
    steps = 14
    step_w = 1.0
    step_l = 2.4 / steps
    step_h = height / steps
    stair_x = W / 2 - 0.6  # Nằm sát vách phải
    for s in range(steps):
        sz = base_z + (s + 0.5) * step_h
        sy = start_y + (s + 0.5) * step_l
        add_box(f"Step_{int(base_z)}_{s}", (stair_x, sy, sz), (step_w, step_l, step_h), mat_floor_wood)
    # Tay vịn cầu thang
    add_box(f"StairRailing_{int(base_z)}", (stair_x - 0.48, start_y + 1.2, base_z + height / 2 + 0.5), (0.04, 2.5, 0.9), mat_metal_black)

def add_bed(name, loc, rotation_deg=0):
    bx, by, bz = loc
    # Khung giường gỗ
    add_box(f"{name}_Frame", (bx, by, bz + 0.2), (1.8, 2.0, 0.4), mat_wood_furn)
    # Nệm đệm êm
    add_box(f"{name}_Mattress", (bx, by, bz + 0.45), (1.7, 1.9, 0.25), mat_bed_sheet)
    # Gối đôi
    add_box(f"{name}_Pillow1", (bx - 0.45, by + 0.7, bz + 0.6), (0.6, 0.4, 0.12), mat_bed_pillow)
    add_box(f"{name}_Pillow2", (bx + 0.45, by + 0.7, bz + 0.6), (0.6, 0.4, 0.12), mat_bed_pillow)
    # Tab đầu giường
    add_box(f"{name}_Nightstand", (bx - 1.15, by + 0.7, bz + 0.25), (0.45, 0.45, 0.5), mat_wood_furn)
    add_box(f"{name}_Lamp", (bx - 1.15, by + 0.7, bz + 0.6), (0.18, 0.18, 0.2), mat_lamp)

def add_wardrobe(name, loc, size=(1.6, 0.6, 2.4)):
    add_box(name, loc, size, mat_wood_furn)

# ==============================================================================
# TẦNG TRỆT (Z = 0 đến 3.6m) - 50m2
# Khách (0 -> 4.8m) | Cầu thang & WC (4.8 -> 7.2m) | Bếp & Bàn ăn (7.2 -> 11.2m)
# ==============================================================================
build_floor_slab(1, 0, mat_floor_tile, has_front_balcony=True, balcony_depth=1.5)
# Sân trước đậu xe
add_box("FrontYard", (0, -0.75, 0.05), (W, 1.5, 0.1), mat_terrace_tile)
add_box("MainGate_Left", (-W/2 + 0.15, -1.5, 1.2), (0.3, 0.3, 2.4), mat_wall_dark)
add_box("MainGate_Right", (W/2 - 0.15, -1.5, 1.2), (0.3, 0.3, 2.4), mat_wall_dark)
add_box("MainGate_Door", (0, -1.5, 1.1), (3.6, 0.06, 2.2), mat_metal_black)

# Vách tường sau & vách ngăn
add_box("Wall_Back_F1", (0, L, H_G / 2), (W, 0.2, H_G), mat_wall_white)
add_box("Wall_Left_F1", (-W / 2, L / 2, H_G / 2), (0.2, L, H_G), mat_wall_white)
add_box("Wall_Right_F1", (W / 2, L / 2, H_G / 2), (0.2, L, H_G), mat_wall_white)

# Cửa chính kính 4 cánh mặt tiền
add_box("Door_Glass_Front", (0, 0, 1.3), (3.8, 0.08, 2.6), mat_glass)
add_box("Door_Frame_Front", (0, 0, 1.3), (3.84, 0.1, 2.64), mat_metal_black)

# --- NỘI THẤT PHÒNG KHÁCH ---
# Bộ Sofa chữ L
add_box("Sofa_Main", (-0.9, 1.8, 0.45), (2.2, 0.9, 0.75), mat_sofa)
add_box("Sofa_L_Part", (-1.55, 2.6, 0.45), (0.9, 0.9, 0.75), mat_sofa)
# Bàn trà kính chân gỗ
add_box("Coffee_Table", (-0.9, 2.5, 0.22), (1.1, 0.6, 0.4), mat_wood_furn)
add_box("Coffee_Table_Top", (-0.9, 2.5, 0.43), (1.15, 0.65, 0.03), mat_glass)
# Thảm phòng khách
add_box("Living_Carpet", (-0.9, 2.4, 0.02), (2.4, 1.8, 0.02), mat_bed_sheet)
# Kệ TV & TV treo tường sát vách phải
add_box("TV_Console", (1.8, 2.4, 0.3), (0.4, 2.2, 0.5), mat_wood_furn)
add_box("TV_Screen", (1.95, 2.4, 1.4), (0.05, 1.6, 0.9), mat_metal_black)

# --- CẦU THANG & WC GẦM CẦU THANG ---
add_staircase(0, H_G, start_y=4.6)
# WC trệt
add_box("WC_Wall_Front_F1", (-0.8, 4.6, H_G * 0.35), (1.8, 0.15, H_G * 0.7), mat_wall_white)
add_box("WC_Wall_Side_F1", (0.1, 5.8, H_G * 0.35), (0.15, 2.4, H_G * 0.7), mat_wall_white)

# --- PHÒNG BẾP & BÀN ĂN (Phía sau) ---
# Tủ bếp chữ L sát góc sau bên trái
add_box("Kitchen_Counter_1", (-1.2, L - 0.4, 0.45), (1.9, 0.7, 0.9), mat_kitchen)
add_box("Kitchen_Counter_2", (-W/2 + 0.45, L - 1.6, 0.45), (0.7, 1.8, 0.9), mat_kitchen)
add_box("Kitchen_Upper", (-1.2, L - 0.3, 2.4), (1.9, 0.45, 0.8), mat_wood_furn)
# Tủ lạnh 2 cánh
add_box("Refrigerator", (-W/2 + 0.5, L - 2.8, 0.95), (0.8, 0.75, 1.9), mat_metal_black)
# Bàn ăn 6 ghế giữa phòng bếp
add_box("Dining_Table", (0.4, 8.8, 0.4), (1.5, 0.9, 0.76), mat_wood_furn)
for dy in [-0.5, 0.0, 0.5]:
    add_box(f"Chair_L_{dy}", (-0.25, 8.8 + dy, 0.4), (0.4, 0.4, 0.85), mat_sofa)
    add_box(f"Chair_R_{dy}", (1.05, 8.8 + dy, 0.4), (0.4, 0.4, 0.85), mat_sofa)

# ==============================================================================
# TẦNG 2 (LẦU 1 - Z = 3.6 đến 6.8m) - 2 PHÒNG NGỦ
# - Phòng Master trước (Y: 0 -> 4.6m) có Ban Công rộng
# - Cầu thang & WC giữa (Y: 4.6 -> 7.2m)
# - Phòng ngủ 2 sau (Y: 7.2 -> 11.2m)
# ==============================================================================
Z2 = H_G
build_floor_slab(2, Z2, mat_floor_wood, has_front_balcony=True, balcony_depth=1.2)

# Vách ngoài tầng 2
add_box("Wall_Back_F2", (0, L, Z2 + H_2 / 2), (W, 0.2, H_2), mat_wall_white)
add_box("Wall_Left_F2", (-W / 2, L / 2, Z2 + H_2 / 2), (0.2, L, H_2), mat_wall_white)
add_box("Wall_Right_F2", (W / 2, L / 2, Z2 + H_2 / 2), (0.2, L, H_2), mat_wall_white)

# Cửa kính lớn ra ban công trước
add_box("Door_Balcony_F2", (0, 0, Z2 + 1.2), (3.6, 0.06, 2.4), mat_glass)
add_box("Door_Frame_F2", (0, 0, Z2 + 1.2), (3.64, 0.08, 2.44), mat_metal_black)

# Vách ngăn phòng Master và Hành lang
add_box("Wall_Master_Div", (-0.4, 4.6, Z2 + H_2 / 2), (W - 1.2, 0.15, H_2), mat_wall_white)

# NỘI THẤT PHÒNG MASTER (Trước)
add_bed("Bed_Master", (-0.4, 2.2, Z2))
add_wardrobe("Wardrobe_Master", (-W/2 + 0.4, 3.2, Z2 + 1.2), (0.6, 1.8, 2.4))
# Bàn làm việc + ghế sát cửa ban công
add_box("Desk_Master", (1.2, 0.6, Z2 + 0.38), (1.2, 0.6, 0.75), mat_wood_furn)
add_box("Chair_Master", (1.2, 1.1, Z2 + 0.4), (0.45, 0.45, 0.85), mat_sofa)

# CẦU THANG TẦNG 2 LÊN 3
add_staircase(Z2, H_2, start_y=4.6)

# PHÒNG TẮM / WC TẦNG 2
add_box("WC_F2_Wall", (-0.8, 5.8, Z2 + H_2 / 2), (1.8, 2.2, H_2), mat_wall_white)

# NỘI THẤT PHÒNG NGỦ 2 (Sau)
add_box("Wall_Bed2_Div", (-0.4, 7.2, Z2 + H_2 / 2), (W - 1.2, 0.15, H_2), mat_wall_white)
add_bed("Bed_Bedroom2", (0.2, 9.2, Z2))
add_wardrobe("Wardrobe_Bed2", (-W/2 + 0.4, 9.2, Z2 + 1.2), (0.6, 1.6, 2.4))
# Cửa sổ thông gió sau
add_box("Window_Bed2", (0, L, Z2 + 1.6), (1.8, 0.15, 1.2), mat_glass)

# ==============================================================================
# TẦNG 3 (LẦU 2 - Z = 6.8 đến 10.0m) - 3 PHÒNG NGỦ
# - Phòng ngủ 3 (Trước, Y: 0 -> 4.2m)
# - Phòng ngủ 4 (Giữa/Trái, Y: 4.2 -> 7.4m)
# - Phòng ngủ 5 (Sau, Y: 7.4 -> 11.2m)
# ==============================================================================
Z3 = H_G + H_2
build_floor_slab(3, Z3, mat_floor_wood, has_front_balcony=True, balcony_depth=1.2)

# Vách ngoài tầng 3
add_box("Wall_Back_F3", (0, L, Z3 + H_3 / 2), (W, 0.2, H_3), mat_wall_white)
add_box("Wall_Left_F3", (-W / 2, L / 2, Z3 + H_3 / 2), (0.2, L, H_3), mat_wall_white)
add_box("Wall_Right_F3", (W / 2, L / 2, Z3 + H_3 / 2), (0.2, L, H_3), mat_wall_white)

# Mặt tiền kính ban công tầng 3
add_box("Door_Balcony_F3", (0, 0, Z3 + 1.2), (3.6, 0.06, 2.4), mat_glass)
add_box("Door_Frame_F3", (0, 0, Z3 + 1.2), (3.64, 0.08, 2.44), mat_metal_black)

# --- PHÒNG NGỦ 3 (Trước) ---
add_box("Wall_Bed3_Div", (-0.4, 4.0, Z3 + H_3 / 2), (W - 1.2, 0.15, H_3), mat_wall_white)
add_bed("Bed_Bedroom3", (-0.4, 2.0, Z3))
add_wardrobe("Wardrobe_Bed3", (-W/2 + 0.4, 3.0, Z3 + 1.2), (0.6, 1.6, 2.3))

# CẦU THANG TẦNG 3 LÊN SÂN THƯỢNG
add_staircase(Z3, H_3, start_y=4.6)

# --- PHÒNG NGỦ 4 (Giữa bên trái cầu thang) ---
add_box("Wall_Bed4_Side", (0.2, 5.8, Z3 + H_3 / 2), (0.15, 2.8, H_3), mat_wall_white)
add_box("Wall_Bed4_Rear", (-1.0, 7.2, Z3 + H_3 / 2), (2.2, 0.15, H_3), mat_wall_white)
add_bed("Bed_Bedroom4", (-1.0, 5.6, Z3))
add_wardrobe("Wardrobe_Bed4", (-W/2 + 0.4, 6.6, Z3 + 1.2), (0.55, 1.2, 2.2))

# --- PHÒNG NGỦ 5 (Phía sau) ---
add_box("Wall_Bed5_Front", (0.5, 7.6, Z3 + H_3 / 2), (1.5, 0.15, H_3), mat_wall_white)
add_bed("Bed_Bedroom5", (0.4, 9.4, Z3))
add_wardrobe("Wardrobe_Bed5", (-W/2 + 0.4, 9.4, Z3 + 1.2), (0.6, 1.5, 2.3))
add_box("Window_Bed5", (0, L, Z3 + 1.6), (1.8, 0.15, 1.2), mat_glass)

# ==============================================================================
# TẦNG 4 (SÂN THƯỢNG & TUM THANG - Z = 10.0 đến 12.8m)
# - Sân thượng trước siêu chill (Pergola lam gỗ, Bàn trà, Cây cảnh)
# - Tum thang & Phòng thờ nhỏ ở giữa
# - Sân phơi sau
# ==============================================================================
Z4 = H_G + H_2 + H_3
build_floor_slab(4, Z4, mat_terrace_tile, has_front_balcony=True, balcony_depth=1.2)

# VÁCH LAN CAN SÂN THƯỢNG (Bao quanh thông thoáng cao 1.1m)
add_box("Parapet_Front", (0, -1.2, Z4 + 0.55), (W, 0.05, 1.1), mat_glass)
add_box("Parapet_Front_Rail", (0, -1.2, Z4 + 1.12), (W, 0.08, 0.05), mat_metal_black)
add_box("Parapet_Left", (-W / 2, L / 2, Z4 + 0.55), (0.15, L + 2.4, 1.1), mat_wall_dark)
add_box("Parapet_Right", (W / 2, L / 2, Z4 + 0.55), (0.15, L + 2.4, 1.1), mat_wall_dark)
add_box("Parapet_Back", (0, L, Z4 + 0.55), (W, 0.15, 1.1), mat_wall_white)

# TUM THANG & PHÒNG THỜ (Ở giữa Y từ 4.2 đến 8.0)
add_box("Tum_Wall_Front", (0, 4.2, Z4 + H_4 / 2), (W - 0.3, 0.15, H_4), mat_wall_white)
add_box("Tum_Wall_Back", (0, 8.0, Z4 + H_4 / 2), (W - 0.3, 0.15, H_4), mat_wall_white)
add_box("Tum_Door_Front", (0, 4.2, Z4 + 1.1), (1.2, 0.08, 2.2), mat_glass)
# Mái tum thang
add_box("Tum_Roof", (0, 6.1, Z4 + H_4), (W, 4.2, 0.2), mat_wall_dark)

# --- SÂN THƯỢNG TRƯỚC VIEW CHILL ---
# Giàn Lam che nắng Pergola hiện đại (Khung sắt đen + nan gỗ)
for px in [-2.0, 2.0]:
    add_box(f"Pergola_Post_{px}", (px, 0.5, Z4 + 1.4), (0.1, 0.1, 2.8), mat_metal_black)
add_box("Pergola_Beam_Front", (0, 0.5, Z4 + 2.8), (4.2, 0.1, 0.1), mat_metal_black)
add_box("Pergola_Beam_Back", (0, 4.0, Z4 + 2.8), (4.2, 0.1, 0.1), mat_metal_black)
# Các nan lam gỗ ngang
for ny in [0.8, 1.4, 2.0, 2.6, 3.2, 3.8]:
    add_box(f"Pergola_Slat_{ny}", (0, ny, Z4 + 2.88), (4.2, 0.12, 0.05), mat_wood_furn)

# Bàn trà & ghế cafe ngoài trời
add_box("Terrace_Table", (0, 2.0, Z4 + 0.38), (0.9, 0.9, 0.75), mat_metal_black)
add_box("Terrace_Chair1", (-0.7, 2.0, Z4 + 0.4), (0.45, 0.45, 0.8), mat_metal_black)
add_box("Terrace_Chair2", (0.7, 2.0, Z4 + 0.4), (0.45, 0.45, 0.8), mat_metal_black)

# Chậu cây xanh cảnh quan sân thượng
for cx in [-1.6, -0.8, 0.8, 1.6]:
    add_box(f"Pot_{cx}", (cx, -0.8, Z4 + 0.25), (0.4, 0.4, 0.5), mat_wall_dark)
    add_box(f"Plant_{cx}", (cx, -0.8, Z4 + 0.7), (0.5, 0.5, 0.6), mat_plant)

# Bàn thờ nhỏ trong phòng thờ (Tum)
add_box("Altar_Table", (0, 6.2, Z4 + 0.6), (1.4, 0.6, 1.2), mat_wood_furn)

# ==============================================================================
# ÁNH SÁNG & CAMERA PHỐI CẢNH ISOMETRIC 3D
# ==============================================================================
# Sun Light (Ánh sáng mặt trời tự nhiên)
bpy.ops.object.light_add(type='SUN', location=(10, -15, 20), rotation=(math.radians(50), math.radians(15), math.radians(-35)))
sun = bpy.context.active_object
sun.name = "Sun_Main"
sun.data.energy = 4.5
sun.data.color = (1.0, 0.96, 0.90)

# Đèn môi trường dịu nhẹ
bpy.ops.object.light_add(type='AREA', location=(-8, 8, 15), rotation=(math.radians(60), 0, math.radians(110)))
fill = bpy.context.active_object
fill.name = "Sky_Fill"
fill.data.energy = 400
fill.data.size = 15
fill.data.color = (0.75, 0.85, 1.0)

# Camera góc phối cảnh 3/4 nhìn thấy cả 4 tầng
bpy.ops.object.camera_add(location=(-14.0, -16.0, 16.0), rotation=(math.radians(62), 0, math.radians(-42)))
cam = bpy.context.active_object
cam.name = "Camera_HouseView"
cam.data.lens = 32
bpy.context.scene.camera = cam

# Render Engine an toàn mọi phiên bản
for eng in ('BLENDER_EEVEE', 'EEVEE', 'BLENDER_EEVEE_NEXT', 'CYCLES'):
    try:
        bpy.context.scene.render.engine = eng
        break
    except Exception:
        pass

print("=" * 60)
print("✅ DỰNG THÀNH CÔNG NHÀ PHỐ 50m2 (4 TẦNG)")
print(" - Trệt: Phòng khách sofa L, bếp bàn ăn 6 ghế, WC gầm thang")
print(" - Tầng 2: 2 Phòng ngủ (Master trước + ban công, PN2 sau)")
print(" - Tầng 3: 3 Phòng ngủ (PN3 trước, PN4 giữa, PN5 sau)")
print(" - Tầng 4: Sân thượng Pergola bàn cafe chill + Tum phòng thờ")
print("👉 Bấm Z > Material Preview để xem phối màu nội thất!")
print("👉 Bấm Numpad 0 để xem toàn cảnh 4 tầng qua Camera!")
print("=" * 60)
