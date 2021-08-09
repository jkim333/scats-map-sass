from django.urls import path
from .views import (
    OpsheetDownloadView,
    ExtractScatsDataView,
    SeasonalityAnalysisView
)

app_name = 'scats'

urlpatterns = [
    path(
        'opsheet-download/<scats_id>',
        OpsheetDownloadView.as_view(),
        name='opsheet-download'
    ),
    path(
        'extract-scats-data/',
        ExtractScatsDataView.as_view(),
        name='extract-scats-data'
    ),
    path(
        'seasonality-analysis/',
        SeasonalityAnalysisView.as_view(),
        name='seasonality-analysis'
    )
]