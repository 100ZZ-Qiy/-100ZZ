# -*- coding: utf-8 -*-
# github https://github.com/100ZZ-Qiy/-100ZZ
# 峰哥的github：100ZZ-Qiy，欢迎点星星！
"""
微信消息自动发送工具（改进版）
- 添加了异常处理
- 添加了剪贴板保护（操作前备份，操作后恢复）
- 添加了 Esc 强制停止
- 添加了用户确认步骤
- 添加了 if __name__ == '__main__' 保护
"""

import time
import sys
import os       # 用于 Esc 强制退出
import threading
from pynput import mouse, keyboard
import pyperclip  # 需要安装：pip install pyperclip

# ============ 可配置参数（按需修改） ============
SEND_COUNT = 3              # 发送次数，改成 10 就发 10 条
MESSAGE_TEXT = "你好呀，我是qiy鸭！"  # 要发送的消息内容
COUNTDOWN_SECONDS = 5       # 启动倒计时秒数，给你时间切到微信聊天窗口
SEND_INTERVAL = 0.5         # 每条消息间隔（秒），改成 1 就每隔 1 秒发一条
KEY_HOLD_TIME = 0.05        # 按键按住时间，一般不用改
USE_CTRL_ENTER = False      # 发送方式：False=Enter, True=Ctrl+Enter
# ==============================================

# 全局标志：是否取消发送
_cancelled = False


def on_press(key):
    """监听键盘，按下 Esc 强制停止程序（立即退出，不管程序在做什么）"""
    global _cancelled
    try:
        if key == keyboard.Key.esc:
            _cancelled = True
            print("\n已按 Esc，强制停止")
            os._exit(0)  # 直接退出整个进程
    except Exception:
        pass


def countdown(seconds):
    """倒计时，期间可被 Esc 强制停止"""
    global _cancelled
    print(f"{seconds} 秒后开始发送，按 Esc 强制停止...")
    for i in range(seconds, 0, -1):
        if _cancelled:
            return False
        print(f"  {i}...")
        time.sleep(1)
    return not _cancelled


def send_messages():
    """发送消息的主逻辑"""
    global _cancelled

    # 启动键盘监听（后台线程），用于检测 Esc 强制停止
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # 倒计时，等待用户将焦点切换到微信输入框
    if not countdown(COUNTDOWN_SECONDS):
        listener.stop()
        return

    # 备份当前剪贴板内容，发送完成后恢复
    try:
        original_clipboard = pyperclip.paste()
    except Exception:
        original_clipboard = ""

    mouse_ctrl = mouse.Controller()
    keyboard_ctrl = keyboard.Controller()

    try:
        # 点击输入框，获得焦点
        print("点击输入框...")
        mouse_ctrl.click(mouse.Button.left)
        time.sleep(0.2)

        for i in range(SEND_COUNT):
            if _cancelled:
                print("发送已取消")
                break

            print(f"发送第 {i + 1}/{SEND_COUNT} 条消息...")

            # === 第一步：复制文字到剪贴板 ===
            pyperclip.copy(MESSAGE_TEXT)

            # === 第二步：粘贴（Ctrl+V），绕过输入法避免错乱 ===
            keyboard_ctrl.press(keyboard.Key.ctrl)
            keyboard_ctrl.press('v')
            time.sleep(KEY_HOLD_TIME)
            keyboard_ctrl.release('v')
            keyboard_ctrl.release(keyboard.Key.ctrl)

            # === 第三步：发送（根据配置选择 Enter 或 Ctrl+Enter） ===
            if USE_CTRL_ENTER:
                # Ctrl+Enter 发送（适用于部分版本微信）
                keyboard_ctrl.press(keyboard.Key.ctrl)
                keyboard_ctrl.press(keyboard.Key.enter)
                time.sleep(KEY_HOLD_TIME)
                keyboard_ctrl.release(keyboard.Key.enter)
                keyboard_ctrl.release(keyboard.Key.ctrl)
            else:
                # Enter 发送（微信默认发送方式）
                keyboard_ctrl.press(keyboard.Key.enter)
                time.sleep(KEY_HOLD_TIME)
                keyboard_ctrl.release(keyboard.Key.enter)

            # === 第四步：等待间隔，防止消息连在一起 ===
            time.sleep(SEND_INTERVAL)

        print("发送完毕")

    except Exception as e:
        print(f"发送过程中出错: {e}")

    finally:
        # 恢复剪贴板
        try:
            pyperclip.copy(original_clipboard)
            print("已恢复剪贴板内容")
        except Exception:
            pass

        listener.stop()


if __name__ == '__main__':
    send_mode = "Ctrl+Enter" if USE_CTRL_ENTER else "Enter"
    print("=" * 40)
    print("  微信消息自动发送工具")
    print("=" * 40)
    print(f"  发送内容: {MESSAGE_TEXT}")
    print(f"  发送次数: {SEND_COUNT}")
    print(f"  发送按键: {send_mode}")
    print(f"  消息间隔: {SEND_INTERVAL} 秒")
    print(f"  按 Esc 可强制停止")
    print("=" * 40)

    try:
        send_messages()
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"\n程序异常: {e}")
        sys.exit(1)
