# -*- coding: utf-8 -*-
"""
桌宠启动器 - 由 bat 调用，负责拉起桌宠主程序
"""
import os
import sys
import subprocess

APP_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(APP_DIR)

pet_script = os.path.join(APP_DIR, "pet.py")

if __name__ == "__main__":
    subprocess.run([sys.executable, pet_script], cwd=APP_DIR)
