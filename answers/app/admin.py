from django.contrib import admin
from .models import Weather, CornGrainYield, WeatherAnalysis
# Register your models here.

class WeatherAdmin(admin.ModelAdmin):
    list_display =['station_id', 'date', 'maximum_temperature', 'minimum_temperature', 'precipitation', ]

class CornGrainYieldAdmin(admin.ModelAdmin):
    list_display = ['year', 'corn_yield']

class WeatherAnalysisAdmin(admin.ModelAdmin):
    list_display = ['station_id', 'year', 'maximum_temperature_average', 'minimum_temperature_average', 'total_precipitation']


admin.site.register(Weather, WeatherAdmin)
admin.site.register(CornGrainYield, CornGrainYieldAdmin)
admin.site.register(WeatherAnalysis, WeatherAnalysisAdmin)
