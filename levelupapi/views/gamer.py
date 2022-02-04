"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer



class GamerView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        
        gamer = Gamer.objects.get(pk=pk)
        serializer = GamerSerializer(gamer)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        gamer = Gamer.objects.all()
        serializer = GamerSerializer(gamer, many=True)
        return Response(serializer.data)
    
    
    
class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Gamer
        fields = ('id','user', 'bio')
        depth = 1