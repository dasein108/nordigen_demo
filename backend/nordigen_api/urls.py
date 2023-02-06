from django.urls import path

from . import views
from .config import institution_connected_url_path

urlpatterns = [
    path("connect/<str:institution_id>", views.connect_bank, name="connect"),
    path(
        f"{institution_connected_url_path}/<str:reference_id>",
        views.process_bank,
        name="connected",
    ),
    path("accounts", views.user_accounts, name="user_accounts"),
    path("institutions", views.institutions, name="institutions"),
    path("transactions/<str:account_id>", views.transactions, name="transactions"),
    path("latest_transactions", views.latest_transactions, name="latest_transactions"),
]
