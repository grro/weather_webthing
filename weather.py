import logging
from threading import Thread
from time import sleep
from datetime import datetime, timedelta
import requests



class Weather:

    def __init__(self, station_id: str):
        self.__is_running = True
        self.__listener = lambda: None    # "empty" listener
        self.station_id = station_id

        self.sunrise_time = None
        self.sunset_time = None
        self.temp_max_day_plus_0 = 0
        self.temp_max_day_plus_1 = 0
        self.temp_max_day_plus_2 = 0
        self.temp_max_day_plus_3 = 0
        self.temp_min_day_plus_0 = 0
        self.temp_min_day_plus_1 = 0
        self.temp_min_day_plus_2 = 0
        self.temp_min_day_plus_3 = 0

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
        today = datetime.now()
        resp = requests.get("https://app-prod-ws.warnwetter.de/v30/stationOverviewExtended?stationIds=" + self.station_id)
        resp.raise_for_status()
        data = resp.json()[self.station_id]
        for day in data['days']:
            if day['dayDate'] == today.strftime("%Y-%m-%d"):
                self.temp_max_day_plus_0 = day['temperatureMax'] / 10
                self.temp_min_day_plus_0 = day['temperatureMin'] / 10
                self.sunset_time = datetime.fromtimestamp(int(day['sunset']/1000))
                self.sunrise_time = datetime.fromtimestamp(int(day['sunrise']/1000))
            elif day['dayDate'] == (today + timedelta(days=1)).strftime("%Y-%m-%d"):
                self.temp_max_day_plus_1 = day['temperatureMax'] / 10
                self.temp_min_day_plus_1 = day['temperatureMin'] / 10
            elif day['dayDate'] == (today + timedelta(days=2)).strftime("%Y-%m-%d"):
                self.temp_max_day_plus_2 = day['temperatureMax'] / 10
                self.temp_min_day_plus_2 = day['temperatureMin'] / 10
            elif day['dayDate'] == (today + timedelta(days=3)).strftime("%Y-%m-%d"):
                self.temp_max_day_plus_3 = day['temperatureMax'] / 10
                self.temp_min_day_plus_3 = day['temperatureMin'] / 10

        logging.info("sunrise:         " + self.sunrise_time.strftime("%H:%M"))
        logging.info("sunset:          " + self.sunset_time.strftime("%H:%M"))
        logging.info("max temp today:  " + str(self.temp_max_day_plus_0))

        self.__listener()


