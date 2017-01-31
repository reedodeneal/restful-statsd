FROM debian:wheezy
MAINTAINER Reed Odeneal - "reed.odeneal@gmail.com"
CMD ["python","/usr/local/bin/restful-statsd.py"]
EXPOSE 8080
RUN useradd restful-statsd
RUN apt-get -y update && \
	apt-get -y install \
	python \
  	python-pip && pip install flask flask_api pyaml statsd
RUN apt-get clean && \
	rm -rf /var/lib/apt/lists/* \
	/tmp/* \
	/var/tmp/*
RUN mkdir -p /opt/apps/restful-statsd/
ADD restful-statsd.py /usr/local/bin/restful-statsd.py
ADD config.yaml /usr/local/bin/config.yaml
ADD version.py /usr/local/bin/version.py
RUN chmod +x /usr/local/bin/restful-statsd.py
USER restful-statsd