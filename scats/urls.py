from django.urls import path
from .views import (
    OpsheetDownloadView,
    ExtractScatsDataView,
    SeasonalityAnalysisView
)

urlpatterns = [
    path('opsheet-download/<scats_id>', OpsheetDownloadView.as_view()),
    path('extract-scats-data/', ExtractScatsDataView.as_view()),
    path('seasonality-analysis/', SeasonalityAnalysisView.as_view())
]