from . import users
from app.users.users_form import RegisterForm, LoginForm
from flask import request, flash, url_for
from app.users import user_model as db
from app.db.database import ensure_tables_exist
from app.mail import mail as mail
from flask import redirect
from flask_login import login_user
from flask import jsonify

# an example.
# remove it when you begin developing and see this bad...


# returns
name_exist_return = jsonify('0', 'Name is exist')
mail_exist_return = jsonify('1', 'Mail is exist')
illegal_name_return = jsonify('2', 'Illegal name')
illegal_mail_return = jsonify('3', 'Illegal mail')
illegal_password_return = jsonify('4', 'Illegal password')
register_success_return = jsonify('5', 'Registered successfully')
wrong_method_return = jsonify('6', 'Wrong Request method')

not_activated_return = jsonify('0', 'Not activated')
login_successful_return = jsonify('1', 'Login successful')
wrong_password_return = jsonify('2', 'Wrong password')
account_exist_return = jsonify('3', 'Account does not exist')
wrong_way_return = jsonify('4', 'Wrong Request method')


@users.route("/users/register", methods=['GET', 'POST'])
def register():
	ensure_tables_exist()
	if request.method == 'POST':
		if not db.validateName(request.form['name']):
			return illegal_name_return
		elif not db.validateMail(request.form['mail']):
			return illegal_mail_return
		elif not db.validatePsd(request.form['password']):
			return illegal_password_return
		else:
			if db.isNameExisted(request.form['name']):
				return name_exist_return
			elif db.isMailExisted(request.form['mail']):
				return mail_exist_return
			else:
				db.addUser(request.form['name'], request.form['mail'], password_hash=db.password(request.form['password']))
				token = db.generate_activate_token(request.form['mail'])
				# 发送激活邮件
				mail.send_email(request.form['mail'], '请确认您的账户', 'activate', name=request.form['name'], token=token)
				return register_success_return
	return


@users.route("/users/activate/<token>")
def activate(token):
	if db.check_activate_token(token):
		# 激活成功
		return redirect(url_for('.login'))
	else:
		# 激活失败
		return redirect(url_for('.register'))


@users.route("/users/login", methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST':
		if db.isMailExisted(request.form['mail']):
			if not db.check_valid(request.form['mail']):
				return not_activated_return
			else:
				if db.verify_password(request.form['password'], request.form['mail']):
					result = db.get_nv(form.mail.data)
					u = db.User(result[0], db.password(request.form['password']), request.form['mail'], result[1])
					login_user(u, request.form['remember'])  # remember:记住密码
					return login_successful_return
				else:
					return wrong_password_return
				return account_exist_return
	return wrong_way_return
