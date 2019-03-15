# coding=gbk
from tkinter import *
from PIL import Image, ImageTk,ImageEnhance,ImageFilter,ImageChops
from tkinter import filedialog,font,messagebox
import numpy as np
import random
import math
import cv2,os

master=Tk()
master.title('ͼ��������ǿϵͳv1.0')
w1=Frame(height=50,width=50,bg='dark grey')
w2=Frame(height=50,width=50,bg='dark grey')
w5=Frame(height=450,width=520,bg='dark grey')
w6=Frame(height=450,width=520,bg='dark grey')

#����padx��pady�����Խ���ܱ߽����ֿ�
w5.grid(row=0,column=0,columnspan=2, rowspan=3,padx=5, pady=5,sticky=E+S+N+W)
w6.grid(row=0,column=2,columnspan=2, rowspan=3,padx=5, pady=5,sticky=E+S+N+W)
w1.grid(row=3,column=0,columnspan=2, rowspan=3,padx=16, pady=45,sticky=E+S+N+W)
w2.grid(row=3,column=2,columnspan=2, rowspan=3,padx=16, pady=45,sticky=E+S+N+W)
t1=Text(w1,bg='gray')
t2=Text(w2,bg='gray')
t5=Text(w5,bg='gray')
t6=Text(w6,bg='gray')

t1.grid(padx=2, pady=3)
t2.grid(padx=2, pady=3)
t5.grid(padx=2, pady=3)
t6.grid(padx=2, pady=3)

# //////////////�����˵���//////////////
menubar=Menu(t1)
fmenu1=Menu(t1,tearoff=0)
fmenu1.add_command(label="�½�",accelerator='Ctrl+N')
fmenu1.add_separator()# �������˵�ѡ���м����һ������
fmenu1.add_command(label="��",accelerator='Ctrl+O')
fmenu1.add_separator()
fmenu1.add_command(label="����",accelerator='Ctrl+S')
fmenu1.add_separator()
fmenu1.add_command(label="���Ϊ",accelerator='Alt+F2')
fmenu1.add_separator()
fmenu1.add_command(label="�˳�",accelerator='Exit')

fmenu2=Menu(t1,tearoff=0)
fmenu2.add_command(label="����",accelerator='Ctrl+C')
fmenu2.add_separator()# �������˵�ѡ���м����һ������
fmenu2.add_command(label="ճ��",accelerator='Ctrl+����')
fmenu2.add_separator()
fmenu2.add_command(label="����",accelerator='Ctrl+S')
fmenu2.add_separator()
fmenu2.add_command(label="ȫѡ",accelerator='Ctrl+A')

fmenu3=Menu(t1,tearoff=0)
for item in ['������','״̬��','�б�','��ϸ��Ϣ']:
    fmenu3.add_command(label=item)
    fmenu3.add_separator()

fmenu4=Menu(t1,tearoff=0)
for item in ['�Ŵ�','��С']:
    fmenu4.add_command(label=item)
    fmenu4.add_separator()

fmenu5=Menu(t1,tearoff=0)
for item in ['����']:
    fmenu5.add_command(label=item)
    fmenu5.add_separator()

menubar.add_cascade(label="�ļ�",menu=fmenu1)
menubar.add_cascade(label="�༭",menu=fmenu2)
menubar.add_cascade(label="�鿴",menu=fmenu3)
menubar.add_cascade(label="����",menu=fmenu4)
menubar.add_cascade(label="����",menu=fmenu5)
menubar.configure(font='Times, 8')
master['menu']=menubar

label_txt1 = Label(t5, height='2', text="ԭʼͼ��",font = "Helvetica 15 bold").grid(row=1, column=6, columnspan=2, rowspan=3, padx=5, pady=3, sticky=E + S + N + W)
label_txt1 = Label(t6, height='2', text="������ǿ���ͼ��",font = "Helvetica 15 bold").grid(row=1, column=6, columnspan=2, rowspan=3, padx=5, pady=3, sticky=E + S + N + W)

# button_upload_photo1 = Button(t1, text='ѡ����Ҫ��ǿ��ͼ��',font = "Helvetica 15 bold", height='2', width='38')
# button_upload_photo1.grid(row=0, column=1, sticky=S, padx=10, pady=3)


py = Button(t1, text='ƽ��',font = "Helvetica 15 bold", height='1', width='11')
py.grid(row=0, column=0, sticky=S, padx=10, pady=3)

xzh = Button(t1, text='����',font = "Helvetica 15 bold", height='1', width='11')
xzh.grid(row=0, column=1, sticky=S, padx=10, pady=3)

