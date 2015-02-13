#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import datetime
import yaml
from glob import glob
from djangorender import render_template
import datetime
import copy


def genfilename(s):
    s=re.sub(r"\W","_",s).lower()
    return s.replace("æ","ae").replace("ø","oe").replace("å","aa")

def initpost(title):
    data={}
    data["filename"]=genfilename(title)
    data["title"]=title
    data["datetime"]=datetime.datetime.now()
    with open("content/"+data["filename"]+".yaml","wb") as o:
        o.write(yaml.dump(data,default_flow_style=False,encoding="utf-8",allow_unicode=True))

def loadall(fileglob):
    data=[]
    for f in glob("content/"+fileglob):
        data.append(loadsingle(f))
    return data

def loadsingle(f):
    parts=[""]
    with open(f) as src:
        p=0
        for line in src:
            if(line.strip() == "---"):
                p=p+1
                parts +=[""]
            else:
                parts[p] +=line
    ctx=yaml.load(parts[0])
    if "event" in ctx:
        ctx["event"]["end"]=ctx["event"]["start"] +  datetime.timedelta(0, 7200)
    ctx["content"]="<p>"+parts[1].replace("\n\n","</p>\n\n<p>").strip()+"</p>"
    return ctx

def indexdata(data):
    index_data={}
    innkallinger=[e for e in data if "class" in e and e["class"]=="innkalling"]
    kommende=[e for e in data if "event" in e and e["event"]["start"]>datetime.datetime.now()]
    kommende=sorted(kommende,key=lambda e:e["event"]["start"])
    index_data["neste"]=kommende[0]
    index_data["kommende"]=kommende[1:]
    tidligere=[e for e in data if "event" in e and e["event"]["start"]<datetime.datetime.now()]
    tidligere=sorted(tidligere,key=lambda e:e["event"]["start"])
    index_data["tidligere"]=tidligere
    return index_data

def write_file(data,template,path):
    print path
    s=render_template(template,data)
    with open(path,"w") as o:
        o.write(s.encode("UTF-8"))

def buildallhtml(data):
    index_data=indexdata(data)
    build_index(index_data)
    for c in data:
        ctx=copy.deepcopy(c)
        ctx["others"]=index_data
        write_file(ctx,"templates/"+ctx["template"],"html/"+ctx["filename"]+".html")
        write_file(ctx,"templates/innkalling.vcs","html/"+ctx["filename"]+".vcs")

def build_index(data):
    write_file(data,"templates/index.html","html/index.html")
    write_file(data,"templates/calendar.vcs","html/calendar.vcs")


def main(*args):
    if args[1] == "init":
        initpost(args[2])
    if args[1] == "build":
        data=loadall("*.yaml")
        buildallhtml(data)


if __name__ == "__main__":
    import sys
    main(*sys.argv)
