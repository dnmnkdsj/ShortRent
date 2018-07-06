#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import db.database as _db
import random

''' show information of serveral houses randomly'''


# 返回house id 与 图片 标题
#  res = "{"id":[idlist],"pictures":[[],[],[]],"title":[titlelist]}"

@app.route('/showhouse/')
def showhouse():
    return render_template("showhouse.html")


@app.route('/housemsg/')
def housemsg():
    db = _db.getdb()
    cur = db.cursor()
    last = cur.execute("SELECT * FROM houses ORDER BY id desc LIMIT 0,1").fetchall()
    lastid = last[0][0]
    COUNT = 3
    ranIdList = random.sample(range(0, lastid + 1), COUNT);
    res = ""
    field1 = '"id"'
    field2 = '"title"'
    res = res + field1 + ':' + ranIdList + ','
    titlelist = []
    exist_id_and_title = cur.execute("SELECT id,title FROM houses").fetchall()
    ranIdList = random.sample(range(0, len(exist_id)), COUNT)
    for each in ranIdList:
        title = "'" + exist_id_and_title[each][1] + "'"
        titlelist.append(title)
    res = res + field2 + ':' + titlelist + ','
    res = '{' + res + '}'
    cur.close()
    return jsonify(res)
