# -- coding: utf-8 --

import sys
import copy
import msvcrt
import threading
import time

from ctypes import *

sys.path.append("../MvImport")
from MvCameraControl_class import *

g_bExit = False

# 为线程定义一个函数
def work_thread(cam, pData=0, nDataSize=0):

    stDeviceList = MV_FRAME_OUT_INFO_EX()  #输出的帧信息结构体
    memset(byref(stDeviceList), 0, sizeof(stDeviceList))  #内存空间初始化
    data_buf = (c_ubyte * nPayloadSize)()

    while True:

        ret = cam.MV_CC_GetOneFrameTimeout(byref(data_buf), nPayloadSize, stDeviceList, 1000) #获取一帧图片，支持获取chunk信息和设置超时时间

        x = input("please input the number of the device to start:")
        while int(x) != 1:
            x = input("please input the number of the device to start:")
        print("intput sucess!")
        print("ret", ret)

        if ret == 0:
            print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (stDeviceList.nWidth, stDeviceList.nHeight, stDeviceList.nFrameNum))

            nRGBSize = stDeviceList.nWidth * stDeviceList.nHeight * 3
            stConvertParam = MV_SAVE_IMAGE_PARAM_EX()   #图片格式转换参数结构体
            stConvertParam.nWidth = stDeviceList.nWidth   #图像分辨率宽
            stConvertParam.nHeight = stDeviceList.nHeight   #图像分辨率高
            stConvertParam.pData = data_buf               #原始图像数据
            stConvertParam.nDataLen = stDeviceList.nFrameLen   #原始图像数据长度
            stConvertParam.enPixelType = stDeviceList.enPixelType   #原始图像数据的像素格式
            stConvertParam.nJpgQuality = 70          # 编码质量，取值范围：(50,99]
            stConvertParam.enImageType = MV_Image_Jpeg   #输出图片格式  MV_Image_Jpeg       = 2, //JPEG图片
            stConvertParam.pImageBuffer = (c_ubyte * nRGBSize)()   #输出数据缓冲区，存放转换之后的图片数据
            stConvertParam.nBufferSize = nRGBSize   #输出数据缓冲区大小
            # 将原始图像数据转换成图片格式并保存在指定内存中，可支持设置JPEG编码质量。成功，返回MV_OK（0）；失败，返回错误码。
            ret = cam.MV_CC_SaveImageEx2(stConvertParam)  #图片数据输入输出参数
            if ret != 0:
                print("convert pixel fail aaaaa! ret[0x%x]" % ret)
                del data_buf
                sys.exit()

            file_path = "G:\\picture\\" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".jpg"
            file_open = open(file_path.encode('ascii'), 'wb+')

            img_buff = (c_ubyte * stConvertParam.nImageLen)()    #nImageLen [out] 转换之后图片数据长度
            cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pImageBuffer, stConvertParam.nImageLen)
            file_open.write(img_buff)
        print("Save Image succeed!")

        if g_bExit == True:
                break

def work_thread1(cam, pData=0, nDataSize=0):

    stDeviceList = MV_FRAME_OUT_INFO_EX()
    memset(byref(stDeviceList), 0, sizeof(stDeviceList))
    data_buf = (c_ubyte * nPayloadSize)()

    while True:

        ret = cam.MV_CC_GetOneFrameTimeout(byref(data_buf), nPayloadSize, stDeviceList, 1100)

        x = input("please input the number of the device to start:")
        while int(x) != 1:
            x = input("please input the number of the device to start:")
        print("intput sucess!")
        print("ret", ret)

        if ret == 0:
            print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (stDeviceList.nWidth, stDeviceList.nHeight, stDeviceList.nFrameNum))

            nRGBSize = stDeviceList.nWidth * stDeviceList.nHeight * 3
            # stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
            stConvertParam = MV_SAVE_IMAGE_PARAM_EX()
            # memset(byref(stConvertParam), 0, sizeof(stConvertParam))
            stConvertParam.nWidth = stDeviceList.nWidth
            stConvertParam.nHeight = stDeviceList.nHeight
            stConvertParam.pData = data_buf
            stConvertParam.nDataLen = stDeviceList.nFrameLen
            stConvertParam.enPixelType = stDeviceList.enPixelType
            stConvertParam.nJpgQuality = 70

            # stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
            stConvertParam.enImageType = MV_Image_Jpeg
            stConvertParam.pImageBuffer = (c_ubyte * nRGBSize)()
            stConvertParam.nBufferSize = nRGBSize
            # ret = cam.MV_CC_ConvertPixelType(stConvertParam)
            ret = cam.MV_CC_SaveImageEx2(stConvertParam)
            if ret != 0:
                print("convert pixel fail aaaaa! ret[0x%x]" % ret)
                del data_buf
                sys.exit()

            file_path = "G:\\picture1\\" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".jpg"
            file_open = open(file_path.encode('ascii'), 'wb+')
            img_buff = (c_ubyte * stConvertParam.nImageLen)()
            cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pImageBuffer, stConvertParam.nImageLen)
            file_open.write(img_buff)
        print("Save Image succeed!")

        if g_bExit == True:
                break


