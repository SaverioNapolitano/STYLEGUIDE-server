from flask import Flask, render_template, request, jsonify
import random
import plotly
import plotly.graph_objs as go
import json
from database import *
from flask_mqtt import Mqtt 
from ai import compute_future_power_consumption
from config import Config

app = Flask(__name__)

#create_db()

mqtt = Mqtt(app)

app.config.from_object(Config)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('home/+/people')
    mqtt.subscribe('home/+/light')
    #mqtt.subscribe('home/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    room = data['topic'].removeprefix('home/')
    if 'people' in data['topic']:    
        room = room.removesuffix('/people').capitalize()
        if room == 'Livingroom':
            room = 'Living Room'
        people_in_rooms[room] = data['payload'].capitalize()
    else:
        room = room.removesuffix('/light').capitalize()
        if room == 'Livingroom':
            room = 'Living Room'
        lights_status[room] = data['payload'].capitalize()

# Sample data for demonstration
rooms = ['Living Room', 'Kitchen', 'Bedroom', 'Bathroom']

# Custom tips based on usage
room_usage = {
    'Living Room': {'usage': 8, 'lights': 'On'},
    'Kitchen': {'usage': 5, 'lights': 'Off'},
    'Bedroom': {'usage': 10, 'lights': 'On'},
    'Bathroom': {'usage': 3, 'lights': 'Off'}
}

lights_status = {room: 'Off' for room in rooms} # MQTT
people_in_rooms = {room: 0 for room in rooms} # MQTT

def generate_custom_tips(room_usage):
    tips = []
    energy_savings = []
    for room, data in room_usage.items():
        if data['lights'] == 'On' and data['usage'] > 6:
            tips.append(f"In the {room}, consider turning off the lights during low activity periods or using dimmer settings.")
            energy_savings.append({'room': room, 'savings': data['usage'] * 0.2})  # Assume 20% savings
        elif data['lights'] == 'On':
            tips.append(f"In the {room}, lights are on. You could save energy by turning them off when not in use.")
            energy_savings.append({'room': room, 'savings': data['usage'] * 0.1})  # Assume 10% savings
        elif data['lights'] == 'Off' and data['usage'] > 4:
            tips.append(f"In the {room}, energy usage is higher despite lights being off. Check for other appliances.")
    return tips, energy_savings

@app.route('/')
def home():
    #lights_status = {room: random.choice(['On', 'Off']) for room in rooms} # MQTT
    #people_in_rooms = {room: random.randint(0, 4) for room in rooms} # MQTT
    
    # Light color usage pie chart
    colors_usage = compute_colors_usage('Saverio')
    color_usage_graph = {
        "data": [
            go.Pie(
                labels=list(colors_usage.keys()),
                values=list(colors_usage.values()),
                hole=.3
            )
        ],
        "layout": go.Layout(title='Most Used Light Colors')
    }

    # Light usage methods pie chart 
    light_usage_methods = compute_light_usage_methods('Saverio')
    light_usage_methods_graph = {
        "data": [
            go.Pie(
                labels=list(light_usage_methods.keys()),
                values=list(light_usage_methods.values()),
                hole=.3
            )
        ],
        "layout": go.Layout(title='Most Used Light On Methods')
    }

    # Correlation between power consumption and electricity bill (continuous graph)
    past_power_consumption = compute_past_power_consumption('Saverio')
    # Simulated electricity bill data (assume price per kWh = 0.15)
    electricity_bill = [consumption * 0.15 for consumption in past_power_consumption.values()]
    consumption_bill_correlation_graph = {
        "data": [
            go.Scatter(
                x=list(past_power_consumption.keys()),
                y=electricity_bill,
                mode='lines+markers',
                name='Electricity Bill',
                line=dict(color='blue')
            ),
            go.Scatter(
                x=list(past_power_consumption.keys()),
                y=list(past_power_consumption.values()),
                mode='lines+markers',
                name='Power Consumption',
                line=dict(color='green')
            )
        ],
        "layout": go.Layout(
            title='Correlation Between Power Consumption and Electricity Bill',
            xaxis={'title': 'Time (Days)'},
            yaxis={'title': 'Value'},
            legend={'title': 'Legend'}
        )
    }

    return render_template(
        'home.html',
        rooms=rooms,
        lights_status=lights_status,
        people_in_rooms=people_in_rooms,
        color_usage_graph=json.dumps(color_usage_graph, cls=plotly.utils.PlotlyJSONEncoder),
        consumption_bill_correlation_graph=json.dumps(consumption_bill_correlation_graph, cls=plotly.utils.PlotlyJSONEncoder),
        light_usage_methods_graph=json.dumps(light_usage_methods_graph, cls=plotly.utils.PlotlyJSONEncoder)
    )

