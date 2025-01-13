from flask import jsonify, render_template, Blueprint, request
from models import Motor, Encoder
import time
from periphery import I2C




BPmotorController = Blueprint("motorController", __name__)
@BPmotorController.route('/motor/number', methods=['POST'])
def receive_number():
    try:
        data = request.get_json()  # Get the JSON data
        number = data['number']  # Extract the number
        m1 = Motor.Motor(55, 73,74, speed_sps=10)
        m1.target_deg(number)
        # Here you can add your business logic, for example:
        result = {"received_angle": number}
        print(number)
        return jsonify(result), 200
    except Exception as e:
        m1.stop()
        return jsonify({"error": str(e)}), 400  

@BPmotorController.route('/motor')
def start():
   
    return render_template('test.html')
    
