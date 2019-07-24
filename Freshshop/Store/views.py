import hashlib
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from Store.models import *
from django.core.paginator import Paginator
#设置一个函数，来判断用户存在
def loginuser(username):
    user=Seller.objects.filter(username=username).first()
    return user
#用户注册(卖家)
def register(request):
    result={"status":"error","content":""}
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        if username and password and not loginuser(username):
            seller=Seller()
            seller.username=username
            seller.password=setpassword(password)
            seller.nickname=username
            seller.save()
            return HttpResponseRedirect('/store/login/')
        else:
            result["content"]="用户名密码不能为空"
    return render(request,"store/register.html",locals())
#用户注册ajax校验
def registerajax(request):
    result={"status":"error","content":""}
    username=request.GET.get("username")
    if username:
        user=loginuser(username)
        if user:
            result["content"]="用户名重复，请重新注册"
        else:
            result["content"] = "用户名可以使用"
            result["status"]="success"
    else:
        result["content"] = "用户名|密码不能为空"
    return JsonResponse(result)
#设置密码
def setpassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()
#登录(卖家）
def login(request):

    response=render(request,'store/login.html')
    response.set_cookie('login_form','login_page')
    #登录功能，如果登陆成功跳转首页，如果不成功则跳转登录页面，故设置登录页面的cookies，做判断
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        if username and password:
            user=loginuser(username)
            if user:
                web_password=setpassword(password)
                cookies=request.COOKIES.get("login_form")
                if user.password==web_password and cookies=='login_page':
                    response=HttpResponseRedirect('/store/index/')
                    response.set_cookie("username",username)#设置cookies
                    response.set_cookie("user_id",user.id)#cookies提供用户id用来方便查询
                    request.session["username"]=username
                    #在查询用户店铺是否存在
                    store=Store.objects.filter(user_id=user.id).first()
                    if store:
                        response.set_cookie("has_store",store.id)#设置拥有店铺的cookies
                    else:
                        #因为传进前端的cookies都被转变为了字符串类型，
                        #不能进行布尔运算，故在此值设置为空
                        response.set_cookie("has_store","")
                    return response
    return response
#登录ajax校验
def loginajax(request):
    result = {"status": "error", "content": ""}
    username=request.GET.get("username")
    if username:
        user=loginuser(username)
        if user:
            result["content"] = "用户存在"
            result["status"] = "success"
        else:
            result["content"] = "用户不存在请注册"
    else:
        result["content"] = "用户不能为空"
    return JsonResponse(result)
#封装一个装饰器，来验证店铺已被注册过了
# def registervalid(fun):
#     def inner1(request,*args,**kwargs):
#         user_id = request.COOKIES.get("user_id")
#         if user_id:
#             user_id = int(user_id)
#         else:
#             user_id = 0
#         store = Store.objects.filter(user_id=user_id).first()
#         if store:
#             is_store = 1
#         else:
#             is_store=0
#         return fun(request,{"is_store":is_store})
#     return inner1
#校验装饰器,验证cookies,session，登录
def loginvalid(fun):
    def inner(request,*args,**kwargs):
        c_u=request.COOKIES.get("username")
        s_u=request.session.get("username")
        if c_u and s_u and c_u==s_u:
            user=Seller.objects.filter(username=c_u).first()
            if user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/store/login/')
    return inner


#@registervalid
@loginvalid
def index(request):
    # user_id=request.COOKIES.get("user_id")
    # if user_id:
    #     user_id=int(user_id)
    # else:
    #     user_id=0
    # store=Store.objects.filter(user_id=user_id).first()
    # if store:
    #     is_store=1
    # else:
    #     is_store=0

    return render(request,'store/index.html',locals())
def blank(request):
    return render(request,'store/blank.html')
