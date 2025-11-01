import pyautogui
import time
import random
import cv2
import numpy as np

# 全局控制变量
running = True

def wait_with_interrupt(seconds):
    """可中断延迟，每0.1秒检查一次running状态"""
    global running
    for _ in range(int(seconds * 10)):
        if not running:
            break
        time.sleep(0.1)

def click_image(img_path, threshold=0.8, delay=0.5):
    """点击图片中心，点击后移动鼠标到安全区域，并延迟0.3秒"""
    try:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(img_path)
        if template is None:
            print(f"[ERROR] 未找到图片文件：{img_path}")
            return False
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        if len(loc[0]) > 0:
            y, x = loc[0][0], loc[1][0]
            h, w = template.shape[:2]
            x += w // 2 + random.randint(-2, 2)
            y += h // 2 + random.randint(-2, 2)
            pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.click()
            wait_with_interrupt(delay)  # 原有延迟保留
            # ---------------------- 新增全局动作 ----------------------
            # 鼠标移到安全位置
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(50, screen_height - 50, duration=0.2)
            # 给慢电脑反应时间，1秒延迟
            time.sleep(0.5)
            # ---------------------------------------------------------
            return True
    except Exception as e:
        print(f"[ERROR] click_image异常: {e}")
    return False

def clear_and_type(text):
    """点击后清空输入框并输入新内容"""
    time.sleep(0.3)  # 等待焦点稳定
    for _ in range(5):
        pyautogui.press('backspace')
        time.sleep(0.15)
    pyautogui.typewrite(text, interval=0.12)
    time.sleep(0.3)
