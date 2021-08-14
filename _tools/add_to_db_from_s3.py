import pandas as pd
import boto3
from django.conf import settings
from scats.models import Scats
from datetime import date
import json

bucket_name = settings.AWS_ADD_TO_DB_BUCKET_NAME

s3 = boto3.resource(
    service_name='s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

bucket = s3.Bucket(bucket_name)

def add_to_db_from_s3():
    for obj in bucket.objects.all():
        key = obj.key
        if key.endswith('.csv'):
            print(key)
            df = pd.read_csv(obj.get()['Body'])
            df_json = json.loads(df.to_json(orient="records"))

            model_instances = []
            for row in df_json:
                model_instance = Scats(**row)
                date_string = row['QT_INTERVAL_COUNT'].split(' ')[0]
                model_instance.QT_INTERVAL_COUNT = date(
                    year=int(date_string.split('-')[0]),
                    month=int(date_string.split('-')[1]),
                    day=int(date_string.split('-')[2])
                )
                model_instances.append(model_instance)

            Scats.objects.bulk_create(model_instances, batch_size=128)

            obj.delete()
