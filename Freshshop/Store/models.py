from django.db import models
import django.utils.timezone as timezone

#卖家
class Seller(models.Model):
    username=models.CharField(max_length=32,verbose_name="用户名")
    password=models.CharField(max_length=32,verbose_name="密码")
    nickname=models.CharField(max_length=32,verbose_name="昵称",null=True,
                              blank=True)
    phone=models.CharField(max_length=32,verbose_name="电话",
                           null=True,blank=True)
    email=models.EmailField(verbose_name="邮箱",null=True,blank=True)
    picture=models.ImageField(upload_to="store/images",verbose_name="用户头像",
                              null=True,blank=True)
    address=models.CharField(max_length=32,verbose_name="地址",
                             null=True,blank=True)
    card_id=models.CharField(max_length=32,verbose_name="身份证",
                             null=True,blank=True)
#店铺类型
class StoreType(models.Model):
    store_type=models.CharField(max_length=32,verbose_name='类型名称')
    type_description=models.TextField(verbose_name="类型名称描述")
#店铺
class Store(models.Model):
    store_name=models.CharField(max_length=32,verbose_name="店铺名称")
    store_address=models.CharField(max_length=32,verbose_name="店铺地址")
    store_description=models.TextField(verbose_name="店铺描述")
    store_logo=models.ImageField(upload_to="store/images",verbose_name="店铺logo")
    store_phone=models.CharField(max_length=32,verbose_name="店铺电话")
    store_money=models.FloatField(verbose_name="店铺注册资金")
    user_id=models.IntegerField(verbose_name="店铺主人")#与店铺是一对一关系
    type=models.ManyToManyField(to=StoreType,verbose_name="店铺类型")

    # 商品类型
class Goodstype(models.Model):
    type_name = models.CharField(max_length=32, verbose_name="类型名称")
    type_description = models.TextField(max_length=32, verbose_name="类型描述")
    picture= models.ImageField(upload_to='buyer/images',default='images/banner01.jpg',verbose_name="图片")
#商品
class Goods(models.Model):
    goods_name=models.CharField(max_length=32,verbose_name="商品名称")
    goods_price=models.FloatField(verbose_name="商品价格")
    goods_image=models.ImageField(upload_to="store/images",verbose_name="商品图片")
    goods_number=models.IntegerField(verbose_name="商品数量")
    goods_description= models.TextField(verbose_name="商品的描述")
    goods_date = models.DateField(verbose_name="出厂日期")
    goods_safedate = models.IntegerField(verbose_name="保质期")
    goods_under=models.IntegerField(verbose_name="商品状态",default=1)#设置商品状态，0为下架，1为待售
    goods_type = models.ForeignKey(to=Goodstype, on_delete=models.CASCADE, verbose_name="商品类型id")  # 与商品类型是多对一的关系
    store_id=models.ForeignKey(to=Store,on_delete=models.CASCADE,verbose_name="商品店铺")#与店铺是多对多关系
#商品图片
class GoodImg(models.Model):
    img_address=models.ImageField(upload_to="store/images",verbose_name="图片地址")
    img_description=models.TextField(max_length=32,verbose_name="图片描述")
    good_id=models.ForeignKey(to=Goods,on_delete=models.CASCADE,
                              verbose_name="商品id")#与商品是多对一关系
#增加一个用户订单表
# class Customer(models.Model):
#     buyer_id=models.ForeignKey(to='Buyer.Buyer',on_delete=models.CASCADE,verbose_name="买家id")
#     goods_id=models.ForeignKey(to='Goods',on_delete=models.CASCADE,  verbose_name="商品id")#与商品是多对一的关系
#     address_id=models.ForeignKey(to='Buyer.Address',on_delete=models.CASCADE,verbose_name="收货地址id",default=1)#与收货地址是多对一关系
#     date=models.DateTimeField(verbose_name="下单时间",default=timezone.now)
#     order_id=models.IntegerField(verbose_name="订单号码")
#     number=models.IntegerField(verbose_name="购买产品的数量")
#     money=models.IntegerField(verbose_name="花费的钱数")
#     order_status=models.IntegerField(verbose_name="订单的状态",default=1)#1代表订单在线0代表订单取消，但未删除
#     pay_status=models.IntegerField(verbose_name="支付状态",default=1)#1代表未支付0代表以支付

# #增加一个购物车的表
# class Buycar(models.Model):
#     number=models.IntegerField(verbose_name="添加商品的数量",default=1)
#     goods_id=models.ManyToManyField(to='Goods',verbose_name="商品id")#与商品是多对多的关系
#     buyer_id=models.ForeignKey(to="Buyer.Buyer",on_delete=models.CASCADE,verbose_name="买家id")#与买家是多对一的关系
# Create your models here.
