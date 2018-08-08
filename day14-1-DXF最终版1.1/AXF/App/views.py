import os

from django.shortcuts import render, redirect, reverse
from .models import *
from django.http import JsonResponse
import hashlib
import uuid
from AXF.settings import MEDIA_ROOT


######################  首页  ######################

# 首页
def home(request):
    # 轮播
    wheels = MainWheel.objects.all()
    # 导航
    navs = MainNav.objects.all()
    # 必购
    mustbuys = MainMustbuy.objects.all()
    # shop
    shops = MainShop.objects.all()
    shop0 = shops.first()
    shop1_2 = shops[1:3]
    shop3_6 = shops[3:7]
    shop7_10 = shops[7:11]
    # 主要商品
    mainshows = MainShow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shop1_2': shop1_2,
        'shop3_6': shop3_6,
        'shop7_10': shop7_10,
        'mainshows': mainshows,
    }

    return render(request, 'home/home.html', data)


######################  闪购   ######################

# 闪购
def market(request):
    return redirect(reverse('axf:marketwithparams', args=['104749', '0', '0']))

def market_with_params(request, typeid, childcid, sortid):

    # 主分类数据
    foodtypes = FoodType.objects.all()
    # 当前主分类下的商品数据
    goods_list = Goods.objects.filter(categoryid=typeid)

    # 子分类下的商品数据
    if childcid != '0':
        goods_list = goods_list.filter(childcid=childcid)

    # 获取当前主分类下的所有子分类数据
    main_type = foodtypes.get(typeid=typeid)
    childtypenames = main_type.childtypenames
    # print(childtypenames)
    # 全部分类:0#进口水果:103534#国产水果:103533

    child_type_list = childtypenames.split('#')
    child_types = []
    for type in child_type_list:
        # type : 进口水果:103534
        type_list = type.split(":")
        child_types.append(type_list)

    # print(child_types)
    # [['全部分类', '0'], ['进口水果', '103534'], ['国产水果', '103533']]
    ### [{'name':'全部分类', 'id':'0'}, ['进口水果', '103534'], ['国产水果', '103533']]

    # 排序
    # 综合排序
    if sortid == '0':
        pass
    # 销量排序
    elif sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    # 价格降序
    elif sortid == '2':
        goods_list = goods_list.order_by('-price')
    # 价格升序
    elif sortid == '3':
        goods_list = goods_list.order_by('price')

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': typeid,
        'child_types': child_types,
        'childcid': childcid,
    }
    return render(request, 'market/market.html', data)



######################  我的   ######################

# 我的
def mine(request):

    data = {
        'name': '',
        'icon': ''
    }

    # session
    userid = request.session.get('userid', 0)

    # 根据userid来获取对应用户的信息
    users = User.objects.filter(id=userid)
    if users.exists():
        data['name'] = users.first().name
        data['icon'] = users.first().icon

    return render(request, 'mine/mine.html', data)


# 注册
def register(request):
    return render(request, 'user/register.html')


