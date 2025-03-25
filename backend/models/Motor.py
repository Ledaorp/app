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

        self.chanell = encoder_channel
        # Setup GPIO modes
        gpio.setup(step_pin, gpio.OUT)
        gpio.setup(dir_pin, gpio.OUT)
        gpio.setup(en_pin, gpio.OUT)
        gpio.output(en_pin, gpio.HIGH)
        gpio.output(step_pin, gpio.LOW)

        self.invert_dir = invert_dir
        
        self.target_pos = 0
        self.pos = 0
        self.poss = []
        
        self.steps_per_sec = speed_sps
        self.steps_per_rev = steps_per_rev
        
        self.trash_hold = 6
        self.transfer = transfer
        
        self.running = False
        #self.step_time = 0.01 / self.steps_per_sec  # Time per step (in seconds)

    def target_deg(self, t):
        #self.target_pos = t
        #self.get_direction()
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
        gpio.output(self.step_pin,gpio.HIGH)


    def set_direction(self):
        if(self.invert_dir):
            gpio.output(self.dir_pin,gpio.LOW)
        else:
            gpio.output(self.dir_pin,gpio.HIGH)

    def get_encoder(self, encoder):
        if encoder is None:
            print("Error encoder is None")
            return (0)
        encoder.set_channel(self.chanell)
        i = encoder.Angle()
        #self.encoder.close()
        return i

    def track_target(self):
        if ((self.pos<=(self.target_pos+self.trash_hold)) and (self.pos>=(self.target_pos-self.trash_hold))):
            self.stop()
        else:
            self.running = True
            
            while self.running:
                self.step()
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
                    if(self.invert_dir==True):
                        gpio.output(self.dir_pin,gpio.LOW)
                    else:
                        gpio.output(self.dir_pin,gpio.HIGH)
                    
                elif(self.target_pos>self.pos):
                    if(self.invert_dir==False):
                        gpio.output(self.dir_pin,gpio.LOW)
                    else:
                        gpio.output(self.dir_pin,gpio.HIGH)
                elif(self.target_pos<(self.pos-180)):
                    if(self.invert_dir==False):
                        gpio.output(self.dir_pin,gpio.LOW)
                    else:
                        gpio.output(self.dir_pin,gpio.HIGH)
            else:
                if(self.target_pos>self.pos and self.target_pos<(self.pos+180)):
                    if(self.invert_dir==False):
                        gpio.output(self.dir_pin,gpio.LOW)
                    else:
                        gpio.output(self.dir_pin,gpio.HIGH)
                if((self.target_pos>=(self.pos+180))):    
                    if(self.invert_dir==True):
                        gpio.output(self.dir_pin,gpio.LOW)
                    else:
                        gpio.output(self.dir_pin,gpio.HIGH)
                elif(self.target_pos<self.pos):
                    if(self.invert_dir==True):
                        gpio.output(self.dir_pin,gpio.LOW)
                    else:
                        gpio.output(self.dir_pin,gpio.HIGH)
                        
    def add_pos_angle(self, angle):
        i = len(self.poss)
        if(i<7):
            self.poss.append(angle)
        else:
            self.poss.pop(0)
            self.poss.insert(7,angle)
        #print(self.poss)
        
    def __str__(self):
        return (self.pos)

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