"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event_Gamer



class EventGamerView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        
        event_gamer = Event_Gamer.objects.get(pk=pk)
        serializer = Event_GamerSerializer(event_gamer)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        event_gamer = Event_Gamer.objects.all()
        serializer = Event_GamerSerializer(event_gamer, many=True)
        return Response(serializer.data)
    
    
    
class Event_GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event_Gamer
        fields = ('id', 'event', 'gamer')
        depth = 1