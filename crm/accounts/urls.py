from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('register/',views.register, name ='register'),
    path('login/',views.loginPage, name ='login'),
    path('logout/',views.logoutUser, name ='logout'),
    path('profile/',views.account_settings, name = 'profile'),

    path('user/',views.userPage, name = 'user-page'),

    path('',views.home,name = 'home'),
    path('product/',views.product, name = 'product'),
    path('customer/<str:pk>/',views.customer, name = 'customer'),
    path('create_order/<str:pk>/',views.create_order, name = 'create_order'),
    path('update_order/<str:pk>/',views.update_order, name = 'update_order'),
    path('delete_order/<str:pk>/',views.delete_order, name = 'delete_order'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset.html'), name = "reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_sent.html'),name = "password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset_form.html'),name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_done.html'), name ="password_reset_complete"),

]
