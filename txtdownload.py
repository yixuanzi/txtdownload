#coding=utf8
import os
import sys
from bs4 import BeautifulSoup
import bs4
import urllib2
import re



def txtrequest(url):
    r=urllib2.Request(url)
    r.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    r.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0")
    return urllib2.urlopen(r)
    
def readconfig(p):
    rs={}
    for line in open(p):
        line=line.strip()
        if len(line)==0 or line[0]=='#':
            continue
        k,v=line.split(':',1)
        rs[k]=parseconfig(k,v)
    return rs

def parseconfig(k,v):
    #解析配置文件内容
    if k in ['chaperhtml','contenthtml']:
        rs={'tag':None,'attrs':{}}
        vlist=v.split(';')
        rs['tag']=vlist.pop(0)
        attrs={}
        for kv in vlist:
            k,v=kv.split(':',1)
            attrs[k]=v
        rs['attrs']=attrs
        return rs
    else:
        return v

def getchapername(contents):
    rs=""
    for i in contents:
        if type(i)==bs4.element.NavigableString:
            rs+=i
        else:
            rs+=i.contents[0]
    return rs

def getchaperlist(config):
    #获取章节信息列表
    chapers=[]
    rootpage=txtrequest(config['rootlink']).read()
    soup=BeautifulSoup(rootpage).find(config['chaperhtml']['tag'],config['chaperhtml']['attrs'])
    links=soup.findAll('a')
    for l in links:
        if not l.attrs.has_key('href'):
            continue
        a=l['href']
        if re.match(config['chapermodel'],a):
            chapers.append((getchapername(l.contents),a))
    return chapers

def getcontent4link(chaper,config):
    #获取对应页面的内容
    if config.has_key('isnumber') and config['isnumber']=='1':
        prefix= u"第%d章 " %index
    else:
        prefix=''
    print (prefix+chaper[0]).encode(config['outcode'])
    if chaper[1][:4].lower()=='http':
        link=chaper[1]
    else:
        link=config['rootcontent']+chaper[1]
    soup=BeautifulSoup(txtrequest(link).read())
    txtag=soup.find(config['contenthtml']['tag'],config['contenthtml']['attrs'])
    if config.has_key('brute') and config['brute']=='1':        
        rs=txtag.__str__()
        rs=rs.replace('<br>','').replace('</br>','').replace('<p>','').decode('utf8').strip()
        print "  ",re.sub(config['filter'],'',rs).encode(config['outcode'])
        return
    for i in txtag.contents:
        if type(i)==bs4.element.NavigableString:
            print "  ",re.sub(config['filter'],'',i.strip()).encode(config['outcode'])

def debugprint(v):
    if config.has_key('debug') and config['debug']=='True':
        print v

def setproxy(config):
    if config.has_key('proxy'):
        opener = urllib2.build_opener( urllib2.ProxyHandler({'http':config['proxy']}))          
        urllib2.install_opener(opener)      

try:
    config=readconfig(sys.argv[1])
    setproxy(config)
    debugprint(config)
except Exception,e:
    print repr(e)
    print "User: Python txtdownload config_file"
    print "config_file: linke txt.config"
    exit()
chapers=getchaperlist(config)
print "chapers nums:",len(chapers)
index=1
for chaper in chapers:
    try:
        getcontent4link(chaper,config)
    except Exception:
        print "get the contents fail"
    index+=1