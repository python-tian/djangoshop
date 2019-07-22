import hashlib
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from Store.models import *
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
                    response.set_cookie("username",username)
                    request.session["username"]=username
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
@loginvalid
def index(request):
    return render(request,'store/index.html')
def blank(request):
    return render(request,'store/blank.html')
# Create your views here.
