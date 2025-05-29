from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import NewItemForm, EditItemForm
from .models import Category, Item

def items(request):
    query = request.GET.get('query', '')
    category_id = int(request.GET.get('category', 0))
    sort_by = request.GET.get('sort', '-created_at')  # Default sort by newest
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    # Sorting
    if sort_by == 'price_low':
        items = items.order_by('price')
    elif sort_by == 'price_high':
        items = items.order_by('-price')
    elif sort_by == 'views':
        items = items.order_by('-views')
    elif sort_by == 'name':
        items = items.order_by('name')
    else:  # default to newest
        items = items.order_by('-created_at')

    # Only filter by category if a specific category is selected
    if category_id and category_id != 0:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    user_wishlist = []
    if request.user.is_authenticated:
        user_wishlist = list(request.user.wishlist.values_list('id', flat=True))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': category_id,
        'sort_by': sort_by,
        'user_wishlist': user_wishlist,
    })

@login_required
def toggle_wishlist(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.user in item.wishlisted_by.all():
        item.wishlisted_by.remove(request.user)
        messages.success(request, 'Item removed from wishlist')
    else:
        item.wishlisted_by.add(request.user)
        messages.success(request, 'Item added to wishlist')
    
    return redirect('item:detail', pk=pk)

@login_required
def wishlist(request):
    items = request.user.wishlist.all()
    return render(request, 'item/wishlist.html', {
        'items': items
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    # Increment view counter
    item.views += 1
    item.save()

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'is_wishlisted': request.user in item.wishlisted_by.all() if request.user.is_authenticated else False,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')