#!/usr/bin/python
#codeing:utf-8
import os
import openpyxl as excel

os.chdir(str(os.getcwd())+"\wordlist")
wb=excel.load_workbook(os.listdir()[0])
print(wb.get_sheet_names())
ws=wb[wb.get_sheet_names()[0]]
data=ws["A"]
for i in data:
	print(i.value)