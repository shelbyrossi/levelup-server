"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models.game_type import Game_Type
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError



class GamesView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
    """
        gamer = Gamer.objects.get(user=request.auth.user)
        try:
         serializer = CreateGameSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save(gamer=gamer)
         return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
         return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']
        depth = 2