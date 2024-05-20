FROM python:3-alpine

ENV port 8443
ENV stationId "K887"


RUN cd /etc
RUN mkdir app
WORKDIR /etc/app
ADD *.py /etc/app/
ADD requirements.txt /etc/app/.
RUN pip install -r requirements.txt

CMD python /etc/app/weather_webthing.py $port $stationId



