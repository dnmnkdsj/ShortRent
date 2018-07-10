from . import users
from flask import request, url_for
from app.users import users_management as db
from app.db.database import ensure_tables_exist
from app.mail import mail as mail
from flask import redirect
from flask_login import login_user, current_user, logout_user, login_required
from flask import jsonify, session, g

# an example.
# remove it when you begin developing and see this bad...


# register
name_exist_return = jsonify([0, 'Name is exist'])
mail_exist_return = jsonify([1, 'Mail is exist'])
illegal_name_return = jsonify([2, 'Illegal name'])
illegal_mail_return = jsonify([3, 'Illegal mail'])
illegal_password_return = jsonify([4, 'Illegal password'])
register_success_return = jsonify([5, 'Registered successfully'])
wrong_method_return = jsonify([6, 'Wrong Request method'])
# login
not_activated_return = jsonify([0, 'Not activated'])
login_successful_return = jsonify([1, 'Login successful'])
wrong_password_return = jsonify([2, 'Wrong password'])
account_exist_return = jsonify([3, 'Account does not exist'])
wrong_way_return = jsonify([4, 'Wrong Request method'])
showhouse_return = jsonify([5, "redirect(url_for('showhouse'))"])
# change_psw
invalid_password_return = jsonify([0, 'Wrong password'])
wrong_request_return = jsonify([1, 'Wrong request method'])
users_signIn_return = jsonify([2, "redirect(url_for('users.signIn'))"])
# reset
not_activated_return = jsonify([0, 'Not activated'])
mail_exist_return = jsonify([1, 'Mail is exist'])
mail_success_return = jsonify([2, 'Reset mail send'])
showhouse_return = jsonify([5, "redirect(url_for('showhouse'))"])
wrong_method_return = jsonify([6, 'Wrong Request method'])
# admin
admin_success_return = jsonify([0, 'administrator logged in successfully'])
admin_fail_return = jsonify(1, 'administrator login failed')


@users.route("/users/signUp", methods=['GET', 'POST'])
def register():
	ensure_tables_exist()
	if request.method == 'POST':
		print(request.form['name'])
		if not db.validateName(request.form['name']):
			print('0')
			return illegal_name_return
		elif not db.validateMail(request.form['mail']):
			print('1')
			return illegal_mail_return
		elif not db.validatePsd(request.form['password']):
			print('2')
			return illegal_password_return
		else:
			if db.isNameExisted(request.form['name']):
				print('4')
				return name_exist_return
			elif db.isMailExisted(request.form['mail']):
				print('5')
				return mail_exist_return
			else:
				db.addUser(request.form['name'], request.form['mail'], password_hash=db.password(request.form['password']))
				token = db.generate_activate_token(request.form['mail'])
				# 发送激活邮件
				mail.send_email(request.form['mail'], '请确认您的账户', 'activate', name=request.form['name'], token=token)
				return register_success_return
	return wrong_method_return


@users.route("/users/activate/<token>")
def activate(token):
	if db.check_activate_token(token):
		# 激活成功
		return redirect('/signIn')
	else:
		# 激活失败
		return redirect(url_for('/signUp'))


@users.before_request
def before_request():
	g.user = current_user


@users.route("/users/signIn", methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		session['_fresh'] = False
		return showhouse_return
	else:
		if request.method == 'POST':
			if db.isMailExisted(request.form['mail']):
				if not db.check_valid(request.form['mail']):
					return not_activated_return  # 账户未激活
				else:
					if db.verify_password(request.form['password'], request.form['mail']):
						result = db.get_nv(request.form['mail'])
						user = db.User(result[0], db.password(request.form['password']), request.form['mail'], result[1], result[2], result[3])
						login_user(user, request.form['remember'])  # remember:记住密码
						return login_successful_return
					else:
						return wrong_password_return
			else:
				return account_exist_return
		return wrong_way_return


@users.route("/users/change_psw", methods=['GET', 'POST'])
@login_required
def change_psw():
	if request.method == 'POST':
		if db.verify_password(request.form['old_password'], current_user.mail):
			current_user.password = db.password(request.form['new_password'])  # 存的是hash值
			db.db_change_password(current_user.password, current_user.id)  # id 即为mail
			logout_user()
			return users_signIn_return
		else:
			return invalid_password_return
	return wrong_request_return


@users.route("/users/reset", methods=['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonmyous:
		#  验证密码是否为登录状态
		return showhouse_return
	if request.method == 'POST':
		if not db.isMailExisted(request.form['mail']):
			return mail_exist_return
		else:
			if not db.check_valid(request.form['mail']):
				return not_activated_return
			else:
				token = db.generate_reset_token(db.password(request.form['password']), request.form['mail'])
				mail.send_email(request.form['mail'], '请确认重置密码', 'reset', name=request.form['mail'], token=token)
			return mail_success_return
	return wrong_method_return


@users.route("/users/reset/<token>", methods=['GET', 'POST'])
def password_reset_token(token):
	if db.check_reset_token(token):
		# 修改密码成功
		return redirect(url_for('users.signIn'))
	else:
		# 修改密码失败
		return redirect(url_for('users.signIn'))


@users.route("/users/admin", methods=['GET', 'POST'])
def check_admin():
	if request.method == 'POST':
		if request.form['mail'] == 'shortrent' and request.form['password'] == 'shortrent':
			session['admin'] = 1
			return admin_success_return
		else:
			return admin_fail_return