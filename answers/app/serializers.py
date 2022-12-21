from rest_framework import serializers
from django import forms
from .models import Weather,CornGrainYield, WeatherAnalysis

class WeatherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Weather
        fields = ["id", "station_id", "date", "maximum_temperature", "minimum_temperature", "precipitation"]


class CornGrainYieldSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CornGrainYield
        fields = ["id", "year", "corn_yield"]


class WeatherAnalysisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WeatherAnalysis
        fields = ["id", "station_id", "year", "maximum_temperature_average", "minimum_temperature_average", "total_precipitation"]