def func(cam):
    # ch:选择设备并创建句柄 | en:Select device and create handle
    stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents

    ret = cam.MV_CC_CreateHandle(stDeviceList)
    if ret != 0:
        print("create handle fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:打开设备 | en:Open device
    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print("open device fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
    if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
        nPacketSize = cam.MV_CC_GetOptimalPacketSize()
        if int(nPacketSize) > 0:
            ret = cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
            if ret != 0:
                print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
        else:
            print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

    # ch:设置触发模式为off | en:Set trigger mode as off
    ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
    if ret != 0:
        print("set trigger mode fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:获取数据包大小 | en:Get payload size
    stParam = MVCC_INTVALUE()
    memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

    ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
    if ret != 0:
        print("get payload size fail! ret[0x%x]" % ret)
        sys.exit()
    global nPayloadSize
    nPayloadSize = stParam.nCurValue

    # ch:开始取流 | en:Start grab image
    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print("start grabbing fail! ret[0x%x]" % ret)
        sys.exit()
    global data_buf
    data_buf = (c_ubyte * nPayloadSize)()

def funstop(cam, data_buf):
    # ch:停止取流 | en:Stop grab image
    ret = cam.MV_CC_StopGrabbing()
    if ret != 0:
        print ("stop grabbing fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    # ch:关闭设备 | Close device
    ret = cam.MV_CC_CloseDevice()
    if ret != 0:
        print ("close deivce fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    # ch:销毁句柄 | Destroy handle
    ret = cam.MV_CC_DestroyHandle()
    if ret != 0:
        print ("destroy handle fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    del data_buf


if __name__ == "__main__":

    deviceList = MV_CC_DEVICE_INFO_LIST()  #设备信息列表
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE  #

    # ch:枚举设备 | en:Enum device
    ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)  #枚举子网内指定的传输协议对应的所有设备。成功，返回MV_OK（0）；失败，返回错误码。
    if ret != 0:
        print ("enum devices fail! ret[0x%x]" % ret)
        sys.exit()

    if deviceList.nDeviceNum == 0:
        print ("find no device!")
        sys.exit()

    print ("find %d devices!" % deviceList.nDeviceNum)

    for i in range(0, deviceList.nDeviceNum):
        mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
            print ("\ngige device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                strModeName = strModeName + chr(per)
            print ("device model name: %s" % strModeName)

            nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
            nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
            nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
            nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
            print ("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
        elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
            print ("\nu3v device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print ("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print ("user serial number: %s" % strSerialNumber)


    # ch:创建相机实例 | en:Creat Camera Object
    cam0 = MvCamera()
    cam1 = MvCamera()


    nConnectionNum = 0
    func(cam0)
    nPayloadSize0 = nPayloadSize
    data_buf0 = data_buf

    nConnectionNum = 1
    func(cam1)
    nPayloadSize1=nPayloadSize
    data_buf1 = data_buf

    try:
        hThreadHandle = threading.Thread(target=work_thread, args=(cam0, byref(data_buf0), nPayloadSize0))
        hThreadHandle1 = threading.Thread(target=work_thread1, args=(cam1, byref(data_buf1),nPayloadSize1))
        hThreadHandle1.start()
        hThreadHandle.start()
    except:
        print ("error: unable to start thread")

    print ("press a key to stop grabbing.")
    msvcrt.getch()

    g_bExit = True
    hThreadHandle.join()

    funstop(cam0,data_buf0)
    funstop(cam1,data_buf1)


