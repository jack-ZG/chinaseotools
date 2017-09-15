#!/usr/bin/python
#coding=utf-8

import requests
from bs4 import BeautifulSoup
from furl import furl


class page(object):
	'''单页面分析，出报告'''
	def __init__(self,url):
		self.url=url

	@property
	def host(self):
		return furl(self.url).host

	@property
	def getsoup(self):
		resp=requests.get(self.url)
		soup=BeautifulSoup(resp.text,'lxml')
		return soup

	def analyzeurl(self):
		'''链接分析'''
		length=self.getfurl.path.segments
		if length>3:
			print 'url结构复杂:',self.url
		return


	def gethtml(self):
		'''获取网页源码'''
		return self.getsoup.prettify()

	def gettext(self):
		'''获取网页文本'''
		newsoup=self.getsoup
		for style in newsoup.find_all('style'):
			newsoup.style.decompose()
		for script in newsoup.find_all("script"):
			newsoup.script.decompose()
		return " ".join(newsoup.get_text().split())

	def checkinsearch(self):
		'''检测是否被baidu/sogou/360/收录'''
		pass

	@property
	def analyzetitle(self):
		'''网页标题分析 标题范围30-120'''
		title=self.getsoup.title.string
		length=len(title)
		if length>120:
			return u'标题太长:'+title
		elif length<10:
			return u'标题太短:'+title
		elif length==0:
			return u'标题缺失:'
		else:
			return u'页面标题:'+title

	def analyzeheadings(self):
		''''H标签分析 H1有且只有一个'''
		headings=['h1','h2','h3','h4','h5','h6']
		info=[]
		mess=[]
		for heading in headings:
			for h in self.getsoup.find_all(heading):
				info.append({h.name:h.get_text()})
				mess.append(h.name)
		if mess.count('h1')!=1:
			print 'H1 标签不唯一'
		else:
			print '有且仅有一个H1'
		return info



	def analyzeimages(self):
		'''
		每个图片都有自己的alt描述
		没有alt描述的时候返回imgs
		'''
		imgs=[]
		for img in self.getsoup.find_all('img'):
			try:
				if img['alt']:
					pass
			except KeyError as e:
				imgs.append(img)
				continue
		return imgs

	@property
	def links(self):
		'''获取页面内所有超链 相对转换为绝对'''
		links=[]
		for a in self.getsoup.find_all('a',href=True):
			f=furl(a['href'])
			if f.host:
				links.append({'url':a['href'],'text':a.get_text().strip()})
			else:
				links.append({'url':'http://'+self.host+a['href'],'text':a.get_text().strip()})
		return links

	@property
	def internallinks(self):
		'''获取内链以及超文本'''
		ilinks=[]
		for i in self.links:
			try:
				p=furl(i['url'])
				if p.host==self.host:
					ilinks.append(i['url'])
				else:
					pass
			except ValueError as e:
				continue
		return list(set(ilinks))

	def externallinks(self):
		'''获取外链接以及超文本'''
		exlinks=[]
		for i in self.links:
			try:
				p=furl(i['url'])
				if p.host==self.host:
					pass
				else:
					exlinks.append(i['url'])
			except ValueError as e:
				continue
		return exlinks

	def getreport(self):
		'''分析报告'''
		self.analyzeurl()
		self.analyzetitle()
		self.analyzeimages()
		self.analyzeheadings()
		pass

def main():
	url="http://www.vrnew.com/"
	vrnew=page(url)
	print vrnew.internallinks


if __name__ == '__main__':
	main()
