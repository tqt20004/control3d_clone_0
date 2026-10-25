import bpy
import random
import math

# ============================================
# BÙI VIỆN STREET - 3D MAP GENERATOR
# Paste vào Blender > Tab Scripting > Run Script
# ============================================

random.seed(42)  # Để mỗi lần chạy ra cùng 1 kết quả

# ----- XÓA SẠCH SCENE CŨ -----
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Xóa sạch data cũ
for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

# ----- TẠO VẬT LIỆU MÀU SẮC -----
def make_mat(name, r, g, b):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (r, g, b, 1)
    bsdf.inputs["Roughness"].default_value = 0.7
    return mat

# Bảng màu Bùi Viện: Tường nhà cũ sặc sỡ, biển hiệu neon
mat_road = make_mat("Road_Asphalt", 0.15, 0.15, 0.17)
mat_sidewalk = make_mat("Sidewalk_Tile", 0.5, 0.48, 0.42)

# Màu tường nhà cổ Sài Gòn (pastel bạc màu, vàng ố, xanh rêu, cam nhạt, hồng phấn)
wall_colors = [
    make_mat("Wall_Yellow", 0.85, 0.78, 0.45),
    make_mat("Wall_Cream", 0.9, 0.85, 0.7),
    make_mat("Wall_Blue", 0.45, 0.6, 0.75),
    make_mat("Wall_Green", 0.5, 0.7, 0.5),
    make_mat("Wall_Pink", 0.85, 0.6, 0.65),
    make_mat("Wall_Orange", 0.9, 0.65, 0.4),
    make_mat("Wall_White", 0.88, 0.87, 0.85),
    make_mat("Wall_Terracotta", 0.75, 0.5, 0.35),
]

# Màu cửa sổ, biển hiệu, mái hiên
mat_window = make_mat("Window_Dark", 0.15, 0.2, 0.3)
mat_door = make_mat("Door_Wood", 0.4, 0.25, 0.12)
mat_awning_red = make_mat("Awning_Red", 0.8, 0.15, 0.1)
mat_awning_blue = make_mat("Awning_Blue", 0.1, 0.3, 0.7)
mat_awning_green = make_mat("Awning_Green", 0.15, 0.5, 0.2)
mat_awning_yellow = make_mat("Awning_Yellow", 0.9, 0.75, 0.1)
mat_balcony = make_mat("Balcony_Metal", 0.3, 0.3, 0.32)
mat_sign_neon1 = make_mat("Neon_Pink", 1.0, 0.2, 0.5)
mat_sign_neon2 = make_mat("Neon_Cyan", 0.1, 0.9, 0.9)
mat_sign_neon3 = make_mat("Neon_Yellow", 1.0, 0.95, 0.2)
mat_sign_board = make_mat("Sign_Board", 0.1, 0.1, 0.12)
mat_roof = make_mat("Roof_Tile", 0.55, 0.3, 0.2)
mat_ac_unit = make_mat("AC_Unit", 0.7, 0.7, 0.72)
mat_table = make_mat("Table_Plastic", 0.9, 0.1, 0.1)
mat_stool = make_mat("Stool_Blue", 0.15, 0.3, 0.8)
mat_lantern = make_mat("Lantern_Red", 0.9, 0.15, 0.05)
mat_pole = make_mat("Pole_Metal", 0.35, 0.35, 0.37)
mat_wire = make_mat("Wire_Black", 0.08, 0.08, 0.1)
mat_plant = make_mat("Plant_Green", 0.2, 0.55, 0.15)
mat_pot = make_mat("Pot_Terracotta", 0.65, 0.4, 0.25)
mat_barrel = make_mat("Barrel_Metal", 0.4, 0.42, 0.45)
mat_light_warm = make_mat("Light_Warm", 1.0, 0.85, 0.5)

# Đèn neon phát sáng (Emission)
for neon_mat in [mat_sign_neon1, mat_sign_neon2, mat_sign_neon3, mat_light_warm]:
    bsdf = neon_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Emission Color"].default_value = bsdf.inputs["Base Color"].default_value
    bsdf.inputs["Emission Strength"].default_value = 5.0

awning_colors = [mat_awning_red, mat_awning_blue, mat_awning_green, mat_awning_yellow]
neon_colors = [mat_sign_neon1, mat_sign_neon2, mat_sign_neon3]

