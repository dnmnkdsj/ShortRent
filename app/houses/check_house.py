#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from . import houses
from ..db import database as _db
import os,shutil

# 接受信息： status: 管理员对房屋的操作，1代表通过，0代表拒绝 id:被操作的房屋的ID

admin_has_check = jsonify("0","house has been checked")
permission_denied = jsonify("1","Permission Denied")
wrong_method = jsonify("2","method not POST")

def DelLastChar(str):
    str_list=list(str)
    str_list.pop()
    return "".join(str_list)

@houses.route('/check/')
def check():
    admin = session.get('admin', 0)
    if admin:
        return render_template("check.html")
    else: 
        return permission_denieds


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
                # Delete the house (lazy delete?)
                picturepath = cur.execute("SELECT picture FROM houses WHERE id = ?", (request.form['id'],)).fetchall()[0][0]
                picturepath = picturepath.split(";")
                dirpath = DelLastChar(picturepath[0])
                shutil.rmtree(dirpath) #?
                #  ./photo/<house id>/0 -> ./photo/<house id>/
                cur.execute("DELETE FROM houses WHERE id = ?", (request.form['id'],))
            if operate == 1:
                cur.execute("UPDATE houses SET valid = 1 WHERE id=?", (request.form['id'],))
            cur.commit()
            cur.close()
            return admin_has_check
        else:
            return wrong_method
    else:
        return permission_denied
