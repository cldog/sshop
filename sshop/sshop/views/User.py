#coding=utf-8
import tornado.web
from sqlwaf import checkwaf,checkuser,checkpass
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User


class UserLoginHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('login.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self):
        if not self.check_captcha():
            return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="验证码错误 ：）")
        username = self.get_argument('username')
        password = self.get_argument('password')
        if (checkwaf(username) or checkwaf(password)):
            return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="存在安全隐患，已拒绝操作 ：）")
        if username and password:
            try:
                user = self.orm.query(User).filter(User.username == username).one()
            except NoResultFound:
                return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
            if user.check(password):
                self.set_secure_cookie('username', user.username)
                self.redirect('/user')
            else:
                return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid)


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('register.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="验证码错误 ：）")
        username = self.get_argument('username')
        mail = self.get_argument('mail')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        invite_user = self.get_argument('invite_user')
        if checkuser(username):
            print 1
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="用户名不合规范 ：）")
        if checkpass(password):
            print 2
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="密码不合规范 ：）")
        if checkwaf(username):
            print 3
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="存在安全隐患1，已拒绝操作 ：）")
        if checkwaf(password):
            print 4
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="存在安全隐患2，已拒绝操作 ：）")
        if checkwaf(password_confirm):
            print 5

            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="存在安全隐患3，已拒绝操作 ：）")
        if checkwaf(invite_user):
            print 6
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="存在安全隐患4，已拒绝操作 ：）")

        if password != password_confirm:
            print 7
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="密码确认错误 ：）")
        if mail and username and password:
            try:
                user = self.orm.query(User).filter(User.username == username).one()
                print 8
                return self.render('register.html', danger=1, ques=self.application.question,uuid=self.application.uuid, tips="用户名已存在 ：）")
            except NoResultFound:
                self.orm.add(User(username=username, mail=mail,
                                  password=bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())))
                self.orm.commit()





                try:
                    if invite_user==username:
                        print 9
                        return self.render('register.html', danger=1, ques=self.application.question,uuid=self.application.uuid, tips="邀请人有误 ：）")
                    inviteUser = self.orm.query(User).filter(User.username == invite_user).one()
                    inviteUser.integral += 10
                    self.orm.commit()
                except NoResultFound:
                    pass
                self.redirect('/login')
        else:
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid)


class ResetPasswordHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('reset.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            return self.render('reset.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
        return self.redirect('/login')


class changePasswordHandler(BaseHandler):
    def get(self):
        return self.render('change.html')

    def post(self, *args, **kwargs):
        old_password = self.get_argument('old_password')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        if (checkwaf(old_password) or checkwaf(password) or checkwaf(password_confirm)):
            return self.render('change.html', danger=1, ques=self.application.question, uuid=self.application.uuid,tips="存在安全隐患，已拒绝操作 ：）")
        print old_password, password, password_confirm
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        if password == password_confirm:
            if user.check(old_password):
                user.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
                self.orm.commit()
                return self.render('change.html', success=1)
        return self.render('change.html', danger=1)


class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        return self.render('user.html', user=user)


class UserLogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie('username')
        self.redirect('/login')
