#!/usr/bin/python
#codeing:utf-8
import re
import requests
from bs4 import BeautifulSoup

def baidu_index(word=" ",num=90):
	"""
	target:根据关键词，获取百度排名前100内容
	params:words是想要获取的关键词，num:0,10,20......90
	return:list 信息列表
	"""
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.7 Safari/537.36"}
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
		


def main():
	site="www.vrnew.com"
	words=["华锐视点","vr","虚拟现实"]
	for i in get_index_baidu(site,*words):
		print(i)


if __name__ == '__main__':
	main()
