from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
import boto3
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Scats
from .serializers import ScatsSerializer
from datetime import date, timedelta
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
        user = request.user

        is_user_free = timezone.now() < user.free_until

        if user.scats_credit == 0 and not user.subscribed and not is_user_free:
            # Not allowed if user has no credit and is not subscribed
            # and is not on the free period.
            return Response(
                {'error': 'Access denied. Please purchase scats credit points or sign up for the monthly subscription.'},
                status=status.HTTP_403_FORBIDDEN
            )

        scats_id = from_date = request.query_params.get('scats_id')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        try:
            scats_id = int(scats_id)
        except Exception:
            return Response(
                {'error': "'scats_id' must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_date_year, from_date_month, from_date_day = [int(i) for i in from_date.split('-')]
            from_date = date(
                from_date_year,
                from_date_month,
                from_date_day,
            )
        except Exception:
            return Response(
                {'error': "'from' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            to_date_year, to_date_month, to_date_day = [int(i) for i in to_date.split('-')]
            to_date = date(
                to_date_year,
                to_date_month,
                to_date_day,
            )
        except Exception as e:
            return Response(
                {'error': "'to' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if from_date < settings.QT_INTERVAL_COUNT_MIN:
            return Response(
                {'error': f"'from' must be a date later than or equal to {settings.QT_INTERVAL_COUNT_MIN}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if to_date > settings.QT_INTERVAL_COUNT_MAX:
            return Response(
                {'error': f"'to' must be a date earlier than or equal to {settings.QT_INTERVAL_COUNT_MAX}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if to_date - from_date > timedelta(days=7-1):
            return Response(
                {'error': "Time difference between 'from' and 'to' cannot be more than 7 days."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if from_date - to_date > timedelta(days=0):
            return Response(
                {'error': "'from' cannot be greater than 'to'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        scats_data = Scats.objects.filter(
            NB_SCATS_SITE=scats_id,
            QT_INTERVAL_COUNT__gte=from_date,
            QT_INTERVAL_COUNT__lte=to_date
        ).order_by('QT_INTERVAL_COUNT', 'NB_DETECTOR').distinct('QT_INTERVAL_COUNT', 'NB_DETECTOR')

        if len(scats_data) == 0:
            return Response(
                {'error': "There was no data found. Please try again with a different request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ScatsSerializer(scats_data, many=True)

        if not user.subscribed and not is_user_free:
            user.scats_credit = user.scats_credit - 1
            user.save()

        return Response(serializer.data)


class SeasonalityAnalysisView(APIView):
    """
    Perform seasonality analysis.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        is_user_free = timezone.now() < user.free_until

        if user.seasonality_credit == 0 and not user.subscribed and not is_user_free:
            # Not allowed if user has no credit and is not subscribed
            #  and is not on the free period.
            return Response(
                {'error': 'Access denied. Please purchase seasonality analysis credit points or sign up for the monthly subscription.'},
                status=status.HTTP_403_FORBIDDEN
            )

        scats_id = from_date = request.query_params.get('scats_id')
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        detectors = request.query_params.get('detectors')
        
        if detectors == 'all' or detectors == None or detectors == '':
            detectors = [i+1 for i in range(50)]
        else:
            try:
                detectors = [int(i) for i in detectors.split(',')]
            except Exception:
                return Response(
                    {'error': "'detectors' must be integers separated by comma."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            scats_id = int(scats_id)
        except Exception:
            return Response(
                {'error': "'scats_id' must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_date_year, from_date_month, from_date_day = [int(i) for i in from_date.split('-')]
            from_date = date(
                from_date_year,
                from_date_month,
                from_date_day,
            )
        except Exception:
            return Response(
                {'error': "'from' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            to_date_year, to_date_month, to_date_day = [int(i) for i in to_date.split('-')]
            to_date = date(
                to_date_year,
                to_date_month,
                to_date_day,
            )
        except Exception as e:
            return Response(
                {'error': "'to' must be a date of format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if from_date < settings.QT_INTERVAL_COUNT_MIN:
            return Response(
                {'error': f"'from' must be a date later than or equal to {settings.QT_INTERVAL_COUNT_MIN}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if to_date > settings.QT_INTERVAL_COUNT_MAX:
            return Response(
                {'error': f"'to' must be a date earlier than or equal to {settings.QT_INTERVAL_COUNT_MAX}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if to_date - from_date > timedelta(days=365-1):
            return Response(
                {'error': "Time difference between 'from' and 'date' cannot be more than 365 days."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if from_date - to_date > timedelta(days=0):
            return Response(
                {'error': "'from' cannot be greater than 'to'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        scats_data = Scats.objects.filter(
            NB_SCATS_SITE=scats_id,
            QT_INTERVAL_COUNT__gte=from_date,
            QT_INTERVAL_COUNT__lte=to_date,
            NB_DETECTOR__in=detectors
        ).order_by('QT_INTERVAL_COUNT', 'NB_DETECTOR').distinct('QT_INTERVAL_COUNT', 'NB_DETECTOR')

        if len(scats_data) == 0:
            return Response(
                {'error': "There was no data found. Please try again with a different request."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        json_data = seasonality_analysis(scats_data)

        if not user.subscribed and not is_user_free:
            user.seasonality_credit = user.seasonality_credit - 1
            user.save()

        return Response(json.loads(json_data))
