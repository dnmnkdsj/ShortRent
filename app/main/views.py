from . import main
from flask import render_template


# url_for('index')
@main.route('/')
def index():
    return render_template('index.html')


# url_for('house_details')
@main.route('/houseDetails/<int:house_id>')
def house_details(house_id):
    return render_template('houseDetails.html')


# url_for('house_display')
@main.route('/houseDisplay')
def house_display():
    return render_template('houseDisplay.html')


# url_for('my_house')
@main.route('/myHouse')
def my_house():
    return render_template('myHouse.html')


# url_for('my_order')
@main.route('/myOrder')
def my_order():
    return render_template('myOrder.html')


# url_for('release_house')
@main.route('/releaseHouse')
def release_house():
    return render_template('releaseHouse.html')


# url_for('sign_in')
@main.route('/signIn')
def sign_in():
    return render_template('signIn.html')


# url_for('sign_up')
@main.route('/signUp')
def sign_up():
    return render_template('signUp.html')


# url_for('user_info')
@main.route('/userInfo')
def user_info():
    return render_template('userInfo.html')




