# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
from django.http.response import HttpResponse,JsonResponse
import json
from django.db.models import Max, Count, F, Case, CharField, When
from django.views.decorators.csrf import csrf_exempt
from ipl_data.models import Season, Match, Delivery



# Create your views here.
def season_analytics(request):
    seasons = Season.objects.all().order_by('-id')
    return render(request, "ipl_data/season_analytics.html", {'seasons': seasons})


@csrf_exempt
def  top4teams_by_wins(request): 
    season_id = request.POST.get('season_id')   
    # Top 4 teams in terms of wins
    winner_result   = Match.objects.filter(season_id=season_id).\
                                    exclude(result = 'no result').\
                                    values('winner').\
                                    annotate(win_count = Count('winner')).\
                                    order_by('-win_count')
    if not winner_result:
        return JsonResponse({"response":"No data available"})
    top_4_win_count = winner_result.values_list('win_count',flat=True).distinct().order_by('-win_count')[:4]
    win_count4      = list(top_4_win_count)[-1]
    top_4_teams     = winner_result.filter(win_count__gte = win_count4).order_by('-win_count')
    
    # Top Team by wincounts 
    top_win_count   = top_4_win_count[0]
    top_team        = winner_result.filter(win_count = top_win_count )
    top_team_names  = top_team.values_list('winner',flat = True)

    # Top team highest victory locations
    win_venues          = Match.objects.filter(season_id = season_id, winner__in =  top_team_names).\
                                        values('winner','venue').\
                                        annotate(venue_count = Count('venue')).\
                                        order_by('-venue_count')
    top_win_venue_data = []
    for top_team_name in top_team_names:   
        win_venues  = Match.objects.filter(season_id = season_id, winner =  top_team_name).\
                                    values('winner','venue').\
                                    annotate(venue_count = Count('venue')).\
                                    order_by('-venue_count')                                 
        top_win_venue_count = win_venues.values_list('venue_count',flat = True).first()
        top_win_venues      = win_venues.filter(venue_count = top_win_venue_count)
        top_win_venue_data.extend(top_win_venues)


    # Which player won the maximum number of Player of the Match awards in the whole season
    mom_top_players = Match.objects.filter(season_id = season_id).\
                                    values('player_of_match').\
                                    annotate(win_count = Count('player_of_match')).\
                                    order_by('-win_count')
    mom_top_count   = mom_top_players.values_list('win_count',flat = True).first()
    top_mom_player  = mom_top_players.filter(win_count = mom_top_count)

    return JsonResponse ({
                'top_4_teams'    : list(top_4_teams),
                'top_team'       : list(top_team),
                'top_win_venues' : list(top_win_venue_data),
                'top_mom_player' : list(top_mom_player)
            },safe=False)

@csrf_exempt
def toss_analytics(request):
    season_id = request.POST.get('season_id')
    # Which % of teams decided to bat when they won the toss
    chose_to_bat_teams = Match.objects.filter(season_id = season_id, toss_decision='bat').\
                                       values('toss_winner').\
                                       distinct().count()
    toss_winner_teams  = Match.objects.filter(season_id = season_id).\
                                       values('toss_winner').\
                                       distinct().count()
    chose_to_bat_percentage = round((chose_to_bat_teams/float(toss_winner_teams))*100.00 ,2)

    # How many times has a team won the toss and the match for the selected season
    team_wise_toss_match_win = Match.objects.filter(season_id = season_id, winner = F('toss_winner')).\
                                              values('winner').\
                                              annotate(team_count = Count('winner')).\
                                              order_by('-team_count')


    # Which team won the most number of tosses in the season
    toss_win_team      = Match.objects.filter(season_id = season_id).\
                                       values('toss_winner').\
                                       annotate(toss_count = Count('toss_winner')).\
                                       order_by('-toss_count')
    toss_win_count     = toss_win_team.values_list('toss_count',flat = True).first()
    top_toss_win_team  = toss_win_team.filter(toss_count = toss_win_count)

    return JsonResponse ({
            'chose_to_bat_percentage'   : chose_to_bat_percentage,
            'team_wise_toss_match_win'  : list(team_wise_toss_match_win),
            'top_toss_win_team'         : list(top_toss_win_team)
           },safe=False)

@csrf_exempt
def  victory_analysis(request):
    season_id = request.POST.get('season_id')
    # Which team won by the highest margin of runs  for the season
    margin_of_run_wins = Match.objects.filter(season_id = season_id).\
                                       values('winner','win_by_runs').\
                                       order_by('-win_by_runs')
    top_margin_of_runs = margin_of_run_wins.values_list('win_by_runs', flat = True).first()
    top_team_by_run_margin = margin_of_run_wins.filter(win_by_runs = top_margin_of_runs)
    
    # Which team won by the highest number of wickets for the season
    margin_of_run_wkts = Match.objects.filter(season_id = season_id).\
                                       values('winner','win_by_wickets').\
                                       order_by('-win_by_wickets')
    top_margin_of_wkts = margin_of_run_wkts.values_list('win_by_wickets', flat = True).first()
    top_team_by_wkt_margin = margin_of_run_wkts.filter(win_by_wickets = top_margin_of_wkts)

    return JsonResponse ({ 
                "top_team_by_run_margin" : list(top_team_by_run_margin),
                "top_team_by_wkt_margin" : list(top_team_by_wkt_margin)
           },safe=False)



@csrf_exempt
def location_analytics(request):
    season_id = request.POST.get('season_id')
    # Which location hosted most number of matches and win % and loss % for the season
    match_by_venue    = Match.objects.filter(season_id = season_id).\
                                      values('venue').\
                                      annotate(venue_count = Count('venue')).\
                                      order_by('-venue_count')
    top_hosting_count = match_by_venue.values_list('venue_count', flat = True).first()
    top_venue_names = match_by_venue.filter(venue_count = top_hosting_count ).values_list('venue',flat=True)

    venue_status_dict = {}
    for _venue in top_venue_names:
        match_status_by_top_host = Match.objects.filter(season_id = season_id,venue = _venue, result = 'normal').\
                                             values('winner').\
                                             annotate(loser = Case(
                                                                    When(winner = F('team1'), then = 'team2'),
                                                                    default     = F('team2'),
                                                                    output_field = CharField()
                                            ))
        match_wins   =  dict(match_status_by_top_host.values_list('winner').annotate(win_count = Count('winner')))
        match_loses  =  dict(match_status_by_top_host.values_list('loser').annotate(win_count = Count('loser')))
        
        team_status  = { k: {'win':match_wins.get(k, 0) ,'lose': match_loses.get(k, 0) , 'tie_or_no_result': 0} for k in set(match_wins) | set(match_loses) }

        tie_no_result_matches = Match.objects.filter(season_id = season_id,venue = _venue).\
                                              exclude(result = 'normal').\
                                              values_list('team1','team2')
        if tie_no_result_matches:
            flattened = []
            for item in tie_no_result_matches:
                flattened.extend(item)
            for item in  flattened:
                if item in  team_status:
                    team_status[item]['tie_or_no_result'] += 1
        venue_status_dict[_venue] = team_status
    return  JsonResponse ({ "venue_status_dict" : venue_status_dict,
                            "top_hosting_count" : top_hosting_count
                           },safe=False)  



# Most number of catches by a fielder in a match for the selected season.
def catch_analysis(request):
    # season_id = request.POST.get('season_id')
    pass
