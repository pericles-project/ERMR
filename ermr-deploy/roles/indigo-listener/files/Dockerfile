FROM python:3.4.3-slim
MAINTAINER GeoSpark <john@geospark.co.uk>

RUN pip install requests oauth2

USER nobody
WORKDIR /scripts
ENTRYPOINT ["/usr/local/bin/python"]