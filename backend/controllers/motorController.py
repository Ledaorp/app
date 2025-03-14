from flask import jsonify, render_template, Blueprint, request
from models import Motor, Encoder
import time
import threading
from periphery import I2C
from app import send, set
import numpy as np
from visual_kinematics.RobotSerial import *

BPmotorController = Blueprint("motorController", __name__)
   
motors = []  # List to store motor instances
motor_count = 1  # Define the number of motors
target_angles = [0]
angle_lock = threading.Lock()  

def setup_motors(config_json):
    for i in range(motor_count):
        motor = Motor.Motor(
            int(config_json['drivers'][i]['step']),
            int(config_json['drivers'][i]['dir']),
            int(config_json['drivers'][i]['enable']),
            speed_sps=10
        )
        motors.append(motor)
   

def update_target_angles():
    while True:
        for i in range(motor_count):
            target_angles[i] = getAngle(send('data.json'),f'm{i+1}')
            time.sleep(1)  

def motor_thread(motor_index):
    while True:
        with angle_lock:
            target_angle = target_angles[motor_index]

        current_angle = motors[motor_index].get_encoder()

        if current_angle != target_angle:
            motors[motor_index].target_deg(target_angle)
        elif current_angle == target_angle:
            motors.stop()

        time.sleep(0.1)  

def __init__():
    if len(motors) == 0:
        setup_motors(send('config.json'))
    for i in range(motor_count):
        thread = threading.Thread(target=motor_thread, args=(i,))
        thread.daemon = True
        thread.start()
    angle_updater_thread = threading.Thread(target=update_target_angles)
    angle_updater_thread.daemon = True
    angle_updater_thread.start()

@BPmotorController.route('/motors/setAngles',methods=['GET'])
def begin():
    encoder_values = {}
    for i, motor in enumerate(motors):
        motor.target_deg(getAngle(send('data.json'),f'm{i+1}'))
        encoder_values[f'm{i+1}'] = motor.get_encoder()
    return encoder_values
  
  
@BPmotorController.route('/motors/position',methods=['POST'])
def possition(): 
    json = send("config.json")["dh"]
    robot = RobotSerial(dh_params=np.array(json))
    position = np.array([[0.5], [1.], [1]])
    rotation = np.array([0, 0., 0])
    end = Frame.from_euler_3(rotation,position)
    joint_angles = robot.inverse(end)
    return joint_angles

def getAngle(angles_json,motorId):
    return((int) (angles_json['angles'][motorId]))


