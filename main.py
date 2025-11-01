import threading
import time
import pyautogui
import keyboard
import tkinter as tk
from bagua import find_bagua_npc
from tianlao import tianlao
from utils import wait_with_interrupt, running

# ---------------- 全局运行状态 ----------------
task_running = False
first_run_xunren = True
status_var = None  # 用于显示当前运行状态

# ---------------- 异常安全的图片识别 ----------------
def safe_locate_center(image_path, confidence=0.8):
    """尝试获取图片中心坐标，找不到返回 None"""
    try:
        return pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None
    except Exception as e:
        print(f"[ERROR] 图片识别异常 {image_path}: {e}")
        return None

# ---------------- 拖动元素到目标位置 ----------------
def drag_element(start_pos, target_pos, duration=0.5):
    """前台鼠标拖动 start_pos -> target_pos"""
    pyautogui.moveTo(*start_pos)
    pyautogui.mouseDown()
    pyautogui.moveTo(*target_pos, duration=duration)
    pyautogui.mouseUp()
    print(f"[INFO] 拖动完成：{start_pos} -> {target_pos}")

# ---------------- 任务启动线程 ----------------
def start_task():
    global task_running, first_run_xunren
    if task_running:
        print("[WARN] 任务已经在运行中")
        return

    task_running = True
    status_var.set("状态：运行中")
    print("[INFO] 按 F10 可停止任务")

    # ---------------- 获取八卦 daboss 等待时间 ----------------
    daboss_wait_time = app_window.daboss_time_var.get()
    daboss_wait_time = max(10, min(120, daboss_wait_time))  # 限制在 10-120 秒

    # ---------------- 步骤 1：识别并拖动自动寻人 ----------------
    xunren_pos = safe_locate_center("picture/xunren.png")
    if not xunren_pos:
        keyboard.send('f12')
        wait_with_interrupt(0.5)
        xunren_pos = safe_locate_center("picture/xunren.png")

    if xunren_pos:
        # 拖动至左下角安全位置
        screen_width, screen_height = pyautogui.size()
        safe_pos = (50, screen_height - 50)
        drag_element((xunren_pos.x, xunren_pos.y), safe_pos)
        wait_with_interrupt(0.5)

    # ---------------- 步骤 2：按 F7 再 F11 ----------------
    keyboard.send('f7')
    wait_with_interrupt(0.2)
    keyboard.send('f11')
    wait_with_interrupt(0.5)

    # ---------------- 步骤 3：启动选择的任务 ----------------
    try:
        if app_window.bagua_var.get() and app_window.tianlao_var.get():
            print("[INFO] 同时勾选八卦和天牢，先执行八卦")
            status_var.set("状态：八卦中")
            find_bagua_npc(daboss_wait_time=daboss_wait_time)
            print("[INFO] 八卦完成，开始天牢")
            status_var.set("状态：天牢中")
            tianlao()
        elif app_window.bagua_var.get():
            print("[INFO] 执行八卦")
            status_var.set("状态：八卦中")
            find_bagua_npc(daboss_wait_time=daboss_wait_time)
        elif app_window.tianlao_var.get():
            print("[INFO] 执行天牢")
            status_var.set("状态：天牢中")
            tianlao()
        else:
            print("[WARN] 未选择任何任务")
            status_var.set("状态：未选择任务")
    except Exception as e:
        print(f"[ERROR] 任务执行异常: {e}")
        status_var.set("状态：异常停止")
    finally:
        task_running = False
        status_var.set("状态：已停止")
        print("[INFO] 任务已结束")

# ---------------- 停止任务 ----------------
def stop_task():
    global task_running
    task_running = False
    status_var.set("状态：已停止")
    print("[INFO] 已手动停止任务")

# ---------------- GUI ----------------
app_window = tk.Tk()
app_window.title("游戏辅助")
app_window.geometry("350x250")
app_window.resizable(False, False)

# 标题
tk.Label(app_window, text="选择任务并启动", font=("微软雅黑", 14, "bold")).pack(pady=5)

# 勾选项（默认勾选八卦和天牢）
app_window.bagua_var = tk.BooleanVar(value=True)
app_window.tianlao_var = tk.BooleanVar(value=True)
tk.Checkbutton(app_window, text="八卦", variable=app_window.bagua_var, font=("微软雅黑", 12)).pack(pady=5)
tk.Checkbutton(app_window, text="天牢", variable=app_window.tianlao_var, font=("微软雅黑", 12)).pack(pady=5)

# 八卦daboss等待时间输入
tk.Label(app_window, text="八卦打Boss等待时间 (10-120秒)", font=("微软雅黑", 10)).pack()
app_window.daboss_time_var = tk.IntVar(value=30)
daboss_entry = tk.Entry(app_window, textvariable=app_window.daboss_time_var, width=10, font=("微软雅黑", 12))
daboss_entry.pack(pady=2)

# 当前状态显示
status_var = tk.StringVar(value="状态：未运行")
tk.Label(app_window, textvariable=status_var, font=("微软雅黑", 12), fg="blue").pack(pady=10)

# 提示信息
tk.Label(app_window, text="按 F9 启动，F10 停止", font=("微软雅黑", 10)).pack(pady=5)

# ---------------- 热键绑定 ----------------
keyboard.add_hotkey('f9', lambda: threading.Thread(target=start_task).start())
keyboard.add_hotkey('f10', stop_task)

# 关闭窗口时停止任务
def on_closing():
    stop_task()
    app_window.destroy()

app_window.protocol("WM_DELETE_WINDOW", on_closing)

# ---------------- 启动 GUI ----------------
app_window.mainloop()
