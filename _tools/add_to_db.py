import pandas as pd
import os
from scats.models import Scats
import json
from datetime import date

def add_to_db(folder_path):
    # e.g. folder_path = r'C:\Users\Jihyung\Downloads\VSDATA_202107'

    for file in os.listdir(folder_path):
        if not file.endswith('.csv'): continue

        print(file)

        df = pd.read_csv(os.path.join(folder_path, file))
        
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
