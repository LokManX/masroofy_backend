from django.urls import path
from main.views import *

urlpatterns = [
    # path('users/', UsersList.as_view())
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('incomes/', IncomeListView.as_view(), name='income_list'),
    path('income/create/', IncomeCreateView.as_view(), name='income_create'),
    path('income/<int:id>/', IncomeDetailView.as_view(), name='income_detail'),
    path('income/<int:id>/update/', IncomeUpdateView.as_view(), name='income_update'),
    path('income/<int:id>/delete/', IncomeDeleteView.as_view(), name='income_delete'),
    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('expenses/create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/<int:id>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/<int:id>/update/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('expenses/<int:id>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
]
