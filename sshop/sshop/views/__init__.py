from Shop import *
from User import *
from Captcha import *
from NotFound import NotFoundHandler
from flag import *

handlers = [
        (r'/', ShopIndexHandler),
        (r'/shop', ShopListHandler),
        (r'/shop.bak', BakHandler),
        (r'/test', TestHandler),
        (r'/info/(\d+)', ShopDetailHandler),
        (r'/seckill', SecKillHandler),
        (r'/shopcar', ShopCarHandler),
        (r'/shopcar/add', ShopCarAddHandler),
        (r'/pay', ShopPayHandler),

        (r'/captcha', CaptchaHandler),

        (r'/user', UserInfoHandler),
        (r'/user/change', changePasswordHandler),
        (r'/pass/reset', ResetPasswordHanlder),

        (r'/login', UserLoginHanlder),
        (r'/logout', UserLogoutHandler),
        (r'/register', RegisterHandler),
        (r'.*', NotFoundHandler)

]