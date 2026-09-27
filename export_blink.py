"""导出眨眼（闭眼）帧到 sprites 目录，方便手动修贴图。

用法：python export_blink.py [朝向 ...]   不给朝向则导出全部
      python export_blink.py 正面
生成：sprites/{朝向}_{高度}_close.png —— 桌宠启动时会优先加载这些文件，
      删掉对应文件即回退到代码自动生成的效果。
"""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

import pet


def main():
    app = QApplication(sys.argv)
    want = sys.argv[1:] or list(pet.BLINK_ORIENTATIONS)
    for label, mult in pet.SIZE_LEVELS.items():
        h = int(340 * mult)
        for name in want:
            if name not in pet.BLINK_ORIENTATIONS:
                continue
            sized = os.path.join(pet.SPRITE_DIR, f"{name}_{h}.png")
            if os.path.exists(sized):
                base = QPixmap(sized)
            else:
                base = QPixmap(os.path.join(pet.SPRITE_DIR, f"{name}.png")).scaledToHeight(
                    h, Qt.TransformationMode.SmoothTransformation)
            pix = pet.make_closed_eye_pix(base, name, h)
            out = os.path.join(pet.SPRITE_DIR, f"{name}_{h}_close.png")
            pix.save(out, "PNG")
            print(f"{label} {name} 高度{h} -> {out} ({pix.width()}x{pix.height()})")
    print("完成")


if __name__ == "__main__":
    main()