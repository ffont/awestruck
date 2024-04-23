#! /bin/bash
(nc -lk -u 127.0.0.1 -p 4558 &) && 
(jackd -r --port-max 20 -d dummy &) && sleep 3 && 
jack_lsp -c && 
(/usr/lib/sonic-pi/server/bin/sonic-pi-server.rb &) && sleep 1 &&
(/app/webrtc-server &) &&
(flask --app server run --host=0.0.0.0 --port 54321)