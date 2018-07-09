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
    last = cur.execute("SELECT * FROM houses ORDER BY id desc LIMIT 0,1").fetchall()
    lastid = last[0][0]
    COUNT = 3
    res = ""
    field1 = '"id"'
    field2 = '"title"'
    field3 = '"picture"'
    res = res + field1 + ':' + ranIdList + ','
    titlelist = []
    picturelist = []
    exist_houses_info = cur.execute("SELECT id,title,picture FROM houses").fetchall()
    ranIdList = random.sample(range(0, len(exist_id)), COUNT)
    for each in ranIdList:
        title = exist_houses_info[each][1] 
        titlelist.append(title)
        pic = exist_houses_info[each][2] 
        picturelist.append(pic)
    res = res + field2 + ':' + titlelist + ',' + field3 + ':' + picturelist
    res = '{' + res + '}'
    cur.close()
    return jsonify(res)
