import threading
import time
import pyautogui
import keyboard
import tkinter as tk
from bagua import find_bagua_npc
from tianlao import tianlao
from utils import wait_with_interrupt, running, stop_all_tasks, reset_running


# 新增的公益声明函数
def show_public_welfare_notice():
    """显示公益软件声明弹窗"""
    notice_text = """
════════════ 使用须知 ════════════

📢 本软件为完全免费的公益软件
🚫 严禁任何形式的倒卖和收费行为
🔒 软件仅用于学习研究，请于24小时内删除

项目网站：https://github.com/lickhing/xyd

【重要提示】
如果您付费购买了本软件，请立即要求退款并举报卖家

"""

    # 创建弹窗
    notice_window = tk.Toplevel()
    notice_window.title("使用须知")
    notice_window.geometry("450x350")
    notice_window.resizable(False, False)
    notice_window.attributes('-topmost', True)

    # 标题
    title_label = tk.Label(notice_window, text="⚠️ 使用须知 ⚠️",
                           font=("微软雅黑", 14, "bold"),
                           fg="red")
    title_label.pack(pady=10)

    # 声明内容
    text_widget = tk.Text(notice_window, font=("微软雅黑", 10),
                          wrap='word', height=15, width=50,
                          relief='solid', bd=1, padx=10, pady=10)
    text_widget.insert('1.0', notice_text)
    text_widget.config(state='disabled')
    text_widget.pack(padx=10, pady=5)

    # 关闭按钮（可选）
    def on_close():
        notice_window.destroy()

    close_btn = tk.Button(notice_window, text="关闭",
                          font=("微软雅黑", 10),
                          command=on_close, width=10)
    close_btn.pack(pady=10)

    # 允许正常关闭（移除强制限制）
    notice_window.protocol("WM_DELETE_WINDOW", on_close)

    # 等待窗口关闭（但不强制）
    notice_window.transient(app_window)
    notice_window.grab_set()
    app_window.wait_window(notice_window)


# ---------------- 全局运行状态 ----------------
task_running = False
first_run_xunren = True
status_var = None


# ---------------- 异常安全的图片识别 ----------------
def safe_locate_center(image_path, confidence=0.8):
    """尝试获取图片中心坐标，找不到返回 None"""
    try:
        # 使用 resource_path 获取正确路径
        from utils import resource_path
        actual_path = resource_path(image_path)
        return pyautogui.locateCenterOnScreen(actual_path, confidence=confidence)
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


# ---------------- 停止任务 ----------------
def stop_task():
    global task_running
    print("[STOP] 正在停止所有任务...")

    task_running = False
    stop_all_tasks()  # 设置全局停止标志

    # 确保状态立即更新
    status_var.set("状态：已停止")
    print("[STOP] 所有任务已停止，等待新的F9命令")


# ---------------- 任务启动线程 ----------------
def start_task():
    global task_running, first_run_xunren
    if task_running:
        print("[WARN] 任务已经在运行中")
        return

    # 重置所有状态，开始新任务
    task_running = True
    first_run_xunren = True
    reset_running()  # 重置全局运行标志
    status_var.set("状态：运行中")
    print("[INFO] 按 F10 可停止任务")

    # ---------------- 获取八卦 daboss 等待时间 ----------------
    daboss_wait_time = app_window.daboss_time_var.get()
    daboss_wait_time = max(10, min(120, daboss_wait_time))

    try:
        # ---------------- 步骤 1：识别并拖动自动寻人 ----------------
        if not running: return

        xunren_pos = safe_locate_center("picture/xunren.png")
        if not xunren_pos:
            if not running: return
            keyboard.send('f12')
            if not wait_with_interrupt(0.5): return
            xunren_pos = safe_locate_center("picture/xunren.png")

        if xunren_pos and running:
            screen_width, screen_height = pyautogui.size()
            safe_pos = (50, screen_height - 50)
            drag_element((xunren_pos.x, xunren_pos.y), safe_pos)
            if not wait_with_interrupt(0.5): return

        # ---------------- 步骤 2：按 F7 再 F11 ----------------
        if not running: return
        keyboard.send('f7')
        if not wait_with_interrupt(0.2): return
        keyboard.send('f11')
        if not wait_with_interrupt(0.5): return

        # ---------------- 步骤 3：启动选择的任务 ----------------
        if not running: return

        if app_window.bagua_var.get() and app_window.tianlao_var.get():
            print("[INFO] 同时勾选八卦和天牢，先执行八卦")
            status_var.set("状态：八卦中")
            find_bagua_npc(daboss_wait_time=daboss_wait_time)

            # 修复：检查 task_running 而不是 running
            if task_running and running:
                print("[INFO] 八卦完成，开始天牢")
                status_var.set("状态：天牢中")
                tianlao()
            else:
                print("[INFO] 八卦被停止，不执行天牢")

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
        print("[INFO] 回到等待状态，按F9可重新开始")


# ---------------- GUI ----------------
app_window = tk.Tk()
app_window.title("AutoXYD")
app_window.geometry("400x300")  # 稍微调整窗口大小
app_window.resizable(False, False)

# 在显示主窗口前先显示公益声明
show_public_welfare_notice()

# 标题
tk.Label(app_window, text="选择任务并启动", font=("微软雅黑", 14, "bold")).pack(pady=5)

# 任务选择（八卦和天牢放在同一行）
task_frame = tk.Frame(app_window)
task_frame.pack(pady=10)

app_window.bagua_var = tk.BooleanVar(value=True)
app_window.tianlao_var = tk.BooleanVar(value=True)
tk.Checkbutton(task_frame, text="八卦", variable=app_window.bagua_var, font=("微软雅黑", 12)).grid(row=0, column=0, padx=30)
tk.Checkbutton(task_frame, text="天牢", variable=app_window.tianlao_var, font=("微软雅黑", 12)).grid(row=0, column=1, padx=30)

# 八卦daboss等待时间输入
tk.Label(app_window, text="八卦打Boss等待时间 (10-120秒)", font=("微软雅黑", 10)).pack()
app_window.daboss_time_var = tk.IntVar(value=30)
daboss_entry = tk.Entry(app_window, textvariable=app_window.daboss_time_var, width=10, font=("微软雅黑", 12))
daboss_entry.pack(pady=2)

# 新增：快捷键设置（放在同一行）
shortcut_frame = tk.Frame(app_window)
shortcut_frame.pack(pady=10)

# 二武快捷键（左边）
tk.Label(shortcut_frame, text="二武快捷键", font=("微软雅黑", 10)).grid(row=0, column=0, padx=5)
app_window.boss_key_var = tk.StringVar(value="b")  # 默认值
boss_key_entry = tk.Entry(shortcut_frame, textvariable=app_window.boss_key_var, width=8, font=("微软雅黑", 12))
boss_key_entry.grid(row=1, column=0, padx=5)

# 领奖武功快捷键（右边）
tk.Label(shortcut_frame, text="领奖快捷键", font=("微软雅黑", 10)).grid(row=0, column=1, padx=5)
app_window.reward_key_var = tk.StringVar(value="n")  # 默认值
reward_key_entry = tk.Entry(shortcut_frame, textvariable=app_window.reward_key_var, width=8, font=("微软雅黑", 12))
reward_key_entry.grid(row=1, column=1, padx=5)

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