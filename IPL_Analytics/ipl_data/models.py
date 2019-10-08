# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Season(models.Model):
    """
    Seasons are made customisable using the Class
    """
    season_name  = models.CharField(max_length = 255)
    def __str__(self):
        return self.season_name

class Match(models.Model):
    """
    Match informations are stored in this class
    """
    season  = models.ForeignKey(Season)
    city    = models.CharField(max_length = 255)
    date    = models.DateField()
    team1   = models.CharField(max_length = 255)
    team2   = models.CharField(max_length = 255)
    toss_winner   = models.CharField(max_length = 255)
    toss_decision = models.CharField(max_length = 255 , default = 'field', 
                                     choices = [('field', 'field'), ('bat', 'bat')])
    result        = models.CharField(max_length = 255 , default = 'normal', 
                                     choices = [('normal', 'normal'), ('no result', 'no result'),('tie','tie')])
            
    dl_applied     = models.IntegerField(default = 0)
    winner         = models.CharField(max_length = 255)
    win_by_runs    = models.IntegerField(default = 0)
    win_by_wickets = models.IntegerField(default = 0)
    player_of_match = models.CharField(max_length = 255)
    venue    = models.CharField(max_length = 255)
    umpire1  = models.CharField(max_length = 255)
    umpire2  = models.CharField(max_length = 255, blank = True, null = True )
    umpire3 = models.CharField(max_length = 255, blank = True, null = True )

    def __str__(self):
        return str(self.season) + " : " + self.team1 +" vs "+ self.team2

class Delivery(models.Model):
    """
    Over by over data of all the matches
    """
    match        = models.ForeignKey(Match)
    inning       = models.IntegerField(default = 1)
    batting_team = models.CharField(max_length = 255)
    bowling_team = models.CharField(max_length = 255)
    over         = models.IntegerField(default = 0)
    ball         = models.IntegerField(default = 0)
    batsman      = models.CharField(max_length = 255)
    non_striker  = models.CharField(max_length = 255)
    bowler       = models.CharField(max_length = 255)
    is_super_over = models.IntegerField(default = 0)
    wide_runs    = models.IntegerField(default = 0)
    bye_runs     = models.IntegerField(default = 0)
    legbye_runs  = models.IntegerField(default = 0)
    noball_runs  = models.IntegerField(default = 0)
    penalty_runs = models.IntegerField(default = 0)
    batsman_runs = models.IntegerField(default = 0)
    extra_runs   = models.IntegerField(default = 0)
    total_runs   = models.IntegerField(default = 0)
    player_dismissed = models.CharField(max_length = 255, blank = True, null = True)
    dismissal_kind   = models.CharField(max_length = 255 , blank = True, null = True ,
                                        choices = [('caught','caught'),
                                                    ('bowled','bowled'),
                                                    ('run out','run out'),
                                                    ('lbw','lbw'),
                                                    ('caught and bowled','caught and bowled'),
                                                    ('stumped','stumped'),
                                                    ('retired hurt','retired hurt'),
                                                    ('hit wicket','hit wicket'),
                                                    ('obstructing the field','obstructing the field')
                                                ])
    fielder =  models.CharField(max_length = 255, blank = True, null = True)
        
