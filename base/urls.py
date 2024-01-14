from django.urls import path

from .views import (
    RegisterUserView,
    LoginUserView,
    AddExpenseView
    )

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("login/", LoginUserView.as_view(), name='register'),
    
    path("add-expense/", AddExpenseView.as_view(), name='add-expense'),
    ]