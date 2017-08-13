#coding=utf8
import os
import sys
from bs4 import BeautifulSoup
import bs4
import urllib2
import re

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
    
def getchaperlist(config):
    #获取章节信息列表
    chapers=[]
    rootpage=urllib2.urlopen(config['rootlink']).read()
    soup=BeautifulSoup(rootpage).find(config['chaperhtml']['tag'],config['chaperhtml']['attrs'])
    links=soup.findAll('a')
    for l in links:
        if not l.attrs.has_key('href'):
            continue
        a=l['href']
        if re.match(config['chapermodel'],a):
            chapers.append((l.contents[0],a))
    return chapers

def getcontent4link(chaper,config):
    #获取对应页面的内容
    print chaper[0].encode(config['outcode'])
    if chaper[1][:4].lower()=='http':
        link=chaper[1]
    else:
        link=config['rootcontent']+chaper[1]
    soup=BeautifulSoup(urllib2.urlopen(link).read())
    txtag=soup.find(config['contenthtml']['tag'],config['contenthtml']['attrs'])
    for i in txtag.contents:
        if type(i)==bs4.element.NavigableString:
            print "  ",re.sub(config['filter'],'',i.strip()).encode(config['outcode'])

def debugprint(v):
    if config.has_key('debug') and config['debug']=='True':
        print v
try:
    config=readconfig(sys.argv[1])
    debugprint(config)
except Exception,e:
    print repr(e)
    print "User: Python txtdownload config_file"
    print "config_file: linke txt.config"
    exit()
chapers=getchaperlist(config)
print "chapers nums:",len(chapers)
for chaper in chapers:
    getcontent4link(chaper,config)