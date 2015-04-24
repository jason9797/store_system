#coding=utf-8

from BeautifulSoup import BeautifulSoup
import urllib,urllib2
f=open("/Users/jason_lee/Downloads/no.txt",'rb')
info=f.readlines()
f1=open("number.txt","a")
for i in info:
    number=i.split()[0]
    url_info=urllib.urlopen("http://www.haosou.com/s?ie=utf-8&shb=1&src=360sou_newhome&q=%s"%number)
    data=url_info.read()
    data_soup=BeautifulSoup(data)
    try:
        data_number=data_soup.find(attrs={"class":"mohe-tips"})("b")[0].text
    except:
        data_number=0
    f1.write("%s %s\n"%(number,data_number))
f.close()
f1.close()


