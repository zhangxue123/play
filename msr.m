close all;clear all;clc;  
I=imread('23_.jpg');
if size(I,3) ~= 3
    error('请输入彩色图像！');
end
R=I(:,:,1);
G=I(:,:,2);
B=I(:,:,3);
[N1,M1]=size(R);
R0=double(R);
G0=double(G);
B0=double(B);
% 取对数
Rlog=log(R0+1);
Glog=log(G0+1);
Blog=log(B0+1);
% 傅里叶变换
Rfft2=fft2(R0);
Gfft2=fft2(G0);
Bfft2=fft2(B0);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 高斯滤波函数
% 可以设置不同的sigma处理后取均值
sigma=100;
F=zeros(N1,M1);
for i=1:N1
    for j=1:M1
        F(i,j)=exp(-((i-N1/2)^2+(j-M1/2)^2)/(2*sigma*sigma));
    end
end
F=F./(sum(F(:)));
% 对高斯滤波函数进行二维傅里叶变换
Ffft=fft2(double(F));
% 卷积运算
DR0=Rfft2.*Ffft;
DG0=Gfft2.*Ffft;
DB0=Bfft2.*Ffft;
DR=ifft2(DR0);
DG=ifft2(DG0);
DB=ifft2(DB0);
% 在对数域中，用原图像减去低通滤波后的的图像，得到高频增强图像
DRdouble=double(DR);
DGdouble=double(DG);
DBdouble=double(DB);
DRlog=log(DRdouble+1);
DGlog=log(DGdouble+1);
DBlog=log(DBdouble+1);
Rr0=Rlog-DRlog;
Gg0=Glog-DGlog;
Bb0=Blog-DBlog;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sigma=200;
F=zeros(N1,M1);
for i=1:N1
    for j=1:M1
        F(i,j)=exp(-((i-N1/2)^2+(j-M1/2)^2)/(2*sigma*sigma));
    end
end
F=F./(sum(F(:)));
% 对高斯滤波函数进行二维傅里叶变换
Ffft=fft2(double(F));
% 卷积运算
DR0=Rfft2.*Ffft;
DG0=Gfft2.*Ffft;
DB0=Bfft2.*Ffft;
DR=ifft2(DR0);
DG=ifft2(DG0);
DB=ifft2(DB0);
% 在对数域中，用原图像减去低通滤波后的的图像，得到高频增强图像
DRdouble=double(DR);
DGdouble=double(DG);
DBdouble=double(DB);
DRlog=log(DRdouble+1);
DGlog=log(DGdouble+1);
DBlog=log(DBdouble+1);
Rr1=Rlog-DRlog;
Gg1=Glog-DGlog;
Bb1=Blog-DBlog;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sigma=400;
F=zeros(N1,M1);
for i=1:N1
    for j=1:M1
        F(i,j)=exp(-((i-N1/2)^2+(j-M1/2)^2)/(2*sigma*sigma));
    end
end
F=F./(sum(F(:)));
% 对高斯滤波函数进行二维傅里叶变换
Ffft=fft2(double(F));
% 卷积运算
DR0=Rfft2.*Ffft;
DG0=Gfft2.*Ffft;
DB0=Bfft2.*Ffft;
DR=ifft2(DR0);
DG=ifft2(DG0);
DB=ifft2(DB0);
% 在对数域中，用原图像减去低通滤波后的的图像，得到高频增强图像
DRdouble=double(DR);
DGdouble=double(DG);
DBdouble=double(DB);
DRlog=log(DRdouble+1);
DGlog=log(DGdouble+1);
DBlog=log(DBdouble+1);
Rr2=Rlog-DRlog;
Gg2=Glog-DGlog;
Bb2=Blog-DBlog;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 取均值
Rr=(Rr0+Rr1+Rr2)/3;
Gg=(Gg0+Gg1+Gg2)/3;
Bb=(Bb0+Bb1+Bb2)/3;
% 定义色彩恢复因子C
a=125;
II=imadd(R0,G0);
II=imadd(II,B0);
Ir=immultiply(R0,a);
C=imdivide(Ir,II);
C=log(C+1);
% 将增强的分量乘以色彩恢复因子
Rr=immultiply(C,Rr);
Gg=immultiply(C,Gg);
Bb=immultiply(C,Bb);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 取反对数
EXPRr=exp(Rr);
EXPGg=exp(Gg);
EXPBb=exp(Bb);
% 对增强后的图像进行对比度拉伸增强
R_MIN=min(min(EXPRr));
G_MIN=min(min(EXPGg));
B_MIN=min(min(EXPBb));
R_MAX=max(max(EXPRr));
G_MAX=max(max(EXPGg));
B_MAX=max(max(EXPBb));
EXPRr=(EXPRr-R_MIN)/(R_MAX-R_MIN);
EXPGg=(EXPGg-G_MIN)/(G_MAX-G_MIN);
EXPBb=(EXPBb-B_MIN)/(B_MAX-B_MIN);
EXPRr=adapthisteq(EXPRr);
EXPGg=adapthisteq(EXPGg);
EXPBb=adapthisteq(EXPBb);
% 融合
I0(:,:,1)=EXPRr;
I0(:,:,2)=EXPGg;
I0(:,:,3)=EXPBb;
figure();
subplot(121);imshow(I);title('雾霾图像');
subplot(122);imshow(I0);title('图像增强');
imwrite(I0,'msr23.jpg');