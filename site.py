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
		will_grab_urls=[]
		had_grab_urls=[]
		will_grab_urls.append(index)
		while will_grab_urls:
			grabing=self.get_absolute_url(will_grab_urls.pop())
			if grabing in had_grab_urls:
				pass
			else:
				grab=htmlpage(grabing)
				will_grab_urls.extend(grab.get_internal_urls())
				had_grab_urls.append(grabing)
		return None



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
		target:友情链接检测 相互连接is a friend  不互相连接 is not friend
		params:index url
		return None
		"""
		friend=htmlpage(self.get_index())
		for exurl in friend.get_external_urls():
			exfriend=htmlpage(exurl)
			if self.get_index() in exfriend.get_external_urls():
				print("{} is a friend ".format(exurl))
			else:
				print("{} is not a friend ".format(exurl))
		return None


def main():
	url="http://www.vrnew.com/index.php/News/newscontent/id/593.html"
	vrnew=htmlpage(url)
	print(vrnew.get_scheme())
	print(vrnew.get_host())
	print(vrnew.get_resp())
	# print(vrnew.get_soup())
	# print(vrnew.get_tdk())
	# print(vrnew.get_content())


	# vrnew=website('www.vrnew.com')
	# # m=vrnew.get_absolute_url("http://www.vrnew.com/index.php/Product/index.html")
	# # print(m)
	# vrnew.get_urls()

if __name__ == '__main__':
	main()