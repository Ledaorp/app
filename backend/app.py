from flask import Flask,render_template,jsonify, request
import os
import importlib
from flask_cors import CORS
import json
app = Flask('app', static_folder= "../frontend-react/build/static", template_folder= "../frontend-react/build")
CORS(app)  

#Comands:
#source venv/bin/activate
# chmod 777 /sys/class/gpio/export


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

def set(file_name):
    response_object = {'status': 'success'}
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {
            'angles': {
                'm1': 0,
                'm2': 0,
                'm3': 0,
                'm4': 0,
                'm5': 0
            },
            'position': {
                'x': 0,
                'y': 0,
                'z': 0
            }
        }
    new_data = request.get_json()
    if 'angles' in new_data:
        for key, value in new_data['angles'].items():
            if key in data['angles']:
                data['angles'][key] = value
                
    if 'positions' in new_data:
        for key, value in new_data['positions'].items():
            if key in data['positions']:
                data['positions'][key] = value
    try:           
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e: 
            print(e)
    return jsonify(response_object)

'''def set(file_name):
    response_object = {'status':'success'}
    data = request.get_json()
    response_object['message'] ='Data added!'
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    file.close
    return jsonify(response_object)'''

def send(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    file.close
    return data

@app.route('/api/set/data', methods=["POST"])
def set_data():
    return set('data.json')
@app.route('/api/get/data')
def get_data():
    return send('data.json')
@app.route('/api/get/config')
def get_config():
    return send('config.json')



#api




#home page
@app.route('/')
def basic():
    return render_template('index.html')
#starting aplication
if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0', port=5000,debug=True)
    