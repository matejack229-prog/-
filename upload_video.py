from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

import os
import time
import shutil

UPLOAD_URL = "https://cybersource.cyberorigin.ai/"
VIDEO_FOLDER = "segments"
UPLOADED_FOLDER = "uploaded"
LOGIN_WAIT_SECONDS = 120
UPLOAD_WAIT_SECONDS = 600


def ensure_folders():
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)
    if not os.path.exists(UPLOADED_FOLDER):
        os.makedirs(UPLOADED_FOLDER)


def get_video_files(folder):
    video_exts = (".mp4", ".mov", ".avi", ".mkv")
    files = []
    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if os.path.isfile(full_path) and f.lower().endswith(video_exts):
            files.append(f)
    return sorted(files)


def wait_for_upload_page(driver, timeout=120):
    wait = WebDriverWait(driver, timeout)
    file_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    return file_input


def click_upload_button(driver, timeout=30):
    wait = WebDriverWait(driver, timeout)
    upload_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., '开始上传')]"))
    )
    upload_button.click()


def wait_for_upload_success(driver, timeout=UPLOAD_WAIT_SECONDS):
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(., '上传成功')]"))
    )


def upload_one_video(driver, video_path, video_name):
    print(f"准备上传: {video_name}")

    file_input = wait_for_upload_page(driver, timeout=60)
    file_input.send_keys(video_path)
    time.sleep(2)

    click_upload_button(driver, timeout=30)
    print(f"正在上传: {video_name}")

    wait_for_upload_success(driver, timeout=UPLOAD_WAIT_SECONDS)
    print(f"上传完成: {video_name}")


def main():
    ensure_folders()
    videos = get_video_files(VIDEO_FOLDER)

    if not videos:
        print("segments 文件夹中没有可上传的视频。")
        return

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(UPLOAD_URL)

        print("请先手动登录账号，并进入可上传页面。")
        print(f"程序将等待 {LOGIN_WAIT_SECONDS} 秒，你也可以尽快完成登录。")
        time.sleep(LOGIN_WAIT_SECONDS)

        wait_for_upload_page(driver, timeout=120)
        print("检测到上传控件，开始批量上传。")

        for video in videos:
            video_path = os.path.abspath(os.path.join(VIDEO_FOLDER, video))

            try:
                upload_one_video(driver, video_path, video)

                target_path = os.path.join(UPLOADED_FOLDER, video)
                shutil.move(video_path, target_path)
                print(f"已移动到 uploaded: {video}")

                driver.refresh()
                time.sleep(5)

            except (TimeoutException, StaleElementReferenceException, Exception) as e:
                print(f"上传失败: {video}")
                print(f"错误信息: {e}")

                try:
                    driver.refresh()
                    time.sleep(5)
                except Exception:
                    pass

        print("全部视频上传流程已执行完毕。")

    finally:
        pass


if __name__ == "__main__":
    main()
