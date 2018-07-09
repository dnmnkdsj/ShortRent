#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from . import houses
from ..db import database as _db
import os,shutil

# 接受信息： status: 管理员对房屋的操作，1代表通过，0代表拒绝 id:被操作的房屋的ID

admin_has_check = jsonify("house has been checked")
permission_denied = jsonify("Permission Denied")
wrong_request = jsonify("method is not POST")

def DelLastChar(str):
    str_list=list(str)
    str_list.pop()
    return "".join(str_list)

@houses.route('/check/')
def check():
    admin = session.get('admin', 0)
    if admin:
        return render_template("templates/check.html")
    else:  # 如果不是管理员就把ta赶回首页去
        return permission_denied


@houses.route('/checkpost/', methods=['GET', 'POST'])
def checkpost():
    # check the admin status
    admin = session.get('admin', 0)
    if admin:
        if request.method == 'POST':
            operate = request.form.get('status', '')  # the status means whether the admin passes the house
            db = _db.getdb()
            cur = db.cursor()
            if operate == 0:
                picturepath = cur.execute("SELECT picture FROM houses WHERE id = ?", (request.form['id'],)).fetchall()[0][0]
                picturepath = picturepath.split(";")
                dirpath = DelLastChar(picturepath[0])
                shutil.rmtree(dirpath)
                #  ./photo/<house id>/0 -> ./photo/<house id>/
                cur.execute("DELETE FROM houses WHERE id = ?", (request.form['id'],))
            if operate == 1:
                cur.execute("UPDATE houses SET valid = 1 WHERE id=?", (request.form['id'],))
            cur.commit()
            cur.close()
            return admin_has_check
        return wrong_request
    return permission_denied
