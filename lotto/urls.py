from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('purchase/', views.purchase, name='purchase'),
    path('purchase/auto/', views.auto_purchase, name='auto_purchase'),
    path('purchase/manual/', views.manual_purchase, name='manual_purchase'),
    path('purchase/complete/', views.purchase_complete, name='purchase_complete'),

    path('my-tickets/', views.my_tickets, name='my_tickets'),

    path('lotto-admin/', views.lotto_admin_home, name='lotto_admin_home'),
    path('lotto-admin/sales/', views.sales_history, name='sales_history'),
    path('lotto-admin/draw/', views.draw_lotto, name='draw_lotto'),
    path('lotto-admin/winning-history/', views.winning_history, name='winning_history'),

    path('check-result/', views.check_result, name='check_result'),
]