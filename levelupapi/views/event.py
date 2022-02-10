"""View module for handling requests about game types"""

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, gamer
from rest_framework.decorators import action

class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        game = request.query_params.get('game', None)

        if game:
            events = events.filter(game_id=game)
         # Set the `joined` property on every event
        for event in events:
    # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
   
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle post requests to events"""
       
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = EventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Update Event"""
        try:
            event = Event.objects.get(pk=pk)
            # event.description = request.data['description']
            # event.time = request.data['time']
            # event.date = request.data['date']
            # event.game = Game.objects.get(pk=request.data['game'])
            # event.save()
            serializer = EventCreateSerializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Delete game"""
        event = Event.objects.get(pk=pk)
        event.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Join an event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        # adds the single gamer to the event
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Leave an event"""
        # detail=false: events/leave
        # detail=true: events/pk/leave
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)

        event.attendees.remove(gamer)
        return Response(status=status.HTTP_204_NO_CONTENT)




class EventSerializer(serializers.ModelSerializer):
    """Serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer',
          'description', 'date', 'time', 'attendees',
          'joined')
        depth = 1

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['description', 'date', 'time', 'game']