from django.urls import path, include
from rest import views

urlpatterns = [
    path('', views.index),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('updateUser', views.updateUser, name='updateUser'),
    path('searchGoods', views.searchGoods, name='searchGoods'),
    path('getGoods', views.getGoods, name='getGoods'),
    path('payGoods', views.payGoods, name='payGoods'),
    path('publishGoods', views.publishGoods, name='publishGoods'),
    path('sellerList', views.sellerList, name='sellerList'),
    path('buyerList', views.buyerList, name='buyerList'),
    path('getOrder', views.getOrder, name='getOrder'),
    path('checkOrder', views.checkOrder, name='checkOrder'),
    path('updateOrder', views.updateOrder, name='updateOrder'),
    path('removeOrder', views.removeOrder, name='removeOrder'),
    path('messageList', views.messageList, name='messageList'),
    path('messageHistory', views.messageHistory, name='messageHistory'),
    path('sendMessage', views.sendMessage, name='sendMessage'),
]
