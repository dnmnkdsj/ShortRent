from app.db.database import getdb
from flask import current_app, flash
from app import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, text_type
import re


class User(UserMixin):
	# is_authenticated（）检验用户的实例化对象是否登录了。
	#
	# is_active（）检验用户是否通过某些验证
	#
	# is_anonymous（）检验用户是否为匿名用户
	#
	# id即为邮箱
	name = ''
	password = ''
	id = ''
	valid = ''
	rank = ''
	rank_times = ''

	def __init__(self, name, password, id, valid, rank, rank_times):
		self.name = name
		self.id = id
		self.password = password
		self.valid = valid
		self.rank = rank
		self.rankTimes = rank_times


# 检验名字是否存在--注册
def isNameExisted(name):
	sql = "select name from users where name='%s'" % name
	result = getdb().execute(sql).fetchall()
	if (0 == len(result)):
		return False
	else:
		return True


# 检验邮箱是否存在--注册
def isMailExisted(mail):
	sql = "select mail from users where mail='%s'" % mail
	result = getdb().execute(sql).fetchall()
	if (0 == len(result)):
		return False
	else:
		return True


# 检验名字是否合法:
def validateName(name):
	if 0 < len(name) < 10:
		return True
	return False


# 检验邮箱是否合法
def validateMail(mail):
	if len(mail) > 7:
		if re.match("^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", mail) is None:
			return False
		else:
			return True
	return False


# 检验密码是否合法
def validatePsd(password):
	if 4 < len(password) < 16:
		return True
	return False


# 保存密码时，保存加密后的hash值
def password(password):
	return generate_password_hash(password)


# 密码校验,正确返回True，错误返回False
def verify_password(password, mail):
	sql = "select password from users where mail = '%s' " % mail
	password_hash = getdb().execute(sql).fetchone()
	return check_password_hash(password_hash[0], password)


# 创建用户
def addUser(name, mail, password_hash):
	sql = "insert into users (name, mail, password, valid, rank_times, rank) values ('%s', '%s', '%s',0 ,0 ,0)" % (name, mail, password_hash)
	getdb().execute(sql)
	getdb().commit()


# 生成账户激活的token
def generate_activate_token(mail, expires_in=3600):
	s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
	return s.dumps({'mail': mail})


# 校验账户激活的token
def check_activate_token(token):
	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		data = s.loads(token)
	except:
		return False
	sql = "select mail from users where mail= '%s'" % data.get('mail')
	result = getdb().execute(sql).fetchone()
	if not result:
		flash('用户不存在')
		return False
	sql2 = "select valid from users where mail='%s'" % data.get('mail')
	result2 = getdb().execute(sql2).fetchone()
	valid = result2[0]
	if not valid:  # 账户没有激活
		flash('用户不存在')
		sql3 = "update users set valid=1 where mail='%s' " % data.get('mail')
		try:
			getdb().execute(sql3)
			getdb().commit()
			getdb().close()
		except:
			getdb().rollback()
	return True


# 生成重置密码激活的token
def generate_reset_token(password_hash, mail, expires_in=3600):
	s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
	return s.dumps({'mail': mail, 'password': password_hash})


# 检验重置密码的token
def check_reset_token(token):
	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		data = s.loads(token)
	except:
		return False
	sql = "update users set password = '%s' where mail = '%s'" % (data.password, data.mail)
	try:
		getdb().execute(sql)
		getdb().commit()
	except:
		getdb().rollback()
	return True


# 获取name, valid
def get_nv(mail):
	sql = "select name, valid ,rank ,rank_times from users where mail = '%s'" % mail
	result = getdb().execute(sql).fetchone()
	return result


# 检查是否激活
def check_valid(mail):
	sql = "select valid from users where mail='%s'" % mail
	result = getdb().execute(sql).fetchone()
	if result is None:
		return False
	else:
		return True


# 登录认证的回调
@login_manager.user_loader
def load_user(user_id):
	sql = "select name, mail, password, valid , rank , rank_times from users where mail = '%s' " % str(user_id)
	result = getdb().execute(sql).fetchone()
	u = User(result[0], result[1], result[2], result[3],result[4] ,result[5])
	return u


# 修改密码
def db_change_password(new_password, mail):
	sql = "update users set password = new_password where mail = '%s'" % mail
	try:
		getdb().execute(sql)
		getdb().commit()
	except:
		getdb().rollback()
