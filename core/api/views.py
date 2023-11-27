from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.api.serializers import RoomSerializer
from core.models import Room

@api_view(["GET"])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(('GET',))
def getRooms(request):
    print("**************************")
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms,many=True)
    print(serializer)
    print(serializer.data)
    
    return Response(serializer.data)

@api_view(('GET',))
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room)
    return Response(serializer.data)
