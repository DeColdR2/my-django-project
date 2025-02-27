import logging
from decimal import Decimal

from rest_framework import generics, permissions

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CategoryForm, TableForm, TransactionForm
from .models import Table, Transaction
from .serializers import TransactionSerializer
from .utils import get_exchange_rates

logger = logging.getLogger(__name__)


class TableListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'finances/table_list.html'
    context_object_name = 'tables'

    def get_queryset(self):
        return Table.objects.filter(user=self.request.user)


class TableDetailView(LoginRequiredMixin, DetailView):
    model = Table
    template_name = 'finances/table_detail.html'
    context_object_name = 'table'

    def get_queryset(self):
        return Table.objects.filter(user=self.request.user)  # Доступ лише до своїх таблиць

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отримуємо всі транзакції для цієї таблиці
        transactions = self.object.transactions.all()

        # Фільтрація по сумі
        min_amount = self.request.GET.get("min_amount")
        max_amount = self.request.GET.get("max_amount")
        if min_amount:
            transactions = transactions.filter(amount__gte=min_amount)
        if max_amount:
            transactions = transactions.filter(amount__lte=max_amount)
        context["transactions"] = transactions
        return context


def table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id, user=request.user)  # Отримуємо конкретну таблицю
    transactions = table.transactions.all()  # Отримуємо всі транзакції цієї таблиці

    return render(request, "finances/table_detail.html", {
        "table": table,
        "transactions": transactions
    })


class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'finances/table_form.html'
    success_url = reverse_lazy('table_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'finances/table_form.html'
    success_url = reverse_lazy('table_list')


class TableDeleteView(LoginRequiredMixin, DeleteView):
    model = Table
    template_name = 'finances/table_confirm_delete.html'
    success_url = reverse_lazy('table_list')


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # Призначаємо категорію поточному користувачу
            category.save()
            return redirect('some_view')  # Перенаправлення після успішного додавання
    else:
        form = CategoryForm(user=request.user)

    return render(request, 'finances/add_category.html', {'form': form})


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "finances/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        """Фільтрація транзакцій по параметрах GET."""
        queryset = Transaction.objects.filter(table__user=self.request.user)

        # Отримання параметрів
        search_query = self.request.GET.get("search", "").strip()
        min_amount = self.request.GET.get("min_amount")
        max_amount = self.request.GET.get("max_amount")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        logger.debug(
            f"Фільтр: search={search_query}, min={min_amount}, max={max_amount}, start={start_date}, end={end_date}"
        )
        # Фільтр по назві таблиці
        if search_query:
            queryset = queryset.filter(Q(table__name__icontains=search_query))

        # Фільтр по сумі
        if min_amount:
            try:
                min_amount = Decimal(min_amount)
                queryset = queryset.filter(amount__gte=min_amount)
            except ValueError:
                logger.error("Некоректне значення min_amount")

        if max_amount:
            try:
                max_amount = Decimal(max_amount)
                queryset = queryset.filter(amount__lte=max_amount)
            except ValueError:
                logger.error("Некоректне значення max_amount")

        # Фільтр по даті
        if start_date:
            parsed_start_date = parse_date(start_date)
            if parsed_start_date:
                queryset = queryset.filter(date__gte=parsed_start_date)
            else:
                logger.error("Некоректна дата start_date")

        if end_date:
            parsed_end_date = parse_date(end_date)
            if parsed_end_date:
                queryset = queryset.filter(date__lte=parsed_end_date)
            else:
                logger.error("Некоректна дата end_date")

        logger.debug(f"Відфільтровані транзакції: {queryset}")
        return queryset

    def get_context_data(self, **kwargs):
        """Додаємо інформацію про конвертацію валют."""
        context = super().get_context_data(**kwargs)
        transactions = context["transactions"]

        # Отримання курсів валют
        exchange_rates = get_exchange_rates()

        # Загальна сума в різних валютах
        total_amounts = {}
        total_uah = Decimal("0.0")

        for transaction in transactions:
            currency = transaction.currency
            amount = transaction.amount

            if currency not in total_amounts:
                total_amounts[currency] = Decimal("0.0")

            total_amounts[currency] += amount

            # Конвертація у гривні
            if currency in exchange_rates and "UAH" in exchange_rates:
                total_uah += (amount / Decimal(exchange_rates[currency])) * Decimal(exchange_rates["UAH"])

        context["total_amounts"] = total_amounts
        context["total_uah"] = total_uah
        context["exchange_rates"] = exchange_rates

        logger.debug(f"📊 Загальні суми: {total_amounts}, Загальна сума в UAH: {total_uah}")

        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'

    def get_success_url(self):
        return reverse_lazy('transaction_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Передаємо `user` у форму, щоб відфільтрувати категорії."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('transaction_list')


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'finances/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(table__user=self.request.user).prefetch_related("categories")


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(table__user=self.request.user)
