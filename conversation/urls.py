from django.urls import path

from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
    path('<int:pk>/archive/', views.archive_conversation, name='archive_conversation'),
    path('<int:pk>/unarchive/', views.unarchive_conversation, name='unarchive_conversation'),
]
