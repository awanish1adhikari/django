from django.shortcuts import render, redirect
from accounts.auth import admin_only
from product.models import *
from product.forms import *
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os


@login_required
@admin_only
def admin_dashboard(request):
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    users = User.objects.all()
    user_count = users.filter(is_staff=0).count()
    admin_count = users.filter(is_staff=1).count()
    context = {
        'order': order_count,
        'product': product_count,
        'user': user_count,
        'admin': admin_count,
        'home': 'active',
    }
    return render(request, 'admins/admin_dashboard.html', context)


@login_required
@admin_only
def product(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product Added Successfully')
            return redirect('/admin/products')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add Product')
            return render(request, 'admins/Products.html', {'form': form})
    context = {
        'products': products,
        'product': 'active',
        'form': ProductForm
    }
    return render(request, 'admins/Products.html', context)


def delete_product(request, p_id):
    product = Product.objects.get(id=p_id)
    os.remove(product.image_url.path)
    product.delete()
    return redirect("/admin/products")


@login_required
@admin_only
def update_product(request, p_id):
    products = Product.objects.all()
    instance = Product.objects.get(id=p_id)
    prev_image = instance.image_url.path
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            new_image = instance.image_url.path
            if prev_image != new_image:
                os.remove(prev_image)
            messages.add_message(request, messages.SUCCESS, 'product updated Successfully')
            return redirect('/admin/products')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update product')
            return render(request, "admins/Products.html", {'form': ProductForm(instance=instance), "products": products, "Products": "active"})
    context = {'form': ProductForm(instance=instance), "products": products, "product": "active"}
    return render(request, "admins/Products.html", context)


@login_required
@admin_only
def order(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'order': 'active',
    }
    return render(request, 'admins/Order.html', context)


def delete_order(request, o_id):
    order = Order.objects.get(id=o_id)
    order.delete()
    return redirect("/admin/order")




@login_required
@admin_only
def get_user(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles,
        'user': 'active'
    }
    return render(request, 'admins/Users.html', context)


@login_required
@admin_only
def update_user_to_admin(request, user_id):
    userprofile = Profile.objects.get(id=user_id)
    userprofile.staff = True
    userprofile.save()

    user = User.objects.get(username=userprofile.username)
    user.is_staff = True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'User has been updated to Admin')
    return redirect('/admin')


@login_required
@admin_only
def register_user_admin(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user,
                                   username=user.username)
            messages.add_message(request, messages.SUCCESS, 'User Registered Successfully')
            return redirect('/admin')
        else:
            messages.add_message(request, messages.ERROR, 'Please provide correct details')
            return render(request, 'admins/register.html', {'form': form})
    context = {
        'form': UserCreationForm
    }
    return render(request, 'admins/register.html', context)
