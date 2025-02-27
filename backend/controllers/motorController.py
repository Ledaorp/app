from flask import jsonify, render_template, Blueprint, request
from models import Motor, Encoder
import time
from periphery import I2C
from app import send, set


BPmotorController = Blueprint("motorController", __name__)
   
motors = []  # List to store motor instances
motor_count = 5  # Define the number of motors

def setup_motors(config_json):
    for i in range(motor_count):
        motor = Motor.Motor(
            int(config_json['drivers'][i]['step']),
            int(config_json['drivers'][i]['dir']),
            int(config_json['drivers'][i]['enable']),
            speed_sps=10
        )
        motors.append(motor)   
   
   
@BPmotorController.route('/motors/setAngles',methods=['GET'])
def begin(): 
    if len(motors) == 0:
        setup_motors(send('config.json'))

    encoder_values = {}
    for i, motor in enumerate(motors):
        encoder_values[f'm{i+1}'] = motor.get_encoder()  
     

def setup(config_json,number):
    m = Motor.Motor(int(config_json['drivers'][number]['step']), int(config_json['drivers'][number]['dir']),int(config_json['drivers'][number]['enable']), speed_sps=10)
    return (m)

def start(angles_json,motorId):
    return((int) (angles_json['angles'][motorId]))

