#coding: utf-8

import os, sys
import json
import traceback
import logging
from datetime import datetime
from datetime import timedelta
import time
import re
import urllib
from collections import defaultdict
import json

import conf

import tornado.web


class Item(object):
    def __init__(self, fg_pic, bg_pic, fg_title, fg_content, bg_title, bg_content, weight):
        self.fg_pic     = fg_pic
        self.bg_pic     = bg_pic
        self.fg_title   = fg_title
        self.fg_content = fg_content
        self.bg_title   = bg_title
        self.bg_content = bg_content
        self.weight     = weight

    def __str__(self):
        return str([
            self.fg_pic     ,
            self.bg_pic     ,
            self.fg_title   ,
            self.fg_content ,
            self.bg_title   ,
            self.bg_content ,
            self.weight     ,
        ])
    __repr__ = __str__


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        abs_show_path = conf.MainConf.single().abs_show_path
        ref_show_path = conf.MainConf.single().ref_show_path

        pics = [i for i in os.listdir(abs_show_path) if i.endswith('.jpg')]
        item = {}
        for pic in pics:
            if pic.endswith('.raw.jpg'):
                name = pic.split('.raw.jpg')[0]
                name = "%s.done.jpg"%name
                if name in pics:
                    item[pic] = name
        for k, v in item.items():
            pics.remove(k)
            pics.remove(v)
        for pic in pics:
            item[pic] = ""
        info = open(abs_show_path + "/info.txt").read()
        info = json.loads(info)
        rets = []
        for fg_pic, bg_pic in item.items():
            fg_title   = info.get(fg_pic,{}).get("show_title", "")
            fg_content = info.get(fg_pic,{}).get("show_content", "")
            bg_title   = info.get(fg_pic,{}).get("hide_title", "")
            bg_content = info.get(fg_pic,{}).get("hide_content", "").split()
            weight  = info.get(fg_pic,{}).get("weight", 0)
            if fg_pic:
                fg_pic = "%s/%s"%(ref_show_path, fg_pic)
            if bg_pic:
                bg_pic = "%s/%s"%(ref_show_path, bg_pic)
            rets.append(Item(fg_pic, bg_pic, fg_title, fg_content, bg_title, bg_content, weight))
        rets.sort(cmp=lambda x, y: cmp(x.weight, y.weight), reverse=True)
        #print len(rets)
        #for ret in rets:
        #    print ret
        self.render("index.html", item=rets)


class ShowsHandler(tornado.web.RequestHandler):
    def get(self):
        name = '/' + self.request.path[6:].strip('/')
        self.render("shows.html", path=name) 


