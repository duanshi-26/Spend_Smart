from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('expenses', views.expenses, name='expenses'),
    path('expenses/<str:id>', views.delete_expense, name='delete_expense'),
]
