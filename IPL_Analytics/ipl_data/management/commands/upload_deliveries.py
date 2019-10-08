"""
Helper function to Upload data into Delivery Tables
run using python manage.py upload_matches
Takes Input as the files from CSVData folder
"""
from django.core.management.base import BaseCommand
import codecs
from ipl_data.models import Delivery,Match
import csv
import ast
from settings import MEDIA_ROOT
import os

class Command(BaseCommand):
    help="Upload Deliveries"
    def handle(self, *args, **options):
        if not Match.objects.exists():
            return "Please run upload_matches command first"
        if Delivery.objects.exists():
            return "Already Deliveries created"
        try:
            delivery_data   = codecs.open(os.path.join(MEDIA_ROOT , 'CSVData/deliveries.csv'), "rb",encoding='ascii', errors='ignore')
            delivery_data_reader = csv.DictReader(delivery_data)
        except Exception as e:
            return "Error in opening the dataCSV: " + str(e)
        i = 0  
        upload_datas  = []
        print "This process May take some time...."
        for i,_data in enumerate(delivery_data_reader,1):  
            try:
                if not isinstance(_data, dict):
                    _data = ast.literal_eval(_data)
                delivery = Delivery(**_data)
                upload_datas.append(delivery)
            except Exception as e:
                return "Error in processing line Number:"+ str(i) + ". Error: "+ str(e)
        # print upload_datas        
        try: 
            if upload_datas:       
                Delivery.objects.bulk_create(upload_datas,batch_size=2500)    
                delivery_data.close()
        except Exception as e:
            return "Error in bulk creation "+ str(e)
        return "Success"    
