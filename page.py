#!/usr/bin/python
#coding:utf-8
import requests
from bs4 import BeautifulSoup
from furl import furl

class htmlpage(object):
	"""
	taraget:单页面分析工具
	"""
	def __init__(self,url):
		self.url=url
		self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}

	@property
	def furl(self):
		return furl(self.url)

	@property
	def scheme(self):
		return self.furl.scheme

	@property
	def host(self):
		return self.furl.host

	def get_resp(self):
		try:
			return requests.get(self.url,headers=self.headers)
		except requests.exceptions.InvalidSchema:
			print(self.url)

	@property	
	def soup(self):
		return BeautifulSoup(self.get_resp().text,'lxml')

	def reduce_noise(self):
		"""
		#target:页面基础降噪
		"""
		newsoup=self.soup
		for style in newsoup.find_all('style'):
			newsoup.style.decompose()
		for script in newsoup.find_all("script"):
			newsoup.script.decompose()
		return newsoup

	
	@property
	def title(self):
		"""
		target:获取网页标题
		"""
		return self.soup.title.string

	@property
	def keywords(self):
		"""
		target:获取网关键词
		"""
		return self.soup.find_all('meta',attrs={'name':'keywords'})[0]['content'].split(',')

	@property
	def description(self):
		"""
		target:获取网页描述
		"""
		return self.soup.find_all('meta',attrs={'name':'description'})[0]['content']

	@property
	def content(self):
		"""
		target:获取页面内容 模仿百度抓取
		params:soup
		return:string conetent
		"""
		newsoup=self.reduce_noise()
		content=newsoup.body.get_text().split()
		return " ".join(content)

	def url_re2abs(self,url):
		"""相对连接->绝对连接"""
		f=furl(url)
		if f.host:
			return url
		else:
			me=self.furl
			me.path=str(f.path)
			return me.url

	@property
	def allurls(self):
		"""
		target:获取页面内的所有urls
		"""
		urls=[]
		newsoup=self.reduce_noise()
		for i in newsoup.find_all('a'):
			if i.string:
				anchor=i.string.strip()
			else:
				anchor=i.string
			urls.append({'url':self.url_re2abs(i.get("href")),'anchor':anchor})
		return urls

	@property
	def internal_urls(self):
		"""
		#target:获取页面内的站内链接和锚文字

		"""
		urls=[]
		for url in self.allurls:
			if furl(url['url']).host in [None,self.host]:
				urls.append(url)
			else:
				pass
		return urls

	@property
	def external_urls(self):
		"""
		#target:获取页面内的站外链接
		"""
		urls=[]
		for url in self.allurls:
			if furl(url['url']).host not in [None,self.host]:
				urls.append(url)
			else:
				pass
		return urls

	def check_in_baidu(self):
		"""
		target:检查在baidu中是否收录
		#收录返回True,没有收录返回False

		"""
		payload = {'wd': self.url}
		req=requests.get("https://www.baidu.com/s",params=payload,headers=self.headers)
		info=self.url[7:]
		soup=BeautifulSoup(req.text,'lxml')
		s=soup.body.get_text()
		if "没有找到该URL。您可以直接访问" in s:
			return False 
		elif "很抱歉，没有找到" in s:
			return False
		else:
			return True


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
		print("url:{}".format(self.get_url()))
		print("title:{}".format(self.get_tdk()["title"]))
		print("keywords:{}".format(self.get_tdk()["keywords"]))
		print("description:{}".format(self.get_tdk()["description"]))
		print("interlurl:{}".format(len(self.get_internal_urls())))
		print("exterlurl:{}".format(len(self.get_external_urls())))
		print(self.get_all_urls())
		print(self.check_in_baidu())



def main():
	url="http://www.vrnew.com/index.php/News/newscontent/id/611.html"
	vrnew=htmlpage(url)
	# for i in vrnew.get_all_urls():
	# 	print(i['anchor'])
	# 	print(i['url'])
	# print(vrnew.host)
	# print(vrnew.title)
	# print(vrnew.content)
	# print(vrnew.allurls)
	print(vrnew.external_urls)





if __name__ == '__main__':
	main()
