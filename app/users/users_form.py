from wtforms import Form, StringField, PasswordField, SubmitField, RadioField, validators
from wtforms.validators import Email, DataRequired, Length, EqualTo
from wtforms.validators import ValidationError
from app.users import user_model as db


# 用户注册表单
class RegisterForm(Form):
    mail = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    name = StringField('用户名', validators=[DataRequired(), Length(4, 20, message='用户名只能在4-20个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message='密码长度必须在6-20个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码输入不一致')])
    submit = SubmitField('立即注册')

    # 验证username
    def validate_name(self, field):
        if db.isNameExisted(name=field.data):
            raise ValidationError('该用户名已注册，请选用其他用户名')

    # 验证邮箱
    def validate_mail(self, field):
        if db.isEmailExisted(mail=field.data):
            raise ValidationError('此邮箱已经注册')


# 用户登陆表单
class LoginForm(Form):
    mail = StringField('用户名', [validators.required()])
    password = PasswordField('密码', [validators.required()])
    login = SubmitField('login')
    remember = RadioField('记住密码', choices=[('1', '记住密码')], validators=[DataRequired()])
    submit = SubmitField('登录')


# 修改密码
class ChangepwdForm(Form):
    oldpassword = PasswordField('旧密码', [validators.required()])
    newpassword = PasswordField('新密码', [validators.required()])
    confirm = PasswordField('确认密码', validators=[EqualTo('newpassword', message='两次密码不一致')])
