#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, jsonify
import sqlite3
import db.database as _db

''' show the information of specific house'''


# 接受信息: house_id:房屋的id

@app.route('/house_info/')
def house_info():
    return render_template('templates/book.html')


@app.route('/house_info/<int:house_id>')
def house_info(house_id):
    db = _db.getdb()
    cur = db.cursor()
    info = cur.execute("SELECT * FROM houses WHERE id = ?", (house_id,)).fetchall()
    info = info[0]  # tuple -> list
    cur.close()
    return jsonify({
        'address': info[1],
        'title': info[2],
        'description': info[3],
        'master': info[4],
        'rank': info[5],
        'pictures': info[6],
        'value': info[8]})
