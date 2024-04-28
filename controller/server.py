import sys, os
from flask import Flask, render_template, request
import psonic
from algoritme import sonic_pi_algo
import random

sonic_pi_algo_test = """
# Fm Noise

# Coded by Sam Aaron

use_synth :fm

live_loop :sci_fi do
  p = play (chord :Eb3, :minor).choose - [0, 12, -12].choose, divisor: 0.01, div_slide: rrand(0, 10), depth: rrand(0.001, 2), attack: 0.01, release: rrand(0, 5), amp: 0.5
  control p, divisor: rrand(0.001, 50)
  sleep [0.5, 1, 2].choose
end

"""

psonic.set_server_parameter('127.0.0.1', 4557, 4559)

app = Flask(__name__)
    
def log(message):
    print(message)
    sys.stdout.flush()


@app.route('/start')
def start():
    # Make jack connections from SC to webrtc server (in case they did not exist)
    os.system('jack_connect SuperCollider:out_1 webrtc-server:in_jackaudiosrc0_1')
    os.system('jack_connect SuperCollider:out_2 webrtc-server:in_jackaudiosrc0_2')
    os.system('jack_lsp -c')

    # Select new seed and run algorithm
    new_seed = request.args.get('seed', default=-1, type=int)
    if new_seed == -1:
        new_seed = random.randint(0, 999999)
    log(f'\n**********Stopping and setting new seed: {new_seed}************\n')
    psonic.stop()
    psonic.run(sonic_pi_algo.format(new_seed))
    return {'result': 'started'}
    
