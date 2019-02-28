from flask import Flask, redirect, url_for, request, jsonify, json, Response

from Persona import Persona

app = Flask(__name__)

segment_persona_map = {
        "segment_0": "Persona 0", "segment_1": "Persona 1", "segment_2": "Persona 2", "segment_3": "Persona 3"
    }


@app.route('/')
def hello_world():
    return 'Welcome to Persona Based Store Service!'


@app.route('/api/v1/categories/<gender>')
def get_categories(gender):
    # hardcoding the gender for the time being since our data is only for female category
    gender = 'female';
    print('Categories for %s' % gender)
    js = open('static/json/categories.json').read()
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/personas/<gender>')
def get_personas(gender):
    # hardcoding the gender for the time being since our data is only for female category
    file_name = 'personas_' + gender+'.json'
    print('Personas for %s' % gender)
    js = open('static/json/' + file_name).read()
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/personas/computed', methods=['POST'])
def predict_persona():
    json_string = json.dumps(request.get_json())
    json_dict = json.loads(json_string)
    print(json_dict["gender"])
    gender_value = json_dict["gender"]
    selected_attributes = json_dict["selectedAttributes"]
    selected_attributes_category = selected_attributes["name"]
    selected_attributes_array = selected_attributes["attributes"]

    param_dict = {}

    for x in selected_attributes_array:
        print ('name %s' % x["name"])
        print ('value %s' % x["value"])
        param_dict[x["name"]] = x["value"][0]

    print(gender_value + " " + selected_attributes_category)
    print (param_dict)

    return calculate_persona(param_dict)


def calculate_persona(param_dict):
    obj = Persona()
    obj.load_model('computation/segment_params.txt', 'computation/segment_predictions.csv')
    predicted_persona = obj.predict_persona(param_dict)
    print('Predicted Persona %s' % predicted_persona)
    persona = predicted_persona.pop()
    return segment_persona_map[persona]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
