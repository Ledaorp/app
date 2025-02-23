from flask import jsonify, render_template, Blueprint, request
from models import Motor, Encoder
import time
from periphery import I2C
from app import send, set


BPmotorController = Blueprint("motorController", __name__)
   

@BPmotorController.route('/motor',methods=['GET'])
def begin(): 
    m1,m2,m3,m4,m5 = Motor.Motor(0,0)
    m1=setup(send('config.json'))
    start(send('data.json'),m1)
    m1.track_target
    if m1:
        encoder_value = m1.get_encoder_value()
        return jsonify({
            "m1": encoder_value,
            "m2": 0,
            "m3": 0,
            "m4": 0,
            "m5": 0})
    else:
        return jsonify({"error": "Motor not initialized"}), 404
     

def setup(config_json):
    m1 = Motor.Motor(config_json['drivers'][0]['step'], config_json['drivers'][0]['dir'],config_json['drivers'][0]['enable'], speed_sps=10)
    return (m1)

def start(angles_json,m1):
    m1.target_deg(angles_json['angles']['m1'])
    return(True)
