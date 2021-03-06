# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fetchScheduler
   Description :
   Author :        JHao
   date：          2019/8/6
-------------------------------------------------
   Change Activity:
                   2019/08/06:
-------------------------------------------------
"""
__author__ = 'JHao'

import os
from handler.logHandler import LogHandler
from handler.proxyHandler import ProxyHandler
from fetcher.proxyFetcher import ProxyFetcher
from handler.configHandler import ConfigHandler
from qqwry import QQwry


class Fetcher(object):
    name = "fetcher"

    def __init__(self):
        self.log = LogHandler(self.name)
        self.conf = ConfigHandler()
        self.proxy_handler = ProxyHandler()
        self.loadIp()

    def loadIp(self):
        if False != os.path.isfile("qqwry.dat"):
            self.ip = QQwry()
            self.ip.load_file('qqwry.dat')
        else:
            self.ip = False

    def fetch(self):
        """
        fetch proxy into db with proxyFetcher
        :return:
        """
        proxy_set = set()
        self.log.info("ProxyFetch : start")
        for fetch_name in self.conf.fetchers:
            self.log.info("ProxyFetch - {func}: start".format(func=fetch_name))
            fetcher = getattr(ProxyFetcher, fetch_name, None)
            if not fetcher:
                self.log.error("ProxyFetch - {func}: class method not exists!")
                continue
            if not callable(fetcher):
                self.log.error("ProxyFetch - {func}: must be class method")
                continue

            try:
                for proxy in fetcher():
                    if proxy in proxy_set:
                        self.log.info('ProxyFetch - %s: %s exist' % (fetch_name, proxy.ljust(23)))
                        continue
                    else:
                        self.log.info('ProxyFetch - %s: %s success' % (fetch_name, proxy.ljust(23)))

                    if proxy.strip():
                        if self.ip:
                            area = " ".join(self.ip.lookup(proxy.split(':')[0]))
                        else:
                            self.loadIp()
                            area = ''
                        proxy_set.add((proxy, fetch_name, area))
                        
            except Exception as e:
                self.log.error("ProxyFetch - {func}: error".format(func=fetch_name))
                self.log.error(str(e))
        self.log.info("ProxyFetch - all complete!")
        return proxy_set
        # origin proxy_set = {'1.1.1.1', '2.2.2.2'}
        # now proxy_set = [('1.1.1.1', 'fetch1', 'area'), ('2.2.2.2', 'fetch2', 'area')]

def runFetcher():
    return Fetcher().fetch()
