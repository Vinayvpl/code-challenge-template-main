from django.core.management.base import BaseCommand

from app.models import Weather, WeatherAnalysis
from django.db.models import Max, Min, Avg, Sum
import datetime
from django.db.models.functions import TruncMonth, TruncYear


class Command(BaseCommand):
    help = 'Analyze aand insert/update Weather Statistics Data'

    def add_argument(self, parser):
        pass

    def format_date(self, date):
        return f'{date[:4]}-{date[4:6]}-{date[6:]}'

    def handle(self, *args, **options):
        records_before_insert = WeatherAnalysis.objects.all().count()
        start_time = datetime.datetime.now()
        weather_data = Weather.objects.all().count()
        if weather_data == 0:
            print("No data available to analyze weather")

        w_data = list(Weather.objects.exclude(maximum_temperature=-9999,precipitation=-9999).annotate(year=TruncYear('date')).values("station_id","date__year").annotate(maximum_temperature_average=Avg('maximum_temperature'),minimum_temperature_average=Avg('minimum_temperature'),total_precipitation=Sum('precipitation')))

        print(len(w_data))
        products = [WeatherAnalysis(station_id=w_datum["station_id"], year=w_datum["date__year"], maximum_temperature_average=w_datum["maximum_temperature_average"], minimum_temperature_average=w_datum["minimum_temperature_average"], total_precipitation=w_datum["total_precipitation"]) for w_datum in w_data]

        WeatherAnalysis.objects.bulk_create(products,ignore_conflicts=True)

        finish_time = datetime.datetime.now()
        records_after_insert = WeatherAnalysis.objects.all().count()

        # using print as log statement for test purposes
        print("Weather statistics data \n")
        print(f"Start Time {start_time}" + "\n")
        print(f"Finish Time {finish_time}" + "\n")
        print(f"Number of records ingested: {records_after_insert - records_before_insert}" + "\n")
        print(f"Execution time =  {finish_time - start_time} \n")
        

