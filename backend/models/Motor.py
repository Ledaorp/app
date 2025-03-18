import time
import threading
import gpio
from models import Encoder

class Motor:
    def __init__(self, step_pin, dir_pin, en_pin=None, encoder_channel=0, steps_per_rev=200, speed_sps=0.0001, invert_dir=False, transfer = 0):
        # Initialize GPIO pin numbers
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        
        self.encoder=Encoder.AS5600()
        self.encoder.set_channel(encoder_channel)
        # Setup GPIO modes
        gpio.setup(step_pin, gpio.OUT)
        gpio.setup(dir_pin, gpio.OUT)
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
        #self.step_time = 0.01 / self.steps_per_sec  # Time per step (in seconds)

    def target_deg(self, t):
        self.target_pos = t
        self.pos = self.encoder.Angle()
        self.get_direction()
        self.track_target()

    def step(self):
        gpio.output(self.step_pin, gpio.HIGH)  # Set step pin HIGH
        time.sleep(self.steps_per_sec)  # Pulse duration
        gpio.output(self.step_pin, gpio.LOW)   # Set step pin LOW
        time.sleep(self.steps_per_sec)  # Pulse duration

    def speed(self, sps):
        self.steps_per_sec = sps
        #self.step_time = 0.001 / self.steps_per_sec

    def stop(self):
        self.running = False


    def set_direction(self):
        if(self.invert_dir):
            gpio.output(self.dir_pin,gpio.HIGH)
        else:
            gpio.output(self.dir_pin,gpio.LOW)

    def get_encoder(self):
        i = self.encoder.Angle()
        return i

    def track_target(self):
        if ((self.pos<=(self.target_pos+self.trash_hold)) and (self.pos>=(self.target_pos-self.trash_hold))):
            self.stop()
        else:
            self.running = True
            
            while self.running:
                self.step()
                self.pos = self.encoder.Angle()
                if ((self.pos<=(self.target_pos+self.trash_hold)) and (self.pos>=(self.target_pos-self.trash_hold))):
                    self.stop()
                    
    '''async def thred_encoder_angle_update(self):
        while True:
            await asyncio.sleep(1)
            pos = self.get_encoder()
            print(pos)'''

    def get_direction(self):
            if((self.target_pos+180)>360):
                if(self.target_pos<self.pos and self.target_pos>(self.pos-180)):
                    self.invert_dir=True
                elif(self.target_pos>self.pos):
                    self.invert_dir=False
                elif(self.target_pos<(self.pos-180)):
                    self.invert_dir=False
            else:
                if(self.target_pos>self.pos and self.target_pos<(self.pos+180)):
                    self.invert_dir=False
                if((self.target_pos>=(self.pos+180))):    
                    self.invert_dir=True
                elif(self.target_pos<self.pos):
                    self.invert_dir=True
            self.set_direction()

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