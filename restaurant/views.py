from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Category, Order, OrderItem
from .forms import ReservationForm, OrderForm
from django.urls import reverse
from django.db import transaction
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm

def home(request):
    return HttpResponse("Добро пожаловать в ресторан!")
# Простая витрина меню
def menu(request):
    categories = Category.objects.all()
    items = MenuItem.objects.filter(available=True)
    return render(request, 'restaurant/menu.html', {'categories': categories, 'items': items})

def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'restaurant/item_detail.html', {'item': item})

# Cart реализуем в сессии
def _get_cart(request):
    return request.session.setdefault('cart', {})

def cart_view(request):
    cart = _get_cart(request)
    cart_items = []
    total = Decimal('0')
    for pk, qty in cart.items():
        try:
            item = MenuItem.objects.get(pk=int(pk))
        except MenuItem.DoesNotExist:
            continue
        line_total = item.price * int(qty)
        total += line_total
        cart_items.append({'item': item, 'quantity': int(qty), 'line_total': line_total})
    return render(request, 'restaurant/cart.html', {'cart_items': cart_items, 'total': total})

def cart_add(request, pk):
    cart = _get_cart(request)
    cart[str(pk)] = int(cart.get(str(pk), 0)) + 1
    request.session.modified = True
    return redirect('cart')

def cart_remove(request, pk):
    cart = _get_cart(request)
    if str(pk) in cart:
        del cart[str(pk)]
        request.session.modified = True
    return redirect('cart')

@transaction.atomic
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('menu')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer_name=form.cleaned_data['name'],
                customer_phone=form.cleaned_data['phone'],
            )
            total = Decimal('0')
            for pk, qty in cart.items():
                item = MenuItem.objects.get(pk=int(pk))
                line_total = item.price * int(qty)
                OrderItem.objects.create(order=order, menu_item=item, quantity=int(qty), price=item.price)
                total += line_total
            order.total = total
            order.save()
            # очистить корзину
            request.session['cart'] = {}
            return redirect('reservation_success')
    else:
        form = OrderForm()
    return render(request, 'restaurant/checkout.html', {'form': form})

def order_success(request):
    return render(request, 'restaurant/reservation_success.html')

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'restaurant/reservation_success.html')
    else:
        form = ReservationForm()
    return render(request, 'restaurant/reservation_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'restaurant/register.html', {'form': form})

