#!/usr/bin/python
#coding:utf-8
__author__='xiaohaige'
import page

import sys
import os
import time
import re
import socket

import requests
import jieba
import jieba.analyse
import sqlite3
from bs4 import BeautifulSoup
from furl import furl

class site(object):
    def __init__(self,host):
        self.host=host
    @property
    def index(self):
        return "http://"+self.host+'/'
    @property
    def ip(self):
        return socket.getaddrinfo(self.host,None)[0][4][0]
    @property
    def whois(self):
        url="http://whois.chinaz.com/"+self.host
        response=requests.get(url)
        bp=BeautifulSoup(response.text,'lxml')
        info=bp.select(".clearfix .bor-b1s")
        register=info[1].get_text()[3:]
        contacter=info[2].get_text()[3:].rstrip(u'[whois反查]')
        mail=info[3].get_text()[4:].rstrip(u"[whois反查]")
        creattime=info[4].get_text()[4:]
        builttime=info[5].get_text()[4:]
        passtime=info[6].get_text()[4:]
        dnshost=info[7].get_text()[5:]
        dns=info[8].get_text()[3:]
        return {'register':register,"contacter":contacter,'mail':mail,'creattime':creattime,'builttime':builttime,'passtime':passtime,'dnshost':dnshost,'dns':dns}
    @property
    def server(self):
        return requests.get(self.index).headers["Server"]
    @property
    def robots(self):
        resp=requests.get(self.index+'robots.txt')
        if resp.status_code==200:
            return resp.text
        else:
            return 'Miss robots.txt'
    @property
    def urls(self):
        needgrab=[]
        havegrab=[]
        needgrab.append(self.index)
        while needgrab:
            grabing=needgrab.pop()
            if grabing not in havegrab:
                temp=page.page(grabing)
                print u'正在抓取:'+grabing+'\t'+temp.analyzetitle+'\n'
                needgrab.extend(temp.internallinks)
                havegrab.append(grabing)
                for i in temp.links:
                    print '\t\t'+i['url']+'\t'+i['text']
            else:
                pass
        return havegrab

def main():
    vrnew=site("www.vrnew.com")
    vrnew.urls

if __name__ == '__main__':
	main()
