import random,time
from Buyer.models import *
from Store.models import *
from django.shortcuts import render
from Store.views import setpassword
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from datetime import datetime
from alipay import AliPay
#设置一个函数。判断用户是否存在
def loginuser(username):
    user=Buyer.objects.filter(username=username).first()
    return user
#设置html的base页面
def base(request):
    return render(request,"buyer/base.html")
#用户注册页面
def register(request):
    result={"status":"error","content":""}
    if request.method=="POST":
        username=request.POST.get("user_name")
        password=request.POST.get("pwd")
        email=request.POST.get("email")
        if username and password and not loginuser(username):
            user=Buyer()
            user.username=username
            user.password=setpassword(password)
            user.email=email
            user.save()
            return HttpResponseRedirect('/buyer/login/')
        else:
            result["content"]="用户密码不能为空"

    return render(request,'buyer/register.html',locals())
#用户登录页面
def login(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("pwd")
        #判断密码用户不能为空
        if username and password:
            user=loginuser(username)
            #判断此用户存在，校验密码
            if user:
                wed_password = setpassword(password)
                if user.password==wed_password:
                    #设置cookies
                    response=HttpResponseRedirect('/buyer/index/')
                    response.set_cookie("username",username)
                    response.set_cookie("user_id",user.id)
                    request.session["username"]=username
                    return response
    return render(request,'buyer/login.html',locals())
#cookies校验
def loginvalid(fun):
    def inner(request,*args,**kwargs):
        c_u=request.COOKIES.get("username")
        s_u=request.session.get("username")
        if c_u and s_u and c_u==s_u:
            user=Buyer.objects.filter(username=c_u).first()
            if user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/buyer/login/')
    return inner
#设置主页页面
@loginvalid
def index(request):
    result=[]
    goods_type_list=Goodstype.objects.all()
    for goods_type in goods_type_list:
        goods_list=goods_type.goods_set.values()[:4]
        if goods_list:
            goodstype={
                "id":goods_type.id,
                "type_name":goods_type.type_name,
                "type_description":goods_type.type_description,
                "picture":goods_type.picture,
                "goods_list":goods_list
            }
            result.append(goodstype)

    return render(request,'buyer/index.html',locals())
#退出功能
def logout(request):
    response=HttpResponseRedirect("/buyer/login/")
    for key in request.COOKIES:
        response.delete_cookie(key)
    return response
#类型列表展示
def goods_list(request):
    id=request.GET.get("id")
    goods_type=Goodstype.objects.filter(id=id).first()
    if goods_type:
        goodslist=goods_type.goods_set.all()
    return render(request,'buyer/goods_list.html',locals())
#支付功能
#支付完结果
def pay_result(request):
    return render(request,'buyer/pay_result.html',locals())
def pay_order(request):
    money=request.GET.get("money")
    order_id=request.GET.get("order_id")


    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzR3vhY7kXDTszlXozA7dM1r5JIwl8CjO/VPegoXLYlFv4NacG9+sahDksPpjJkNnxG22saxuNGC8QzkYpIdKKgDVFernvFBWAEt9OXfiwK8yKVvd3eQ33nItXm4IOHGewHF2SLBNWtIa6uY4AahRcZIOa6vAVrw7egw1tJpTFgKAsdrZugrTYOpnQ3ar36hMkOEjTiasMfDKJwkfFt8YbkaoyEFCOw18qd4AMDvU4kx3AbMDw926ghlI4lIP8lt4UhLyzhcdlq8u5lavv5zE6gAC9PEdHtVitCwgTJdkwtnr/QBam77fOlMynvdjgHQkJh9BJumzDUCOR0JJ4lqo5wIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAzR3vhY7kXDTszlXozA7dM1r5JIwl8CjO/VPegoXLYlFv4NacG9+sahDksPpjJkNnxG22saxuNGC8QzkYpIdKKgDVFernvFBWAEt9OXfiwK8yKVvd3eQ33nItXm4IOHGewHF2SLBNWtIa6uY4AahRcZIOa6vAVrw7egw1tJpTFgKAsdrZugrTYOpnQ3ar36hMkOEjTiasMfDKJwkfFt8YbkaoyEFCOw18qd4AMDvU4kx3AbMDw926ghlI4lIP8lt4UhLyzhcdlq8u5lavv5zE6gAC9PEdHtVitCwgTJdkwtnr/QBam77fOlMynvdjgHQkJh9BJumzDUCOR0JJ4lqo5wIDAQABAoIBAAnb3H1g5tz/tjocqvnT5RHo13zIN7KZY4mNlG5Vm/b3zxbReeNlFtZqRXO0NTvLlZs9YsCbdxiRZbsdbW/LCOeH7rYE+mp0ug19k2FFv+JfCVwvjDR0GbNZbZDSXRbJb0X0rijEQJOS8bREqIB75J4+1O6b7Ly+g2VUXOh3WnL+ScOAEG9b2fPOhDQcygN8g8Ax/XJ0F6nOf3rN4i3BjV6p1Y4OMvxYElSIk3atpt+ZViaNtbbo7U706JLpnwmkrwyOq2fEyJcmzEmbwwkCrTUaqmuP3aMrBSTqP6aajxxqqX3SSm3RKojcbQV7yb2k6oWPLHDS+bTOQzV8FxxLhjECgYEA7BdD8yI0qDSC17o/199cPLp7wUSxPTrtcH6p4zF9hiGcQiVAYcqjqcP4yO4NiDQNQ5eN4S4T47xdiWFeiIkTkHjPs2mLYKdoLSigS976eYFNsYbjo/sVjfSuoV8VgBYk94pdVndt75dglrO1PfVadZnAYg9HlwGWpeywf4GQDmUCgYEA3moBC1+8tLW2ZD/T/mbRFNGKeJgLH32+0QS/DXBf2sZPXGfb5UVqvogJTMY8Jt6qqPCTo+qU/u3c8b42f9TnoDr4zreWmVgArDZQGbJVZUVF8Vm2QSRYl80HxWaVGJuom/ymklr2X3Yr1SPrQD76dfIlK3x0jiqMfJxK3/btL1sCgYBdZV7GIjP+jrdsLAvxlDTi+UrXzBrphBRGOnVuoTdtBoLQT/hGN2nDUPlsU3Aa/6x3ns7L0/SeVPgTzucc0E1jC8fuy8QNemxl4Pp4yT8BLjvUDO6lAkEmpTMoN3tD7n61RpFiEWD2NUZKl9ENL7CXcTmAEVdaz5APF7FC37hjWQKBgDctr1KmDsf6aOSYHTz5PxfeIG9osSG/7Y4nkkqAPZemKVwwfBJ2VVQtpbkBWTz/cvF0tfwtn4dbdbwXx6eRJ2HOH5oRW/BxL8GJu/eUEbGNLRwCeL/Sh5Qpjqr/ly/CtmL0nFKk9IicZaV8Qsnule6bA3O1bakzjyT/FWhY92EPAoGBAKHaoH2xi1zrHHfoxts8u82/5ECJSvWtOG3GeC/C2QqFr3D0xUj8xTyoP7rhrP3/kaTWRNWnMzd4wfSnAe/35UhagX29ql5mlMHLGAbDYl6UXdesuYvJPdQzCvYDBkYmtsDUnxms5SADEbnLxEszHzdR6fY8ACYGtISdMrajj2rD
    -----END RSA PRIVATE KEY-----
    """
    # 实例化支付应用
    alipay = AliPay(
        appid="2016101000652517",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )
    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主题
        return_url="http://127.0.0.1:8000/buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/buyer/pay_result/",
    )
    order = Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()
    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)
#商城页面展示单个产品的详情
def goods(request):
    id=request.GET.get("id")
    if id:
        goods = Goods.objects.filter(id=id).first()
        if goods:
            goods_type = Goodstype.objects.filter(id=goods.goods_type_id).first()
            return render(request,'buyer/goods.html',locals())
    return HttpResponse("没有指定商品")
#保存东西到订单中
#设置一个函数来实现订单号
def setorderid(user_id,goods_id,store_id):
    order_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    order_id=order_time+str(user_id)+str(goods_id)+str(store_id)
    return order_id
def place_order(request):
    #从商品详情因为form表单action指向，post提交到了这个视图。
    if request.method=='POST':
        goods_id=request.POST.get("goods_id")
        goods=Goods.objects.filter(id=goods_id).first()
        user_id=request.COOKIES.get("user_id")
        count=request.POST.get("count")
        store_id=goods.store_id.id#商品与店铺多对一的关系,
        price=goods.goods_price
        order=Order()
        order.order_id=setorderid(user_id,goods_id,store_id)
        order.goods_count=int(count)
        order.order_user=Buyer.objects.get(id=user_id)
        order.order_price=int(count)*price
        order.order_status=1#生成订单的时候，都是未支付状态
        order.save()
        #保存订单详情
        order_detail=OrderDetail()
        order_detail.order_id=order
        order_detail.goods_id=goods_id
        order_detail.goods_name=goods.goods_name
        order_detail.goods_price=price
        order_detail.goods_number=int(count)
        order_detail.goods_store=store_id
        order_detail.goods_total=int(count)*price
        order_detail.goods_image=goods.goods_image

        order_detail.save()
        detail=[order_detail]
    return render(request,'buyer/place_order.html',locals())
# def goods(request):
#     id=request.GET.get("id")
#     goods=Goods.objects.filter(id=id).first()
#     goods_price = goods.goods_price
#     goods_type = Goodstype.objects.filter(id=goods.goods_type_id).first()
#     user_id = request.COOKIES.get("user_id")  # 通过cookies找到对应的买家
#     buyer = Buyer.objects.filter(id=int(user_id)).first()  # 找到买家，只有买家存在才有订单
#     if buyer:
#         if request.method=='POST':
#             #开始商品对应的订单,先判断订单号是否存在，如果存在咋重新生成订单号
#             order_id = random.randint(100000, 500000)
#             customer = order(order_id)
#             number=request.POST.get("number")
#             if not customer:
#                 customer=Customer()
#                 customer.date=datetime.now()
#                 customer.order_id=order_id
#                 customer.number=number
#                 customer.buyer_id_id=buyer.id
#                 customer.money=goods_price*int(number)
#                 customer.goods_id_id=id
#                 customer.save()
#                 return HttpResponseRedirect('/buyer/user/')
#     else:
#         return HttpResponseRedirect('/buyer/login/')  # 如果没有买家，返回到登录页面
#     return render(request,"buyer/goods.html",{"goods":goods,"goods_type":goods_type})
#单个商品详情中，立即购买的页面，用户中心
#先做个base页面
def base1(request):
    return render(request,'buyer/base1.html')
#卖家订单详情
#判断这个订单已经存在，不能重复
# def order(order_id):
#     customer=Customer.objects.filter(order_id=order_id).first()
#     return customer
# def user(request):
#     customer_list=Customer.objects.all().order_by("date").reverse()
#     result=[]
#     result1=[]
#     for t in customer_list:
#         if t.order_status:
#             good = []
#             num=t.number
#             goods=t.goods_id
#             for i in range(num):
#                 good.append(goods)
#             lst={
#                 "date":t.date,
#                 "order_id":t.order_id,
#                 "money":t.money,
#                 "goods_list":good,
#                 "customer_id":t.id,
#
#             }
#
#             result.append(lst)
#         else:
#             good = []
#             num = t.number
#             goods = t.goods_id
#             for i in range(num):
#                 good.append(goods)
#             lst1 = {
#                 "date": t.date,
#                 "order_id": t.order_id,
#                 "money": t.money,
#                 "goods_list": good,
#                 "customer_id": t.id,
#             }
#             result1.append(lst1)
#     return render(request,'buyer/user.html',locals())
# #删除订单
# def cut_delete(request,state):
#     if state=="cancel":
#         state_num=0
#     else:
#         state_num=1
#     id=request.GET.get("id")
#     referer = request.META.get("HTTP_REFERER")  # 返回当前请求的来源
#     if id:
#         customer=Customer.objects.filter(id=id).first()
#         if state=="delete":
#             customer.delete()
#         elif state=="restore":
#             customer.order_status = state_num
#             customer.save()
#         else:
#             customer.order_status=state_num
#             customer.save()
#     return HttpResponseRedirect(referer)
# #购物车的功能
# def buyercar(request):
#     pass
#     return render(request,"buyer/buyercar.html",locals())
# Create your views here.
