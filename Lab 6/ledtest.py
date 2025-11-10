from gpiozero import RGBLED
from time import sleep

led = RGBLED(red=17, green=23, blue=26)

while True:
    for color in [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]:
        led.color = color
        sleep(1)
    led.off()
    sleep(1)
