from django.urls import path

from . import views
from .views import (
    TableCreateView,
    TableDeleteView,
    TableDetailView,
    TableListView,
    TableUpdateView,
    TransactionCreateView,
    TransactionDeleteView,
    TransactionDetailView,
    TransactionListCreateView,
    TransactionListView,
    TransactionUpdateView,
    add_category,
    table_detail,
)

urlpatterns = [
    path('tables/', TableListView.as_view(), name='table_list'),
    path('tables/add/', TableCreateView.as_view(), name='table_create'),
    path("tables/<int:pk>/", TableDetailView.as_view(), name="table_detail"),
    path('tables/<int:pk>/edit/', TableUpdateView.as_view(), name='table_update'),
    path('tables/<int:pk>/delete/', TableDeleteView.as_view(), name='table_delete'),
    path('new/', TransactionCreateView.as_view(), name='transaction_create'),
    path("tables/<int:table_id>/", table_detail, name="table_detail"),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/add/<int:table_id>/', TransactionCreateView.as_view(), name='transaction_add'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list"),
    path("transactions/<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path('add-category/', add_category, name='add_category'),
    ]