@app.route('/consumption')
def consumption():
    # Past power consumption graph
    past_power_consumption = compute_past_power_consumption('Saverio')
    past_power_consumption_graph = {
        "data": [
            go.Scatter(
                x=list(past_power_consumption.keys()),
                y=list(past_power_consumption.values()),
                mode='lines+markers',
                name='Past Consumption'
            )
        ],
        "layout": go.Layout(
            title='Past Power Consumption',
            xaxis={'title': 'Time (Days)'},
            yaxis={'title': 'Power Consumption (kWh)'}
        )
    }

    # Future power consumption graph
    future_power_consumption = compute_future_power_consumption('Saverio') # FBProphet / AI
    future_power_consumption_graph = {
        "data": [
            go.Scatter(
                x=list(future_power_consumption.keys()),
                y=list(future_power_consumption.values()),
                mode='lines+markers',
                name='Future Consumption'
            )
        ],
        "layout": go.Layout(
            title='Future Power Consumption',
            xaxis={'title': 'Time (Days)'},
            yaxis={'title': 'Power Consumption (kWh)'}
        )
    }

    # Energy savings graph
    tips_to_reduce_power, energy_savings_data = generate_custom_tips(room_usage)
    energy_savings_graph = {
        "data": [
            go.Bar(
                x=[entry['room'] for entry in energy_savings_data],
                y=[entry['savings'] for entry in energy_savings_data],
                name='Potential Savings'
            )
        ],
        "layout": go.Layout(
            title='Potential Energy Savings by Room',
            xaxis={'title': 'Room'},
            yaxis={'title': 'Energy Savings (kWh)'}
        )
    }

    return render_template(
        'consumption.html',
        tips_to_reduce_power=tips_to_reduce_power,
        past_power_consumption_graph=json.dumps(past_power_consumption_graph, cls=plotly.utils.PlotlyJSONEncoder),
        future_power_consumption_graph=json.dumps(future_power_consumption_graph, cls=plotly.utils.PlotlyJSONEncoder),
        energy_savings_graph=json.dumps(energy_savings_graph, cls=plotly.utils.PlotlyJSONEncoder)
    )

@app.route('/ranking')
def ranking():
    ranking_data = compute_rankings()
    return render_template('ranking.html', ranking=ranking_data)

@app.route('/bridge', methods = ['POST'])
def post_bridge():
    request_json = request.get_json()
    db_row = Data(request_json['timestamp'], request_json['username'], request_json['duration'], request_json['on mode'], request_json['off mode'], request_json['color'], request_json['light intensity'], request_json['power consumption'])
    add_data(db_row)
    print('add row to db')
    return 'OK', '200 OK'

@app.route('/colors')
def send_app_colors():
    return jsonify(compute_colors_usage('Saverio'))

@app.route('/lights')
def send_app_lights():
    return jsonify(compute_light_usage_methods('Saverio'))

@app.route('/cost')
def send_app_power():
    past_power_consumption = compute_past_power_consumption('Saverio')
    #electricity_bill = [consumption * 0.15 for consumption in past_power_consumption.values()]
    electricity_bill = {str(key): 0.15*value for key, value in past_power_consumption.items()}
    return jsonify(electricity_bill)

@app.route('/rank')
def send_app_ranking():
    ranking_data = compute_rankings()
    ranking_dict = {}
    for item in ranking_data:
        for key, value in item:
            ranking_dict[key] = value 
    return jsonify(ranking_dict)


@app.route('/past')
def send_app_past():
    past_power_consumption = {str(key): value for key, value in compute_past_power_consumption('Saverio').items()}
    return jsonify(past_power_consumption) 

@app.route('/future')
def send_app_future():
    future_power_consumption = {str(key): value for key, value in compute_future_power_consumption('Saverio').items()}
    return jsonify(future_power_consumption)



if __name__ == '__main__':
    app.run(host=app.config.get('FLASK_RUN_HOST', 'localhost'), port=app.config.get('FLASK_RUN_PORT', 8000))
