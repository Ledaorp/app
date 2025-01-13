import time
import gpio
#import Encoder
from models import Encoder

class Motor:
    def __init__(self, step_pin, dir_pin, en_pin=None, steps_per_rev=200, speed_sps=10, invert_dir=False, transfer = 0):
        # Initialize GPIO pin numbers
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        
        self.encoder=Encoder.AS5600()
        # Setup GPIO modes
        gpio.setup(step_pin, gpio.OUT)
        gpio.setup(dir_pin, gpio.OUT)
        if en_pin is not None:
            gpio.setup(en_pin, gpio.OUT)
            gpio.output(en_pin, gpio.HIGH)

        self.invert_dir = invert_dir
        
        self.target_pos = 0
        self.pos = 0
        
        self.steps_per_sec = speed_sps
        self.steps_per_rev = steps_per_rev
        
        self.trash_hold = 5
        self.transfer = transfer
        
        self.running = False
        self.free_run_mode = 0  # Represents direction for free run
        self.step_time = 0.01 / self.steps_per_sec  # Time per step (in seconds)

    def target_deg(self, t):
        self.target_pos = t
        self.track_target()

    def step(self, d):
        gpio.output(self.step_pin, gpio.HIGH)  # Set step pin HIGH
        time.sleep(0.001)  # Pulse duration
        gpio.output(self.step_pin, gpio.LOW)   # Set step pin LOW
        time.sleep(0.001)  # Pulse duration
        self.pos += 1

    def speed(self, sps):
        self.steps_per_sec = sps
        self.step_time = 0.001 / self.steps_per_sec

    def stop(self):
        self.free_run_mode = 0
        self.running = False


    def update(self):
        if self.free_run_mode > 0:
            self.step(1)
        elif self.free_run_mode < 0:
            self.step(-1)
        elif self.target_pos > self.pos:
            self.step(1)
        elif self.target_pos < self.pos:
            self.step(-1)


    def track_target(self):
        self.free_run_mode = 0
        self.running = True
        while self.running:
            self.update()
            #time.sleep(self.step_time)  # Wait according to the set speed
            self.encoder.PrintAngle()
            if ((self.encoder.Angle()<=(self.target_pos+self.trash_hold)) and (self.encoder.Angle()>=(self.target_pos-self.trash_hold))):
                self.stop()

    
    
'''    
    def update(self):
        if self.free_run_mode > 0:
            self.step(1)
        elif self.free_run_mode < 0:
            self.step(-1)
        elif self.target_pos > self.pos:
            self.step(1)
        elif self.target_pos < self.pos:
            self.step(-1)
    def free_run(self, d):
        self.free_run_mode = d
        if d != 0:
            self.running = True
            while self.running:
                self.update()
                time.sleep(self.step_time)  # Wait according to the set speed
        else:
            self.stop()
'''