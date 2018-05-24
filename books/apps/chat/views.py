from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import Room


# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name_json):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(name=room_name_json)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = room.messages.order_by('timestamp')[:50]

    return render(
        request,
        'chat/room.html',
        {
            'root_name_json': mark_safe(json.dumps(room.name)),
            'messages': messages,
            'handle':mark_safe(json.dumps('zkerpy')),
        }
    )
