import requests
import data
from colorama import Fore, Back, Style
import time

def main():
    class Station:
        def __init__(self, id: int, ip: str) -> None:
            self.id = id
            self.ip = ip

    stations = []
    for s in data.get_all_stations():
        stations.append(Station(s[0], s[1]))

    while True:
        for station in stations:
            try:
                result = requests.get(station.ip)
                temperature, humidity = result.text.split(":")
                print(Fore.GREEN + temperature + "°C " + Style.RESET_ALL + Fore.BLUE + humidity + "%" + Style.RESET_ALL)
                data.add_value(station.id, temperature, humidity)
            except:
                print(Fore.RED + "SYSTEM ERROR: STATION IS OFFLINE!" + Style.RESET_ALL)
        time.sleep(10)