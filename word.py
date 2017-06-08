#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import openpyxl as excel



def get_checkwordlist():
	"""
	文件结尾必须以：xlsx结尾 切放到wordlist文件夹下
	"""
	wordlist=[]
	for file in os.listdir():
		if os.path.isfile(file) and str(file).endswith(".xlsx",):
			wb=wb=excel.load_workbook(file)
			ws=wb[wb.get_sheet_names()[0]]
			data=ws["A"]
			for i in data:
				wordlist.append(i.value)
	return list(set(wordlist))

def get_defaultwordlist():
	"""
	"""
	relwords=[]
	with open('defaultwords.txt',"r",encoding='UTF-8') as words:
		info=words.readlines()
		for word in info:
			relwords.append(tuple(word.split()))
	return relwords

def check_relationship(testword=None):
	# print(testword)
	score=0
	for i in get_defaultwordlist():
		if str(i[0]) in testword:
			score=score+1
		else:
			score=score+0
	if score==5:
		print("{word}\t{score}".format(word=testword,score=score))
	return score

def main():
	os.chdir(str(os.getcwd())+"\wordlist")
	for i in get_checkwordlist():
		check_relationship(str(i))


if __name__ == '__main__':
	main()

