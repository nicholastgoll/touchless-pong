from gpiozero import LED
from time import sleep

led = LED(22)
led.on()
print("LED should be solid green for 10 seconds...")
sleep(10)
led.off()
print("Done.")