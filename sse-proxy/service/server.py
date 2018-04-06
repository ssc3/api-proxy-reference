#!/usr/bin/env python3
from flask import Flask
#from flask_cors import CORS, cross_origin


from sse_proxy import sse_proxy_bp


import logging






app = Flask(__name__)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/')
def index():
	init()
	return 'Hello World'



def init():
	logging.basicConfig(filename='log/server.log', level=logging.DEBUG)
	
	app.url_map.strict_slashes = False
	app.register_blueprint(sse_proxy_bp, url_prefix='/v1')



if __name__ == "__main__":
	init()
	#app.run(debug=True)
	app.run()
