import pyautogui
import time
import random
import cv2
import numpy as np
import win32api
import win32con
import sys
import os

def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和打包后环境"""
    try:
        # 打包后的环境
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 全局运行状态
running = True

def stop_all_tasks():
    """停止所有任务"""
    global running
    running = False
    print("[STOP] 全局停止标志已设置")

def reset_running():
    """重置运行状态"""
    global running
    running = True

def wait_with_interrupt(seconds):
    """可中断延迟"""
    global running
    for _ in range(int(seconds * 10)):
        if not running:
            return False  # 返回False表示被中断
        time.sleep(0.1)
    return True  # 返回True表示正常完成


def click_image(img_path, threshold=0.8, delay=0.3):
    """点击图片中心"""
    try:
        # 使用 resource_path 获取正确路径
        actual_path = resource_path(img_path)

        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(actual_path)  # 使用实际路径
        if template is None:
            print(f"[ERROR] 未找到图片文件：{actual_path}")
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
            if not wait_with_interrupt(delay):
                return False
            # 鼠标移到安全位置
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(50, screen_height - 50, duration=0.2)
            time.sleep(0.5)
            return True
    except Exception as e:
        print(f"[ERROR] click_image异常: {e}")
    return False

def clear_and_type(text):
    """点击后清空输入框并输入新内容"""
    time.sleep(0.2)
    for _ in range(3):
        pyautogui.press('backspace')
        time.sleep(0.15)
    pyautogui.typewrite(text, interval=0.12)
    time.sleep(0.3)

def drag_in_game(start_x1, start_y1, start_x2, start_y2, duration=0.5):
    """在游戏窗口中模拟拖动操作"""
    steps = 30
    dx = (start_x2 - start_x1) / steps
    dy = (start_y2 - start_y1) / steps
    delay = duration / steps

    win32api.SetCursorPos((start_x1, start_y1))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)

    for i in range(steps):
        nx = int(start_x1 + dx * i)
        ny = int(start_y1 + dy * i)
        win32api.SetCursorPos((nx, ny))
        time.sleep(delay)

    win32api.SetCursorPos((start_x2, start_y2))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print(f"[INFO] 拖动完成：({start_x1},{start_y1}) -> ({start_x2},{start_y2})")