import os
import subprocess

input_folder = "videos"
output_folder = "segments"

segment_time = 900  # 15分钟

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file in os.listdir(input_folder):

    if file.endswith(".mp4"):

        input_path = os.path.join(input_folder, file)

        filename = os.path.splitext(file)[0]

        output_path = os.path.join(output_folder, filename + "_%03d.mp4")

        print("正在处理:", file)

        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-f", "segment",
            "-segment_time", str(segment_time),
            "-reset_timestamps", "1",
            output_path
        ]

        subprocess.run(cmd)

print("全部视频切割完成")