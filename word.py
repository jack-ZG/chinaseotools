#!/usr/bin/python
#codeing:utf-8
import os
import openpyxl as excel



def get_wordlist():
	"""
	文件结尾必须以：xlsx结尾 切放到wordlist文件夹下
	"""
	wordlist=[]
	os.chdir(str(os.getcwd())+"\wordlist")
	for file in os.listdir():
		if os.path.isfile(file) and str(file).endswith(".xlsx",):
			wb=wb=excel.load_workbook(file)
			ws=wb[wb.get_sheet_names()[0]]
			data=ws["A"]
			for i in data:
				wordlist.append(i.value)
	return list(set(wordlist))
def get_relation_bool():
	""""""
	relwords=[]
	return relwords

def main():
	wordlist=get_wordlist()
	for i in wordlist:
		print(i)

if __name__ == '__main__':
	main()

