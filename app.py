from flask import Flask, render_template
import random
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Sample data for demonstration
rooms = ['Living Room', 'Kitchen', 'Bedroom', 'Bathroom', 'Garage']
lights_status = {room: random.choice(['On', 'Off']) for room in rooms}
people_in_rooms = {room: random.randint(0, 4) for room in rooms}

past_power_consumption = [random.uniform(50, 150) for _ in range(10)]
future_power_consumption = [random.uniform(60, 140) for _ in range(10)]
colors_usage = {'Blue': 35, 'Cool White': 20, 'Green': 15, 'Red': 10, 'Warm White': 5}
light_usage_methods = {"Automatically": 50, "Voice": 20, "Switch": 15, "Mobile App": 15}

# Simulated electricity bill data (assume price per kWh = 0.15)
electricity_bill = [consumption * 0.15 for consumption in past_power_consumption]

# Custom tips based on usage
room_usage = {
    'Living Room': {'usage': 8, 'lights': 'On'},
    'Kitchen': {'usage': 5, 'lights': 'Off'},
    'Bedroom': {'usage': 10, 'lights': 'On'},
    'Bathroom': {'usage': 3, 'lights': 'Off'},
    'Garage': {'usage': 2, 'lights': 'Off'}
}

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

tips_to_reduce_power, energy_savings_data = generate_custom_tips(room_usage)

@app.route('/')
def home():
    # Light color usage pie chart
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
    consumption_bill_correlation_graph = {
        "data": [
            go.Scatter(
                x=list(range(10)),
                y=electricity_bill,
                mode='lines+markers',
                name='Electricity Bill',
                line=dict(color='blue')
            ),
            go.Scatter(
                x=list(range(10)),
                y=past_power_consumption,
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
    past_power_consumption_graph = {
        "data": [
            go.Scatter(
                x=list(range(10)),
                y=past_power_consumption,
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
    future_power_consumption_graph = {
        "data": [
            go.Scatter(
                x=list(range(10)),
                y=future_power_consumption,
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

if __name__ == '__main__':
    app.run(debug=True)
