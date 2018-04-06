# api-proxy-reference

This is an example of how to use docker-compose to orchestrate 2 containers:
1. An API proxy server. This server takes in flask requests and makes calls to another destination, collects response and sends it back to the original requester. This server is run with gunicorn
2. An nginx instance used as a load balancer for the app server

HOW TO USE?
Just download the whole thing and run ./run_docker_compose.sh. It is useful for AWS implemementations.
