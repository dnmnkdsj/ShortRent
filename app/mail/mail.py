from flask_mail import Message
from flask import current_app, render_template
from . import mailServer
from threading import Thread


# 异步发送邮件
def async_send_mail(app, msg):
	with app.app_context():
		mailServer.send(message=msg)


# 封装函数，发送邮件
def send_email(to, subject, template, **kwargs):
	# 获取当前实例
	app = current_app._get_current_object()
	# 创建邮件对象
	msg = Message(subject=subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
	# 浏览器打开邮件显示内容
	msg.html = render_template(template + '.html', **kwargs)
	# 终端接受邮件显示内容
	msg.body = render_template(template + '.txt', **kwargs)
	# 创建线程
	thread = Thread(target=async_send_mail, args=[app, msg])
	# 启动线程
	thread.start()
	return thread
