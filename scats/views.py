from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import boto3
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Scats
from .serializers import ScatsSerializer
from datetime import datetime, timedelta
import pytz
from .logics.seasonality_analysis import seasonality_analysis
import json


class OpsheetDownloadView(APIView):
    """
    Provide presigned url to opsheets on s3.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, scats_id, format=None):
        s3 = boto3.resource(
            service_name='s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        url = s3.meta.client.generate_presigned_url(
            ClientMethod="get_object", ExpiresIn=3600,
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": f'{scats_id}.zip',
            },
        )
        return Response({'url': url})


class ExtractScatsDataView(APIView):
    """
    Extract and return SCATS data from the database.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        scats_id = from_date = request.query_params.get('scats_id')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        tz = pytz.timezone('Australia/Melbourne')

        try:
            scats_id = int(scats_id)
        except Exception:
            return Response(
                {'error': "'scats_id' must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_date_year, from_date_month, from_date_day = [int(i) for i in from_date.split('-')]
            from_date = datetime(
                from_date_year,
                from_date_month,
                from_date_day,
                tzinfo=tz
            )
        except Exception:
            return Response(
                {'error': "'from' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            to_date_year, to_date_month, to_date_day = [int(i) for i in to_date.split('-')]
            to_date = datetime(
                to_date_year,
                to_date_month,
                to_date_day,
                tzinfo=tz
            )
        except Exception as e:
            return Response(
                {'error': "'to' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if to_date - from_date > timedelta(days=7-1):
            return Response(
                {'error': "Time difference between 'from' and 'date' cannot be more than 7 days."},
                status=status.HTTP_400_BAD_REQUEST
            )

        scats_data = Scats.objects.filter(
            NB_SCATS_SITE=scats_id,
            QT_INTERVAL_COUNT__gte=from_date,
            QT_INTERVAL_COUNT__lte=to_date
        ).order_by('QT_INTERVAL_COUNT', 'NB_DETECTOR')

        if len(scats_data) == 0:
            return Response(
                {'error': "There was no data found. Please try again with a different request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ScatsSerializer(scats_data, many=True)
        return Response(serializer.data)


class SeasonalityAnalysisView(APIView):
    """
    Perform seasonality analysis.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        scats_id = from_date = request.query_params.get('scats_id')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        detectors = request.query_params.get('detectors')
        
        if detectors == 'all' or detectors == None or detectors == '':
            detectors = [i+1 for i in range(24)]
        else:
            try:
                detectors = [int(i) for i in detectors.split(',')]
            except Exception:
                return Response(
                    {'error': "'detectors' must be integers separated by comma."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        tz = pytz.timezone('Australia/Melbourne')

        try:
            scats_id = int(scats_id)
        except Exception:
            return Response(
                {'error': "'scats_id' must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_date_year, from_date_month, from_date_day = [int(i) for i in from_date.split('-')]
            from_date = datetime(
                from_date_year,
                from_date_month,
                from_date_day,
                tzinfo=tz
            )
        except Exception:
            return Response(
                {'error': "'from' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            to_date_year, to_date_month, to_date_day = [int(i) for i in to_date.split('-')]
            to_date = datetime(
                to_date_year,
                to_date_month,
                to_date_day,
                tzinfo=tz
            )
        except Exception as e:
            return Response(
                {'error': "'to' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if to_date - from_date > timedelta(days=365-1):
            return Response(
                {'error': "Time difference between 'from' and 'date' cannot be more than 365 days."},
                status=status.HTTP_400_BAD_REQUEST
            )

        scats_data = Scats.objects.filter(
            NB_SCATS_SITE=scats_id,
            QT_INTERVAL_COUNT__gte=from_date,
            QT_INTERVAL_COUNT__lte=to_date,
            NB_DETECTOR__in=detectors
        )

        if len(scats_data) == 0:
            return Response(
                {'error': "There was no data found. Please try again with a different request."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        json_data = seasonality_analysis(scats_data)

        return Response(json.loads(json_data))