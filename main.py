import threading
import keyboard
from bagua import find_bagua_npc
from utils import running
import time

running = False  # 控制脚本运行状态

def start_script():
    global running
    if not running:
        running = True
        print("[INFO] 脚本启动")
        threading.Thread(target=run_loop).start()
    else:
        print("[INFO] 脚本已在运行中")

def stop_script():
    global running
    running = False
    print("[INFO] 脚本停止")

def run_loop():
    global running
    while running:
        print("[INFO] 进入八卦循环")
        success = find_bagua_npc()
        if not success:  # 点击领取八卦奖励后返回 False
            print("[INFO] 八卦结束，退出程序")
            running = False
            break
        time.sleep(1)

# ---------- 热键绑定 ----------
keyboard.add_hotkey('f9', start_script)   # F9启动
keyboard.add_hotkey('f10', stop_script)   # F10停止

print("[INFO] 按 F9 启动脚本，F10 停止脚本")
keyboard.wait()
