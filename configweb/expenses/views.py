# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum
from datetime import datetime

def register_view(request):

    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    categories = []
    amounts = []

    for category in ['Food', 'Travel', 'Bills', 'Shopping', 'Other']:

        total_amount = expenses.filter(
            category=category
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        categories.append(category)
        amounts.append(float(total_amount))

    context = {
        'total': total,
        'categories': categories,
        'amounts': amounts,
    }

    return render(request, 'dashboard.html', context)


@login_required
def expense_list(request):

    expenses = Expense.objects.filter(user=request.user)

    month = request.GET.get('month')
    category = request.GET.get('category')

    if month:
        expenses = expenses.filter(date__month=month)

    if category:
        expenses = expenses.filter(category=category)

    return render(request, 'expense_list.html', {
        'expenses': expenses
    })


@login_required
def add_expense(request):

    form = ExpenseForm(request.POST or None)

    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('expense_list')
    return render(request, 'add_expense.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(
        Expense,
        pk=pk,
        user=request.user
    )

    form = ExpenseForm(
        request.POST or None,
        instance=expense
    )

    if form.is_valid():
        form.save()
        return redirect('expense_list')

    return render(request, 'add_expense.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(
        Expense,
        pk=pk,
        user=request.user
    )
    expense.delete()

    return redirect('expense_list')