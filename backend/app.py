from random import randint
from flask import Flask,render_template,jsonify, request
import os
import importlib
from flask_cors import CORS
app = Flask('app', static_folder= "../dist/static", template_folder= "../dist")
CORS(app)  

#Comands:
#source venv/bin/activate


# import blueprints
def register_blueprints(app):
    for filename in os.listdir('controllers'):
        if filename.endswith('Controller.py'):
            module_name = filename[:-3]
            module = importlib.import_module(f'controllers.{module_name}')
            
            blueprint_name = f'BP{module_name}'
            blueprint = getattr(module, blueprint_name, None)
            if blueprint is not None:
                app.register_blueprint(blueprint)

#api
'''@app.route('/api', methods=["POST"])
def submitData():
    response_object = {'status':'success'}
    data = request.get_json()
    num   = data['number']
    print(num)
    response_object['message'] ='Data added!'
    return jsonify(response_object)'''


'''@app.route('/motor/number', methods=['POST'])
def receive_number():
    try:
        data = request.get_json()  # Get the JSON data
        number = data['number']  # Extract the number
        motorControl = number
        # Here you can add your business logic, for example:
        result = {"received_angle": number}
        print(number)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400  '''
    

    
#api




#home page
@app.route('/')
def basic():
    return render_template('index.html')
#starting aplication
if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0', port=5000,debug=True)