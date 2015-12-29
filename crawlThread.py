#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : pengxiangxiong
# email  : pengxiangxiong@baidu.com

import time

class CrawlThread(object):
    def __init__(self, config = None, queue = None):
        self.config = config
        self.queue = queue

    def init(self):
        self.crawlInterval = self.config.getint('spider', 'crawl_interval')

    def run(self):
        if not self.config or not self.queue:
            return
        try:
            self.init()
        except:
            return
        while not self.queue.empty():
            url = self.queue.get(block=1, timeout=5)
            self.queue.task_done()
            time.sleep(self.crawlInterval)




# vim: set expandtab ts=4 sw=4 sts=4 tw=100:

