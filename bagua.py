# bagua.py
import pyautogui
import time
from utils import click_image, clear_and_type, wait_with_interrupt, running

first_run = True  # 是否第一次八卦

def find_bagua_npc():
    global running, first_run
    print("[INFO] 开始寻找八卦NPC...")

    # ---------- 第一次八卦: F12 + 坐标输入 ----------
    if first_run:
        pyautogui.press('f12')
        print("[INFO] 按下 F12 打开地图")
        wait_with_interrupt(1)
        if not running:
            return False

        # 点击自动寻路 NPC
        if click_image("picture/zidongxunren.png"):
            print("[INFO] 找到 zidongxunren.png")
        else:
            print("[ERROR] 未找到 zidongxunren.png")
            return False

        # 输入 X 坐标
        if click_image("picture/zuobiao_x.png"):
            print("[INFO] 点击坐标输入X轴图片")
            clear_and_type("191")
            print("[INFO] 输入 X=191")
        else:
            print("[ERROR] 未找到坐标输入X轴图片")
            return False

        # 输入 Y 坐标
        if click_image("picture/zuobiao_y.png"):
            print("[INFO] 点击坐标输入Y轴图片")
            clear_and_type("271")
            print("[INFO] 输入 Y=271")
        else:
            print("[ERROR] 未找到坐标输入Y轴图片")
            return False

        # 点击自主寻路
        if click_image("picture/zizhuyidong.png"):
            print("[INFO] 点击自主寻路")
        else:
            print("[ERROR] 未找到自主寻路图片")
            return False

        # 检测继续按钮
        delay = 10
        for attempt in range(3):
            print(f"[INFO] 第 {attempt+1} 次检测继续图片，等待 {delay} 秒...")
            wait_with_interrupt(delay)
            if click_image("picture/jixu.png"):
                print("[INFO] 找到继续图片，进入八卦")
                break
            delay += 5
        else:
            print("[ERROR] 未找到八卦NPC，程序结束")
            return False

        first_run = False

    # ---------- 第二轮及以后 ----------
    else:
        wait_with_interrupt(1.5)
        if click_image("picture/npc_baguawai.png"):
            print("[INFO] 点击 npc_baguawai.png")
            wait_with_interrupt(0.5)
            if click_image("picture/jixu.png"):
                print("[INFO] 点击继续，开始八卦")
        else:
            print("[ERROR] 未找到 npc_baguawai.png，终止本轮八卦")
            return False

    # ---------- 进入8层 ----------
    if click_image("picture/jinru8ceng.png"):
        print("[INFO] 点击进入8层")
        wait_with_interrupt(2)

    # ---------- 检测今日八卦是否已完成 ----------
    if click_image("picture/baguayiwancheng.png"):
        print("[INFO] 今日八卦已完成，领取奖励")
        if click_image("picture/baguayiwancheng_queding.png"):
            print("[INFO] 点击确认")
            wait_with_interrupt(0.5)
            # 自动寻路到 NPC
            if click_image("picture/zidongxunren.png"):
                print("[INFO] 点击自动寻路")
                wait_with_interrupt(0.5)
            # 输入 X/Y 坐标
            if click_image("picture/zuobiao_x.png"):
                clear_and_type("273")
            if click_image("picture/zuobiao_y.png"):
                clear_and_type("239")
            # 点击自主寻路
            click_image("picture/zizhuyidong.png")
            wait_with_interrupt(10)
            # 点击领取八卦奖励
            if click_image("picture/bagualingjiang.png"):
                print("[INFO] 点击领取八卦奖励，自动八卦结束")
                running = False
                return False

    # ---------- 八卦循环 ----------
    while running:
        # 点击 NPC
        if click_image("picture/npc_zhennei.png"):
            print("[INFO] 点击 npc_zhennei")
            wait_with_interrupt(0.3)

        # 战斗准备
        if click_image("picture/wozuohaozhunbeil.png"):
            print("[INFO] 点击 wozuohaozhunbeil")
            wait_with_interrupt(0.3)
            if click_image("picture/jieshoutiaozhan.png"):
                print("[INFO] 点击 jieshoutiaozhan")
                wait_with_interrupt(0.3)
                pyautogui.press('b')
                print("[INFO] 按下 B 开始自动攻击")
                wait_with_interrupt(20)
                pyautogui.press('n')
                print("[INFO] 按下 N 选择领奖武功")
                wait_with_interrupt(0.3)

        # 消灭心魔
        if click_image("picture/jixuxiaomiexinmo.png"):
            print("[INFO] 找到 jixuxiaomiexinmo，点击")
            wait_with_interrupt(0.3)
            pyautogui.press('b')
            print("[INFO] 按下 B 开始自动攻击")
            wait_with_interrupt(10)
            pyautogui.press('n')
            print("[INFO] 按下 N 选择领奖武功")
            wait_with_interrupt(0.3)
            click_image("picture/npc_zhennei.png")
            continue

        # 领奖逻辑
        if click_image("picture/lingqujiangli.png"):
            print("[INFO] 找到 lingqujiangli")
            wait_with_interrupt(0.5)
            click_image("picture/lingqujiangli_2.png")
            click_image("picture/likaibagua.png")
            print("[INFO] 完成一轮八卦")
            wait_with_interrupt(1.5)
            # 自动进入下一轮
            return True

    return True
