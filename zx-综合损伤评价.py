# encoding:utf-8
#import re
#import pandas as pd
import xlrd
import xlwt
#from pyExcelerator import *
#import numpy
table=xlrd.open_workbook(r'car.xlsx','r')
#print(table.sheet_names())
result=open("result.txt").readlines()
f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
sheet1.write(0, 0, "图像名称")
sheet1.write(0, 1, "车体型号")
sheet1.write(0, 2, "火力功能损伤")
sheet1.write(0, 3, "通讯功能损伤")
sheet1.write(0, 4, "行驶功能损伤")
sheet1.write(0, 5, "综合功能损伤")
data = table.sheet_by_name("穿-96")
r0=data.row_values(0)
i=6
while i < len(r0):
    sheet1.write(0, i, r0[i - 6])
    i += 1
j=1
for line in result:
    n=len(line.split(' '))
    #print(n)
    arr=list(line.split(' '))

    if n==3:
        sheet1.write(j, 0, arr[0])
        sheet1.write(j, 1, arr[n - 2])
        sheet1.write(j, 6, "无损伤")
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
            if data.cell(1, 11).value == 1 and data.cell(1, 12).value == 1 and data.cell(1, 18).value == 1:
                hl=1
            elif (data.cell(1, 13).value == 1 and data.cell(1, 16).value == 1 and data.cell(1, 19).value == 1) or (data.cell(1, 10).value == 1 and data.cell(1, 15).value == 1 and data.cell(1, 17).value == 1 and data.cell(1, 14).value == 1):
                hl=2
            else:
                hl=3
            if (data.cell(1, 25).value == 1 and data.cell(1, 26).value == 1) or data.cell(1, 28).value == 1:
                tx=1
            elif (data.cell(1, 22).value == 1 and data.cell(1, 23).value == 1 and data.cell(1, 24).value == 1) or (data.cell(1, 27).value == 1):
                tx=2
            else:
                tx=3
            if data.cell(1, 3).value == 1:
                xs=1
            elif data.cell(1, 2).value == 1:
                xs=2
            else:
                xs=0
            r1=data.row_values(1)
            i = 6
            while i < len(r0):
                sheet1.write(j, i, r1[i-6])
                i += 1
        if arr[n - 3] == 'body_bullet':
            if data.cell(2, 11).value == 1 and data.cell(2, 12).value == 1 and data.cell(2, 18).value == 1:
                hl=1
            elif (data.cell(2, 13).value == 1 and data.cell(2, 16).value == 1 and data.cell(2, 19).value == 1) or (data.cell(2, 10).value == 1 and data.cell(2, 15).value == 1 and data.cell(2, 17).value == 1 and data.cell(2, 14).value == 1):
                hl=2
            else:
                hl=3
            if (data.cell(2, 25).value == 1 and data.cell(2, 26).value == 1) or data.cell(2, 28).value == 1:
                tx=1
            elif (data.cell(2, 22).value == 1 and data.cell(2, 23).value == 1 and data.cell(2, 24).value == 1) or (data.cell(2, 27).value == 1):
                tx=2
            else:
                tx=3
            if data.cell(2, 3).value == 1:
                xs=1
            elif data.cell(2, 2).value == 1:
                xs=2
            else:
                xs=0
            r1 = data.row_values(2)
            i = 6
            while i < len(r0):
                sheet1.write(j, i, r1[i - 6])
                i += 1
        if arr[n - 3] == 'track_bullet':
            if data.cell(3, 11).value == 1 and data.cell(3, 12).value == 1 and data.cell(3, 18).value == 1:
                hl=1
            elif (data.cell(3, 13).value == 1 and data.cell(3, 16).value == 1 and data.cell(3, 19).value == 1) or (data.cell(3, 10).value == 1 and data.cell(3, 15).value == 1 and data.cell(3, 17).value == 1 and data.cell(3, 14).value == 1):
                hl=2
            else:
                hl=3
            if (data.cell(3, 25).value == 1 and data.cell(3, 26).value == 1) or data.cell(3, 28).value == 1:
                tx=1
            elif (data.cell(3, 22).value == 1 and data.cell(3, 23).value == 1 and data.cell(3, 24).value == 1) or (data.cell(3, 27).value == 1):
                tx=2
            else:
                tx=3
            if data.cell(3, 3).value == 1:
                xs=1
            elif data.cell(3, 2).value == 1:
                xs=2
            else:
                xs=0
            r1 = data.row_values(3)
            i = 6
            while i < len(r0):
                sheet1.write(j, i, r1[i - 6])
                i += 1
        if arr[n - 3] == 'burn':
            sheet1.write(j, 6, "燃烧")
        if arr[n - 3] == 'shed':
            sheet1.write(j, 6, "脱落")
            xs=3
        if data.cell(2,6).value==1:
            print(data.cell(2,6).value)
        if tx == 1:
            zh = 1
        elif (tx != 1 and hl != 1 and xs == 1) or tx == 2 or hl == 2:
            zh = 2
        elif xs==0 and hl==0 and tx==0:
            zh=0
        else:
            zh = 3
        if hl==1:
            sheet1.write(j, 2, "重损")
        if hl==2:
            sheet1.write(j, 2, "中损")
        if hl==3:
            sheet1.write(j, 2, "轻损")
        if hl==0:
            sheet1.write(j, 2, "无损")
        if tx==1:
            sheet1.write(j, 3, "重损")
        if tx==2:
            sheet1.write(j, 3, "中损")
        if tx==3:
            sheet1.write(j, 3, "轻损")
        if tx==0:
            sheet1.write(j, 3, "无损")
        if xs==1:
            sheet1.write(j, 4, "重损")
        if xs==2:
            sheet1.write(j, 4, "中损")
        if xs==3:
            sheet1.write(j, 4, "轻损")
        if xs==0:
            sheet1.write(j, 4, "无损")
        if zh==1:
            sheet1.write(j, 5, "重损")
        if zh==2:
            sheet1.write(j, 5, "中损")
        if zh==3:
            sheet1.write(j, 5, "轻损")
        if zh==0:
            sheet1.write(j, 5, "无损")
        j=j+1
f.save('final_result.xlsx')  # 保存文件



