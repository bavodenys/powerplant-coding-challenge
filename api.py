from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Calibrations
CO2_ton_MWh = 0.3

@app.route('/productionplan', methods=['POST'])
def determine_production_plan():
    data = request.json
    for powerplant in data['powerplants']:
        if powerplant['type'] == 'gasfired':
            powerplant['cost'] = data['fuels']['gas(euro/MWh)']/powerplant['efficiency'] + \
                                 data['fuels']['co2(euro/ton)']*CO2_ton_MWh
        elif powerplant['type'] == 'turbojet':
            powerplant['cost'] = data['fuels']['kerosine(euro/MWh)']/powerplant['efficiency']
        elif powerplant['type'] == 'windturbine':
            powerplant['pmax_op'] = powerplant['pmax']*data['fuels']['wind(%)']/100
            powerplant['cost'] = 0
        else:
            print('other type')

    # Sort the powerplants on cost to produce energy
    data['powerplants'] = sorted(data['powerplants'], key=lambda d: d['cost'])
    remaining_load = data['load']
    response = []
    for count, powerplant in enumerate(data['powerplants']):
        if remaining_load == 0:
            response.append({'name': powerplant['name'],
                             'p': 0})
        else:
            if remaining_load >= powerplant['pmin']:
                # Get the max P of the plant
                if powerplant['type'] == 'windturbine':
                    pmax_op = powerplant['pmax_op']
                else:
                    pmax_op = powerplant['pmax']
                # Compare remaining load with Pmax of powerplant
                if pmax_op < remaining_load:
                    # Check if provisioned remaining load is smaller than Pmin of the next powerplant
                    # If so, limit P just so that next powerplant runs at min P
                    if (remaining_load - pmax_op) < data['powerplants'][count+1]['pmin']:
                        response.append({'name': powerplant['name'],
                                         'p': remaining_load - data['powerplants'][count+1]['pmin']})
                        remaining_load = data['powerplants'][count+1]['pmin']
                    else:
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
