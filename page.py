#!/usr/bin/python
#codeing:utf-8
import requests
from bs4 import BeautifulSoup
from furl import furl

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
		headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
		return requests.get(self.url,headers=headers)

	def get_soup(self):
		return BeautifulSoup(self.get_resp().text,'lxml')

	def reduce_noise(self):
		"""
		#target:页面基础降噪
		"""
		newsoup=self.get_soup()
		for style in newsoup.find_all('style'):
			newsoup.style.decompose()
		for script in newsoup.find_all("script"):
			newsoup.script.decompose()
		return newsoup

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

	def show(self):
		print(self.get_url())	
		print(self.get_scheme())
		print(self.get_host())
		# print(self.get_resp())
		# print(self.get_soup())
		# print(self.get_tdk())
		print(self.get_content())
		print(self.reduce_noise())


def main():
	url="http://blog.csdn.net/appleheshuang/article/details/7602499"
	vrnew=htmlpage(url)
	vrnew.show()





if __name__ == '__main__':
	main()