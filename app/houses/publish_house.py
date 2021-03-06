#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, request, render_template, jsonify, session
from ..db import database as _db
from . import houses

'''publish the house information'''
# 接受信息： address: 房屋地址 title:房屋标题 description:房屋介绍 value:房屋价格 pictures:房屋图片
# 空字段 提交后为 '' 而非 None

anonymous = "hasn't log in"
null_field = "null_field"
long_title = "the tile is too long"
long_description = "the description is too long"


def str_len(str):
    row_l = len(str)
    utf8_l = len(str.encode('utf-8'))
    return ((utf8_l - row_l) / 2 + row_l) / 2


@houses.route('/publishpage/')
def publishpage():
    return render_template("publish.html")


@houses.route('/publish/', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':  # 将提交的合法房屋信息插入到数据库中
        # if has log in
        if session.get('email', '') != '':
            db = _db.getdb()
            cur = db.cursor()
            # check whether the info is valid
            if not (request.form.get('address') | request.form.get('title') | request.form.get(
                    'description') | request.form.get('value')):  # request.form.get('pictures')
                return null_field
            if str_len(request.form.get('title')) > 20:
                return long_title
            if str_len(request.form.get('description')) > 100:
                return long_description
            # number of photos???
            # start to insert
            last = cur.execute("SELECT * FROM houses ORDER BY id desc LIMIT 0,1").fetchall()
            last = last[0][0]
            id = last + 1
            info_list = list()
            info_list.append(id)
            info_list.append(request.form['address'])
            info_list.append(request.form['title'])
            info_list.append(request.form['description'])
            info_list.append(request.form['email'])
            info_list.append(0)  # initial rank
            info_list.append(request.form['pictures'])  # 传图片、保存 直接使用BASE64编码
            info_list.append('')
            info_list.append(request.form['value'])
            info_list.append(False)
            info_list.append(0)  # number of ratings
            # info_list = [id,request.form.get('address',''),request.form.get('title',''),request.form.get('description',''),request.form.get('email',''),0,pictutres,'',request.form.get('value',''),'False']
            info = tuple(info_list)
            cur.execute("INSERT INTO houses (?,?,?,?,?,?,?,?,?,?)", info)
            cur.commit()
            cur.close()
            return jsonify({'status': 1})  # ???
        return anonymous
