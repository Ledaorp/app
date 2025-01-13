from models import Motor
import time
import gpio
step_pin=55
dir_pin=73
enb_pin=74
gpio.setup(step_pin, gpio.OUT)
gpio.setup(enb_pin, gpio.OUT)
gpio.setup(dir_pin, gpio.OUT)
gpio.output(dir_pin, gpio.HIGH) 
gpio.output(enb_pin, gpio.HIGH)
m1 = Motor.Motor(step_pin=55, dir_pin=73, speed_sps=10)

while True:
    m1.target_deg(90)
    m1.track_target()
    time.sleep(2.0)
    m1.target_deg(0)
    m1.track_target()
    time.sleep(2.0)
    print("stop")

while True:
    gpio.output(enb_pin, gpio.HIGH)
    gpio.output(step_pin, gpio.HIGH)  # Set step pin HIGH
    time.sleep(0.1)  # Pulse duration
    gpio.output(step_pin, gpio.LOW) 
    time.sleep(0.1)  # Pulse duration
