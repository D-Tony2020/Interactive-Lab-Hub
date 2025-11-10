from gpiozero import RGBLED
from time import sleep

# 使用 GPIO17 / GPIO16 / GPIO26
led = RGBLED(red=17, green=16, blue=26)

while True:
    led.color = (1, 0, 0)  # 红
    sleep(3)
    led.color = (0, 1, 0)  # 绿
    sleep(3)
    led.color = (0, 0, 1)  # 蓝
    sleep(3)
    led.color = (1, 1, 1)  # 白
    sleep(3)
    led.off()
    sleep(5)