# ----- HÀM TẠO KHỐI HỘP (BUILDING BLOCK) -----
def create_box(name, x, y, z, sx, sy, sz, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    obj.data.materials.append(mat)
    return obj

# ----- HÀM TẠO MỘT NGÔI NHÀ BÙI VIỆN -----
def create_building(x_pos, side, index):
    """
    x_pos: vị trí dọc theo con phố (trục X)
    side: 1 = bên trái đường, -1 = bên phải đường
    """
    # Kích thước nhà ngẫu nhiên (nhà ống Sài Gòn: hẹp ngang, sâu vào trong)
    width = random.uniform(3.5, 6.0)    # Mặt tiền (trục X)
    depth = random.uniform(6.0, 10.0)   # Chiều sâu vào trong (trục Y)
    floors = random.randint(2, 5)       # Số tầng
    floor_h = random.uniform(3.0, 3.5)  # Chiều cao mỗi tầng
    height = floors * floor_h

    # Vị trí Y: bên trái hoặc bên phải đường
    street_half_width = 4.0  # Nửa chiều rộng đường
    y_pos = side * (street_half_width + depth / 2)

    wall_mat = random.choice(wall_colors)

    # --- THÂN NHÀ CHÍNH ---
    building = create_box(
        f"Building_{index}",
        x_pos, y_pos, height / 2,
        width / 2, depth / 2, height / 2,
        wall_mat
    )

    # --- CỬA RA VÀO (Tầng trệt) ---
    door_w = min(width * 0.5, 2.5)
    door_h = 2.8
    door_y = y_pos - side * (depth / 2 - 0.05)
    create_box(f"Door_{index}", x_pos, door_y, door_h / 2, door_w / 2, 0.08, door_h / 2, mat_door)

    # --- CỬA SỔ CÁC TẦNG ---
    for f in range(1, floors):
        win_y_center = f * floor_h + floor_h / 2 + 0.3
        num_windows = random.randint(1, min(3, int(width / 1.8)))
        win_spacing = width / (num_windows + 1)

        for w in range(num_windows):
            win_x = x_pos - width / 2 + win_spacing * (w + 1)
            win_front_y = y_pos - side * (depth / 2 - 0.05)
            create_box(
                f"Window_{index}_F{f}_W{w}",
                win_x, win_front_y, win_y_center,
                0.5, 0.06, 0.65,
                mat_window
            )

    # --- MÁI HIÊN (AWNING) TẦNG TRỆT ---
    if random.random() > 0.2:
        awning_mat = random.choice(awning_colors)
        awning_y = y_pos - side * (depth / 2 + 0.6)
        create_box(
            f"Awning_{index}",
            x_pos, awning_y, floor_h - 0.3,
            width / 2 + 0.3, 0.7, 0.06,
            awning_mat
        )

    # --- BAN CÔNG TẦNG 2 (Đặc trưng nhà phố Bùi Viện) ---
    if floors >= 2 and random.random() > 0.3:
        balc_y = y_pos - side * (depth / 2 + 0.4)
        balc_z = floor_h + 0.1

        # Sàn ban công
        create_box(f"BalcFloor_{index}", x_pos, balc_y, balc_z, width / 2 + 0.2, 0.5, 0.05, mat_balcony)

        # Lan can ban công
        create_box(f"BalcRail_{index}", x_pos, balc_y - side * 0.45, balc_z + 0.45, width / 2 + 0.2, 0.03, 0.4, mat_balcony)

        # Chậu cây trên ban công
        if random.random() > 0.4:
            pot_x = x_pos + random.uniform(-width / 4, width / 4)
            create_box(f"Pot_{index}", pot_x, balc_y, balc_z + 0.25, 0.15, 0.15, 0.2, mat_pot)
            create_box(f"Plant_{index}", pot_x, balc_y, balc_z + 0.65, 0.25, 0.25, 0.2, mat_plant)

    # --- BIỂN HIỆU / BẢNG TÊN QUÁN ---
    if random.random() > 0.15:
        sign_mat = random.choice(neon_colors)
        sign_y = y_pos - side * (depth / 2 + 0.15)
        sign_z = floor_h * 0.65
        sign_w = width * random.uniform(0.5, 0.85)
        sign_h = random.uniform(0.5, 0.9)

        # Bảng nền
        create_box(f"SignBoard_{index}", x_pos, sign_y, sign_z, sign_w / 2, 0.04, sign_h / 2, mat_sign_board)
        # Chữ neon (mỏng hơn, đè lên trên bảng)
        create_box(f"SignNeon_{index}", x_pos, sign_y - side * 0.03, sign_z, sign_w / 2 - 0.15, 0.02, sign_h / 2 - 0.08, sign_mat)

    # --- MÁY LẠNH GẮN TƯỜNG (Đặc sản nhà phố VN) ---
    if floors >= 2 and random.random() > 0.4:
        ac_x = x_pos + random.choice([-1, 1]) * (width / 2 - 0.5)
        ac_y = y_pos - side * (depth / 2 - 0.2)
        ac_z = random.uniform(floor_h + 1.5, floor_h + 2.5)
        create_box(f"AC_{index}", ac_x, ac_y, ac_z, 0.4, 0.2, 0.25, mat_ac_unit)

    return width

# ===========================
# DỰNG CON PHỐ BÙI VIỆN
# ===========================

# --- MẶT ĐƯỜNG ---
street_length = 80.0
create_box("Road", street_length / 2, 0, -0.05, street_length / 2, 3.8, 0.05, mat_road)

# --- VỈA HÈ 2 BÊN ---
create_box("Sidewalk_Left", street_length / 2, 5.2, 0.05, street_length / 2, 1.5, 0.08, mat_sidewalk)
create_box("Sidewalk_Right", street_length / 2, -5.2, 0.05, street_length / 2, 1.5, 0.08, mat_sidewalk)

# --- DÃY NHÀ 2 BÊN ĐƯỜNG ---
x_cursor_left = 1.0
x_cursor_right = 1.5
idx = 0

while x_cursor_left < street_length - 2 or x_cursor_right < street_length - 2:
    # Bên trái đường (Y dương)
    if x_cursor_left < street_length - 2:
        w = create_building(x_cursor_left, 1, idx)
        x_cursor_left += w + random.uniform(0.3, 1.2)  # Khoảng cách giữa các nhà
        idx += 1

    # Bên phải đường (Y âm)
    if x_cursor_right < street_length - 2:
        w = create_building(x_cursor_right, -1, idx)
        x_cursor_right += w + random.uniform(0.3, 1.2)
        idx += 1

# --- BÀN GHẾ NHỰA VỈA HÈ (Đặc sản Bùi Viện) ---
for i in range(0, int(street_length), 6):
    if random.random() > 0.35:
        tx = i + random.uniform(1, 4)
        t_side = random.choice([1, -1])
        ty = t_side * random.uniform(4.2, 5.5)

        # Bàn nhựa đỏ
        create_box(f"Table_{i}", tx, ty, 0.35, 0.3, 0.3, 0.02, mat_table)
        # Chân bàn
        create_box(f"TableLeg_{i}", tx, ty, 0.17, 0.03, 0.03, 0.16, mat_pole)

        # 2-4 ghế đẩu xung quanh bàn
        for s in range(random.randint(2, 4)):
            sx_off = random.uniform(-0.5, 0.5)
            sy_off = random.uniform(-0.5, 0.5)
            create_box(f"Stool_{i}_{s}", tx + sx_off, ty + sy_off, 0.2, 0.12, 0.12, 0.01, mat_stool)
            create_box(f"StoolLeg_{i}_{s}", tx + sx_off, ty + sy_off, 0.1, 0.02, 0.02, 0.1, mat_pole)

# --- CỘT ĐÈN ĐƯỜNG ---
for i in range(2, int(street_length), 10):
    pole_side = 1 if (i // 10) % 2 == 0 else -1
    pole_y = pole_side * 3.9
    # Thân cột
    create_box(f"LampPole_{i}", i, pole_y, 2.5, 0.06, 0.06, 2.5, mat_pole)
    # Bóng đèn
    create_box(f"LampBulb_{i}", i, pole_y, 5.2, 0.2, 0.2, 0.1, mat_light_warm)

# --- DÂY ĐIỆN CHĂNG NGANG ĐƯỜNG (Đặc trưng phố cổ VN) ---
for i in range(5, int(street_length), 8):
    wire_x = i + random.uniform(-1, 1)
    wire_z = random.uniform(5.5, 8.0)
    # Dây điện ngang qua đường
    create_box(f"Wire_{i}", wire_x, 0, wire_z, 0.01, 4.0, 0.01, mat_wire)

    # Đèn lồng treo giữa đường (ngẫu nhiên)
    if random.random() > 0.5:
        lantern_x = wire_x + random.uniform(-0.5, 0.5)
        create_box(f"Lantern_{i}", lantern_x, random.uniform(-1, 1), wire_z - 0.5, 0.15, 0.15, 0.2, mat_lantern)

# --- THÙNG BIA / THÙNG PHUY ---
for i in range(3, int(street_length), 12):
    if random.random() > 0.4:
        bx = i + random.uniform(0, 3)
        b_side = random.choice([1, -1])
        by = b_side * random.uniform(5.0, 6.0)
        create_box(f"Barrel_{i}", bx, by, 0.4, 0.2, 0.2, 0.4, mat_barrel)

# === ÁNH SÁNG & CAMERA ===

# Ánh sáng chính (đèn đường warm light ban đêm)
bpy.ops.object.light_add(type='SUN', location=(40, 0, 30))
sun = bpy.context.active_object
sun.name = "Sunlight"
sun.data.energy = 1.0
sun.data.color = (1.0, 0.9, 0.75)
sun.rotation_euler = (math.radians(45), 0, math.radians(30))

# Thêm ambient light
bpy.ops.object.light_add(type='AREA', location=(40, 0, 12))
area = bpy.context.active_object
area.name = "AmbientFill"
area.data.energy = 200
area.data.size = 80
area.data.color = (0.8, 0.75, 0.9)

# Camera nhìn từ đầu phố
bpy.ops.object.camera_add(location=(-5, 0, 4), rotation=(math.radians(78), 0, math.radians(-90)))
cam = bpy.context.active_object
cam.name = "StreetView_Camera"
cam.data.lens = 28  # Góc rộng giống mắt người
bpy.context.scene.camera = cam

# === CẤU HÌNH RENDER ===
bpy.context.scene.render.engine = 'EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

print("=" * 50)
print("✅ ĐÃ DỰNG XONG CON PHỐ BÙI VIỆN!")
print(f"  📊 Tổng số Objects: {len(bpy.data.objects)}")
print(f"  📏 Chiều dài phố: {street_length} mét")
print(f"  🏠 Số nhà: ~{idx} căn")
print("=" * 50)
print("💡 Bấm Numpad 0 để xem qua Camera")
print("💡 Export sang Unity: File > Export > FBX")
