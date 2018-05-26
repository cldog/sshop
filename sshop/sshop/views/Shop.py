#coding=utf-8
import tornado.web
import tornado.options
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User, Shopcar
from sshop.settings import limit



class ShopIndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.redirect('/shop')


class ShopListHandler(BaseHandler):
    def get(self):
        page = self.get_argument('page', 1)
        page = int(page) if int(page) else 1
        commoditys = self.orm.query(Commodity) \
            .filter(Commodity.amount > 0) \
            .order_by(Commodity.price.desc()) \
            .limit(limit).offset((page - 1) * limit).all()
        return self.render('index.html', commoditys=commoditys, preview=page - 1, next=page + 1, limit=limit)


class ShopDetailHandler(BaseHandler):
    def get(self, id=1):
        try:
            commodity = self.orm.query(Commodity) \
                .filter(Commodity.id == int(id)).one()
        except NoResultFound:
            return self.redirect('/')
        return self.render('info.html', commodity=commodity)


class ShopPayHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        try:
            price = self.get_argument('price')
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            user.integral = user.pay(float(price))
            self.orm.commit()
            id = self.get_argument('id')
            commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
            commodity.amount=commodity.amount-1
            self.orm.commit()
            return self.render('pay.html', success=1)
        except:
            return self.render('pay.html', danger=1)


class ShopCarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        shopcar = self.orm.query(Shopcar) \
            .filter(Shopcar.amount > 0)\
            .order_by(Shopcar.price.desc())
        return self.render('shopcar.html', shopcar=shopcar)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        try:
            price = self.get_argument('price')
            name = self.get_argument('name',"1")
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            if name=="1":
                res = user.pay(float(price))
                user.integral = res
                self.orm.commit()
                shopcar = self.orm.query(Shopcar) \
                    .filter(Shopcar.amount > 0) \
                    .order_by(Shopcar.price.desc())
            else:
                shop = self.orm.query(Shopcar).filter(Shopcar.name == name).one()
                res = user.pay(float(price))
                if res:
                    user.integral = res
                    shop.amount -= 1
                    self.orm.commit()
                    shopcar = self.orm.query(Shopcar) \
                        .filter(Shopcar.amount > 0) \
                        .order_by(Shopcar.price.desc())
            return self.render('shopcar.html', shopcar=shopcar, success=1)
        except Exception as ex:
            print str(ex)
        return self.redirect('/shopcar')


class ShopCarAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        id = self.get_argument('id')
        commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
        try:
            sc = self.orm.query(Shopcar).filter(Shopcar.name == commodity.name).one()
            sc.amount += 1
        except NoResultFound:
            self.orm.add(Shopcar(name=commodity.name, price=commodity.price, amount=1))
        self.orm.commit()
        return self.redirect('/shop')


class SecKillHandler(BaseHandler):
    def get(self, *args, **kwargs):
        commodity = self.orm.query(Commodity).filter(Commodity.id == 1).one()
        return self.render('seckill.html', commodity = commodity)


    def post(self, *args, **kwargs):
        try:
            id = self.get_argument('id')
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
            if user.flag == 0:
                commodity.amount -= 1
                user.flag = 1
                self.orm.commit()
                return self.render('seckill.html', commodity = commodity, success=1)
            else:
                return self.render('seckill.html', commodity=commodity, tips="已经参与过秒杀的用户无法再次参与", danger=1)
        except:
            return self.render('seckill.html',commodity = commodity, danger=1)
