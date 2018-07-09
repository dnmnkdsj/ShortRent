#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, request, render_template, jsonify
from . import houses
from ..db import database as _db
import random

''' show information of serveral houses randomly'''


# 返回house id 与 图片 标题
#  res = "{"id":[[],[],[]],"pictures":[[],[],[]],"title":[[],[],[]]}"

@houses.route('/showhouse/')
def showhouse():
    return render_template("showhouse.html")


@houses.route('/housemsg/')
def housemsg():
    db = _db.getdb()
    cur = db.cursor()
    COUNT = 3
    res = ""
    field1 = '"id"'
    field2 = '"title"'
    field3 = '"picture"'
    titlelist = []
    picturelist = []
    exist_houses_info = cur.execute("SELECT id,title,picture FROM houses").fetchall()
    if len(exist_houses_info) < COUNT:
        return jsonify("No enough entry")
    else:
        ranIdList = random.sample(range(0, len(exist_houses_info)), COUNT)
        res = res + field1 + ':' + ranIdList + ','    
        for each in ranIdList:
            title = exist_houses_info[each][1] 
            titlelist.append(title)
            pic = exist_houses_info[each][2] 
            picturelist.append(pic)
        res = res + field2 + ':' + titlelist + ',' + field3 + ':' + picturelist
        res = '{' + res + '}'
        cur.close()
        return jsonify(res)
