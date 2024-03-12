import math
import json
from paraview.simple import *
import numpy as np
import matplotlib.pyplot as plt

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


# 获取活动视图
renderView1 = GetActiveViewOrCreate('RenderView')
# 设置渲染视图的分辨率
renderView1.ViewSize = [2560, 1440]


# 初始相机设置，读取当前的相机设置
focalPoint = renderView1.CameraFocalPoint
cameraViewUp = renderView1.CameraViewUp
cameraParallelScale = renderView1.CameraParallelScale
radius = np.linalg.norm(np.array(renderView1.CameraPosition) - np.array(focalPoint))

# 循环旋转相机并截图
for angle in range(90):
    cameraX = focalPoint[0] + radius * math.cos(math.radians(4 * angle))
    cameraY = focalPoint[1] + radius * math.sin(math.radians(4 * angle))
    cameraPosition = [cameraX, cameraY, renderView1.CameraPosition[2]]

    # 更新相机设置
    renderView1.CameraPosition = cameraPosition
    renderView1.CameraFocalPoint = focalPoint
    renderView1.CameraViewUp = cameraViewUp
    renderView1.CameraParallelScale = cameraParallelScale

    # 构造并添加转换矩阵数据
    # 注意：下面的 transform_matrix 是示例，您需要根据相机的实际位置和方向计算
    transform_matrix = compute_transform_matrix(cameraPosition, focalPoint, cameraViewUp)
    transform_matrix_list = transform_matrix.tolist()
    
    # 保存RGB截图
    screenshotFilename = f'/mnt/group/yuchi/instant-ngp/scripts/database1/screenshotz_{angle:03d}.png'
    SaveScreenshot(screenshotFilename, renderView1, ImageResolution=[2560, 1440], TransparentBackground=1, CompressionLevel='0')
    # 保存深度截图
    imageDepth = renderView1.CaptureDepthBuffer()
    width=2560
    height = 1440
    depth_array = np.array(imageDepth).reshape(height, width)
    depthFilename = f'/mnt/group/yuchi/instant-ngp/scripts/database1/depthz_{angle:03d}.png'
    plt.imsave(depthFilename, depth_array, cmap='gray')
    # 获取当前活动的视图
    activeView = GetActiveViewOrCreate('RenderView')
    # 获取相机
    camera = activeView.GetActiveCamera()
    # 获取相机的参数
    position = camera.GetPosition()
    focalPoint = camera.GetFocalPoint()
    viewUp = camera.GetViewUp()
    viewAngle = camera.GetViewAngle()
    # 构造一个字典来保存这些参数
    cameraSettings = {
        'Position': position,
        'FocalPoint': focalPoint,
        'ViewUp': viewUp,
        'ViewAngle': viewAngle
    }
    # 将这些参数保存到文件
    cameraSettingsFilename = f'/mnt/group/yuchi/instant-ngp/scripts/database1_pvcc/camera_settingsz_{angle:03d}.pvcc'
    with open(cameraSettingsFilename, 'w') as file:
        json.dump(cameraSettings, file)


# 循环旋转相机并截图
for angle in range(90):
    cameraX = focalPoint[0] + radius * math.cos(math.radians(4 * angle))
    cameraZ = focalPoint[2] + radius * math.sin(math.radians(4 * angle))
    cameraPosition = [cameraX, renderView1.CameraPosition[1], cameraZ]

    # 更新相机设置
    renderView1.CameraPosition = cameraPosition
    renderView1.CameraFocalPoint = focalPoint
    renderView1.CameraViewUp = cameraViewUp
    renderView1.CameraParallelScale = cameraParallelScale

    # 构造并添加转换矩阵数据
    # 注意：下面的 transform_matrix 是示例，您需要根据相机的实际位置和方向计算
    transform_matrix = compute_transform_matrix(cameraPosition, focalPoint, cameraViewUp)
    transform_matrix_list = transform_matrix.tolist()
    
    # 保存RGB截图
    screenshotFilename = f'/mnt/group/yuchi/instant-ngp/scripts/database1/screenshoty_{angle:03d}.png'
    SaveScreenshot(screenshotFilename, renderView1, ImageResolution=[2560, 1440], TransparentBackground=1, CompressionLevel='0')
    # 保存深度截图
    imageDepth = renderView1.CaptureDepthBuffer()
    width = 2560
    height = 1440
    depth_array = np.array(imageDepth).reshape(height, width)
    depthFilename = f'/mnt/group/yuchi/instant-ngp/scripts/database1/depthy_{angle:03d}.png'
    plt.imsave(depthFilename, depth_array, cmap='gray')
    # 获取当前活动的视图
    activeView = GetActiveViewOrCreate('RenderView')
    # 获取相机
    camera = activeView.GetActiveCamera()
    # 获取相机的参数
    position = camera.GetPosition()
    focalPoint = camera.GetFocalPoint()
    viewUp = camera.GetViewUp()
    viewAngle = camera.GetViewAngle()
    # 构造一个字典来保存这些参数
    cameraSettings = {
        'Position': position,
        'FocalPoint': focalPoint,
        'ViewUp': viewUp,
        'ViewAngle': viewAngle
    }
    # 将这些参数保存到文件
    cameraSettingsFilename = f'/mnt/group/yuchi/instant-ngp/scripts/database1_pvcc/camera_settingsy_{angle:03d}.pvcc'
    with open(cameraSettingsFilename, 'w') as file:
        json.dump(cameraSettings, file)
