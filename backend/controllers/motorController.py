from flask import jsonify, render_template, Blueprint, request
from models import Motor, Encoder
import time
import threading
from periphery import I2C
from app import send, set
#import numpy as np
#from visual_kinematics.RobotSerial import *

BPmotorController = Blueprint("motorController", __name__)
   
motors = []  # List to store motor instances
motor_count = 2  # Define the number of motors
target_angles = [None] * motor_count
threds = []
angle_lock = threading.Lock()  
enc =  Encoder.AS5600()

def setup_motors(config_json):
    for i in range(motor_count):
        try:
            motor = Motor.Motor(
                int(config_json['drivers'][i]['step']),
                int(config_json['drivers'][i]['dir']),
                int(config_json['drivers'][i]['enable']),
                encoder_channel=i
            )
            if(i == 0):
                motor.invert_dir=True
        except:
            print(f"Error in setup motors: {i}")
        motors.append(motor)
   

def update_target_angles():
    while True:
        for i, motor in enumerate(motors):
            try:
                target_angles[i] = getAngle(send('data.json'),f'm{i+1}')
                #print (target_angles[i],motors[i].pos)
                time.sleep(0.1) 
            except Exception as e: print(e, "update_target_angles")
def update_encoder_angles():
    while True:
        for i, motor in enumerate(motors):
            try:
                time.sleep(0.0001)
                motors[i].pos = motors[i].get_encoder(enc)
                motors[i].add_pos_angle(motors[i].pos)
                motors[i].target_pos = (target_angles[i])
                motors[i].get_direction()
                #print (f'm{i+1} ---- '+str(motors[i].pos))
            except Exception as e: print(e, "update_encoder_angles")
            

            

def motor_thread(motor_index):
    m  = motor_index
    while True:
        #motors[m].target_pos = (target_angles[m])
        motors[m].track_target()
        time.sleep(0.1)
        '''if(motors[m].target_pos is not None and ((motors[m].pos<=(motors[m].target_pos+motors[m].trash_hold)) and (motors[m].pos>=(motors[m].target_pos-motors[m].trash_hold)))):
            motors[m].target_deg(motors[m].target_pos)
        else:
            motors[m].stop
        
        time.sleep(1)'''
        '''
        with angle_lock:
            target_angle = target_angles[m]

        current_angle = motors[m].get_encoder()
        print(motors[m].step_pin)
        if current_angle != target_angle:
            motors[m].target_deg(target_angle)
        elif current_angle == target_angle:
            motors[m].stop()'''

def setup_threds():
    thred_update_target_angles = threading.Thread(target=update_target_angles)
    thred_update_target_angles.start()
    thred_update_encoder_angles = threading.Thread(target=update_encoder_angles)
    thred_update_encoder_angles.start()
    for i, motor in enumerate(motors):
        threds.append(threading.Thread(target=motor_thread, args=(i,)))
        print(i)
        threds[i].start()
    
    
def __init__():
    if len(motors) == 0:
        setup_motors(send('config.json'))
    setup_threds()

@BPmotorController.route('/motors/setAngles',methods=['GET'])
def begin():
    if (len(motors) == 0 or len(motors)!=motor_count):
        setup_motors(send('config.json'))
    if len(threds) == 0:
        setup_threds()
    encoder_values = {}
    for i in range(motor_count):
        try:
            #motors[i].target_deg(getAngle(send('data.json'),f'm{i+1}'))
            encoder_values[f'm{i+1}'] = motors[i].pos
            print(motors[i].poss)
        except Exception as e: 
            print(e)
            #return ("Error")
        #print (encoder_values[f'm{i+1}'])
    print(encoder_values)
    
    return encoder_values

@BPmotorController.route('/motors/position',methods=['POST'])
def possition(): 
    #json = send("config.json")["dh"]
    #robot = RobotSerial(dh_params=np.array(json))
    #position = np.array([[0.5], [1.], [1]])
    #rotation = np.array([0, 0., 0])
    #end = Frame.from_euler_3(rotation,position)
    #joint_angles = robot.inverse(end)
    #return joint_angles
    return 1

def getAngle(angles_json,motorId):
    return((int) (angles_json['angles'][motorId]))

