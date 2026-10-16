from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.utils import timezone
from .models import Account, Card, Transaction, Client


def index(request):
    return render(request, 'index.html')


def account_list(request):
    accounts = Account.objects.select_related('client').all().order_by('id')
    return render(request, 'account_list.html', {'accounts': accounts})


def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk)
    transactions = account.transaction_set.all().order_by('-date')
    try:
        card = account.card
    except Card.DoesNotExist:
        card = None
    return render(request, 'account_detail.html', {
        'account': account,
        'transactions': transactions,
        'card': card,
    })


def transaction_list(request):
    date = request.GET.get('date', '')
    transactions = Transaction.objects.select_related(
        'account', 'account__client'
    ).order_by('-date')
    if date:
        transactions = transactions.filter(date__date=date)
    return render(request, 'transaction_list.html', {
        'transactions': transactions,
        'date': date,
    })


def transaction_create(request):
    accounts = Account.objects.select_related('client').all()

    if request.method == 'POST':
        account = get_object_or_404(Account, pk=request.POST.get('account'))
        amount = Decimal(request.POST.get('amount'))
        type_ = request.POST.get('type')

        max_id = Transaction.objects.aggregate(models.Max('id'))['id__max'] or 0

        Transaction.objects.create(
            id=max_id + 1,
            date=timezone.now(),
            amount=amount,
            type=type_,
            account=account,
        )

        if type_ == 'пополнение':
            account.balance = account.balance + amount
        else:
            account.balance = account.balance - amount
        account.save()

        return redirect('account_detail', pk=account.id)

    return render(request, 'transaction_create.html', {'accounts': accounts})

def account_create(request):
    clients = Client.objects.all()

    if request.method == 'POST':
        client = get_object_or_404(Client, pk=request.POST.get('client'))

        max_id = Account.objects.aggregate(models.Max('id'))['id__max'] or 0

        Account.objects.create(
            id=max_id + 1,
            number=request.POST.get('number'),
            type=request.POST.get('type'),
            balance=Decimal(request.POST.get('balance') or '0'),
            currency=request.POST.get('currency') or 'RUB',
            client=client,
        )

        return redirect('account_list')

    return render(request, 'account_create.html', {'clients': clients})