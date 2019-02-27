from flask import Flask, redirect, url_for, request, jsonify, json, Response

from Persona import Persona

app = Flask(__name__)


def __init__(self):
    self.categories = ['dress', 'denim']
    return


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
    gender = 'female';
    print('Personas for %s' % gender)
    js = open('static/json/personas.json').read()
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/personas/computed', methods=['POST'])
def predict_persona():
    json_string = request.get_json()
    print(json_string)
    return jsonify(json_string)

    # input_request_object = json.loads(json_string)
    # return input_request_object['selectedAttributes']

    # return 'Computed persona'


@app.route('/api/v1/test', methods=['GET'])
def dummy():
    paramdict = {'Attribute_material': 'knit',
                 'Attribute_sleeve_length': 'long',
                 'Attribute_silhouette': 'sheath',
                 'Attribute_pattern_specific': 'ethnic',
                 'Attribute_price_band': 'best'}

    obj = Persona()
    obj.load_model('computation/segment_params.txt', 'computation/segment_predictions.csv')
    print(obj.predict_persona(paramdict))
    return 'success'
    # print(obj.segmentAffinities('segment_0'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
