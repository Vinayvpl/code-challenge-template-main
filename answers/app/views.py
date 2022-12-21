from django.shortcuts import render
from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from .models import Weather,CornGrainYield,WeatherAnalysis
import pandas as pd
import os
import datetime
from django.db.models import Max, Min, Avg, Sum
from django.db.models.functions import TruncMonth, TruncYear


from .serializers import WeatherSerializer, CornGrainYieldSerializer, WeatherAnalysisSerializer
# Create your views here.

class WeatherAnalysisListApi(APIView):
    serializer_classes = WeatherAnalysisSerializer
    paginator = PageNumberPagination()

    def get(self, request, format=None):
        query_dic = self.request.query_params
        if query_dic:
            fields_dic = {f.name:'' for f in WeatherAnalysis._meta.get_fields()}
            fields_dic.update(query_dic)
            analysis_data = WeatherAnalysis.objects.filter(station_id__in= fields_dic['station_id'], year__in = fields_dic['year'])
            context = self.paginator.paginate_queryset(analysis_data, request)
            serializer = self.serializer_classes(context, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        else:
            analysis_data = WeatherAnalysis.objects.all()
            context = self.paginator.paginate_queryset(analysis_data, request)
            serializer = self.serializer_classes(context, many=True)
            return self.paginator.get_paginated_response(serializer.data)


    def post(self, request, format=None):
        try:
            records_before_insert = WeatherAnalysis.objects.all().count()
            start_time = datetime.datetime.now()
            weather_data = Weather.objects.all().count()
            if weather_data == 0:
                return Response("No Data available to analyze weather data", status=status.HTTP_201_CREATED)
            weather_data = list(Weather.objects.exclude(maximum_temperature=-9999,precipitation=-9999).annotate(year=TruncYear('date')).values("station_id","date__year").annotate(maximum_temperature_average=Avg('maximum_temperature'),minimum_temperature_average=Avg('minimum_temperature'),total_precipitation=Sum('precipitation')))
            data_analys_list =[]
            for w_datum in weather_data:
                data_analysis = WeatherAnalysis(station_id=w_datum["station_id"], 
                year=w_datum["date__year"], 
                maximum_temperature_average=w_datum["maximum_temperature_average"], 
                minimum_temperature_average=w_datum["minimum_temperature_average"],
                total_precipitation=w_datum["total_precipitation"])
                data_analys_list.append(data_analysis)
            if data_analys_list:
                WeatherAnalysis.objects.bulk_create(data_analys_list,ignore_conflicts=True)
            finish_time = datetime.datetime.now()
            number_of_records_after_insert = WeatherAnalysis.objects.all().count()
            data = {
                "messages":"data stored.",
                "start_time":start_time,
                "end":finish_time,
                "completion_time ":finish_time - start_time,
                "Number of records ingested":number_of_records_after_insert-records_before_insert
                }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data=[]
            print(e)
            data["messages"]="error"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class WeatherListApi(APIView):
    serializer_classes = WeatherSerializer
    paginator = PageNumberPagination()

    def format_date(self, date):
        return date[:4] + '-' + date[4:6]+'-' + date[6:]
    

    def get(self, request, format=None):
        weather = Weather.objects.all()
        context = self.paginator.paginate_queryset(weather, request)
        serializer = self.serializer_classes(context, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        try:
            records_before_insert = Weather.objects.all().count() 
            start_time = datetime.datetime.now()
            data = os.listdir('../wx_data/')
            for file in data:
                fileName,fileExtension = os.path.splitext(file)
                if fileExtension == '.txt':
                    datafile = pd.read_csv(f"../wx_data/{str(file)}", sep="\t", header=None, names=['date', 'max_temp', 'min_temp', 'precipitation'])
                    data_records = datafile.to_dict('records')
                    wx_create_list = []
                    for records in data_records:
                        dp = Weather(station_id=str(file.split('.')[0]), date=self.format_date(str(records['date'])), maximum_temperature=records['max_temp'], minimum_temperature=records['min_temp'], precipitation=records['precipitation'])
                        wx_create_list.append(dp)
                    if wx_create_list:
                        Weather.objects.bulk_create(wx_create_list)
                finish_time = datetime.datetime.now()
                records_after_insert = Weather.objects.all().count()
                data = {"messages":" Weather data stored.", "start_time":start_time, "end_time":finish_time, "completion_time ":finish_time - start_time, "Number of records ingested":records_after_insert-records_before_insert }
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data=[]
            data["messages"]=str(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class YieldListApi(APIView):
    paginator = PageNumberPagination()
    serializer_classes = CornGrainYieldSerializer

    def get(self, request, format=None):
        yield_data = CornGrainYield.objects.all()
        context = self.paginator.paginate_queryset(yield_data, request)
        serializer = self.serializer_classes(context, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        try:
            records_before_insert = CornGrainYield.objects.all().count()
            start_time = datetime.datetime.now()
            datafile = pd.read_csv("../yld_data/US_corn_grain_yield.txt", sep="\t", header=None, names=['year', 'corn_yield'])
            data_records = datafile.to_dict('records')
            yld_create_list = []
            for record in data_records:
                dp = CornGrainYield(year=record['year'], corn_yield=record['corn_yield'])
                yld_create_list.append(dp)
            if yld_create_list:
                CornGrainYield.objects.bulk_create(yld_create_list)
            finish_time = datetime.datetime.now()
            records_after_insert = CornGrainYield.objects.all().count()
            data = {"messages":" yield data stored.", "start_time":start_time, "end_time":finish_time, "completion_time ":finish_time - start_time, "Total Number of records":records_after_insert-records_before_insert}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data=[]
            data["messages"]=str(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)




