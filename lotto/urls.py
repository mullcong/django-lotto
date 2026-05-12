from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("buy/manual/", views.buy_manual, name="buy_manual"),
    path("buy/auto/", views.buy_auto, name="buy_auto"),
    path("tickets/", views.my_tickets, name="my_tickets"),
    path("check/", views.check_result, name="check_result"),

    path("manager/", views.admin_dashboard, name="admin_dashboard"),
    path("manager/draw/", views.draw_lotto, name="draw_lotto"),
    path("manager/sales/", views.sales_history, name="sales_history"),
    path("manager/winning/", views.winning_history, name="winning_history"),
]