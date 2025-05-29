from django.shortcuts import render, redirect
from item.models import Category, Item
from django.db.models import Count
from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    featured_items = Item.objects.filter(is_sold=False).order_by('-created_at')[0:3]
    popular_items = Item.objects.filter(is_sold=False).order_by('-views')[0:3]

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
        'featured_items': featured_items,
        'popular_items': popular_items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })