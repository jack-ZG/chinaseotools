#!/usr/bin/python
#codeing:utf-8

import requests,time,sys,jieba,os,re,openpyxl,sqlite3,socket
from bs4 import BeautifulSoup 
from furl import furl

class website(object):
	"""
	# target:to analyse website for seo rank
	"""
	def __init__(self,domain):
		self.domain=domain

	def getip(self):
		ip=socket.getaddrinfo(self.domain,None)[0][4][0]
		return ip
	def getwhois(self):
		url="https://cloud.baidu.com/product/bcd/whois.html?domain="+self.domain
		headers={'User-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.4 Safari/537.36"}
		response=requests.get(url,headers=headers)
		bp=BeautifulSoup(response.text,'lxml')
		#bp.body.get_text()
		print(bp.body.get_text())



def main():
	domain='www.vrnew.com'
	vrnew=website(domain)
	vrnew.getwhois()
	sys.exit("game over")


if __name__ == '__main__':
	main()
