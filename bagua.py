import pyautogui
import time
from utils import click_image, clear_and_type, wait_with_interrupt, running

first_run = True  # 是否第一次八卦

def find_bagua_npc():
    global running, first_run
    print("[INFO] 开始寻找八卦NPC...")

    # ---------- 阶段1：开始寻路找 NPC ----------
    while running:
        if click_image("picture/xunren.png"):
            print("[INFO] 点击 xunren.png，准备输入坐标")
            break
        else:
            pyautogui.press('f12')
            print("[INFO] 按 F12 打开地图")
            wait_with_interrupt(0.5)
            if click_image("picture/xunren.png"):
                print("[INFO] 点击 xunren.png，准备输入坐标")
                break
        wait_with_interrupt(0.5)

    # 第一次八卦使用固定坐标 191,271
    if first_run:
        if click_image("picture/zuobiao_x.png"):
            clear_and_type("191")
        if click_image("picture/zuobiao_y.png"):
            clear_and_type("271")
        if click_image("picture/zizhuyidong.png"):
            print("[INFO] 第一次八卦，点击自主寻路")
            wait_with_interrupt(10)

    # 等待角色移动并检测 hulve.png 或 jixu.png
    detected = False
    for attempt in range(4):  # 第一次10秒 + 3次5秒
        wait_time = 10 if attempt == 0 else 5
        wait_with_interrupt(wait_time)
        if click_image("picture/hulve.png"):
            print("[INFO] 出现 hulve.png，点击")
            wait_with_interrupt(1)
        if click_image("picture/jixu.png"):
            print("[INFO] 出现 jixu.png，点击")
            detected = True
            break
        print(f"[INFO] 第 {attempt+1} 次未检测到 hulve/jixu，重试")
        # 额外检查 npc_baguawai.png
        if click_image("picture/npc_baguawai.png"):
            print("[INFO] 点击 npc_baguawai.png，尝试检测 hulve/jixu")
            if click_image("picture/hulve.png"):
                print("[INFO] 出现 hulve.png，点击")
                wait_with_interrupt(1)
            if click_image("picture/jixu.png"):
                print("[INFO] 出现 jixu.png，点击")
                detected = True
                break
        if attempt == 3:
            print("[ERROR] 寻路失败，重新执行寻路")
            return find_bagua_npc()  # 重试寻路

    if not detected:
        print("[ERROR] 寻路失败，无法与NPC对话")
        return False

    first_run = False

    # ---------- 阶段2：进入八卦 ----------
    while not click_image("picture/jinru8ceng.png"):
        print("[INFO] 点击进入8层")
        wait_with_interrupt(1)

    # 点击后检测八卦是否已完成
    if click_image("picture/baguayiwancheng.png"):
        print("[INFO] 今日八卦已完成，点击确定去领奖")
        click_image("picture/baguayiwancheng_queding.png")
        wait_with_interrupt(1)
        go_receive_reward()
        return

    # ---------- 阶段3~5：八卦内循环 ----------
    def battle_loop():
        while running:
            # 阶段3：八卦内
            while not click_image("picture/npc_zhennei.png"):
                wait_with_interrupt(0.5)
            print("[INFO] 点击 npc_zhennei")
            wait_with_interrupt(1)

            while not click_image("picture/wozuohaozhunbeil.png"):
                wait_with_interrupt(0.5)
            print("[INFO] 点击 wozuohaozhunbeil")
            wait_with_interrupt(1)

            while not click_image("picture/jieshoutiaozhan.png"):
                wait_with_interrupt(0.5)
            print("[INFO] 点击 jieshoutiaozhan")
            wait_with_interrupt(1)

            # 阶段4：打Boss
            pyautogui.press('b')
            print("[INFO] 按B打Boss")
            wait_with_interrupt(30)
            pyautogui.press('n')
            print("[INFO] 按N给经验")
            click_image("picture/npc_zhennei.png")

            while True:
                wait_with_interrupt(1)
                if click_image("picture/jixuxiaomiexinmo.png"):
                    pyautogui.press('b')
                    print("[INFO] 按B消灭心魔")
                    wait_with_interrupt(10)
                    pyautogui.press('n')
                    print("[INFO] 按N给经验")
                    click_image("picture/npc_zhennei.png")
                elif click_image("picture/lingqujiangli.png"):
                    print("[INFO] 找到 lingqujiangli")
                    click_image("picture/lingqujiangli_2.png")
                    click_image("picture/likaibagua.png")
                    print("[INFO] 当前轮八卦结束")
                    break
                else:
                    wait_with_interrupt(1)

            # ---------- 阶段5：循环下一轮 ----------
            while running:
                if click_image("picture/npc_baguawai.png"):
                    print("[INFO] 点击 npc_baguawai.png")
                    wait_with_interrupt(1)
                    # 检测 hulve.png
                    if click_image("picture/hulve.png"):
                        print("[INFO] 出现 hulve.png，点击")
                        wait_with_interrupt(1)
                    # 检测 jixu.png
                    if click_image("picture/jixu.png"):
                        print("[INFO] 出现 jixu.png，点击")
                        wait_with_interrupt(1)
                    # 点击 jinru8ceng.png 进入下一轮八卦
                    while not click_image("picture/jinru8ceng.png"):
                        print("[INFO] 等待进入八卦8层")
                        wait_with_interrupt(1)
                    print("[INFO] 点击进入8层")
                    wait_with_interrupt(1)
                    # 检测八卦是否完成
                    if click_image("picture/baguayiwancheng.png"):
                        print("[INFO] 今日八卦已完成，点击确定去领奖")
                        click_image("picture/baguayiwancheng_queding.png")
                        wait_with_interrupt(1)
                        go_receive_reward()
                        return
                    break
                else:
                    wait_with_interrupt(1)

    battle_loop()

