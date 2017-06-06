#!/usr/bin/python
#codeing:utf-8
import requests
from bs4 import BeautifulSoup

def baidu_index(word="华锐视点",domain="www.vrnew.com"):
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
	payload = {'wd': word}
	req=requests.get("https://www.baidu.com/s",params=payload,headers=headers)
	soup=BeautifulSoup(req.text,'lxml')
	for i in soup.select(".c-container "):
		print(i['id'])
		print(i.get_text())
		


def main():
	baidu_index()


if __name__ == '__main__':
	main()
