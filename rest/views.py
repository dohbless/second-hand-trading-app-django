from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Q
import json
import datetime
from rest.models import *


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def success(data):
    return HttpResponse(json.dumps({"code": 0, "msg": "成功", "data": data}, ensure_ascii=False),
                        content_type="application/json")


def fail(error):  # 错误返回error 不返回数据
    return HttpResponse(json.dumps({"code": -1, "msg": error, "data": None}, ensure_ascii=False),
                        content_type="application/json")


# Create your views here.
def index(request: HttpRequest):
    return HttpResponse(success("It works"), content_type="application/json")


# POST
def register(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
        pwd = request.GET.get("pwd", '')
        role = request.GET.get("role", '')
    else:
        data = json.loads(request.body)
        account = data['account']
        pwd = data['pwd']
        role = data['role']
    user = User.objects.filter(account=account).first()  # 匹配结果
    if user:
        return fail("账号已存在")

    user = User.objects.create(account=account, pwd=pwd, role=role,
                               headUrl='https://b-ssl.duitang.com/uploads/item/201802/12/20180212223628_XUH4f.jpeg',
                               money=0.00,
                               username=account,
                               createTime=now(),
                               modifyTime=now())
    user.save()
    return success(user.to_dict())  #


# POST
def login(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
        pwd = request.GET.get("pwd", '')
    else:
        data = json.loads(request.body)
        account = data['account']
        pwd = data['pwd']
    user = User.objects.filter(account=account, pwd=pwd).first()
    if user:
        return success(user.to_dict())
    else:
        return fail("账号或密码错误")


# POST
def searchGoods(request: HttpRequest):
    if request.method == "GET":
        # account = request.GET.get("account", '')
        searchKey = request.GET.get("searchKey", '')
    else:
        data = json.loads(request.body)
        # account = data['account']
        searchKey = data['searchKey']  # 模糊搜索
    goodsList = Goods.objects.filter(title__contains=searchKey, status="已审核")  # search
    result = []
    for goods in goodsList:
        result.append(goods.to_dict())

    return success(result)


# POST
def getGoods(request: HttpRequest):  # 详情
    if request.method == "GET":
        goodsId = request.GET.get("keyword", '')
    else:
        data = json.loads(request.body)
        # account = data['account']
        goodsId = data['goodsId']
    goods = Goods.objects.filter(goodsId=goodsId, status="已审核").first()
    return success(goods.to_dict())


# POST
def payGoods(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
        goodsId = request.GET.get("goodsId", '')
    else:
        data = json.loads(request.body)
        account = data['account']
        goodsId = data['goodsId']

    goods = Goods.objects.filter(goodsId=goodsId, status="已审核").first()
    if goods is None:
        return fail("商品不存在")
    if goods.seller == account:
        return fail("您发布的商品无法购买")

    order = Orders.objects.create(img=goods.img, bigImg=goods.bigImg, title=goods.title, status="待收货",
                                  num=1, price=goods.price, money=float(goods.price) * 1,
                                  seller=goods.seller,
                                  buyer=account,
                                  address="-",
                                  phone="-", createTime=now(),
                                  modifyTime=now())
    order.save()
    return success(order.to_dict())


# POST
def publishGoods(request: HttpRequest):  # 发布
    data = json.loads(request.body)
    account = data['account']
    title = data['title']
    desc = data['desc']
    content = data['content']
    img = data['img']
    price = data['price']

    goods = Goods.objects.create(img=img, title=title, desc=desc, content=content, price=price, status="待审核",
                                 seller=account, bigImg=img, createTime=now(),
                                 modifyTime=now())
    goods.save()
    return success(goods.to_dict())


# POST
def sellerList(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
    else:
        data = json.loads(request.body)
        account = data['account']

    result = []
    order_list = Orders.objects.filter(seller=account)
    for order in order_list:
        result.append(order.to_dict())
    return success(result)


# POST
def buyerList(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
    else:
        data = json.loads(request.body)
        account = data['account']

    result = []
    order_list = Orders.objects.filter(buyer=account)
    for order in order_list:
        result.append(order.to_dict())
    return success(result)


# POST
def getOrder(request: HttpRequest):
    if request.method == "GET":
        # account = request.GET.get("account", '')
        orderId = request.GET.get("orderId", '')
    else:
        data = json.loads(request.body)
        # account = data['account']
        orderId = data['orderId']

    order = Orders.objects.filter(orderId=orderId).first()
    return success(order.to_dict())


# POST
def checkOrder(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
        orderId = request.GET.get("orderId", '')
    else:
        data = json.loads(request.body)
        account = data['account']
        orderId = data['orderId']

    order = Orders.objects.filter(orderId=orderId, buyer=account).first()
    if order is None:
        return fail("订单不存在")

    order.status = "已完成"
    order.save()
    return success(order.to_dict())


# POST
def updateOrder(request: HttpRequest):
    if request.method == "GET":
        orderId = request.GET.get("orderId", '')
        address = request.GET.get("address", '')
        phone = request.GET.get("phone", '')
    else:
        data = json.loads(request.body)
        orderId = data['orderId']
        address = data['address']
        phone = data['phone']

    order = Orders.objects.filter(orderId=orderId).first()
    if order is None:
        return fail("订单不存在")

    order.address = address
    order.phone = phone
    order.money = 1 * float(order.price)
    order.modifyTime = now()
    order.save()
    return success(order.to_dict())


# POST
def removeOrder(request: HttpRequest):
    if request.method == "GET":
        orderId = request.GET.get("orderId", '')
    else:
        data = json.loads(request.body)
        orderId = data['orderId']

    order = Orders.objects.filter(orderId=orderId).first()
    if order is None:
        return fail("订单不存在")
    order.status = "已取消"
    order.modifyTime = now()
    order.delete()  # 直接删除吧
    print("删除订单:", order)
    return success(order.to_dict())


# POST
def messageList(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
    else:
        data = json.loads(request.body)
        account = data['account']

    # 先查询全部聊天过的人                  # 减号倒序
    messages = Messages.objects.order_by("-modifyTime").filter(Q(sendName=account) | Q(receiveName=account))
    users = set()  # 去重
    for message in messages:
        users.add(message.sendName)
        users.add(message.receiveName)
    if account in users:
        users.remove(account)  # 删除当前用户
    result = []
    for user in users:
        message = Messages.objects.order_by("-modifyTime").filter(
            Q(sendName=account, receiveName=user) | Q(sendName=user, receiveName=account)).first()
        result.append(message.to_dict())
    return success(result)


# POST
def messageHistory(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
        receiver = request.GET.get("receiver", '')
    else:
        data = json.loads(request.body)
        account = data['account']
        receiver = data['receiver']

    messages = Messages.objects.order_by("-modifyTime").filter(
        Q(sendName=account, receiveName=receiver) | Q(sendName=receiver, receiveName=account))
    result = []
    for message in messages:
        result.append(message.to_dict())
    result.reverse()
    return success(result)


# POST
def sendMessage(request: HttpRequest):
    if request.method == "GET":
        msgId = request.GET.get("msgId", '')
        account = request.GET.get("account", '')
        receiver = request.GET.get("receiver", '')
        content = request.GET.get("content", '')
    else:
        data = json.loads(request.body)
        msgId = data['msgId']
        account = data['account']
        receiver = data['receiver']
        content = data['content']

    message = Messages.objects.create(msgId=msgId, sendName=account, receiveName=receiver, content=content,
                                      createTime=now(), modifyTime=now())
    message.save()
    return success(message.to_dict())


# POST
def updateUser(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
        username = request.GET.get("username", '')
        headurl = request.GET.get("headurl", '')  # 注意大小写区分
    else:
        data = json.loads(request.body)
        account = data['account']
        username = data['username']
        headurl = data['headurl']  # 注意大小写区分

    user = User.objects.filter(account=account).first()
    if user is None:
        return fail("账号不存在")
    user.username = username
    user.headUrl = headurl
    user.modifyTime = now()
    user.save()
    return success(user.to_dict())


# POST
def logout(request: HttpRequest):
    if request.method == "GET":
        account = request.GET.get("account", '')
    else:
        data = json.loads(request.body)
        account = data['account']
    user = User.objects.filter(account=account).first()
    if user is None:
        return fail("账号不存在")
    user.modifyTime = now()
    user.save()
    return success(user.to_dict())