mh = Button(t1, text='ģ��',font = "Helvetica 15 bold", height='1', width='11')
mh.grid(row=0, column=2, sticky=S, padx=10, pady=3)

shb = Button(t2, text='��ɫ����',font = "Helvetica 15 bold", height='1', width='11')
shb.grid(row=1, column=0, sticky=S, padx=10, pady=3)

hd = Button(t2, text='�Ҷ�����',font = "Helvetica 15 bold", height='1', width='11')
hd.grid(row=1, column=1, sticky=S, padx=10, pady=3)

cc = Button(t2, text='�������',font = "Helvetica 15 bold", height='1', width='11')
cc.grid(row=1, column=2, sticky=S, padx=10, pady=3)

def RandomErasing(img):
    probability = 1
    sl = 0.02
    sh = 0.4
    r1 = 0.3
    mean = [0.4914, 0.4822, 0.4465]

    if random.uniform(0, 1) > probability:
        return img

    for attempt in range(100):
        area = img.size[0] * img.size[1]
        target_area = random.uniform(sl, sh) * area
        aspect_ratio = random.uniform(r1, 1 / r1)

        h = int(round(0.8*math.sqrt(target_area * aspect_ratio)))
        w = int(round(0.8*math.sqrt(target_area / aspect_ratio)))

        if w < img.size[1] and h < img.size[0]:
            x1 = random.randint(0, img.size[0] - h)
            y1 = random.randint(0, img.size[1] - w)
            img = np.array(img)
            if img.shape[2] == 3:
                img[x1:x1 + h, y1:y1 + w,0] = mean[0]
                img[x1:x1 + h, y1:y1 + w,1] = mean[1]
                img[x1:x1 + h, y1:y1 + w,2] = mean[2]
            else:
                img[ x1:x1 + h, y1:y1 + w,0] = mean[0]
            return Image.fromarray(np.uint8(img))
    return img

def one_image_upload():
    # global fname
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    # print(fname)
    im = Image.open(fname)
    showImg_yuan(im)
    return im

def fpy():
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    # print(fname)
    im = Image.open(fname)
    showImg_yuan(im)
    out = ImageChops.offset(im,150,150)
    showImg_detect(out)

def fxzh():
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    # print(fname)
    im = Image.open(fname)
    showImg_yuan(im)
    # out = im.rotate(25)  # ��ʱ����ת45��
    out = im.transpose(Image.FLIP_LEFT_RIGHT)
    # region = region.transpose(Image.ROTATE_180��
    showImg_detect(out)

def fmh():
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    # print(fname)
    im = Image.open(fname)
    showImg_yuan(im)
    out = im.filter(ImageFilter.BLUR)
    showImg_detect(out)

def fshb():
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    # print(fname)
    im = Image.open(fname)
    showImg_yuan(im)
    random_factor = np.random.randint(0, 31) / 10.  # �������
    color_image = ImageEnhance.Color(im).enhance(random_factor)  # ����ͼ��ı��Ͷ�
    random_factor = np.random.randint(10, 21) / 10.  # �������
    brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)  # ����ͼ�������
    random_factor = np.random.randint(10, 21) / 10.  # �����1��
    contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # ����ͼ��Աȶ�
    random_factor = np.random.randint(0, 31) / 10.  # �������
    out = ImageEnhance.Sharpness(contrast_image).enhance(random_factor)
    showImg_detect(out)

def fhd():
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    # print(fname)
    im = Image.open(fname)
    showImg_yuan(im)
    out = im.point(lambda i: i * 1.5)
    showImg_detect(out)

def fcc():
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    # print(fname)
    im = Image.open(fname)
    showImg_yuan(im)
    out = RandomErasing(im)

    showImg_detect(out)

def showImg_yuan(im):
    im = im.resize((500, 350), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(im)
    label = Label(t5, image=photo)
    label.image = photo
    label.grid(row=4, column=6, columnspan=2, rowspan=3, padx=5, pady=5, sticky=E + S + N + W)

def showImg_detect(im):
    im = im.resize((500, 350), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(im)
    label = Label(t6, image=photo)
    label.image = photo
    label.grid(row=4, column=6, columnspan=2, rowspan=3, padx=5, pady=5, sticky=E + S + N + W)

if __name__ == '__main__':

    global fname,fname1,fname2
    fname2 = 'm.jpg'
    im = Image.open(fname2)
    showImg_yuan(im)
    fname1 = 'h.jpg'
    im1 = Image.open(fname1)
    showImg_detect(im1)
    py['command'] = fpy
    xzh['command'] = fxzh
    mh['command'] = fmh
    shb['command'] = fshb
    hd['command'] = fhd
    cc['command'] = fcc

    master.mainloop()
