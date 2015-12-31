#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : pengxiangxiong
# email  : pengxiangxiong@baidu.com

import time
import logging
import re
import urlparse
import webPageParse
import webPageSave
import urllib2

class CrawlThread(object):
    def __init__(self, config = None, queue = None, urlTable = None):
        self.config = config
        self.queue = queue
        self.urlTable = urlTable

    def init(self):
        self.crawlInterval = self.config.getint('spider', 'crawl_interval')
        self.crawlTimeout = self.config.getint('spider', 'crawl_timeout')
        self.targetUrl = self.config.get('spider', 'target_url')
        self.crawlMaxDepth = self.config.getint('spider', 'max_depth')
        self.crawlOutputDir = self.config.get('spider', 'output_directory')
        self.target_pattern = re.compile(self.targetUrl)
        self.webPageParse = webPageParse.WebPageParse()
        self.webPageSave = webPageSave.WebPageSave()

    def getPage(self, url, timeout):
        try:
            response = urllib2.urlopen(url = url, timeout = timeout)
        except urllib2.URLError:
            return None

        return response.read()

    def run(self, threadName):
        logging.info(threadName + ' start subthread')
        if not self.config or not self.queue or not self.urlTable:
            logging.info(threadName + ' of args fail')
            return
        try:
            self.init()
        except:
            logging.info(threadName + ' init fail')
            return
        while True:
            if not self.queue.empty():
                try:
                    url, depth = self.queue.get(block=1, timeout=5)
                except Exception as e:
                    logging.info(threadName + ' get queue failed: ' + str(e))
                    continue
                try:
                    if depth <= self.crawlMaxDepth:
                        if not self.urlTable.contains(url):
                            self.urlTable.add(url)
                            logging.info(threadName + ' current process url:' + url)
                            pageContent = self.getPage(url, self.crawlTimeout)
                            nextUrlList = self.webPageParse.getNextUrl(pageContent)
                            for nextUrl in nextUrlList:
                                parseResult = urlparse.urlparse(nextUrl)
                                newUrl = nextUrl
                                if parseResult.scheme == 'javascript':
                                    continue
                                if parseResult.scheme == '' and parseResult.netloc == '':
                                    newUrl = urlparse.urljoin(url, nextUrl)
                                if depth + 1 <= self.crawlMaxDepth:
                                    self.queue.put((newUrl, depth + 1))
                                
                            if self.target_pattern.match(url):
                                self.webPageSave.save(url, self.crawlOutputDir)
                except Exception as e:
                    logging.info(threadName + ' crawl url: ' + url + 'failed at: ' + str(e))
                logging.info(threadName + ' taskDone of url: ' + url)
                self.queue.task_done()
                time.sleep(self.crawlInterval)




# vim: set expandtab ts=4 sw=4 sts=4 tw=100:

