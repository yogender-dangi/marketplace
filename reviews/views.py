from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from item.models import Item
from .forms import ReviewForm
from .models import Review
from django.contrib import messages

@login_required
def add_review(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Check if user has already reviewed this item
    if Review.objects.filter(item=item, reviewer=request.user).exists():
        messages.error(request, 'You have already reviewed this item!')
        return redirect('item:detail', pk=item_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('item:detail', pk=item_id)
    else:
        form = ReviewForm()
        
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'item': item
    })

def item_reviews(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    reviews = Review.objects.filter(item=item)
    
    return render(request, 'reviews/item_reviews.html', {
        'item': item,
        'reviews': reviews
    })

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('item:detail', pk=review.item.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'item': review.item,
        'edit_mode': True
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    item_id = review.item.id
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('item:detail', pk=item_id)
    return render(request, 'reviews/confirm_delete.html', {'review': review})
