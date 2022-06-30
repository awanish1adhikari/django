from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import *
from .filters import *
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from django.contrib.auth import views as auth_views


def product(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'home': "active"
    }
    return render(request, 'product/product.html', context)


@login_required
@user_only
def order(request, o_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            ins = form.save(commit=False)
            ins.username = request.user
            ins.product_name = Product.objects.get(id=o_id)
            ins.save()
            messages.add_message(request, messages.SUCCESS, 'Order Successfully')
            return redirect('/shopping')
        else:
            messages.add_message(request, messages.ERROR, 'Unable  to Register')
            return render(request, 'product/order.html', {'form': form})
    context = {
        'form': OrderForm
    }
    return render(request, 'product/order.html', context)


def shopping(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'shopping': "active"
    }
    return render(request, 'product/Shopping.html', context)





