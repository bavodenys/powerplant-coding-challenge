from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def determine_production_plan():
    data = request.json
    response = []
    for powerplant in data['powerplants']:
        response.append({'name': powerplant['name'],
                         'p': 0})
    return jsonify(response)

@app.route('/')
def testpoint():
    return jsonify("Powerplan coding challenge")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8888))
    app.run(debug=True, host='0.0.0.0', port=port)
