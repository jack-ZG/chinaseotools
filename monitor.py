#!/usr/bin/python
#coding:utf-8
import re
import requests
from bs4 import BeautifulSoup

headers={'Connection':"keep-alive","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.7 Safari/537.36"}

def baidu_index(word=" ",num=90):
	"""
	target:根据关键词，默认获取百度排名前100内容
	params:words是想要获取的关键词，num:0,10,20......90
	return:list 信息列表
	"""
	info=[]
	page=0
	while page<=num:
		payload = {'wd': word,'pn':page,'ie':"utf-8","tn":"baiduhome_pg"}
		req=requests.get("https://www.baidu.com/s",params=payload,headers=headers)
		soup=BeautifulSoup(req.text,'lxml')
		for i in soup.select(".c-container "):
			if i.select(".c-showurl"):
				domain=i.select(".c-showurl")[0].get_text().strip()
			else:
				domain=""
			info.append({'id':i["id"],'srcid':i['srcid'],'domain':domain,'title':i.h3.get_text().strip(),'tpl':i['tpl'],'data-click':eval(re.sub(r"\s","",str(i.h3.a.get("data-click"))))})
		page+=10
	return info

def so_index(word="vr",page=""):
	"""
	target:
	params:
	return:
	"""
	info=[]
	payload = {'q': word,'pn':page,'src':"srp_paging","fr":"none"}
	req=requests.get("https://www.so.com/s",params=payload,headers=headers)
	soup=BeautifulSoup(req.text,'lxml')
	newsoup=soup.body
	for style in newsoup.find_all("style"):
		newsoup.style.decompose()
	for script in newsoup.find_all("script"):
		newsoup.script.decompose()
	for i in newsoup.select('.result')[1]:
		for s in i.select('h3 > a'):
			print(s)
			if 'data-res' in str(s):
				print(s['data-res'])
		info.append({'timte':i.select('h3')[0].get_text(),})


def sogou_index(word="vr",page=""):
		"""
	target:
	params:
	return:
	"""
		
def get_index_baidu(site,*words):
	"""
	target:关键词排名监控
	param:关键词列表
	return:关键词位置定位信息[{"word":"",rank:[1,68,93,100]},]"""

	ranklist=[]
	for word in words:
		rank=[]
		for index in baidu_index(word):
			if site in index['domain']:
				rank.append(index['id'])
			else:
				pass
		ranklist.append({"word":word,"rank":rank})
	return ranklist
		
def get_words():
	"""
	target:获取需要监控的词
	"""
	monitor=[]
	with open("vrnewwords.txt",'r',encoding="utf-8") as words:
		for word in words.readlines():
			if word.strip():
				monitor.append(word.strip())
			else:
				pass
	return monitor


def main():
	print(so_index())



if __name__ == '__main__':
	main()
