

from django.urls import path
from .views import *

urlpatterns = [
    path("report-data-table/<int:id>",ReportQuery.as_view(),name="report-data-table"),
]