from django.urls import path
from Store.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/',index),
    path('ra/',registerajax),
    path('la/',loginajax),
    path('blank/',blank),
    path('register_store/',register_store),
    path('add_good/',add_good),
    path('good_list/',list_good),
    path('goods/',goods),
    path('goods_update/',goods_update),
]
