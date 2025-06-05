from django.urls import path

from reports.views import summary_report, chart_data

urlpatterns = [
    path('summary/',summary_report),
  path('chart_data/', chart_data),

]