import logging
from threading import Thread
from time import sleep
from datetime import datetime, timedelta
from pyowm import OWM



class Weather:

    def __init__(self, key: str, location: str):
        self.__is_running = True
        self.__listener = lambda: None    # "empty" listener
        self.__location = location
        lat, lon = self.__location.split(",")
        self.lat = float(lat.strip())
        self.lon = float(lon.strip())

        self.sunrise_time = None
        self.sunset_time = None
        self.temp_max_day_plus_0 = 0
        self.temp_max_day_plus_1 = 0
        self.temp_max_day_plus_2 = 0
        self.temp_max_day_plus_3 = 0

        self.__mgr = OWM(key).weather_manager()
        self.__sync()

    def set_listener(self,listener):
        self.__listener = listener

    def start(self):
        Thread(target=self.__sync_loop, daemon=True).start()

    def stop(self):
        self.__is_running = False

    def __sync_loop(self):
        while self.__is_running:
            try:
                self.__sync()
                sleep(9 * 60)
            except Exception as e:
                logging.warning("error occurred on sync " + str(e))
                sleep(3)


    def __datetime_day_granuality(self, dt: datetime) -> datetime:
        return datetime.strptime(dt.strftime("%Y-%m-%d")+ "T12:00", "%Y-%m-%dT%H:%M")


    def __sync(self):
        today = self.__mgr.weather_at_coords(self.lat, self.lon)
        self.temp_max_day_plus_0 = today.weather.temperature('celsius')['temp_max']

        self.sunset_time = datetime.fromtimestamp(today.weather.sunset_time())
        self.sunrise_time = datetime.fromtimestamp(today.weather.sunrise_time())

        forecast = self.__mgr.forecast_at_coords(self.lat, self.lon, 'daily')
        plus_1 = forecast.get_weather_at(self.__datetime_day_granuality(datetime.utcnow() + timedelta(days=1)))
        self.temp_max_day_plus_1 = plus_1.temperature('celsius')['max']
        plus_2 = forecast.get_weather_at(self.__datetime_day_granuality(datetime.utcnow() + timedelta(days=2)))
        self.temp_max_day_plus_2 = plus_2.temperature('celsius')['max']
        plus_3 = forecast.get_weather_at(self.__datetime_day_granuality(datetime.utcnow() + timedelta(days=3)))
        self.temp_max_day_plus_3 = plus_3.temperature('celsius')['max']

        self.__listener()


