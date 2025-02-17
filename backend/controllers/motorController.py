from flask import jsonify, render_template, Blueprint, request
#from models import Motor, Encoder
import time
#from periphery import I2C
from app import send, set


BPmotorController = Blueprint("motorController", __name__)
'''
@BPmotorController.route('/motor/api/M1Angle', methods=['POST'])
def receive_number():
    try:
        data = request.get_json()  # Get the JSON data
        number = data['M1angle']  # Extract the number
        #m1 = Motor.Motor(55, 73,74, speed_sps=10)
        #m1.target_deg(number)
        # Here you can add your business logic, for example:
        result = {"received_angle": number}
        print(number)
        return jsonify(result), 200
    except Exception as e:
        #m1.stop()
        return jsonify({"error": str(e)}), 400  

@BPmotorController.route('/motor')
def start():
   
    return render_template('test.html')
   ''' 
@BPmotorController.route('/motor')
def begin():
    #return setup(send('config.json'))
    return start(send('data.json'))

def setup(config_json):
    #m1 = Motor.Motor(config_json['drivers'][0]['step'], config_json['drivers'][0]['dir'],config_json['drivers'][0]['enable'], speed_sps=10)
    return (config_json['drivers'][0]['step'])

def start(angles_json):
    #m1.target_deg(angles_json['angles']['m1'])
    return(angles_json['angles']['m1'])
    