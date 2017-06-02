#!/usr/bin/python
#codeing:utf-8

import sys
import os
import time
import re
import socket

import requests
import jieba
import jieba.analyse
import openpyxl
import sqlite3 


from bs4 import BeautifulSoup 
from furl import furl

class website(object):
	"""
	# 网站分析
	"""
	def __init__(self,domain):
		self.domain=domain
		
	def get_index(self):
		return "http://"+self.domain #暂不支持https

	def get_ip(self):
		"""
		target:获取网站的IP地址
		params:domain
		return:string ip address
		"""
		ip=socket.getaddrinfo(self.domain,None)[0][4][0]
		return ip
	
	def get_whois(self):
		"""
		target:获取网站的whois信息
		params:domain
		return:dict whois info

		"""
		url="http://whois.chinaz.com/"+self.domain
		headers={'User-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.4 Safari/537.36"}
		cookie={"Cookie":"BAIDUID=0C5608327F1D060AF6434C52FEA7F30D:FG=1; BIDUPSID=CBC07341311B0A31165A5B0A42F8D373; PSTM=1481992218; BDUSS=XhLdlltaXpxaU1ySDdtZ0NuRUtwbnRzSjNub00ySi03QThtTVY5fndVZnJNcGRZSVFBQUFBJCQAAAAAAAAAAAEAAAB6-OY1xu~Xxc31sMvIpb-01u0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOulb1jrpW9YN; BAIDUCUID=++; __cfduid=dd608171a35a5a40e06fc0b9cdcc8e1131489502762; Hm_lvt_28a17f66627d87f1d046eae152a1c93d=1495719879; Hm_lpvt_28a17f66627d87f1d046eae152a1c93d=1495719879"}
		response=requests.get(url,headers=headers,cookies=cookie)
		bp=BeautifulSoup(response.text,'lxml')
		register=bp.select(".clearfix .bor-b1s")[1].get_text()[3:]
		contacter=bp.select(".clearfix .bor-b1s")[2].get_text()[3:].rstrip("[whois反查]")
		mail=bp.select(".clearfix .bor-b1s")[3].get_text()[4:].rstrip("[whois反查]")
		creattime=bp.select(".clearfix .bor-b1s")[4].get_text()[4:]
		builttime=bp.select(".clearfix .bor-b1s")[5].get_text()[4:]
		passtime=bp.select(".clearfix .bor-b1s")[6].get_text()[4:]
		dnsdomain=bp.select(".clearfix .bor-b1s")[7].get_text()[5:]
		dns=bp.select(".clearfix .bor-b1s")[8].get_text()[3:]
		return {'register':register,"contacter":contacter,'mail':mail,'creattime':creattime,'builttime':builttime,'passtime':passtime,'dnsdomain':dnsdomain,'dns':dns}
	
	def get_env(self):
		"""
		#target:获取网站的服务器环境
		#params:domain
		#return:string env info
		"""
		url='http://'+self.domain
		me=requests.get(url)
		return me.headers["Server"]
	

	
	def get_robots(self):
		"""
		#target:获取网页的robots
		#params:url
		#return:string robosts.txt
		"""
		url="http://"+"self.domain"+'robots.txt'
		resp=requests.get(url)
		return resp.text

	def get_num_baidu_included(self):
		"""
		#target:获取百度收录数 备案方名称
		#params:
		#return:
		"""
		num=0
		return num

	def get_num_so_included(self):
		"""
		#target:获取360收录数 备案号
		#params:
		#return:
		"""
		num=0
		return num

	def get_num_sogou_included(self):
		"""
		#target:获取sougou收录数
		#params:
		#return:
		"""
		num=0
		return num

	def get_absolute_url(self,url):
		"""
		#target:得到绝对地址
		"""
		if 'javascript' in url :
			pass
		else:
			f=furl(url)
			if f.host :
				return url
			else:
				return "http://"+self.domain+url

	def get_urls(self):
		""" 抓取网站所有连接"""
		index=self.get_index()
		needgraburls=[]
		hadgraburls=[]
		needgraburls.append(index)
		while needgraburls:
			grabingurl=self.get_absolute_url(needgraburls.pop()) #转换为绝对地址
			if grabingurl:
				if grabingurl in hadgraburls:
					pass
				else:
					grabing=htmlpage(grabingurl)
					needgraburls.extend(grabing.get_internal_urls()) #只抓取本站连接
					hadgraburls.append(grabingurl)

		print(index.get_all_urls())
		return hadgraburls

	def create_file_sitemap(self):
		"""
		#生成网站地图
		"""
		return None
	def create_file_404(self):
		"""
		#生产网站死链
		"""
		return None

	def analyse_log(self):
		"""
		#日志分析
		"""
		return None
	def check_friend(self):
		"""
		target:友情链接检测
		params:index url
		return None
		"""
		friend=htmlpage(self.get_index())
		print(friend.get_external_urls())
		for exurl in friend.get_external_urls():
			exfriend=htmlpage(exurl)
			if self.get_index() in exfriend.get_external_urls():
				print("{} is a friend ".format(exurl))
			else:
				print("{} is not a friend ".format(exurl))
		return None

class htmlpage(object):
	"""
	to analyse a html page
	"""
	def __init__(self,url):
		self.url=url

	def get_scheme(self):
		return furl(self.url).scheme

	def get_host(self):
		return furl(self.url).host

	def get_resp(self):
		return requests.get(self.url)

	def get_soup(self):
		return BeautifulSoup(self.get_resp().text,'lxml')

	def reduce_noise(self):
		"""
		#target:页面基础降噪
		"""
		for style in self.get_soup().find_all('style'):
			self.get_soup().style.decompose()
		for script in self.get_soup().find_all("script"):
			self.get_soup().script.decompose()
		return self.get_soup()


	def get_url(self):
		"""
		#target:获取访问url
		"""
		return self.url
		
	def get_tdk(self):
		"""
		#target:获取网页的TDK
		#params:soup
		#return:dict tdk
		"""
		title=self.get_soup().title.string
		keywords=self.get_soup().find_all('meta',attrs={'name':'keywords'})[0]['content'].split(',')
		description=self.get_soup().find_all('meta',attrs={'name':'description'})[0]['content']
		return {'title':title,'keywords':tuple(keywords),'description':description}

	def get_content(self):
		"""
		target:获取页面内容 模仿百度抓取
		params:soup
		return:string conetent
		"""
		newsoup=self.reduce_noise()
		content=newsoup.body.get_text().split()
		return " ".join(content)

	def get_all_urls(self):
		"""
		target:获取页面内的所有urls
		"""
		urls=[]
		newsoup=self.reduce_noise()
		for i in newsoup.find_all('a'):
			urls.append(i.get("href"))
		return urls
		
	def get_internal_urls(self):
		"""
		#target:获取页面内的站内链接

		"""
		urls=[]
		for url in self.get_all_urls():
			if furl(url).host in [None,self.get_host()]:
				urls.append(url)
			else:
				pass
		return urls

	def get_external_urls(self):
		"""
		#target:获取页面内的站外链接
		"""
		urls=[]
		for url in self.get_all_urls():
			if furl(url).host not in [None,self.get_host()]:
				urls.append(url)
			else:
				pass
		return urls

	def check_in_baidu(self):
		"""
		target:检查在baidu中是否收录
		#如果被展现则返回1,否则返回0

		"""
		payload = {'wd': self.url}
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.4 Safari/537.36'}
		req=requests.get("https://www.baidu.com/s",params=payload,headers=headers)
		info=self.url[7:]
		soup=BeautifulSoup(req.text,'lxml')
		s=soup.body.get_text()
		if "没有找到该URL。您可以直接访问" in s:
			return '没有收录'
		elif "很抱歉，没有找到" in s:
			return '没有收录'
		else:
			return '已经收录'


	def check_in_so(self):
		"""
		target:检查在360中是否收录

		"""
		return None

	def check_in_sogou(self):
		"""
		target:检查在sogou中是否收录

		"""
		return None

	def get_words(self):
		"""
		target:获取正文中频率出现最高的几个词
		
		"""
		tags = jieba.analyse.extract_tags(self.get_content(), topK=20)
		print(",".join(tags))
		return None


def main():
	# url="http://www.vrnew.com/index.php/News/newscontent/id/593.html"
	# vrnew=htmlpage(url)
	# print(vrnew.get_tdk())
	vrnew=website('www.vrnew.com')
	# m=vrnew.get_absolute_url("http://www.vrnew.com/index.php/Product/index.html")
	# print(m)
	vrnew.check_friend()

if __name__ == '__main__':
	main()
