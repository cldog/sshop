#coding=utf-8
from tornado import escape

import binascii
import hashlib
import os
from sshop.base import BaseHandler


class BakHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('bak.txt')
class TestHandler(BaseHandler):

    def get(self,*args,**kwargs):
        f = open(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "views/flag.txt"))
        flag = f.read()
        f.close()
        md=hashlib.md5()
        md.update(flag+"hhh")
        md5=md.hexdigest()
        self.set_header("Hint", "parameter")
        self.set_header("length",len(flag))
        self.set_header("md5",md5)
        return self.render('pac.html')
    def post(self):

        #print self.request.body

        para = self.get_argument('parameter',"hhhh")

        md5_post = self.get_argument('md5',"xiaoyueyue")
        f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "flag.txt"))
        flag = f.read()
        f.close()
        md = hashlib.md5()
        if para:
            if para == "hhhh":
                self.set_header("Hint", "parameter")
                self.set_header("length", len(flag))
                md.update(flag + "hhh")
                md5 = md.hexdigest()
                self.set_header("md5", md5)
                return self.render('pac.html')
            else:
                
                a = para.encode('unicode-escape').decode('string_escape')
                b=list(a)
                for i in range(len(a)):
                    if b[i]==" ":
                        b[i]="\x00"

                c=''.join(b)
                str=flag+c
                md.update(str)
                md5_gen=md.hexdigest()
                print md5_gen
                if md5_gen==md5_post:
                    return self.render('flag.html',flag=flag)
                else:

                    self.set_header("Hint", "parameter")
                    self.set_header("length", len(flag))
                    md.update(flag + "hhh")
                    md5=md.hexdigest()
                    self.set_header("md5", md5)
                    return self.render('pac.html')
        else:
            return self.render('pac.html')
