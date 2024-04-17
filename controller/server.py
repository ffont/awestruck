import sys
from flask import Flask, render_template, request
from pythonosc import udp_client
import psonic
from algoritme import sonic_pi_algo

osc_client = None
psonic.set_server_parameter('worker', 4557, 4559)

app = Flask(__name__)

def send_osc_message(address, value):
    global osc_client
    if osc_client is None:
        try:
            osc_client = udp_client.SimpleUDPClient('worker', 57120)
        except Exception:
            # Could not establish connection
            log("Could not establish osc connection")
            return False
    log(f"Sending osc message! {address} {value}")
    osc_client.send_message(f'/{address}', float(value))
    return True
    
def log(message):
    print(message)
    sys.stdout.flush()

@app.route('/send_osc')
def send_osc():
    # Endpoint to receive OSC message command via HTTP
    # Will forward the messages to the worker service
    address = request.args.get('address')
    value = request.args.get('value')
    result = send_osc_message(address, value)
    return {'result': result}


@app.route('/start')
def start():
    new_seed = request.args.get('seed', default=1234, type=int)
    log(f'\n**********Stopping and setting new seed: {new_seed}************\n')
    psonic.stop()
    psonic.run(sonic_pi_algo.format(new_seed))
