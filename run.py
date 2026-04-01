import os

print("开始切割视频...")

os.system("python split_video.py")

print("视频切割完成")

print("开始上传视频...")

os.system("python upload_video.py")

print("全部流程完成")
