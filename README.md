# UDP Server

The server parses the received messages and prints the timestamp and the message body in JSON to the stdout.

Messages are parsed with `pygrok`. Patterns are defined in [patterns](app/patterns/) directory. 
Refer to [requirements.txt](requirements.txt) for dependencies versions.

Use environments variables `UDP_IP` and `UDP_PORT` to configure the server.

## Build

`docker-compose build`

## Run

`docker-compose run`

## Test

The application can be tested with `nc` of `iperf`:

`echo -n "[17/06/2016 12:30] Time to move" | nc -u localhost 5001`

`iperf -c localhost -u -b 100m -t 100`

Test code changes with `nosetests app`.

Install testing requirements with `pip install -r app/tests/requirements.txt`
