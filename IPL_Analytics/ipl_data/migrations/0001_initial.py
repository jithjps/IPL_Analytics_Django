# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-10-05 18:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inning', models.IntegerField(default=1)),
                ('batting_team', models.CharField(max_length=255)),
                ('bowling_team', models.CharField(max_length=255)),
                ('over', models.IntegerField(default=0)),
                ('ball', models.IntegerField(default=0)),
                ('batsman', models.CharField(max_length=255)),
                ('non_striker', models.CharField(max_length=255)),
                ('bowler', models.CharField(max_length=255)),
                ('is_super_over', models.IntegerField(default=0)),
                ('wide_runs', models.IntegerField(default=0)),
                ('bye_runs', models.IntegerField(default=0)),
                ('legbye_runs', models.IntegerField(default=0)),
                ('noball_runs', models.IntegerField(default=0)),
                ('penalty_runs', models.IntegerField(default=0)),
                ('batsman_runs', models.IntegerField(default=0)),
                ('extra_runs', models.IntegerField(default=0)),
                ('total_runs', models.IntegerField(default=0)),
                ('player_dismissed', models.CharField(blank=True, max_length=255, null=True)),
                ('dismissal_kind', models.CharField(blank=True, choices=[('caught', 'caught'), ('bowled', 'bowled'), ('run out', 'run out'), ('lbw', 'lbw'), ('caught and bowled', 'caught and bowled'), ('stumped', 'stumped'), ('retired hurt', 'retired hurt'), ('hit wicket', 'hit wicket'), ('obstructing the field', 'obstructing the field')], max_length=255, null=True)),
                ('fielder', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('team1', models.CharField(max_length=255)),
                ('team2', models.CharField(max_length=255)),
                ('toss_winner', models.CharField(max_length=255)),
                ('toss_decision', models.CharField(choices=[('field', 'field'), ('bat', 'bat')], default='field', max_length=255)),
                ('result', models.CharField(choices=[('normal', 'normal'), ('no result', 'no result'), ('tie', 'tie')], default='normal', max_length=255)),
                ('dl_applied', models.IntegerField(default=0)),
                ('winner', models.CharField(max_length=255)),
                ('win_by_runs', models.IntegerField(default=0)),
                ('win_by_wickets', models.IntegerField(default=0)),
                ('player_of_match', models.CharField(max_length=255)),
                ('venue', models.CharField(max_length=255)),
                ('umpire1', models.CharField(max_length=255)),
                ('umpire2', models.CharField(blank=True, max_length=255, null=True)),
                ('umpire3', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipl_data.Season'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipl_data.Match'),
        ),
    ]
