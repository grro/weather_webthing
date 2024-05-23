import sys
import logging
import tornado.ioloop
from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
from weather import Weather




class WeatherThing(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, description: str, weather: Weather):
        Thing.__init__(
            self,
            'urn:dev:ops:weather-1',
            'WeatherSensor',
            ['MultiLevelSensor'],
            description
        )
        self.ioloop = tornado.ioloop.IOLoop.current()
        self.weather = weather
        self.weather.set_listener(self.on_value_changed)

        self.temp_max_day_plus_0 = Value(weather.temp_max_day_plus_0)
        self.add_property(
            Property(self,
                     'temp_max_day_plus_0',
                     self.temp_max_day_plus_0,
                     metadata={
                         'title': 'temp_max_day_plus_0',
                         "type": "float",
                         'description': 'the max temp today',
                         'readOnly': True,
                     }))

        self.temp_max_day_plus_1 = Value(weather.temp_max_day_plus_1)
        self.add_property(
            Property(self,
                     'temp_max_day_plus_1',
                     self.temp_max_day_plus_1,
                     metadata={
                         'title': 'temp_max_day_plus_1',
                         "type": "float",
                         'description': 'the max temp today + 1 day',
                         'readOnly': True,
                     }))

        self.temp_max_day_plus_2 = Value(weather.temp_max_day_plus_2)
        self.add_property(
            Property(self,
                     'temp_max_day_plus_2',
                     self.temp_max_day_plus_2,
                     metadata={
                         'title': 'temp_max_day_plus_2',
                         "type": "float",
                         'description': 'the max temp today + 2 days',
                         'readOnly': True,
                     }))


        self.temp_max_day_plus_3 = Value(weather.temp_max_day_plus_3)
        self.add_property(
            Property(self,
                     'temp_max_day_plus_3',
                     self.temp_max_day_plus_3,
                     metadata={
                         'title': 'temp_max_day_plus_3',
                         "type": "float",
                         'description': 'the max temp today + 3 days',
                         'readOnly': True,
                     }))

        self.temp_min_day_plus_0 = Value(weather.temp_min_day_plus_0)
        self.add_property(
            Property(self,
                     'temp_min_day_plus_0',
                     self.temp_min_day_plus_0,
                     metadata={
                         'title': 'temp_min_day_plus_0',
                         "type": "float",
                         'description': 'the min temp today',
                         'readOnly': True,
                     }))

        self.temp_min_day_plus_1 = Value(weather.temp_min_day_plus_1)
        self.add_property(
            Property(self,
                     'temp_min_day_plus_1',
                     self.temp_min_day_plus_1,
                     metadata={
                         'title': 'temp_min_day_plus_1',
                         "type": "float",
                         'description': 'the min temp today +  1 day',
                         'readOnly': True,
                     }))

        self.temp_min_day_plus_2 = Value(weather.temp_min_day_plus_2)
        self.add_property(
            Property(self,
                     'temp_min_day_plus_2',
                     self.temp_min_day_plus_2,
                     metadata={
                         'title': 'temp_min_day_plus_2',
                         "type": "float",
                         'description': 'the min temp today + 2 days',
                         'readOnly': True,
                     }))

        self.temp_min_day_plus_3 = Value(weather.temp_min_day_plus_3)
        self.add_property(
            Property(self,
                     'temp_min_day_plus_3',
                     self.temp_min_day_plus_3,
                     metadata={
                         'title': 'temp_min_day_plus_3',
                         "type": "float",
                         'description': 'the min temp today + 3 days',
                         'readOnly': True,
                     }))

        self.sunrise_time= Value(weather.sunrise_time.strftime("%Y-%m-%dT%H:%M"))
        self.add_property(
            Property(self,
                     'sunrise_time_utc',
                     self.sunrise_time,
                     metadata={
                         'title': 'sunrise_time_utc',
                         "type": "string",
                         'description': 'the sunrise time as ISO8602 string (utc)',
                         'readOnly': True,
                     }))

        self.sunset_time = Value(weather.sunset_time.strftime("%Y-%m-%dT%H:%M"))
        self.add_property(
            Property(self,
                     'sunset_time_utc',
                     self.sunset_time,
                     metadata={
                         'title': 'sunset_time_utc',
                         "type": "string",
                         'description': 'the sunset time as ISO8602 string (utc)',
                         'readOnly': True,
                     }))

    def on_value_changed(self):
        self.ioloop.add_callback(self._on_value_changed)

    def _on_value_changed(self):
        self.temp_max_day_plus_0.notify_of_external_update(self.weather.temp_max_day_plus_0)
        self.temp_max_day_plus_1.notify_of_external_update(self.weather.temp_max_day_plus_1)
        self.temp_max_day_plus_2.notify_of_external_update(self.weather.temp_max_day_plus_2)
        self.temp_max_day_plus_3.notify_of_external_update(self.weather.temp_max_day_plus_3)
        self.temp_min_day_plus_0.notify_of_external_update(self.weather.temp_min_day_plus_0)
        self.temp_min_day_plus_1.notify_of_external_update(self.weather.temp_min_day_plus_1)
        self.temp_min_day_plus_2.notify_of_external_update(self.weather.temp_min_day_plus_2)
        self.temp_min_day_plus_3.notify_of_external_update(self.weather.temp_min_day_plus_3)
        self.sunset_time.notify_of_external_update(self.weather.sunset_time.strftime("%Y-%m-%dT%H:%M"))
        self.sunrise_time.notify_of_external_update(self.weather.sunrise_time.strftime("%Y-%m-%dT%H:%M"))


def run_server(description: str, port: int, station_id: str):
    weather = Weather(station_id)
    server = WebThingServer(SingleThing(WeatherThing(description, weather)), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server http://localhost:' + str(port))
        weather.start()
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        weather.stop()
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger('tornado.access').setLevel(logging.ERROR)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    run_server("description", int(sys.argv[1]), sys.argv[2])
