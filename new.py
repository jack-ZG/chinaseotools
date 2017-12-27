#!/usr/bin/python
#coding=utf-8
__author__='xiaohaige'


import sys
import os
import time
import re
import socket

import pymysql
import requests
import jieba
import jieba.analyse
import sqlite3
from bs4 import BeautifulSoup
from furl import furl 

myconfig={
	'host':'127.0.0.1',
	'port':3306,
	'user':'root',
	'passwd':'root',
	'db':'test',
	'charset':'utf8',
}
url='http://www.xinsiwen.com'

def getonepageurls(url):
	urls=[]
	response=requests.get(url)
	bp=BeautifulSoup(response.text,'lxml')
	s=bp.find_all('a')
	for i in s:
		if i.has_attr('href'):
			urls.append(i['href'])
		else:
			pass
	return urls


def execu(myconfig,exesql):
	conn = pymysql.connect(**myconfig)
	cursor = conn.cursor()
	result=cursor.execute("select * from dede_area")
	conn.commit()
	cursor.close()
	conn.close()
	return result	

def rel2abs(rel):
	2abs=""
	retrun 2abs

def geturl(RuKouUrl):
	needgrab=[]
	havegrab=[]
	needgrab.append(RuKouUrl)
	while needgrab:
		grabing=needgrab.pop()
		if grabing not in havegrab:
			needgrab.extend(getonepageurls(grabing))
			havegrab.append(grabing)
			print(grabing)
	return havegrab

# print(getonepageurls(url))
geturl('www.xiaochuanjiang.com')




