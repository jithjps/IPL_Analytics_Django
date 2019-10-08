"""
Helper function to Upload data into Match Tables
run using python manage.py upload_matches
Takes Input as the files from CSVData folder
"""
from django.core.management.base import BaseCommand
import codecs
from ipl_data.models import Season,Match
import csv
import ast
import os
from settings import MEDIA_ROOT

class Command(BaseCommand):
    help="Upload Matches"
    def handle(self, *args, **options):
        if not Season.objects.exists():
            upload_seasons = []
            for year in ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']:
                try:
                    upload_seasons.append(Season(season_name = year))
                except Exception as e:
                    print "Error in creating Seasons:" + str(e)
            if upload_seasons:
                try:
                    Season.objects.bulk_create(upload_seasons)
                except Exception as e:
                    return "Error in Bulk creation of Seasons:" + str(e)
            else:
                return "Error"        
        else:
            print "Already Seasons Created"


        if Match.objects.exists():
            return "Already Matches created"
        try:
            match_data   = codecs.open(os.path.join(MEDIA_ROOT, 'CSVData/matches.csv', "rb",encoding='ascii', errors='ignore')
            match_data_reader = csv.DictReader(match_data)
        except Exception as e:
            return  "Error in opening the dataCSV: " + str(e)
        i = 0  
        upload_datas  = []
        for i,_data in enumerate(match_data_reader,1):  
            try:
                if not isinstance(_data, dict):
                    _data = ast.literal_eval(_data)
                if 'season' in _data:
                    _data['season_id'] = _data['season']    
                    del _data['season']
                match = Match(**_data)
                upload_datas.append(match)
            except Exception as e:
                return "Error in processing line Number:"+ str(i) + ". Error: "+ str(e)
        try: 
            if upload_datas:       
                Match.objects.bulk_create(upload_datas)    
                match_data.close()
        except Exception as e:
            return "Error in bulk creation "+ str(e)
        return "Success"    



