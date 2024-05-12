"""
Copyright 2024 Sanghoon Lee (DSsoli). All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import logging
import pandas as pd
import azure.functions as func
import os
import re
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta


storage_account_name = ''
storage_account_key = ''
container_name = ''
total_question_numbers = 10


def generate_sas_url(container_name, blob_name, storage_account_name, storage_account_key):
    sas_token = generate_blob_sas(account_name=storage_account_name,
                                  container_name=container_name,
                                  blob_name=blob_name,
                                  account_key=storage_account_key,
                                  permission=BlobSasPermissions(read=True),
                                  expiry=datetime.utcnow() + timedelta(hours=1))  # Set expiration as needed
    return f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"


# {"prompt": "give me visualization for Q_1"}
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    
    valid_imgs = [f'Q_{i}' for i in range(1,total_question_numbers+1)]
    
    prompt = req_body.get('prompt')
    
    for valid_img in valid_imgs:
        # Use regex to find exact match of valid_img followed by a non-numeric character or the end of the string
        if re.search(f'{valid_img}(\\D|$)', prompt):
            file_name = valid_img
            blob_name = file_name + ".png"
            return func.HttpResponse(generate_sas_url(container_name, 
                                                      blob_name, 
                                                      storage_account_name, 
                                                      storage_account_key))
    
    return func.HttpResponse(status_code=204)