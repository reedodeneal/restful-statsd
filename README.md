# restful-statsd

restful-statsd is a simple RESTful API used to send metrics to statsd.

## example POST payload
```
[
	{"name":"some.metric","type":"gauge","value":"123"},
	{"name":"some.other.metric","type":"gauge","value":"123"}
]
```
