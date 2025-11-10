from gpiozero import RGBLED
from time import sleep

led = RGBLED(red=17, green=5, blue=6)

while True:
    led.color = (1,0,0)
    sleep(1)
    led.color = (0,1,0)
    sleep(1)
    led.color = (0,0,1)
    sleep(1)
    led.color = (1,1,1)
    sleep(1)
    led.off()
    sleep(1)