# 注册操作
def register_handle(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        icon = request.FILES.get('file')

        # 服务器端也要做验证
        if len(username) < 6:
            data = {
                'status': 0,
                'msg': '用户名长度至少为6位',
            }
            return render(request, 'user/register.html', data)

        # 注册，加入数据库表中
        user = User()
        user.name = username
        user.passwd = password # my_md5(password)  # 加密后存入数据库
        user.email = email
        if icon:

            # 图片名称
            icon_name = generate_iconname() + '.png'

            # 将图片名称存入数据库
            user.icon = '/uploads/icon/' + icon_name

            #将图片存入本地
            file_path = os.path.join(MEDIA_ROOT, icon_name)
            with open(file_path, 'ab') as f:
                for part in icon.chunks():
                    f.write(part)
                    f.flush()

        user.save()

        # 注册成功后自动登录
        # session
        request.session['userid'] = user.id

        # 自动跳转到‘我的’页面
        return redirect(reverse('axf:mine'))

    return redirect(reverse('axf:register'))


# md5加密
def my_md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()

# 生成随机图片名称
def generate_iconname():
    u = str(uuid.uuid4())
    return my_md5(u)


# 验证用户名是否存在
def check_username(request):
    if request.method == "GET":
        username = request.GET.get('username')

        # 检测用户表中是否存在该用户
        users = User.objects.filter(name=username)
        if users.exists():
            return JsonResponse({'status':0, 'msg':'用户名已存在!'})
        else:
            return JsonResponse({'status':1, 'msg':'用户名可以使用!'})

    return JsonResponse({'status': -1, 'msg': '请求方式错误'})


# 退出登录
def logout(request):
    # session
    del request.session['userid']
    request.session.flush()

    return redirect(reverse('axf:mine'))


# 登录页面
def login(request):
    return render(request, 'user/login.html')


# 登录操作
def login_handle(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # password = my_md5(password)

        # 登录: 去匹配数据库中的用户和密码是否存在
        users = User.objects.filter(name=username, passwd=password)
        if users.exists():
            # 登录成功
            request.session['userid'] = users.first().id

            # 返回‘我的’页面
            return redirect(reverse('axf:mine'))
        else:
            # 登录失败
            data = {
                'status': 0,
                'msg': '用户名或密码错误！'
            }
            return render(request, 'user/login.html', data)

    data = {
        'status': -1,
        'msg': '请求方式错误！'
    }
    return render(request, 'user/login.html', data)


######################  购物车   ######################
# 购物车
def cart(request):

    # 从session中获取userid
    userid = request.session.get('userid', 0)

    # 如果没有登录，则跳转到登录页面
    if not userid:
        return redirect(reverse('axf:login'))

    # 获取当前登录用户的所有购物车的数据
    carts = Cart.objects.filter(user_id=userid)
    data = {
        'carts': carts,
    }
    return render(request, 'cart/cart.html', data)


# 加入购物车
def cart_add(request):

    data = {
        'status': 1,
        'msg': 'ok',
    }

    # 判断用户是否已经登录
    userid = request.session.get('userid')
    if not userid:
        # 未登录
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        # 已登录
        if request.method == "GET":
            goodsid = request.GET.get('goodsid')
            num = request.GET.get('num')

            # 先判断该商品是否已经存在于该用户的购物车中
            # 1, 如果商品已经存在购物车中，则将数量增加
            # 2, 如果不存在则将该商品加入到当前用户的购物车中

            carts = Cart.objects.filter(user_id=userid, goods_id=goodsid)

            # 1, 如果商品已经存在购物车中，则将数量增加
            if carts.exists():
                cart = carts.first()
                cart.num += int(num)    # 数量增加
                cart.save()

            # 2, 如果不存在则将该商品加入到当前用户的购物车中
            else:
                # 加入购物车
                cart = Cart()
                cart.user_id = userid
                cart.goods_id = goodsid
                cart.num = int(num)
                cart.save()

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误!'

    return JsonResponse(data)


# 数量+
def cart_num_add(request):

    data = {
        'status': 1,
        'msg': 'ok',
    }

    # 判断是否登录
    userid = request.session.get('userid')
    # 如果未登录
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        if request.method == "GET":
            cartid = request.GET.get('cartid')

            # 数量+
            carts = Cart.objects.filter(id=cartid)
            if carts.exists():
                cart = carts.first()
                cart.num += 1
                cart.save()

                # 把最新的num返回给浏览器
                data['num'] = cart.num

            else:
                data['status'] = -1
                data['msg'] = '购物车中没有该商品'

        else:
            data['status'] = -2
            data['msg'] = '请求方式错误!'

    return JsonResponse(data)

    # 逻辑


# 数量-
def cart_num_reduce(request):

    data = {
        'status': 1,
        'msg': 'success',
    }

    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')

            # 数量-
            carts = Cart.objects.filter(id=cartid)
            if carts.exists():
                cart = carts.first()
                if cart.num > 1:
                    cart.num -= 1
                cart.save()

                data['num'] = cart.num

            else:
                data['status'] = -1
                data['msg'] = '购物车中不存在该商品'
        else:
            data['status'] = -2
            data['msg'] = '请求方式错误!'

    return JsonResponse(data)


# 删除
def cart_del(request):

    data = {
        'status': 1,
        'msg': 'success',
    }

    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')

            # 删除
            Cart.objects.filter(id=cartid).delete()

        else:
            data['status'] = -2
            data['msg'] = '请求方式错误!'

    return JsonResponse(data)


# 勾选/取消勾选
def cart_select(request):

    data = {
        'status': 1,
        'msg': 'success',
    }

    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        if request.method == 'POST':
            cartid = request.POST.get('cartid')

            # 勾选/取消勾选
            carts = Cart.objects.filter(id=cartid)
            if carts.exists():
                cart = carts.first()
                cart.is_select = not cart.is_select  # 将选中状态取反
                cart.save()

                data['select'] = cart.is_select

            else:
                data['status'] = -1
                data['msg'] = '购物车中不存在该商品'

        else:
            data['status'] = -2
            data['msg'] = '请求方式错误!'

    return JsonResponse(data)


# 全选/全不选
def cart_allselect(request):

    data = {
        'status': 1,
        'msg': 'success',
    }

    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        if request.method == 'POST':
            action = request.POST.get('action')
            # unselects = request.POST.get('unselects', '')
            # unselect_list = unselects.split('#')
            # print('action:', action)  # 'true'
            # print('unselects:', unselects)  # '9#15'

            # 要'取消全选'
            if action == 'true':
                Cart.objects.filter(user_id=userid).update(is_select=False)

            # 要 ‘全选’
            else:
                # Cart.objects.filter(id__in=unselect_list).update(is_select=True)
                Cart.objects.filter(user_id=userid, is_select=False).update(is_select=True)

        else:
            data['status'] = -2
            data['msg'] = '请求方式错误!'

    return JsonResponse(data)



######################  订单   ######################

# 订单
def order(request, oid):
    order = Order.objects.get(id=oid)
    return render(request, 'order/order.html', {'order': order})


# 添加订单
def order_add(request):
    data = {
        'status': 1,
        'msg': 'success',
    }

    # 判断是否登录
    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        if request.method == 'POST':

            # 下单：给订单表添加一条数据
            #      给订单商品表添加多个商品
            order = Order()
            # 订单编号：后端生成,随机且唯一
            order.order_id = my_md5(str(uuid.uuid4()))
            order.user_id = userid
            order.save()

            # 将当前用户的购物车中选中的商品添加到订单商品表中
            carts = Cart.objects.filter(user_id=userid, is_select=True)

            total = 0  # 订单总价
            for cart in carts:
                # 订单商品
                order_goods = OrderGoods()
                order_goods.goods_id = cart.goods_id
                order_goods.num = cart.num
                order_goods.order_id = order.id
                order_goods.price = cart.goods.price
                order_goods.save()

                total += order_goods.num * order_goods.price

            # 订单总价
            order.order_price = total
            order.save()

            # 生成订单成功后要删除购物车对应的商品
            carts.delete()

            # 将订单的id返回
            data['orderid'] = order.id

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 修改订单状态
def order_change_status(request):
    data = {
        'status': 1,
        'msg': 'success',
    }

    # 判断是否登录
    userid = request.session.get('userid')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'

    else:
        if request.method == 'POST':
            orderid = request.POST.get('orderid')
            status = request.POST.get('status')

            # 修改订单状态
            Order.objects.filter(id=orderid).update(order_status=status)

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 待付款订单
def order_unpay(request):

    # 判断是否登录
    userid = request.session.get('userid')
    if not userid:
        return redirect(reverse('axf:login'))

    # 获取所有未付款订单
    orders = Order.objects.filter(user_id=userid, order_status='0')
    return render(request, 'order/order_unpay.html', {'orders': orders})


# 待收货订单
def order_unreceive(request):

    # 判断是否登录
    userid = request.session.get('userid')
    if not userid:
        return redirect(reverse('axf:login'))

    # 获取所有未付款订单
    orders = Order.objects.filter(user_id=userid, order_status='1')
    return render(request, 'order/order_unreceive.html', {'orders': orders})




