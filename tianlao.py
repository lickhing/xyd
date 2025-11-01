import pyautogui
import time
from utils import click_image, clear_and_type, wait_with_interrupt, running

first_run = True  # 是否第一次天牢


def tianlao():
    global first_run, running
    print("[INFO] 天牢流程启动...")

    while running:
        # ---------- 阶段1：天牢入口寻路 ----------
        if first_run:
            print("[INFO] 第一次天牢，执行入口寻路")
            retry_count = 0
            while running:
                if click_image("picture/xunren.png"):
                    print("[INFO] 点击 xunren.png，准备输入坐标")
                else:
                    pyautogui.press('f12')
                    print("[INFO] F12 打开地图")
                    wait_with_interrupt(0.5)
                    click_image("picture/xunren.png")
                    print("[INFO] 点击 xunren.png")

                if click_image("picture/zuobiao_x.png"):
                    clear_and_type("193")
                if click_image("picture/zuobiao_y.png"):
                    clear_and_type("268")
                if click_image("picture/zizhuyidong.png"):
                    print("[INFO] 开始自动寻路到天牢入口")
                    wait_with_interrupt(20)

                if click_image("picture/tl_wlss.png"):
                    print("[INFO] 点击 tl_wlss.png")
                    wait_with_interrupt(1)
                    if click_image("picture/tl_jrtl.png"):
                        print("[INFO] 点击 tl_jrtl.png，确认进入天牢")
                        wait_with_interrupt(1)
                        # 检查今日是否完成天牢
                        if click_image("picture/tl_tlwc.png"):
                            print("[INFO] 今日天牢已完成，进入金币领奖阶段")
                            wait_with_interrupt(1)
                            if click_image("picture/tl_zdl.png"):
                                print("[INFO] 点击 tl_zdl.png 进入金币领奖")
                                wait_with_interrupt(1)
                                go_receive_reward_jinbi()
                                return
                        break
                else:
                    retry_count += 1
                    if retry_count >= 3:
                        if click_image("picture/tl_npc_wai.png"):
                            print("[INFO] 点击 tl_npc_wai.png")
                            if click_image("picture/tl_wlss.png"):
                                click_image("picture/tl_jrtl.png")
                                break
                        else:
                            print("[ERROR] 寻路天牢入口失败，重新尝试")
                            retry_count = 0
                    else:
                        print(f"[INFO] 未找到 tl_wlss.png，等待5秒重试 ({retry_count}/3)")
                        wait_with_interrupt(5)
        else:
            print("[INFO] 非第一次天牢，跳过寻路阶段")
            if click_image("picture/tl_npc_wai.png"):
                print("[INFO] 点击 tl_npc_wai.png")
                wait_with_interrupt(1)
                if click_image("picture/tl_wlss.png"):
                    print("[INFO] 点击 tl_wlss.png")
                    wait_with_interrupt(1)
                    if click_image("picture/tl_jrtl.png"):
                        print("[INFO] 点击 tl_jrtl.png，进入天牢")
                        wait_with_interrupt(1)
                        if click_image("picture/tl_tlwc.png"):
                            print("[INFO] 今日天牢已完成，进入金币领奖阶段")
                            wait_with_interrupt(1)
                            if click_image("picture/tl_zdl.png"):
                                print("[INFO] 点击 tl_zdl.png 进入金币领奖")
                                wait_with_interrupt(1)
                                go_receive_reward_jinbi()
                                return

        first_run = False

        # ---------- 阶段2：战斗过程 ----------
        print("[INFO] 开始战斗阶段")
        if click_image("picture/tl_zdl.png"):
            print("[INFO] 点击 tl_zdl.png 开始战斗")
            wait_with_interrupt(1)

        # 移动到战斗坐标
        if click_image("picture/xunren.png"):
            print("[INFO] 点击 xunren.png，准备输入坐标")
        else:
            pyautogui.press('f12')
            print("[INFO] F12 打开地图")
            wait_with_interrupt(0.5)
            click_image("picture/xunren.png")
            print("[INFO] 点击 xunren.png")
        if click_image("picture/zuobiao_x.png"):
            clear_and_type("12")
        if click_image("picture/zuobiao_y.png"):
            clear_and_type("10")
        if click_image("picture/zizhuyidong.png"):
            print("[INFO] 自动移动到战斗坐标")
            wait_with_interrupt(1)

        # 等待Boss死亡
        while running:
            if click_image("picture/tl_npc.png"):
                print("[INFO] 检测到 tl_npc.png，Boss死亡")
                wait_with_interrupt(0.5)
                if click_image("picture/tl_bossdead.png"):
                    print("[INFO] 点击 tl_bossdead.png")
                    wait_with_interrupt(0.5)
                elif click_image("picture/tl_bossdead2.png"):
                    print("[INFO] 点击 tl_bossdead2.png")
                    wait_with_interrupt(0.5)
                break
            wait_with_interrupt(0.5)

        wait_with_interrupt(5)  # 拾取掉落物
        while running:
            if click_image("picture/tl_sqwc.png"):
                print("[INFO] 点击 tl_sqwc.png 拾取完成")
                wait_with_interrupt(1)
            if click_image("picture/tl_npc.png"):
                print("[INFO] 点击下一层 NPC tl_npc.png")
                wait_with_interrupt(1)
            if click_image("picture/tl_queren.png"):
                print("[INFO] 点击 tl_queren.png 进入下一层")
                wait_with_interrupt(1)
                break  # 回到循环开始进行下一层
            elif click_image("picture/tl_huijc.png"):
                print("[INFO] 天牢完成一轮，进行玉石领奖")
                wait_with_interrupt(1)
                go_receive_reward_yushi()
                break  # 领奖完成后自动进入下一轮

        # 等待1秒再进行下一轮
        wait_with_interrupt(1)


