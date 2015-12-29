#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : pengxiangxiong
# email  : pengxiangxiong@baidu.com

import sys
import ConfigParser
import Queue
import threading
import argparse
import crawlThread

VERSION = '1.0'

class MiniSpider(object):
    def __init__(self, confName):
        self.config = ConfigParser.ConfigParser()
        self.seedList = []
        self.queue = Queue.Queue()
        self.crawlThread = None
        self.threadList = []
        self.confName = confName

    def init(self):
        self.config.read(self.confName)
        self.seedList = self.loadSeed()
        self.queue = self.loadQueue()
        self.crawlThread = crawlThread.CrawlThread(config = self.config, queue = self.queue)

    def loadSeed(self):
        seedList = []
        seedFile = self.config.get('spider', 'url_list_file')
        with open(seedFile) as sf:
            for line in sf:
               seedList.append(line.strip()) 
        return seedList

    def loadQueue(self):
        q = Queue.Queue()
        for seed in self.seedList:
            q.put(seed, 1)
        return q

    def run(self):
        try:
            threadCnt = self.config.getint('spider', 'thread_count')
        except:
            threadCnt = 1
        for i in range(threadCnt):
            t = threading.Thread(target = self.crawlThread.run)
            t.setDaemon(True)
            self.threadList.append(t)

        for thread in self.threadList:
            thread.start()
        
        self.queue.join()


if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="miniSpider") 
    argParser.add_argument('-v', '--verbose', help='display current version', action='store_true')
    argParser.add_argument('-c', '--conf', help='spider conf file', action='store', dest='conf')
    args = argParser.parse_args()
    if args.verbose:
        print 'current version is : ' + VERSION
        sys.exit(0)
    if not args.conf:
        argParser.print_help()
        sys.exit(1)
    spider = MiniSpider(args.conf)
    try:
        spider.init()
    except:
        print 'spider init failed, exit'
        sys.exit(1)
    spider.run()


# vim: set expandtab ts=4 sw=4 sts=4 tw=100:

