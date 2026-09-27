# -*- coding: utf-8 -*-
"""生成大肥鱼的梗图卡片到 memes/ 目录。

右键桌宠时会从 memes/ 里随机抽一张显示在左侧气泡里。
想换成真正的网图，直接把 png/jpg 丢进 memes/ 即可，不用改代码。
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

APP_DIR = os.path.dirname(os.path.abspath(__file__))
MEME_DIR = os.path.join(APP_DIR, "memes")
SPRITE_DIR = os.path.join(APP_DIR, "sprites")

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"

CARD_W, CARD_H = 344, 300
TAIL = 34                       # 右侧指向桌宠的小尾巴长度
W, H = CARD_W + TAIL, CARD_H
RADIUS = 26

# (文案, 卡片底色, 文字颜色, 点缀色)
MEMES = [
    ("前台不语\n只是一味地 os……", "#fef3c7", "#92400e", "#f59e0b"),
    ("先吃饭后干活\n不对，是只吃饭不干活", "#dbeafe", "#1e40af", "#3b82f6"),
    ("我不胖！\n我这叫圆润", "#fce7f3", "#9d174d", "#ec4899"),
    ("不吃压力\n我行我素", "#e0e7ff", "#3730a3", "#6366f1"),
    ("梁圣？\n涨价之后叫梁子了", "#dcfce7", "#166534", "#22c55e"),
    ("V4 都出正式版了\n我还在摸鱼", "#ffe4e6", "#9f1239", "#fb7185"),
    ("鲇鱼效应？\n我明明是鲸鱼", "#cffafe", "#155e75", "#06b6d4"),
    ("2840 亿参数\n激活 130 亿\n省电又省饭", "#f3e8ff", "#6b21a8", "#a855f7"),
]


def fit_font(draw, text, max_w, start=40, floor=18):
    for size in range(start, floor - 1, -1):
        f = ImageFont.truetype(FONT_BOLD, size)
        if max(draw.textlength(ln, font=f) for ln in text.split("\n")) <= max_w:
            return f
    return ImageFont.truetype(FONT_BOLD, floor)


def make_card(text, bg, fg, accent, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([0, 0, CARD_W - 1, CARD_H - 1], RADIUS, fill=bg, outline=accent, width=3)
    d.polygon([(CARD_W - 3, 118), (W - 2, 150), (CARD_W - 3, 182)], fill=bg)
    d.line([(CARD_W - 3, 118), (W - 2, 150)], fill=accent, width=3)
    d.line([(W - 2, 150), (CARD_W - 3, 182)], fill=accent, width=3)

    d.rounded_rectangle([18, 16, 18 + 62, 16 + 22], 11, fill=accent)
    tag = ImageFont.truetype(FONT_REG, 13)
    d.text((49, 27), "梗图", font=tag, fill="#ffffff", anchor="mm")

    font = fit_font(d, text, CARD_W - 96)
    d.multiline_text((24, 150), text, font=font, fill=fg, align="left", spacing=10, anchor="lm")

    d.text((24, CARD_H - 20), "大肥鱼桌宠", font=ImageFont.truetype(FONT_REG, 13),
           fill=fg + "99" if len(fg) == 7 else fg, anchor="lm")

    sprite_path = os.path.join(SPRITE_DIR, "正面_306.png")
    if os.path.exists(sprite_path):
        sp = Image.open(sprite_path).convert("RGBA")
        sh = 128
        sp = sp.resize((max(1, int(sp.width * sh / sp.height)), sh), Image.LANCZOS)
        img.alpha_composite(sp, (CARD_W - sp.width - 10, CARD_H - sp.height - 6))

    img.save(path, "PNG")
    return path


if __name__ == "__main__":
    os.makedirs(MEME_DIR, exist_ok=True)
    for i, (text, bg, fg, accent) in enumerate(MEMES, 1):
        p = make_card(text, bg, fg, accent, os.path.join(MEME_DIR, f"meme_{i:02d}.png"))
        print("生成", os.path.relpath(p, APP_DIR))
    print(f"共 {len(MEMES)} 张，目录 {os.path.relpath(MEME_DIR, APP_DIR)}")