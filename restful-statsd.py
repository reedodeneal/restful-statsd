# restful-statsd
# Author: Reed Odeneal

import os, logging, yaml, statsd, socket
from flask import Flask, jsonify, request
from flask_api import status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = Flask(__name__)
prefix = "/api/v1"

@api.route(prefix + "/version/")
def version():
    return jsonify(version=__version__)

# accepts content-type=application/json with a json list of metic objects each containing a name, type, and value
@api.route(prefix + "/metrics/", methods=['POST'])
def recordMetric():
	logger.info("Received metrics payload. Streaming to statsd endpoint at " + config["statsd.server"] + ":" + config["statsd.port"])
	
	metrics = request.json

	# get the metric type
	for m in metrics:
		# TODO: Support timer type.
		if m["type"] == "count":
			logger.info("Recording count metric with name " + m["name"] + " and value " + m["value"])
			sc.incr(m["name"], int(m["value"]))
		elif m["type"] == "gauge":
			logger.info("Recording gauge metric with name " + m["name"] + " and value " + m["value"])
			sc.gauge(m["name"], int(m["value"]))
		else:
			logger.error("Invalid metric type " + m["type"] + " for " + m["name"])

	return "",status.HTTP_202_ACCEPTED

if __name__ == "__main__":

	with open(os.path.dirname(os.path.realpath(__file__)) + "/version.py") as vf:
		exec(vf.read())

	logger.info("Loading config")
	config = yaml.safe_load(open(os.path.dirname(os.path.realpath(__file__)) + "/config.yaml"))

	# we have to pass the ip of the statsd endpoint to the client, so
	if not config["statsd.server"].isdigit():
		statsdIp = repr(socket.gethostbyname_ex(config["statsd.server"])[2][0]).translate(None, "'")
	else:
		statsdIp = config["statsd.server"]

	logger.info("Creating connection object for to statsd endpoint at " + config["statsd.server"] + ":" + config["statsd.port"])
	sc = statsd.StatsClient(statsdIp,config["statsd.port"])

	logger.info("Starting restful-statsd API listener on TCP " + config["api.port"])
	api.run(host='0.0.0.0',port=int(config["api.port"]))
