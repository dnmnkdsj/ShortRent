from flask import Flask, render_template, request, url_for, redirect
from . import inner_test


@inner_test.route('/test/<a>/<b>')
def inner_test_add(a, b):
    """
    Sample: take two intergers, show their sum.
    """
    return str(int(a)+int(b))

@inner_test.route('/test/page')
def inner_test_mainpage():
    """
    Sample: Using templates.
    """
    return render_template('inner_test.html')

@inner_test.route('/test/login', methods=['POST'])
def inner_test_react():
    """
    Sample: Receive a POST, return sum of number, or return to login page if input is not number.
    """
    try:
        for i in request.form:
            print(i + ' ' + request.form[i])
        xa = int(request.form['user'])
        xb = int(request.form['password'])
        print('succ.')
        return redirect('/test/' + str(xa) + '/' + str(xb))
    except Exception as err:
        pass
    finally:
        pass
    return redirect('/test/page')

@inner_test.route('/test/picture')
def inner_test_picture():
    """
    Sample: Redirect to a picture.
    """
    return redirect(url_for('static', filename='inner_test/DKAvatar.png'))