# ---------- 阶段4：天牢完成一轮后的玉石领奖 ----------
def go_receive_reward_yushi():
    retry_count = 0
    while retry_count < 3:
        if click_image("picture/tl_npc_wai.png"):
            print("[INFO] 点击领奖 NPC tl_npc_wai.png")
            wait_with_interrupt(1)
            if click_image("picture/tl_lqjl.png"):
                print("[INFO] 点击领取奖励 tl_lqjl.png")
                wait_with_interrupt(1)
                if click_image("picture/tl_queren.png"):
                    print("[INFO] 点击 tl_queren.png 确认奖励")
                    wait_with_interrupt(1)
                return
        else:
            retry_count += 1
            print(f"[INFO] 第 {retry_count} 次领奖未找到 NPC，等待5秒重试")
            wait_with_interrupt(5)
    print("[WARN] 玉石领奖未成功，继续下一轮天牢")


# ---------- 阶段5：当天所有天牢完成后的金币领奖 ----------
def go_receive_reward_jinbi():
    print("[INFO] 开始金币领奖阶段")
    if click_image("picture/xunren.png"):
        print("[INFO] 点击 xunren.png")
    else:
        pyautogui.press('f12')
        print("[INFO] F12 打开地图")
        wait_with_interrupt(0.5)
        click_image("picture/xunren.png")
        print("[INFO] 点击 xunren.png")

    if click_image("picture/zuobiao_x.png"):
        clear_and_type("273")
    if click_image("picture/zuobiao_y.png"):
        clear_and_type("239")
    if click_image("picture/zizhuyidong.png"):
        print("[INFO] 自动移动到金币领奖坐标")
        wait_with_interrupt(15)

    retry_count = 0
    while retry_count < 3:
        if click_image("picture/tl_xyy.png"):
            print("[INFO] 点击 tl_xyy.png")
            wait_with_interrupt(1)
            if click_image("picture/tllingjiang.png"):
                print("[INFO] 点击 tllingjiang.png")
                wait_with_interrupt(1)
            return
        else:
            retry_count += 1
            print(f"[INFO] 未找到 tl_xyy.png，等待5秒重试 ({retry_count}/3)")
            wait_with_interrupt(5)

    # 最后重试未成功，检测npc_lingjiang.png
    if click_image("picture/npc_lingjiang.png"):
        print("[INFO] 点击 npc_lingjiang.png")
        wait_with_interrupt(1)
        if click_image("picture/tl_xyy.png"):
            click_image("picture/tllingjiang.png")
            print("[INFO] 金币领奖完成")
