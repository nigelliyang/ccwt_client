#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/10/27 17:18    @Author  : xycfree
# @Descript: 
from pyalgotrade.barfeed import dbfeed
from pyalgotrade.barfeed import membf
from pyalgotrade import bar
from pyalgotrade.utils import dt


class Feed(membf.BarFeed):
    def __init__(self, frequency, dbConfig=None, maxLen=None):
        super(Feed, self).__init__(frequency, maxLen)
        self.__db = Database(dbConfig)

    def barsHaveAdjClose(self):
        return False

    def getDatabase(self):
        return self.__db

    def loadBars(self, instrument, timezone=None, fromDateTime=None, toDateTime=None):
        bars = self.__db.getBars(instrument, self.getFrequency(), timezone, fromDateTime, toDateTime)
        self.addBarsFromSequence(instrument, bars)