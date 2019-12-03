# ESP32Peacock Slow Blink.py 
# Complete project details at https://RandomNerdTutorials.com

from machine import Pin
led = Pin(22, Pin.OUT)

while True:
led.value(not led.value())
