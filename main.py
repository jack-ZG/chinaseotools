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
		'the website ip'
		ip=socket.getaddrinfo(self.domain,None)[0][4][0]
		return ip
	def getwhois(self):
		'the website whois'
		url="http://whois.chinaz.com/"+self.domain
		headers={'User-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3018.4 Safari/537.36"}
		cookie={"Cookie":"BAIDUID=0C5608327F1D060AF6434C52FEA7F30D:FG=1; BIDUPSID=CBC07341311B0A31165A5B0A42F8D373; PSTM=1481992218; BDUSS=XhLdlltaXpxaU1ySDdtZ0NuRUtwbnRzSjNub00ySi03QThtTVY5fndVZnJNcGRZSVFBQUFBJCQAAAAAAAAAAAEAAAB6-OY1xu~Xxc31sMvIpb-01u0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOulb1jrpW9YN; BAIDUCUID=++; __cfduid=dd608171a35a5a40e06fc0b9cdcc8e1131489502762; Hm_lvt_28a17f66627d87f1d046eae152a1c93d=1495719879; Hm_lpvt_28a17f66627d87f1d046eae152a1c93d=1495719879"}
		print(url)
		response=requests.get(url,headers=headers,cookies=cookie)
		bp=BeautifulSoup(response.text,'lxml')
		register=bp.select(".clearfix .bor-b1s")[1].get_text()[3:]
		contacter=bp.select(".clearfix .bor-b1s")[2].get_text()[3:].replace("[whois反查]"," ")
		mail=bp.select(".clearfix .bor-b1s")[3].get_text()[4:].replace("[whois反查]"," ")
		creattime=bp.select(".clearfix .bor-b1s")[4].get_text()[4:]
		builttime=bp.select(".clearfix .bor-b1s")[5].get_text()[4:]
		passtime=bp.select(".clearfix .bor-b1s")[6].get_text()[4:]
		dnsdomain=bp.select(".clearfix .bor-b1s")[7].get_text()[5:]
		dns=bp.select(".clearfix .bor-b1s")[8].get_text()[3:]
		return {'register':register,"contacter":contacter,'mail':mail,'creattime':creattime,'builttime':builttime,'passtime':passtime,'dnsdomain':dnsdomain,'dns':dns}
			



def main():
	domain=sys.argv[1]
	vrnew=website(domain)
	print(vrnew.getwhois())
	sys.exit("game over")


if __name__ == '__main__':
	main()
