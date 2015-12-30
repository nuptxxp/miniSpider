#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : pengxiangxiong
# email  : pengxiangxiong@baidu.com

import sys
import ConfigParser
import Queue
import threading
import argparse
import logging
import time

import crawlThread
import urlTable
import log

VERSION = '1.0'

class MiniSpider(object):
    def __init__(self, confName):
        self.config = ConfigParser.ConfigParser()
        self.seedList = []
        self.queue = Queue.Queue()
        self.urlTable = urlTable.UrlTable()
        self.crawlThread = None
        self.threadList = []
        self.confName = confName

    def init(self):
        self.config.read(self.confName)
        self.seedList = self.loadSeed()
        self.queue = self.loadQueue()
        self.crawlThread = crawlThread.CrawlThread(config = self.config, queue = self.queue,
                urlTable = self.urlTable)
        logging.info('init conf success')

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
            q.put((seed, 1), 1)
        return q

    def stop(self):
        while not self.queue.empty():
            self.queue.get()
            self.queue.task_done()

    def monitor(self):
        while True:
            deadThread = 0
            for thread, threadName in self.threadList:
                if not thread.isAlive():
                    logging.warning(threadName + ' not alive')
                    deadThread += 1
            if deadThread == len(self.threadList):
                logging.warning('all thread not alive, exit')
                self.stop()
            time.sleep(10)

    def run(self):
        try:
            threadCnt = self.config.getint('spider', 'thread_count')
        except:
            threadCnt = 1
        logging.info('start multi thread of ' + str(threadCnt))
        for i in range(threadCnt):
            threadName = 'thread-' + str(i)
            t = threading.Thread(target = self.crawlThread.run, args = [threadName], name = threadName)
            t.setDaemon(True)
            self.threadList.append((t, threadName))

        for thread, threadName in self.threadList:
            thread.start()

        monitorThread = threading.Thread(target = self.monitor)
        monitorThread.setDaemon(True)
        monitorThread.start()
        
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
    log.init_log('./log/miniSpider')
    spider = MiniSpider(args.conf)
    try:
        spider.init()
    except:
        print 'spider init failed, exit'
        sys.exit(1)
    spider.run()


# vim: set expandtab ts=4 sw=4 sts=4 tw=100:

