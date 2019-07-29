from django.db import models
class Buyer(models.Model):
    username=models.CharField(max_length=32,verbose_name="用户名")
    password=models.CharField(max_length=32,verbose_name="密码")
    email=models.EmailField(verbose_name="用户邮箱")
    phone=models.CharField(max_length=32,verbose_name="联系电话",blank=True,null=True)
    connect_address=models.TextField(verbose_name="联系地址",blank=True,null=True)
class Address(models.Model):
    address=models.TextField(verbose_name="收货地址")
    recver=models.CharField(max_length=32,verbose_name="接收人")
    recv_phone=models.CharField(max_length=32,verbose_name="收货人电话")
    post_number=models.CharField(max_length=32,verbose_name="邮编")
    buyer_id=models.ForeignKey(to="Buyer",on_delete=models.CASCADE,verbose_name="用户id")
#创建订单表
class Order(models.Model):
    order_id=models.CharField(max_length=32,verbose_name="订单编号")
    goods_count=models.IntegerField(verbose_name="商品数量")
    order_user=models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name="订单用户")#与买家是多对一的关系
    order_address=models.ForeignKey(to=Address,on_delete=models.CASCADE,verbose_name="订单地址",null=True,blank=True)#与地址是多对一的关系
    order_price=models.FloatField(verbose_name="订单总价")
    order_status=models.IntegerField(default=1,verbose_name="商品订单的状态")
    #商品订单的状态：
                #未支付1
                #待发货2
                #已发货3
                #以收货4
                #退货0
#创建订单详情表
class OrderDetail(models.Model):
    order_id=models.ForeignKey(to=Order,on_delete=models.CASCADE,verbose_name="订单编号")#与订单编号是多对一的关系
    goods_id=models.IntegerField(verbose_name="商品id")
    goods_name=models.CharField(max_length=32,verbose_name="商品名称")
    goods_price=models.FloatField(verbose_name="商品价格")
    goods_number=models.IntegerField(verbose_name="商品购买数量")
    goods_total=models.FloatField(verbose_name="商品总价")
    goods_store=models.IntegerField(verbose_name="店铺id")
    goods_image=models.ImageField(upload_to='buyer/images',default='images/banner01.jpg',verbose_name="商品图片")
# Create your models here.
