from django.contrib import admin
from .models import DataType, Correlation


class CorrelationAdmin(admin.ModelAdmin):
    list_display = ("user", "x_data_type", "y_data_type", "value")


admin.site.register(DataType)
admin.site.register(Correlation, CorrelationAdmin)
