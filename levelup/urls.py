from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from rest_framework import routers
from levelupapi.views.event import EventView
from levelupapi.views.event_gamer import EventGamerView
from levelupapi.views.game_type import GameTypeView
from levelupapi.views.gamer import GamerView
from levelupapi.views.games import GamesView





router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', GameTypeView, 'gametype')

router.register(r'games', GamesView, 'game')

router.register(r'gamers', GamerView, 'gamer')

router.register(r'eventgamers', EventGamerView, 'eventgamer')

router.register(r'events', EventView, 'event')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('levelupreports.urls')),
]
