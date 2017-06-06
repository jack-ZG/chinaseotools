#!/usr/bin/python
#codeing:utf-8
import requests
from bs4 import BeautifulSoup

def baidu_index(word=" "):
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.7 Safari/537.36"}
	info=[]
	page=0
	while page<=90:
		payload = {'wd': word,'pn':page,'ie':"utf-8","tn":"baiduhome_pg"}
		req=requests.get("https://www.baidu.com/s",params=payload,headers=headers)
		print(req.url)
		soup=BeautifulSoup(req.text,'lxml')
		for i in soup.select(".c-container "):
			if i.select(".c-showurl"):
				domain=i.select(".c-showurl")[0].get_text().strip()
			else:
				domain=""
			info.append({'id':i["id"],'srcid':i['srcid'],'domain':domain,'title':i.h3.get_text()})
		page+=10
	return info

		
def get_index_baidu(*words):
	for word in words:
		for index in baidu_index(word):
			if 'www.vrnew.com' in index['domain']:
				print('{word}排名在{index}'.format(word=word,index=index['id']))
				print(index)
			else:
				pass
		


def main():
	words=["vr新闻发展至今,还处于起步的阶段。"]
	get_index_baidu(*words)


if __name__ == '__main__':
	main()
