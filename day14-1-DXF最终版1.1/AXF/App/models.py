from django.db import models


# 首页
class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

    class Meta:
        abstract = True  # 抽象类, 不会生成表


# 首页-轮播
class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


# 首页-导航
class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'


# 首页-必购
class MainMustbuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'


# 首页-商品
class MainShop(Main):
    class Meta:
        db_table = 'axf_shop'


'''
insert into axf_mainshow(
    trackid,name,img,
    categoryid,brandname,
    img1,childcid1,productid1,longname1,price1,marketprice1,
    img2,childcid2,productid2,longname2,price2,marketprice2,
    img3,childcid3,productid3,longname3,price3,marketprice3) 
    
  values(
    "21782","优选水果","1Q.jpg",
    "103532","爱鲜蜂",
    "img01.jpg","103533","118824","爱鲜蜂·特小凤西瓜1.5-2.5kg/粒","25.80","25.8",
    "img02.jpg","103534","116950","蜂觅·越南直采红心火龙果350-450g/盒","15.3","15.8",
    "img03.jpg","103533","118826","爱鲜蜂·海南千禧果400-450g/盒","9.9","13.8");
'''
# 主要商品
class MainShow(Main):
    categoryid = models.CharField(max_length=20)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=20)
    productid1 = models.CharField(max_length=20)
    longname1 = models.CharField(max_length=40)
    price1 = models.CharField(max_length=20)
    marketprice1 = models.CharField(max_length=20)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=20)
    productid2 = models.CharField(max_length=20)
    longname2 = models.CharField(max_length=40)
    price2 = models.CharField(max_length=20)
    marketprice2 = models.CharField(max_length=20)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=20)
    productid3 = models.CharField(max_length=20)
    longname3 = models.CharField(max_length=40)
    price3 = models.CharField(max_length=20)
    marketprice3 = models.CharField(max_length=20)

    class Meta:
        db_table = 'axf_mainshow'


'''
insert into axf_foodtypes(
    typeid,typename,childtypenames,typesort) 
  values("104749","热销榜","全部分类:0",1),
        ("104747","新品尝鲜","全部分类:0",2),
        ("103549","饮料酒水","全部分类:0#饮用水:103550#茶饮/咖啡:103554#功能饮料:103553#酒类:103555#果汁饮料:103551#碳酸饮料:103552#整箱购:104503#植物蛋白:104489#进口饮料:103556",6)
  
'''

# 商品分类
class FoodType(models.Model):
    typeid = models.CharField(max_length=20)
    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'


'''
insert into axf_goods(
    productid,productimg,productname,productlongname,
    isxf,pmdesc,specifics,price,marketprice,categoryid,
    childcid,childcidname,dealerid,storenums,productnum) 
  values("11951","img.png","","乐吧薯片鲜虾味50.0g",
    0,0,"50g",2.00,2.500000,103541,
    103543,"膨化食品","4858",200,4);
'''

# 商品数据
class Goods(models.Model):
    productid = models.CharField(max_length=20)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=50)
    productlongname = models.CharField(max_length=200)

    isxf = models.BooleanField(default=False)
    pmdesc = models.IntegerField()
    specifics = models.CharField(max_length=20)
    price = models.FloatField()
    marketprice = models.FloatField()
    categoryid = models.CharField(max_length=20)

    childcid = models.CharField(max_length=20)
    childcidname = models.CharField(max_length=40)
    dealerid = models.CharField(max_length=40)
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'


# 用户
class User(models.Model):
    name = models.CharField(max_length=20, unique=True)
    passwd = models.CharField(max_length=40)
    email = models.EmailField()
    icon = models.CharField(max_length=200, default='')
    gender = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


# 购物车
class Cart(models.Model):
    user = models.ForeignKey(User)
    goods = models.ForeignKey(Goods)
    num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)


# 订单
class Order(models.Model):
    order_id = models.CharField(max_length=32, unique=True)
    order_create = models.DateTimeField(auto_now_add=True)
    order_price = models.FloatField(default=0)
    user = models.ForeignKey(User)
    # 订单状态: 0表示未支付, 1表示待收货, 2表示待评价, 3表示交易完成
    order_status = models.CharField(max_length=10, default=0)


# 订单商品
class OrderGoods(models.Model):
    goods = models.ForeignKey(Goods)
    num = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)
    order = models.ForeignKey(Order)








