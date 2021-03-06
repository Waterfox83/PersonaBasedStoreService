from flask import Flask, redirect, url_for, request, jsonify, json, Response
from twilio.rest import Client

from Persona import Persona

app = Flask(__name__)

segment_persona_map = {
        "segment_0": "Persona 0", "segment_1": "Persona 1", "segment_2": "Persona 2", "segment_3": "Persona 3"
    }
account_sid = '<twilio account_sid>'
auth_token = '<twilio auth_token>'
whatsapp_sender = 'whatsapp:<twilio number>'

@app.route('/')
def hello_world():
    return 'Welcome to Persona Based Store Service!'


@app.route('/api/v1/sendMessage', methods=['POST'])
def send_message():
    json_string = json.dumps(request.get_json())
    json_dict = json.loads(json_string)

    phone_number = 'whatsapp:' + json_dict['phoneNumber']
    location = json_dict['location']
    persona_name = json_dict['personaName']
    result_summary = 'Your persona is ' + persona_name + ' . Please head to ' + location + ' to enjoy the collection '
    'curate according to your taste. Happy shopping!'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=whatsapp_sender,
        body=result_summary,
        to=phone_number
    )

    return Response(message.sid, status=200, mimetype='application/json')


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
        if len(x["value"]) != 0:
            param_dict['Attribute_' + (x["name"].lower()).replace(' ','_')] = x["value"][0]

    print(gender_value + " " + selected_attributes_category)

    return Response(calculate_persona(param_dict, selected_attributes_category), status=200, mimetype='application/json')


def calculate_persona(param_dict, selected_attributes_category):
    obj = Persona()

    if selected_attributes_category == 'Dresses for Women':
        obj.load_model('computation/segment_params.txt', 'computation/segment_predictions.csv')
    elif selected_attributes_category == 'Denims for Women':
        obj.load_model('computation/segment_params_denim.txt', 'computation/segment_predictions_denim.csv')

    file_name = 'personas_female.json'
    js = open('static/json/' + file_name).read()
    personas_list = json.loads(js)

    results_list = personas_list

    if len(param_dict) != 0:
        predicted_persona = obj.predict_persona(param_dict)
        print('Predicted Persona %s' % predicted_persona)
        persona = predicted_persona.pop()
        persona_name = segment_persona_map[persona]
        print ('Computed Persona: %s' % persona_name)

        index_of_space = persona_name.index(' ')
        persona_id = int(persona_name[index_of_space+1:])
        results_list = personas_list[persona_id:persona_id+1]

    return json.dumps(results_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

