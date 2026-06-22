from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .mpesa import stk_push
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from .models import Transaction


@login_required
def wallet_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:20]
    context = {
        'user': request.user,
        'transactions': transactions,
    }
    return render(request, 'wallet/wallet.html', context)


@login_required
def deposit(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', ''))
            if amount <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, 'Please enter a valid deposit amount.')
            return redirect('wallet')

        request.user.balance += amount
        request.user.save()
        Transaction.objects.create(user=request.user, transaction_type=Transaction.DEPOSIT, amount=amount)
        messages.success(request, f'${amount:.2f} deposited successfully.')
    return redirect('wallet')


@login_required
def withdraw(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', ''))
            if amount <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, 'Please enter a valid withdrawal amount.')
            return redirect('wallet')

        if request.user.balance < amount:
            messages.error(request, f'Insufficient funds. Your balance is ${request.user.balance:.2f}.')
            return redirect('wallet')

        request.user.balance -= amount
        request.user.save()
        Transaction.objects.create(user=request.user, transaction_type=Transaction.WITHDRAWAL, amount=amount)
        messages.success(request, f'${amount:.2f} withdrawn successfully.')
    return redirect('wallet')
