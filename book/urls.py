# urls.py
from django.urls import path
from .views import book_list, book_spider

urlpatterns = [
    path('book_list/', book_list, name='book_list'),
    path('book_spider/', book_spider, name='book_spider'),

]
