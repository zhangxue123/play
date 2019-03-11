import os,re
from os import listdir, getcwd
from os.path import join
import xml.etree.ElementTree as ET
import pickle


if __name__ == '__main__':
    source_folder='enhancement1/'
    dest='train.txt'
    dest2='val.txt'  
    file_list=os.listdir(source_folder)       
    train_file=open(dest,'w')                 
    val_file=open(dest2,'w')                 
    file_num = 0
    for file_obj in file_list:               
        if re.search(".jpg",file_obj):
            file_path=os.path.join(source_folder,file_obj)

            file_name,file_extend=os.path.splitext(file_obj)
            file_num=file_num+1

            if(file_num%4!=0):                    
                #print file_num
                train_file.write(file_name+'\n')  
            else :
                val_file.write(file_name+'\n')   
    train_file.close()
    val_file.close()

    classes = ["weed","rust","crack","collapse"]  
    def convert_annotation(image_id):
        in_file = open(
            'enhancement1/%s.xml' % (image_id)) 
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')  
        w = int(size.find('width').text)  
        h = int(size.find('height').text)  

        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:  # or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            bb = []
            xmlbox = obj.find('bndbox') 
            bb.append(xmlbox.find('xmin').text)
            bb.append(xmlbox.find('ymin').text)
            bb.append(xmlbox.find('xmax').text)
            bb.append(xmlbox.find('ymax').text)
            bb.append(cls_id)
            list_file.write(",".join(str(a) for a in bb)+  ' ')


    image_ids = open('train.txt').read().strip().split() 
    list_file = open('infrared_train.txt', 'w') 
    for image_id in image_ids:
        list_file.write('/home/%s.jpg ' % (image_id) )
        convert_annotation(image_id)  
        list_file.write('\n')
    list_file.close()  

    image_ids = open('val.txt').read().strip().split()  
    list_file = open('infrared_val.txt', 'w')    
    for image_id in image_ids:
        list_file.write('./enhancement1/%s.jpg ' % (image_id))
        convert_annotation(image_id)  
        list_file.write('\n')
    list_file.close()  