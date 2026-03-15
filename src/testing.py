from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

led = LED(22, pin_factory=PiGPIOFactory())
led.on()
print("LED should be solid green for 10 seconds...")
sleep(10)
led.off()
print("Done.")