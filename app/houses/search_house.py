#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, jsonify
from . import houses
import sqlite3, json
from ..db import database as _db

''' search the houses by keyword '''


# 接受： keyword 返回:查找状态（1：有结果，0：无结果）、house id 与 图片 标题
#  res = "{'status': ,id':[idlist],'pictures':[[],[],[]],'title':[titlelist]}"

@houses.route('/searchpage/')
def searchpage():
    return render_template('search_house.html')


@houses.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        db = _db.getdb()
        cur = db.cursor()
        keyword = request.form['keyword']
        result = cur.execute("SELECT * FROM houses WHERE address = ?", keyword).fetchall()
        cur.close()
        idlist = []
        titlelist = []
        #		picturelist = []
        if result == []:
            return jsonify({'status': 0, 'houses_id': ''})
        else:
            for each in result:
                idlist.append(each[0])
                titlelist.append(each[2])
            res = "{'status':1,'id':'" + idlist + "'," + "'title':" + titlelist + "}"
            return jsonify(res)
