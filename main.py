import keyboard
from bagua import find_bagua_npc
from tianlao import tianlao
import threading

# 全局运行标志
running = True

def start_bagua():
    print("[INFO] 八卦启动 (F9)")
    threading.Thread(target=find_bagua_npc).start()

def start_tianlao():
    print("[INFO] 天牢启动 (F6)")
    threading.Thread(target=tianlao).start()

print("[INFO] 等待按键触发...")
# F9 启动八卦
keyboard.add_hotkey('F9', start_bagua)
# F6 启动天牢
keyboard.add_hotkey('F6', start_tianlao)

# 持续监听按键
keyboard.wait('esc')  # 按 Esc 可以退出程序
running = False
print("[INFO] 程序退出")
