# coding=gbk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog,font,messagebox

master=Tk()
master.title('�������˼��ʶ��ϵͳv1.0')
w1=Frame(height=50,width=50,bg='dark grey')
w2=Frame(height=50,width=50,bg='dark grey')
w5=Frame(height=450,width=520,bg='dark grey')
w6=Frame(height=450,width=520,bg='dark grey')

#����padx��pady�����Խ���ܱ߽����ֿ�
w5.grid(row=0,column=0,columnspan=2, rowspan=3,padx=5, pady=5,sticky=E+S+N+W)
w6.grid(row=0,column=2,columnspan=2, rowspan=3,padx=5, pady=5,sticky=E+S+N+W)
w1.grid(row=3,column=0,columnspan=2, rowspan=3,padx=16, pady=45,sticky=E+S+N+W)
w2.grid(row=3,column=2,columnspan=2, rowspan=3,padx=5, pady=5,sticky=E+S+N+W)
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

label_txt1 = Label(t5, height='2', text="���������ͼ��",font = "Helvetica 15 bold").grid(row=1, column=6, columnspan=2, rowspan=3, padx=5, pady=3, sticky=E + S + N + W)
label_txt1 = Label(t6, height='2', text="���������ͼ��",font = "Helvetica 15 bold").grid(row=1, column=6, columnspan=2, rowspan=3, padx=5, pady=3, sticky=E + S + N + W)

button_file3 = Button(t1, text='����ͼƬ���ؼ��ʶ��',font = "Helvetica 15 bold", height='2', width='18')
button_file3.grid(row=0, column=1, sticky=S, padx=10, pady=3)

button_upload_photo3 = Button(t1, text='����ͼƬ���ؼ��ʶ��',font = "Helvetica 15 bold", height='2', width='18')
button_upload_photo3.grid(row=0, column=0, sticky=S, padx=10, pady=3)

num = Label(t2, height='2', text="�������˸���:",font = "Helvetica 14 bold").grid(row=1, column=0, sticky=E, padx=6, pady=13)
label_0 = Label(t2, height='2', width='36', relief='ridge', text='',font = "Helvetica 13 bold")
label_0.grid(row=1, column=1, padx=2, pady=2)

d_type = Label(t2, height='2', text="������������:",font = "Helvetica 14 bold").grid(row=2, column=0, sticky=E, padx=6, pady=13)
label_1 = Label(t2, height='2', width='36', relief='ridge', text='',font = "Helvetica 13 bold")
label_1.grid(row=2, column=1, padx=2, pady=2)

def one_image_upload():
    global fname
    name_ = filedialog.askopenfilename()
    if name_ != '':
        fname = name_
    print(fname)
    im = Image.open(fname)
    showImg_yuan(im)

def batch_image_upload():
    global fname
    name_ = filedialog.askdirectory()
    if name_ != '':
        fname = "3.jpg"
    print(fname)
    im = Image.open(fname)
    showImg_yuan(im)

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
    caffe_root = '/home/gpu/caffe-master'
    global fname,fname1
    fname = '1.jpg'
    im = Image.open(fname)
    showImg_yuan(im)
    fname1 = '2.jpg'
    im1 = Image.open(fname1)
    showImg_detect(im1)
    button_upload_photo3['command'] = one_image_upload
    button_file3['command'] = batch_image_upload
    master.mainloop()
