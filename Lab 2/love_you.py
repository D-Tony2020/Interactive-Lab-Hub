import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# ==== 显示屏硬件配置 (你要确认 CS/DC 脚位是否一致) ====
cs_pin = None   # 推荐屏幕 CS 接 CE0 (GPIO8, Pin24)
dc_pin = digitalio.DigitalInOut(board.D25)   # DC 脚请按接线调整
reset_pin = None
BAUDRATE = 64000000

# ==== 初始化 SPI 总线 ====
spi = board.SPI()
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# ==== 创建画布 ====
height = disp.width     # 旋转后交换宽高
width = disp.height
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# ==== 填充黑色背景 ====
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

# ==== 选择字体 ====
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)

# ==== 写字 ====
text1 = "LOVE YOU"
text2 = "MOM"
bbox1 = draw.textbbox((0, 0), text1, font=font)
w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
bbox2 = draw.textbbox((0, 0), text2, font=font)
w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
x1 = (width - w1) // 2
y1 = height // 3
draw.text((x1, y1), text1, font=font, fill="#FF69B4")
x2 = (width - w2) // 2
y2 = y1 + h1 + 10
draw.text((x2, y2), text2, font=font, fill="#00BFFF")
# ==== 显示到屏幕 ====
disp.image(image, 90)
