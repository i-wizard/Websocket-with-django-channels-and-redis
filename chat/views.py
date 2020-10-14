from django.shortcuts import render
from .models import Thread, ChatMessage
from django.db.models import Q
from .forms import MessageForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def thread(request, username):
    qlookup1 = Q(first__username=request.user.username) & Q(second__username=username)
    qlookup2 = Q(first__username=username) & Q(second__username=request.user.username)
    thread = Thread.objects.filter(qlookup1 | qlookup2).first()
    chat = ChatMessage.objects.filter(thread=thread)
    form = MessageForm()
    context = {
        'thread':thread,
        'chats':chat,
        'form': form
    }
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            ChatMessage.objects.create(user=request.user, message=message, thread=thread)
            print('success')
    return render(request, 'thread.html', context)