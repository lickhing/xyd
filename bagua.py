import pyautogui
import time
from utils import click_image, clear_and_type, wait_with_interrupt, running

first_run = True


def find_bagua_npc(daboss_wait_time=30):
    global first_run
    print("[INFO] 开始寻找八卦NPC...")

    # ---------- 阶段1：开始寻路找 NPC ----------
    while running:
        if click_image("picture/xunren.png"):
            print("[INFO] 点击 xunren.png，准备输入坐标")
            break
        else:
            pyautogui.press('f12')
            print("[INFO] 按 F12 打开地图")
            if not wait_with_interrupt(0.5):
                return
            if click_image("picture/xunren.png"):
                print("[INFO] 点击 xunren.png，准备输入坐标")
                break

    if not running:
        return

    # 第一次八卦使用固定坐标 191,271
    if first_run:
        if click_image("picture/zuobiao_x.png"):
            clear_and_type("191")
        if click_image("picture/zuobiao_y.png"):
            clear_and_type("271")
        if click_image("picture/zizhuyidong.png"):
            print("[INFO] 第一次八卦，点击自主寻路")
            if not wait_with_interrupt(10):
                return

    if not running:
        return

    # 等待角色移动并检测 hulve.png 或 jixu.png
    detected = False
    for attempt in range(4):
        wait_time = 10 if attempt == 0 else 5
        if not wait_with_interrupt(wait_time):
            return

        if not running:
            return

        if click_image("picture/hulve.png"):
            print("[INFO] 出现 hulve.png，点击")
            wait_with_interrupt(1)
        if click_image("picture/jixu.png"):
            print("[INFO] 出现 jixu.png，点击")
            detected = True
            break
        print(f"[INFO] 第 {attempt + 1} 次未检测到 hulve/jixu，重试")

        if click_image("picture/npc_baguawai.png"):
            print("[INFO] 点击 npc_baguawai.png，尝试检测 hulve/jixu")
            if click_image("picture/hulve.png"):
                print("[INFO] 出现 hulve.png，点击")
                wait_with_interrupt(1)
            if click_image("picture/jixu.png"):
                print("[INFO] 出现 jixu.png，点击")
                detected = True
                break

    if not running:
        return

    first_run = False

    # ---------- 阶段2：进入八卦 ----------
    while running and not click_image("picture/jinru8ceng.png"):
        print("[INFO] 点击进入8层")
        if not wait_with_interrupt(1):
            return

    if not running:
        return

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
            while running and not click_image("picture/npc_zhennei.png"):
                if not wait_with_interrupt(0.5):
                    return

            if not running:
                return
            print("[INFO] 点击 npc_zhennei")
            if not wait_with_interrupt(1):
                return

            while running and not click_image("picture/wozuohaozhunbeil.png"):
                if not wait_with_interrupt(0.5):
                    return

            if not running:
                return
            print("[INFO] 点击 wozuohaozhunbeil")
            if not wait_with_interrupt(1):
                return

            while running and not click_image("picture/jieshoutiaozhan.png"):
                if not wait_with_interrupt(0.5):
                    return

            if not running:
                return
            print("[INFO] 点击 jieshoutiaozhan")
            if not wait_with_interrupt(1):
                return

            # 阶段4：打Boss
            pyautogui.press('b')
            print("[INFO] 按B打Boss")
            if not wait_with_interrupt(daboss_wait_time):
                return
            pyautogui.press('n')
            print("[INFO] 按N给经验")
            click_image("picture/npc_zhennei.png")

            while running:
                if not wait_with_interrupt(1):
                    return
                if click_image("picture/jixuxiaomiexinmo.png"):
                    pyautogui.press('b')
                    print("[INFO] 按B消灭心魔")
                    if not wait_with_interrupt(10):
                        return
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
                    if not wait_with_interrupt(1):
                        return
                    if click_image("picture/hulve.png"):
                        print("[INFO] 出现 hulve.png，点击")
                        wait_with_interrupt(1)
                    if click_image("picture/jixu.png"):
                        print("[INFO] 出现 jixu.png，点击")
                        wait_with_interrupt(1)
                    while running and not click_image("picture/jinru8ceng.png"):
                        print("[INFO] 等待进入八卦8层")
                        if not wait_with_interrupt(1):
                            return
                    print("[INFO] 点击进入8层")
                    if not wait_with_interrupt(1):
                        return
                    if click_image("picture/baguayiwancheng.png"):
                        print("[INFO] 今日八卦已完成，点击确定去领奖")
                        click_image("picture/baguayiwancheng_queding.png")
                        wait_with_interrupt(1)
                        go_receive_reward()
                        return
                    break
                else:
                    if not wait_with_interrupt(1):
                        return

    battle_loop()


def go_receive_reward():
    """自动领取八卦奖励"""
    if click_image("picture/xunren.png"):
        print("[INFO] 点击自动寻路领奖")
        if not wait_with_interrupt(1):
            return
        if click_image("picture/zuobiao_x.png"):
            clear_and_type("273")
        if click_image("picture/zuobiao_y.png"):
            clear_and_type("239")
        click_image("picture/zizhuyidong.png")
        print("[INFO] 等待20秒寻路到领奖位置")
        if not wait_with_interrupt(20):
            return

        if click_image("picture/bagualingjiang.png"):
            print("[INFO] 找到 bagualingjiang.png，点击领取奖励")
            click_image("picture/bagualingjiang.png")
        if click_image("picture/zhidaol.png"):
            print("[INFO] 奖励已领过，点击确认")
            return True

    for retry in range(3):
        if not running:
            return False
        print(f"[INFO] 第 {retry + 1} 次未找到奖励，等待5秒重试")
        if not wait_with_interrupt(5):
            return False
        if click_image("picture/bagualingjiang.png"):
            print("[INFO] 找到 bagualingjiang.png，点击领取奖励")
            click_image("picture/bagualingjiang.png")
            return True

    if click_image("picture/npc_lingjiang.png"):
        print("[INFO] 点击 npc_lingjiang.png，尝试触发领奖")
        wait_with_interrupt(1)
        if click_image("picture/bagualingjiang.png"):
            print("[INFO] 找到 bagualingjiang.png，点击领取奖励")
        if click_image("picture/zhidaol.png"):
            print("[INFO] 奖励已领过，点击确认")
            return True

    print("[ERROR] 领奖寻路失败，需重新执行领奖流程")
    return False