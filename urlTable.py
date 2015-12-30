#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : pengxiangxiong
# email  : pengxiangxiong@baidu.com

import pybloom

class UrlTable(object):
    def __init__(self):
        self.table = pybloom.BloomFilter(capacity=50000, error_rate=0.0001)

    def add(self, url):
        self.table.add(url)

    def contains(self, url):
        return url in self.table


# vim: set expandtab ts=4 sw=4 sts=4 tw=100:

