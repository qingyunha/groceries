# coding:utf-8
from __future__ import division, print_function
import os
import re
import time
import logging
import argparse

import requests
from bs4 import BeautifulSoup

from buslines import BUSLINES

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)


class GJ(object):
    BUSLINES = BUSLINES
    HOME = "http://shanghaicity.openservice.kankanews.com"
    USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0.1; ATH-TL00H Build/HONORATH-TL00H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.8 TBS/036872 Safari/537.36 MicroMessenger/6.3.30.920 NetType/WIFI Language/zh_CN"
    HEADERS = {
        "Host": "shanghaicity.openservice.kankanews.com",
        "User-Agent": USER_AGENT
        }

    def __init__(self, busname):
        self.busname = busname
        self.sid = None
        self.s = requests.session()
        self.s.headers.update(self.HEADERS)
        self.direction = 1
        self.stations = {}
        self.prepare()

    def prepare(self):
        try:
            logging.debug("Visit Home")
            self.s.get(self.HOME)

            logging.debug("Visit public bus")
            self.s.get(self.HOME+'/public/bus',
                headers={"Referer": "http://shanghaicity.openservice.kankanews.com"})

            logging.debug("Get 161路 sid")
            r = self.s.post(self.HOME+'/public/bus/get',data={"idnum": self.busname},
                headers={"Referer": "http://shanghaicity.openservice.kankanews.com/public/bus"})
            self.sid = r.json()["sid"]

            logging.debug("Visite 161路")
            self.s.get(self.HOME+'/public/bus/mes/sid/'+self.sid,
                headers={"Referer": "http://shanghaicity.openservice.kankanews.com/public/bus"})
        except Exception as e:
            logging.error(e)
            self._prepared = False
            return False
        else:
            self._prepared = True
            return True

    def get_stop_info(self, direction=1, stopid=6):
        # stoptype=0 stopid=6 成山路博华路 上班
        # stoptype=1 stopid=6 碧波路晨晖路 下班
        if not self._prepared:
            if not self.prepare():
                return -2, -2
        logging.debug("Get time")
        stopid = str(stopid) + "."
        r = self.s.post(self.HOME+"/public/bus/Getstop",
            # data="stoptype=0&stopid=12.&sid=0145427642ef6ef77fc0652c39d5039c",
            data=dict(stoptype=direction, stopid=stopid, sid=self.sid),
            headers={
                "Referer": "http://shanghaicity.openservice.kankanews.com/public/bus/mes/sid/"+self.sid,
                # "Origin": "http://shanghaicity.openservice.kankanews.com",
                # "Content-Type": "application/x-www-form-urlencoded",
            })
        print(r.content)
        try:
            j = r.json()
            left_stop = int(j[0]["stopdis"])
            left_time = int(re.findall("\d+", j[0]["time"])[0])
            if u"分钟" not in j[0]["time"]:
                left_time = left_time/60.0
            return left_stop, left_time
        except Exception as e:
            import traceback
            logging.error(traceback.format_exc())
            # logging.error(e)
            return -1, -1

    def get_cur_stop_info(self, stopid=6):
        return self.get_stop_info(self.direction, stopid)

    def get_stations(self, direction=1):
        if direction in self.stations:
            return self.stations[direction]
        else:
            url = self.HOME + '/public/bus/mes/sid/' + self.sid
            if direction == 1:
                url = url + "/stoptype/1"
            r = self.s.get(url,
                headers={"Referer": "http://shanghaicity.openservice.kankanews.com/public/bus"})
            if r.ok:
                bs = BeautifulSoup(r.content, "html.parser")
                stations = bs.find_all("div", {"class": "station"})
                stations = list(map(lambda x: x.get_text().strip(), stations))
                self.stations[direction] = stations
                return stations
            else:
                logging.warn("can't get stations")

    def get_cur_stations(self):
        return self.get_stations(self.direction)

    @classmethod
    def search_bus(cls, busname):
        return filter(
            lambda busline: busname in busline,
            cls.BUSLINES)

    @classmethod
    def get_bus(cls, busname):
        if isinstance(busname, str):
            busname = busname.decode("utf-8", errors="ignore")
        assert busname in cls.BUSLINES, "没有这条线路"
        return cls(busname)


def alert(left_stop, left_time):
    if left_time < 0:
        msg = "TMD, 还没发车"
    else:
        msg = "快！还有%d站，%.2f分钟" % (left_stop, left_time)

    os.system("notify-send 注意 '%s'" % msg)
    os.system("for i in `pgrep bash|xargs ps -f|grep pts|awk '{print $6}'`; do echo %s >/dev/$i; done" % msg)


def parse_time(time_string):
    v = time_string.split(":")
    if len(v) != 2:
        raise ValueError("not suitbale time format", time_string)
    else:
        return list(map(int, v))
    

def parse_argments():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--direction', type=int, 
                        choices=[0,1],
                        required=True,
                        help='0 上班   1 下班')
    parser.add_argument('--time', type=parse_time, 
                        required=True,
                        help='报警时间 hh:mm')
    parser.add_argument('--interval', "-i", type=float, 
                        default=3.0,
                        help='报警间隔时间(min) 默认3min')
    parser.add_argument('--num', "-n", type=int, 
                        default=10,
                        help='报警次数 默认10次')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_argments()
    alert_time = args.time[0]*60 + args.time[1] 
    gj = GJ("161路")
    while True:
        now = time.localtime()
        if alert_time < now.tm_hour*60 + now.tm_min:
            time.sleep(args.interval*60)
            continue
        for i in range(args.num):
            alert(*gj.get_stop_info(args.direction))
            time.sleep(args.interval*60)
        break
