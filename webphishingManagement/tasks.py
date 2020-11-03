from celery import shared_task
from webphishingClient.models import ClientFiles, Colaborator
from webphishingAuth.models import ClientModel

import pandas as pd
import numpy as np

@shared_task
def CreateUsersFromXLS(client_pk, document_pk):
    results = {}
    results['status'] = ""
    results['errors'] = []

    client = ClientModel.getClient(client_pk)
    if client is None:
        results['status'] = "FAILED"
        results['errors'].append("El cliente seleccionado no existe.")
        return results

    file_xls = client.getFileById(document_pk)
    if file_xls is None:
        results['status'] = "FAILED"
        results['errors'].append("El archivo no existe en ese cliente.")
        return results

    ## PandaFile
    df = pd.read_excel(file_xls.file_data.open('rb'), header = 0)
    df.columns = df.columns.str.strip().str.lower()
    fields = list(df.columns)
    print(fields)

    # Process users
    user_added = 0
    users_ignored = 0
    for index, row in df.iterrows():
        email = row['email']
        first_name = row['first_name']
        last_name = row['last_name']

        # If exists, ignore
        if Colaborator.Exists(email, client):
            users_ignored += 1
        else:
            # Create colaborator
            colab = Colaborator()

            colab.client = client
            colab.first_name = first_name
            colab.last_name = last_name
            colab.email = str(email).lower()

            extra_data = {}
            if len(fields) > 3:
                for field in fields:
                    if field not in ["email", "first_name", "last_name"]:
                        extra_data[field] = row[field]

            colab.extra_data = extra_data
            colab.save()
            user_added += 1

    results['users_added'] = user_added
    results['users_ignored'] = users_ignored
    results['status'] = "SUCCESS"

    return results