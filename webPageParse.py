#!/usr/bin/python
# -*- coding: utf-8 -*-
# author : pengxiangxiong
# email  : pengxiangxiong@baidu.com

from bs4 import BeautifulSoup
import logging

class WebPageParse(object):
    def __init__(self):
        pass

    def getNextUrl(self, pageContent):
        urlList = []
        if not pageContent:
            return urlList
        soup = BeautifulSoup(pageContent)
        aEleList = soup.find_all('a')
        for aEle in aEleList:
            if aEle.has_attr('href'):
                urlList.append(aEle['href'])
            else:
                logging.warning('unexpected link found' + str(aEle))
        return urlList



# vim: set expandtab ts=4 sw=4 sts=4 tw=100:

