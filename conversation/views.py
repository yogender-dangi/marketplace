from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage
from django.contrib import messages
from django.db.models import Q

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members=request.user).exclude(archived_by=request.user)

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)
    # Mark all messages as read for this user
    conversation.conversationmessage_set.filter(~Q(created_by=request.user), read=False).update(read=True)
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()
    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })

@login_required
def archive_conversation(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)
    conversation.archived_by.add(request.user)
    messages.success(request, 'Conversation archived.')
    return redirect('conversation:inbox')

@login_required
def unarchive_conversation(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)
    conversation.archived_by.remove(request.user)
    messages.success(request, 'Conversation unarchived.')
    return redirect('conversation:inbox')