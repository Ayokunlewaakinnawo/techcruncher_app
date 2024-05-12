from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('<slug:slug>/', news, name="news_content"),
    #path('get-response/', get_response, name='get_response'),
]