def go_receive_reward():
    """
    自动领取八卦奖励，优化重试逻辑
    """
    # 第一次尝试：自动寻路并等待20秒
    if click_image("picture/xunren.png"):
        print("[INFO] 点击自动寻路领奖")
        wait_with_interrupt(1)
        if click_image("picture/zuobiao_x.png"):
            clear_and_type("273")
        if click_image("picture/zuobiao_y.png"):
            clear_and_type("239")
        click_image("picture/zizhuyidong.png")
        print("[INFO] 等待20秒寻路到领奖位置")
        wait_with_interrupt(20)

        if click_image("picture/bagualingjiang.png"):
            print("[INFO] 找到 bagualingjiang.png，点击领取奖励")
            click_image("picture/bagualingjiang.png")
        if click_image("picture/zhidaol.png"):
            print("[INFO] 奖励已领过，点击确认")
            return True  # 成功领取奖励

    # 重试3次，不重新寻路，每次等待5秒
    for retry in range(3):
        print(f"[INFO] 第 {retry + 1} 次未找到奖励，等待5秒重试")
        wait_with_interrupt(5)
        if click_image("picture/bagualingjiang.png"):
            print("[INFO] 找到 bagualingjiang.png，点击领取奖励")
            click_image("picture/bagualingjiang.png")
            return True

    # 三次重试仍未找到，尝试点击 npc_lingjiang.png
    if click_image("picture/npc_lingjiang.png"):
        print("[INFO] 点击 npc_lingjiang.png，尝试触发领奖")
        wait_with_interrupt(1)
        if click_image("picture/bagualingjiang.png"):
            print("[INFO] 找到 bagualingjiang.png，点击领取奖励")
        if click_image("picture/zhidaol.png"):
            print("[INFO] 奖励已领过，点击确认")
            return True

    # 仍未成功，判定领奖寻路失败，需要重新执行领奖寻路
    print("[ERROR] 领奖寻路失败，需重新执行领奖流程")
    return False
