from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add-expenses', views.add_expenses, name='add-expenses'),
    path('edit-expense/<str:id>', views.edit_expense, name='edit-expense'),
]