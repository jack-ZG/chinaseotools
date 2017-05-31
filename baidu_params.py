#!/usr/bin/python
#codeing:utf-8

import openpyxl
from furl import furl

class baidu_url(object):
	"""docstring for baidu_url"""
	def __init__(self,url):
		self.url=url
		self.rep=furl(self.url)
		self.scheme=self.rep.scheme
		self.path=self.rep.path
		self.query=self.rep.query
		self.params=self.rep.query.params
	def explain_params(self):
		"""
		# to explain the params
		# url=http://blog.sina.com.cn/s/blog_7ff492150101lay6.html
		"""
		info={
		"wd"="查询词汇",
		"bs"="上一次查询的词",
		"oq"="上一次查询的词",
		"rn"="一页展现的条数",
		"pn"="显示结果所在第几页",
		"si"="限定在某网站内搜索",
		"lm"="限定在多少天内搜索",
		"ie"="关键字默认编码格式",
		"rsv_bp"="使用的是百度哪一个搜索框0是首页输入；1是顶部搜索输入；2是底部搜索输入",
		}
		return None
	def compare_params():
		return 0

		

def main():
	# url="http://www.vrnew.com/index.php/News/newscontent/id/593.html"
	# vrnew=htmlpage(url)
	# print(vrnew.get_words())
	_123=baidu_url("https://www.baidu.com/s?wd=123&rsv_spt=1&rsv_iqid=0x8021c68800000fe7&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=4&rsv_sug1=3&rsv_sug7=100&rsv_t=cf89ZqZkn7WH3SRrAoEJcEjM5j5MBRJBzTVxHw3oMz%2FCEazMVhjtU%2FpsqkkXFn%2BnD1ng&rsv_sug2=0&inputT=1052&rsv_sug4=3391")
	print(_123.scheme)
	print(_123.path)
	print(_123.query)
	print(_123.params)
if __name__ == '__main__':
	main()

