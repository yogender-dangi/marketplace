from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:item_id>/', views.add_review, name='add_review'),
    path('item/<int:item_id>/', views.item_reviews, name='item_reviews'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
