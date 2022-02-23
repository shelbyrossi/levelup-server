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
        
        try:
            game = Game.objects.get(pk=pk)
            serializer = CreateGameSerializer(game)
            return Response(serializer.data)
        
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
        
        
        
        

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

        Returns
         Response -- JSON serialized game instance
         """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = Game_Type.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
             maker=request.data["maker"],
             number_of_players=request.data["number_of_players"],
             skill_level=request.data["skill_level"],
             gamer=gamer,
             game_type=game_type
         )
        serializer = CreateGameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """PUT update"""
        game = Game.objects.get(pk=pk)
        game.title = request.data['title']
        game.maker = request.data['maker']
        game.number_of_players = request.data['number_of_players']
        game.skill_level = request.data['skill_level']
        game.game_type = Game_Type.objects.get(pk=request.data['game_type'])
        game.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Delete game"""
        game = Game.objects.get(pk=pk)
        game.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type') 
   
    
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']
        depth = 2