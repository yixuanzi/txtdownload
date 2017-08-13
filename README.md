# txtdownload,TXT文件在线爬取下载
### author:yixuanzi
### email:yeying0311@126.com
### date:2017-8-13

#### Use
```bash
python txtdownload {txt.config}
```

#### config
```python
rootlink:http://www.xs.la/112_112260/
#章节目录所处结构，tag;[name:value;,...]
chaperhtml:div;id:list
#网页内容前缀
rootcontent:http://www.xs.la
#章节链接模式
chapermodel:\/112_112260\/\d+\.html
#章节内容结构
contenthtml:div;id:content
#输出编码
outcode:gbk
#过滤字符
filter:\x0a|\xa0
```