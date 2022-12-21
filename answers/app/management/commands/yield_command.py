from django.core.management.base import BaseCommand
from app.models import CornGrainYield
import pandas as pd
import datetime


class Command(BaseCommand):
    help = 'import crop data'

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        records_before_insert = CornGrainYield.objects.all().count()
        start_time = datetime.datetime.now()
        # load data into pandas data frame
        df = pd.read_csv("../yld_data/US_corn_grain_yield.txt", sep="\t", header=None, names=['year', 'corn_yield'])
        df_records = df.to_dict('records')

        # load data from data frame to model instances
        model_instances = [CornGrainYield(
            year=record['year'],
            corn_yield=record['corn_yield'],
        ) for record in df_records]

        # use django bulk_create to insert data into tables
        CornGrainYield.objects.bulk_create(model_instances, ignore_conflicts=True)
        finish_time = datetime.datetime.now()
        records_after_insert = CornGrainYield.objects.all().count()

        # using print as log statement for test purposes
        print("Data Ingested for crop data \n")
        print(f"Start Time {start_time}" + "\n")
        print(f"Finish Time {finish_time}" + "\n")
        print(f"Number of records ingested: {records_after_insert - records_before_insert}" + "\n")
        print(f"Execution time =  {finish_time - start_time} \n")

