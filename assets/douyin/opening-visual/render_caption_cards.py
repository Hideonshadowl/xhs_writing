from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("assets/douyin/opening-visual")
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 209, 74, 255)
STROKE = (10, 15, 22, 245)

CARDS = [
    ("card-01.png", "我删掉了她稿子里\n【最漂亮的那句话】", "hook", False),
    ("card-02.png", "单位宣讲稿讲完\n台下一半人在【刷手机】", "caption", False),
    ("card-03.png", "正确的话\n不等于【有人听的话】", "caption", False),
    ("card-04.png", "哪一个瞬间\n还会【起鸡皮疙瘩】？", "caption", False),
    ("card-05.png", "护士冲过来\n【双膝跪地】开始按压", "caption", False),
    ("card-06.png", "先让人看见画面\n膝盖下面，【压着一条命】", "caption", False),
    ("card-07.png", "所谓先锋\n膝盖已经【落地】", "caption", False),
    ("card-08.png", "那次讲完\n【没人刷手机】", "caption", False),
    ("card-09.png", "人是被【画面】击中的\n你先想道理，还是先想画面？", "end", True),
]


def segments(line):
    result = []
    buffer = ""
    highlighted = False
    for char in line:
        if char in "【】":
            if buffer:
                result.append((buffer, highlighted))
                buffer = ""
            highlighted = char == "【"
        else:
            buffer += char
    if buffer:
        result.append((buffer, highlighted))
    return result


def draw_marked_line(draw, line, font, y, center_x):
    parts = segments(line)
    widths = [draw.textlength(text, font=font) for text, _ in parts]
    total = sum(widths)
    x = center_x - total / 2
    for (text, highlighted), width in zip(parts, widths):
        color = YELLOW if highlighted else WHITE
        draw.text(
            (x, y),
            text,
            font=font,
            fill=color,
            stroke_width=5,
            stroke_fill=STROKE,
        )
        x += width


def render(file, text, kind, disclosure):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if kind == "hook":
        font = ImageFont.truetype(FONT, 78)
        y = 220
        line_gap = 96
    elif kind == "end":
        font = ImageFont.truetype(FONT, 56)
        y = 1280
        line_gap = 78
    else:
        font = ImageFont.truetype(FONT, 58)
        y = 250
        line_gap = 82

    for line in text.split("\n"):
        draw_marked_line(draw, line, font, y, 540)
        y += line_gap

    if disclosure:
        tip = ImageFont.truetype(FONT, 30)
        tip_text = "画面由AI辅助生成，案例已脱敏"
        tw = draw.textlength(tip_text, font=tip)
        draw.text(
            (540 - tw / 2, 1760),
            tip_text,
            font=tip,
            fill=(220, 220, 220, 230),
            stroke_width=3,
            stroke_fill=(10, 15, 22, 180),
        )

    img.save(ROOT / file)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for item in CARDS:
        render(*item)
        print("wrote", item[0])


if __name__ == "__main__":
    main()
