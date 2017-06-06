#!/usr/bin/python
#codeing:utf-8
import requests
from bs4 import BeautifulSoup

def baidu_index(word="外卖",domain="www.vrnew.com"):
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
	info=[]
	page=0
	while page<=90:
		payload = {'wd': word,'pn':page}
		req=requests.get("https://www.baidu.com/s",params=payload,headers=headers)
		soup=BeautifulSoup(req.text,'lxml')
		for i in soup.select(".c-container "):
			if i.select(".c-showurl"):
				domain=i.select(".c-showurl")[0].get_text().strip()
			else:
				domain=""
			info.append({'id':i["id"],'srcid':i['srcid'],'domain':domain,'title':i.h3.get_text()})
		page+=10
	return info

		


def main():
	for i in baidu_index():
		print(i)


if __name__ == '__main__':
	main()
