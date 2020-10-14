from django.contrib import admin
from .models import *

class ChatAdmin(admin.TabularInline):
    model = ChatMessage
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatAdmin]
    class Meta:
        model: Thread
admin.site.register(Thread, ThreadAdmin)
