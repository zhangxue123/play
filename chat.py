# coding=utf-8
import itchat
itchat.login()
f=itchat.get_friends(update=True)[0:]
print f
male=female=other=0
for i in f[1:]:
    sex=i["Sex"]
    if sex==1:
         male+=1
    elif sex==2:
         female+=1
    else:
        other+=1
total=len(f[1:])
print ("好友总数:%d"%(total)+"\n"+
       "男性好友:%2f%%"%(float(male)/total*100)+"\n"+
       "女性好友:%2f%%"%(float(female)/total*100)+"\n"+
       "不明性别好友:%2f%%"%(float(other)/total*100)+"\n")
from pylab import bar, show
bar(left = (0,1,2),height = (male,female,other),width = 0.5)
show()

def get_var(var):
    variable=[]
    for i in f:
        value=i[var]
        variable.append(value)
    return variable
nickname=get_var("NickName")
sex=get_var("Sex")
province=get_var("Province")
city=get_var("City")
signature=get_var("Signature")
from pandas import DataFrame
data={"NickName":nickname,"Sex":sex,"Province":province,
      "City":city,"Signature":signature}
print data
frame=DataFrame(data)
print frame
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
frame.to_csv('data.csv')
#from ggplot import qplot, show
#qplot(city, data = frame, geom = "histogram", fill = color)
#show()
import re
siglist=[]
for i in f:
    signature=i["Signature"].strip().replace("span","").replace("class","").replace("emoji","")
    rep=re.compile("1f\d+\w*|[<>/=]")
    signature=rep.sub("",signature)
    siglist.append(signature)
text="".join(siglist)
print text
import jieba
wordlist=jieba.cut(text,cut_all=True)
word_space_split="".join(wordlist)
import matplotlib.pyplotasplt
