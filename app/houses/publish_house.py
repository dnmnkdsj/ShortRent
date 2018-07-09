#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, request, render_template, jsonify, session
from ..db import database as _db
from . import houses
import os

'''publish the house information'''
# 接受信息： address: 房屋地址 title:房屋标题 description:房屋介绍 value:房屋价格 pictures:房屋图片
# 空字段 提交后为 '' 而非 None

anonymous = jsonify("hasn't log in")
null_field = jsonify("null_field")
long_title = jsonify("the tile is too long")
long_description = jsonify("the description is too long")
photos_number_wrong = jsonify("the number of photos is unvalid")
success = jsonify("success")

#caculate the length of Chinese
def str_len(str):
    row_l = len(str)
    utf8_l = len(str.encode('utf-8'))
    return ((utf8_l - row_l) / 2 + row_l) / 2

def savephoto(photolist,id):
    path = "./photo" + str(id)
    mkdir = os.mkdir(path)
    url_list = []
    for i in range(len(photolist)):
        photopath = path + "/" + str(i)  # ./photo/<house id>/<i>
        f = open(photopath,'rb')
        f.write(photolist[i])
        f.close()
        url_list.append(photopath)
    all_url = ';'.join(url_list)
    return all_url

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
            photos = request.form.get('pictures')
            if len(photos) < 4 and len(photos) > 10:
                return photos_number_wrong 
            # start to insert
            last = cur.execute("SELECT * FROM houses ORDER BY id desc LIMIT 0,1").fetchall()
            if last == []:
                id = 1
            else:
                last = last[0][0]
                id = last + 1
            pictures_url = savephoto(photos,id) # "./photo/<house id>/0;./photo/<house id>/1 ...etc"
            info_list = list()
            info_list.append(id)
            info_list.append(request.form['address'])
            info_list.append(request.form['title'])
            info_list.append(request.form['description'])
            info_list.append(request.form['email'])
            info_list.append(0)  # number of ratings            
            info_list.append(0)  # initial rank
            info_list.append(pictures_url)  # format:
            info_list.append(request.form['value'])
            info_list.append(False)
            # info_list = [id,request.form.get('address',''),request.form.get('title',''),request.form.get('description',''),request.form.get('email',''),0,pictutres,'',request.form.get('value',''),'False']
            info = tuple(info_list)
            cur.execute("INSERT INTO houses (?,?,?,?,?,?,?,?,?,?)", info)
            cur.commit()
            cur.close()
            return success
        return anonymous
