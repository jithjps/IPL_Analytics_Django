from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.season_analytics, name='season_analytics'),
    url(r'^top-winners/$', views.top4teams_by_wins, name='top_teams'),
    url(r'^toss/$', views.toss_analytics, name='top_toss'),
    url(r'^location/$', views.location_analytics, name='top_locations'),
    url(r'^victory/$', views.victory_analysis, name='top_wins'),
]