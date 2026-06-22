from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from .models import Trade


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    trades = Trade.objects.filter(user=request.user).order_by('-created_at')[:10]
    total_buy = sum(t.total_value for t in Trade.objects.filter(user=request.user, trade_type=Trade.BUY, status=Trade.COMPLETED))
    total_sell = sum(t.total_value for t in Trade.objects.filter(user=request.user, trade_type=Trade.SELL, status=Trade.COMPLETED))
    context = {
        'user': request.user,
        'trades': trades,
        'total_buy': total_buy,
        'total_sell': total_sell,
    }
    return render(request, 'dashboard.html', context)


@login_required
def place_trade(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol', '').strip().upper()
        trade_type = request.POST.get('trade_type', '')
        quantity_str = request.POST.get('quantity', '')
        price_str = request.POST.get('price', '')

        try:
            quantity = Decimal(quantity_str)
            price = Decimal(price_str)
            if quantity <= 0 or price <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, 'Invalid quantity or price.')
            return redirect('dashboard')

        if not symbol or trade_type not in (Trade.BUY, Trade.SELL):
            messages.error(request, 'Invalid trade details.')
            return redirect('dashboard')

        total_cost = quantity * price
        user = request.user

        if trade_type == Trade.BUY:
            if user.balance < total_cost:
                messages.error(request, f'Insufficient balance. You need ${total_cost:.2f} but have ${user.balance:.2f}.')
                return redirect('dashboard')
            user.balance -= total_cost
            user.save()

        elif trade_type == Trade.SELL:
            user.balance += total_cost
            user.save()

        Trade.objects.create(
            user=user,
            symbol=symbol,
            trade_type=trade_type,
            quantity=quantity,
            price=price,
            status=Trade.COMPLETED,
        )
        messages.success(request, f'{trade_type} order for {quantity} {symbol} @ ${price} executed successfully.')
    return redirect('dashboard')
