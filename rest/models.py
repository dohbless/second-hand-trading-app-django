from django.db import models


# Create your models here.

class Goods(models.Model):
    choices = (("待审核", "待审核"), ("已审核", "已审核"))

    goodsId = models.AutoField(db_column='goodsId',
                            primary_key=True, verbose_name='商品编号')  # Field name made lowercase.
    img = models.TextField(blank=True, null=True, default='', verbose_name='图片')
    bigImg = models.TextField(blank=True, null=True, verbose_name="大图")
    title = models.TextField(blank=True, null=True, default='', verbose_name='标题')
    desc = models.TextField(blank=True, null=True, default='', verbose_name='描述')
    content = models.TextField(blank=True, null=True, default='', verbose_name="内容")
    price = models.FloatField(blank=True, default=0.00, verbose_name='单价')
    status = models.TextField(blank=True, null=True, default='待审核', verbose_name='状态', choices=choices)
    seller = models.TextField(blank=True, null=True, verbose_name="卖家")
    createTime = models.TextField(blank=True, null=True, verbose_name="创建时间")
    modifyTime = models.TextField(blank=True, null=True, verbose_name="更新时间")

    class Meta:
        managed = True
        db_table = 'goods'
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.title + " 单价:" + str(self.price) + " 状态:" + self.status + "(卖家:" + self.seller + ")"

    def to_dict(self):
        return {
            "goodsId": self.goodsId,
            "img": self.img,
            "bigImg": self.bigImg,
            "title": self.title,
            "desc": self.desc,
            "content": self.content,
            "price": self.price,
            "status": self.status,
            "seller": self.seller,
            "createTime": self.createTime,
            "modifyTime": self.modifyTime
        }


class Messages(models.Model):
    id = models.AutoField(db_column='id', primary_key=True, verbose_name='id')
    msgId = models.TextField(db_column='msgId', verbose_name='消息编号')  # Field name made lowercase.
    sendName = models.TextField(db_column='sendName', blank=True,
                                null=True, verbose_name="发送人")  # Field name made lowercase.
    receiveName = models.TextField(db_column='receiveName', blank=True,
                                   null=True, verbose_name="接收人")  # Field name made lowercase.
    content = models.TextField(blank=True, null=True, verbose_name="内容")
    createTime = models.TextField(blank=True, null=True, verbose_name="创建时间")
    modifyTime = models.TextField(blank=True, null=True, verbose_name="更新时间")

    class Meta:
        managed = True
        db_table = 'messages'
        verbose_name = "消息"
        verbose_name_plural = "消息"

    def __str__(self):
        return self.sendName + " 发送消息给:" + self.receiveName + " 内容:" + self.content

    def to_dict(self):
        return {
            "id": self.id,
            "msgId": self.msgId,
            "sendName": self.sendName,
            "receiveName": self.receiveName,
            "content": self.content,
            "createTime": self.createTime,
            "modifyTime": self.modifyTime
        }


class Orders(models.Model):
    choices = (("待收货", "待收货"), ("已完成", "已完成"))

    orderId = models.AutoField(
        db_column='orderId', primary_key=True, verbose_name="订单编号")  # Field name made lowercase.
    img = models.TextField(blank=True, null=True, verbose_name="图片")
    bigImg = models.TextField(blank=True, null=True, verbose_name="大图")
    title = models.TextField(blank=True, null=True, verbose_name="标题")
    status = models.TextField(blank=True, null=True, verbose_name="状态", default="待收货", choices=choices)
    num = models.IntegerField(blank=True, null=True, verbose_name="数量")
    price = models.FloatField(blank=True, null=True, verbose_name="价格")
    money = models.FloatField(blank=True, null=True, verbose_name="总金额")
    seller = models.TextField(blank=True, null=True, verbose_name="卖家")
    buyer = models.TextField(blank=True, null=True, verbose_name="买家")
    address = models.TextField(blank=True, null=True, verbose_name="收货地址")
    phone = models.TextField(blank=True, null=True, verbose_name="收货电话")
    createTime = models.TextField(blank=True, null=True, verbose_name="创建时间")
    modifyTime = models.TextField(blank=True, null=True, verbose_name="更新时间")

    class Meta:
        managed = True
        db_table = 'orders'
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def __str__(self):
        return self.buyer + " 购买商品:" + self.title + " 卖家:" + self.seller + " 总金额:" + str(self.money)

    def to_dict(self):
        return {
            "orderId": self.orderId,
            "img": self.img,
            "bigImg": self.bigImg,
            "title": self.title,
            "status": self.status,
            "num": self.num,
            "price": self.price,
            "money": self.money,
            "seller": self.seller,
            "buyer": self.buyer,
            "address": self.address,
            "phone": self.phone,
            "createTime": self.createTime,
            "modifyTime": self.modifyTime
        }


class User(models.Model):
    userId = models.AutoField(db_column='userId',
                              primary_key=True, verbose_name="用户编号")  # Field name made lowercase.
    account = models.TextField(unique=True, blank=True, null=True, verbose_name="账号")
    pwd = models.TextField(blank=True, null=True, verbose_name="密码")
    role = models.TextField(blank=True, null=True, verbose_name="角色")
    headUrl = models.TextField(db_column='headUrl', blank=True,
                               null=True, verbose_name="头像")  # Field name made lowercase.
    username = models.TextField(blank=True, null=True, verbose_name="昵称")
    money = models.FloatField(blank=True, null=True, verbose_name="总金额")  # TODO 暂不实现金额转账
    createTime = models.TextField(blank=True, null=True, verbose_name="创建时间")
    modifyTime = models.TextField(blank=True, null=True, verbose_name="更新时间")

    class Meta:
        managed = True  # 后台admin显示
        db_table = 'user'
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username + " 账号:" + self.account + " 角色:" + self.role + " 余额:" + str(self.money)

    def to_dict(self):  # 转换为json
        return {"userId": self.userId,
                "account": self.account,
                # "pwd":self.pwd,
                "role": self.role,
                "headUrl": self.headUrl,
                "username": self.username,
                "money": self.money,
                "createTime": self.createTime,
                "modifyTime": self.modifyTime}
