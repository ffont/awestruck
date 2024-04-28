#! /bin/bash
(nc -lk -u 127.0.0.1 -p 4558 &) && 
(jackd -r -d dummy &) && sleep 1 &&  # --port-max 20 <- this seems to make things fail!
(/usr/lib/sonic-pi/app/server/ruby/bin/sonic-pi-server.rb &) &&  # start sonic pi, but don't load any patch
(/app/webrtc-server &) &&  # start go server that handles the gstreamer->webrtc stuff
(flask --app server run --host=0.0.0.0 --port 54321)  # start the flask server that controls the things!