from django.shortcuts import render, redirect
from .models import Room, Message

# Create your views here.

def home_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        room = request.POST["room"]
        try:
            existing_room = Room.objects.get(room_name=room)
        except Room.DoesNotExist:
            r = Room.objects.create(room_name=room)
        return redirect("in_game", room_name = room, username = username)
    return render(request, 'home/main.html')

def in_game(request, room_name, username):

    # Get the existing room
    existing_room = Room.objects.get(room_name=room_name)

    # Check if the room is full
    if existing_room.current_members >= existing_room.max_members:
        # Redirect to a 'room full' page or return an error message
        return render(request, 'home/room_full.html', {'room_name': room_name})

    get_message = Message.objects.filter(room=existing_room)
    context = {
        "messages":get_message,
        "username":username,
        "room_name":existing_room.room_name,
    }
    return render(request, 'board/lobby.html', context)