#店铺注册
def register_store(request):
    type_list=StoreType.objects.all()
    if request.method=='POST':
        post_data=request.POST
        store_name=post_data.get("store_name")
        store_address=post_data.get("store_address")
        store_description=post_data.get("store_description")
        store_logo=request.FILES.get("store_logo")#图片通过这种方式获取信息
        store_phone=post_data.get("store_phone")
        store_money=post_data.get("store_money")
        user_id=int(request.COOKIES.get("user_id"))#用户id通过cookies获取
        type_lst=post_data.getlist("type")
        #开始保存到数据库中去
        store=Store()
        store.store_name=store_name
        store.store_address=store_address
        store.store_description=store_description
        store.store_logo=store_logo
        store.user_id=user_id
        store.store_phone=store_phone
        store.store_money=store_money
        store.save()
        #因为类型和店铺是多对多类型，所以要做遍历处理
        for i in type_lst:
            store_type=StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
        print(post_data)
        return HttpResponseRedirect('/store/index/')
    return render(request,'store/register_store.html',locals())
#在对应的店铺内，添加商品
#@registervalid
@loginvalid
def add_good(request):
    if request.method=='POST':
        post_data = request.POST
        goods_name = post_data.get("goods_name")
        goods_description = post_data.get("goods_description")
        goods_number = post_data.get("goods_number")
        goods_image = request.FILES.get("goods_image")  # 图片通过这种方式获取信息
        goods_date = post_data.get("goods_date")
        goods_price= post_data.get("goods_price")
        goods_safedate=post_data.get("goods_safedate")
        store_id = request.COOKIES.get("has_store")#店铺和商品依赖关系
        goods=Goods()
        goods.goods_name=goods_name
        goods.goods_description=goods_description
        goods. goods_number =  goods_number
        goods.goods_image =goods_image
        goods. goods_date  =  goods_date
        goods.goods_price = goods_price
        goods. goods_safedate = goods_safedate
        goods.save()
        #因为有多对多的关系，随意要多保存一次
        goods.store_id.add(
            Store.objects.get(id=int(store_id))
        )
        goods.save()
        return HttpResponseRedirect('/store/good_list/')
    return render(request,'store/add_good.html',locals())
#商品展示类表
#@registervalid
@loginvalid
def list_good(request):
    keywords=request.GET.get("keywords","")
    page_num=request.GET.get("page_num",1)
    #查询店铺
    store_id=request.COOKIES.get("has_store")
    store=Store.objects.get(id=int(store_id))
    if keywords:
        good_list=store.goods_set.filter(goods_name__contains=keywords)
    else:
        #多对多关系的反向获取商品的列表
        good_list=store.goods_set.all()
    # 分页，把第一个参数是把谁给分页，第2个参数是一页多少东西
    paginator=Paginator(good_list,2)
    # 第几页所包含的东西
    page=paginator.page(int(page_num))
    start=int(page_num)-3
    end=int(page_num)+2
    if start<=0:
        start=0
    page_range=paginator.page_range[start:end]#分页，分了多少页的范围
    return render(request,'store/good_list.html',locals())
#ajax刷新更改价格(还没实现)

#商品的详情
#@registervalid
@loginvalid
def goods(request,is_store=""):
    id=request.GET.get("id")
    goods_data=Goods.objects.filter(id=id).first()
    return render(request,'store/goods.html',locals())
#商品的修改
def goods_update(request):
    id = request.GET.get("id")
    goods_data = Goods.objects.filter(id=id).first()
    if request.method=='POST':
        post_data = request.POST
        goods_name = post_data.get("goods_name")
        goods_description = post_data.get("goods_description")
        goods_number = post_data.get("goods_number")
        goods_image = request.FILES.get("goods_image")  # 图片通过这种方式获取信息
        goods_date = post_data.get("goods_date")
        goods_price = post_data.get("goods_price")
        goods_safedate = post_data.get("goods_safedate")
        goods=Goods.objects.get(id=id)
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_number = goods_number
        goods.goods_date = goods_date
        goods.goods_price = goods_price
        goods.goods_safedate = goods_safedate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect('/store/goods/?id=%s'%goods.id)

    return render(request,'store/goods_update.html',locals())
# Create your views here.
