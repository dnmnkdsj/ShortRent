#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, jsonify
import sqlite3, os
import db.database as _db

# 接受信息： status: 管理员对房屋的操作，1代表通过，0代表拒绝 id:被操作的房屋的ID

admin_has_check = "house has been checked"
permission_denied = "Permission Denied"


@app.route('/check/')
def check():
    admin = session.get('admin', 0)
    if admin:
        return render_template("check.html")
    else:  # 如果不是管理员就把ta赶回首页去
        return redirect(url_for('home'))


@app.route('/checkpost/', methods=['GET', 'POST'])
def checkpost():
    # check the admin status
    admin = session.get('admin', 0)
    if admin:
        if request.method == 'POST':
            operate = request.form.get('status', '')  # the status means whether the admin passes the house
            #			if operate == '':
            #				return render_template("check.html")	# 如果只是手贱瞎xx点了一下提交
            db = _db.getdb()
            cur = db.cursor()
            if operate == 0:
                # Delete the house (lazy delete?)
                cur.execute("DELETE FROM houses WHERE id = ?", (request.form['id'],))
            if operate == 1:
                cur.execute("UPDATE houses SET valid = 1 WHERE id=?", (request.form['id'],))
            cur.commit()
            cur.close()
            return admin_has_check
        # return wrong_request???  (while not post)
    return permission_denied
