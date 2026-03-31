from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
import shutil

driver = webdriver.Chrome()

driver.get("https://cybersource.cyberorigin.ai/")

print("请登录账号...")
time.sleep(60)

video_folder = "segments"
uploaded_folder = "uploaded"

videos = os.listdir(video_folder)

for video in videos:

    video_path = os.path.abspath(os.path.join(video_folder, video))

    print("准备上传:", video)

    try:

        # 找到文件上传框
        file_input = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input[type='file']"))
        )

        file_input.send_keys(video_path)

        time.sleep(2)

        # 点击开始上传
        upload_button = driver.find_element(By.XPATH,"//button[contains(text(),'开始上传')]")
        upload_button.click()

        print("正在上传...")

        # 等待上传完成（检测按钮重新出现）
        WebDriverWait(driver,300).until(
            EC.presence_of_element_located((By.XPATH,"//button[contains(text(),'开始上传')]"))
        )

        print("上传完成:", video)

        shutil.move(video_path, os.path.join(uploaded_folder, video))

        driver.refresh()

        time.sleep(5)

    except Exception as e:

        print("上传失败:", video)
        print(e)

print("全部视频上传完成")