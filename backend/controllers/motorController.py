from flask import jsonify, render_template, Blueprint, request
from models import Motor, Encoder
import time
from periphery import I2C
from app import send, set


BPmotorController = Blueprint("motorController", __name__)
   

@BPmotorController.route('/motor',methods=['GET'])
def begin(): 
    print  ("begin mc ------------------------------1")
    m1=setup(send('config.json'))
    start(send('data.json'),m1)
    if m1:
        encoder_value = m1.get_encoder()
        ("begin mc ------------------------------3")
        return jsonify(
            {
                "angles":{
                    "m1": encoder_value,
                    "m2": 0,
                    "m3": 0,
                    "m4": 0,
                    "m5": 0,
                },
                "position":{
                    "x":0,
                    "y":0,
                    "z":0,
                }
            })
    else:
        return jsonify({"error": "Motor not initialized"}), 404
     

def setup(config_json):
    m1 = Motor.Motor(int(config_json['drivers'][0]['step']), int(config_json['drivers'][0]['dir']),int(config_json['drivers'][0]['enable']), speed_sps=10)
    #m1 = Motor.Motor(55,73,74)
    return (m1)

def start(angles_json,m1):
    m1.target_deg((int) (angles_json['angles']['m1']))
    return(True)
