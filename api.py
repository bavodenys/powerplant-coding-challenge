from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def determine_production_plan():
    data = request.json
    for powerplant in data['powerplants']:
        if powerplant['type'] == 'gasfired':
            powerplant['cost'] = data['fuels']['gas(euro/MWh)']/powerplant['efficiency']
        elif powerplant['type'] == 'turbojet':
            powerplant['cost'] = data['fuels']['kerosine(euro/MWh)']/powerplant['efficiency']
        elif powerplant['type'] == 'windturbine':
            powerplant['pmax_op'] = powerplant['pmax']*data['fuels']['wind(%)']/100
            powerplant['cost'] = 0
        else:
            print('other type')
    remaining_load = data['load']
    response = []
    for powerplant in sorted(data['powerplants'], key=lambda d: d['cost']):
        print(f"{powerplant['name']}:{remaining_load}, {powerplant['pmin']}")
        if remaining_load == 0:
            response.append({'name': powerplant['name'],
                             'p': 0})
        else:
            if remaining_load >= powerplant['pmin']:
                if powerplant['type'] == 'windturbine':
                    pmax_op = powerplant['pmax_op']
                else:
                    pmax_op = powerplant['pmax']
                if pmax_op < remaining_load:
                    response.append({'name': powerplant['name'],
                                     'p': pmax_op})
                    remaining_load = remaining_load - pmax_op
                else:
                    response.append({'name': powerplant['name'],
                                     'p': remaining_load})
                    remaining_load = 0
            else:
                pass

    return jsonify(response)

@app.route('/')
def testpoint():
    return jsonify("Powerplan coding challenge")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8888))
    app.run(debug=True, host='0.0.0.0', port=port)
