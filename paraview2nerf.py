import json
import numpy as np
import os


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def compute_transform_matrix(camera_position, camera_focal_point, camera_view_up):
    D = normalize(np.array(camera_focal_point) - np.array(camera_position))
    R = normalize(np.cross(D, camera_view_up))
    U = np.cross(R, D)
    
    # 计算原始平移向量
    original_translation = np.array(camera_position) - np.array(camera_focal_point)
    # 计算原始平移向量的模长
    original_translation_magnitude = np.linalg.norm(original_translation)
    # 计算缩放因子，以使平移向量的模长等于4
    scale_factor = 4 / original_translation_magnitude
    # 应用缩放因子
    scaled_translation = original_translation * scale_factor
    
    transform_matrix = np.array([
        [R[0], U[0], -D[0], scaled_translation[0]],
        [R[1], U[1], -D[1], scaled_translation[1]],
        [R[2], U[2], -D[2], scaled_translation[2]],
        [  0,   0,    0,                1]
    ])
    return transform_matrix



# 假设的图像分辨率和视场角
w, h = 2560, 1440
view_angle_deg_y = 30.0  # 假定的垂直视场角，您需要替换为实际值
view_angle_rad_y = np.deg2rad(view_angle_deg_y)

# 初始化JSON结构
paraview2nerf = {
    "camera_angle_x": 2 * np.arctan(np.tan(view_angle_rad_y/2)*(w/h)),
    "camera_angle_y": view_angle_rad_y,
    "w": w,
    "h": h,
    "enable_depth_loading": True,
    "frames": []
}

# 处理每个相机配置
for i in range(9):  # 假设有90个相机配置
    file_name = f"/mnt/group/yuchi/instant-ngp/scripts/images_test_pvcc/camera_settingsz_{10*i:03}.pvcc"  # 格式化文件名
    with open(file_name, 'r') as f:
        cam_settings = json.load(f)
    
    # 计算外参矩阵（这里简化处理，实际需要根据ParaView相机模型调整）
    position = cam_settings['Position']
    focal_point = cam_settings['FocalPoint']
    view_up = cam_settings['ViewUp']
    
    transform_matrix = compute_transform_matrix(position, focal_point, view_up)
    
    transform_matrix = transform_matrix.tolist()
    
    # 添加到frames
    paraview2nerf['frames'].append({
        "file_path": f"/mnt/group/yuchi/instant-ngp/scripts/images_test/screenshotz_{10*i:03}.png",
        "depth_path": f"/mnt/group/yuchi/instant-ngp/scripts/images_test/depthz_{10*i:03}.png",
        "transform_matrix": transform_matrix
    })
    
# 处理每个相机配置
for i in range(9):  # 假设有90个相机配置
    file_name = f"/mnt/group/yuchi/instant-ngp/scripts/images_test_pvcc/camera_settingsy_{10*i:03}.pvcc"  # 格式化文件名
    with open(file_name, 'r') as f:
        cam_settings = json.load(f)
    
    # 计算外参矩阵（这里简化处理，实际需要根据ParaView相机模型调整）
    position = cam_settings['Position']
    focal_point = cam_settings['FocalPoint']
    view_up = cam_settings['ViewUp']
    
    transform_matrix = compute_transform_matrix(position, focal_point, view_up)
    
    transform_matrix = transform_matrix.tolist()
    
    # 添加到frames
    paraview2nerf['frames'].append({
        "file_path": f"/mnt/group/yuchi/instant-ngp/scripts/images_test/screenshoty_{10*i:03}.png",
        "depth_path": f"/mnt/group/yuchi/instant-ngp/scripts/images_test/depthy_{10*i:03}.png",
        "transform_matrix": transform_matrix
    })

# 保存为JSON文件
with open('paraview2nerf.json', 'w') as f:
    json.dump(paraview2nerf, f, indent=2)
