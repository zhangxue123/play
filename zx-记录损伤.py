# encoding:utf-8
import re
import pandas as pd
import xlrd
import xlwt
#from pyExcelerator import *
import numpy
table=xlrd.open_workbook(r'car.xlsx','r')
#print(table.sheet_names())
result=open("result.txt").readlines()
f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
sheet1.write(0, 0, "图像名称")
sheet1.write(0, 1, "车体型号")
data = table.sheet_by_name("穿-96")
r0=data.row_values(0)
i=2
while i < len(r0):
    sheet1.write(0, i, r0[i - 2])
    i += 1
j=1
for line in result:
    n=len(line.split(' '))
    #print(n)
    arr=list(line.split(' '))

    if n==3:
        sheet1.write(j, 0, arr[0])
        sheet1.write(j, 1, arr[n - 2])
        sheet1.write(j, 2, "无损伤")
        j=j+1
    if n>3:
        #f = xlrd.open_workbook(r'final_result.xlsx', 'a')
        #sheet1 = f.sheet_by_name('sheet1')
        sheet1.write(j, 0, arr[0])
        sheet1.write(j, 1, arr[n - 2])
        if arr[n - 2] == '04':
            data = table.sheet_by_name("穿-04")
        if arr[n-2]=='59':
            data = table.sheet_by_name("穿-59")
        if arr[n - 2] == '96':
            data = table.sheet_by_name("穿-96")
        if arr[n - 2] == '99':
            data = table.sheet_by_name('穿-99')
        #print(arr[n-3])
        if arr[n-3]=='turret_bullet':
            r1=data.row_values(1)
            i = 2
            while i < len(r0):
                sheet1.write(j, i, r1[i-2])
                i += 1
        if arr[n - 3] == 'body_bullet':
            r1 = data.row_values(2)
            i = 2
            while i < len(r0):
                sheet1.write(j, i, r1[i - 2])
                i += 1
        if arr[n - 3] == 'track_bullet':
            r1 = data.row_values(3)
            i = 2
            while i < len(r0):
                sheet1.write(j, i, r1[i - 2])
                i += 1
        if arr[n - 3] == 'burn':
            sheet1.write(j, 2, "燃烧")
        if arr[n - 3] == 'shed':
            sheet1.write(j, 2, "脱落")
        j=j+1
f.save('final_result.xlsx')  # 保存文件



