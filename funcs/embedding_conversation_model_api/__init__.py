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
import azure.functions as func

import os
import io

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain

from langchain.vectorstores import faiss # chroma, 

import pickle
from azure.storage.blob import BlobServiceClient


AZURE_OPENAI_API_KEY  = ""
AZURE_OPENAI_ENDPOINT = ""
DEPLOYMENT_NAME       = ""
OPENAI_API_VERSION    = ""
MODEL_NAME = ""
API_TYPE = ""

EMBEDDING_DEPLOYMENT_NAME = ""
EMBEDDING_MODEL_NAME = ""

connection_string = ''
container_name = ''

    
llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=OPENAI_API_VERSION,
    openai_api_type=API_TYPE,
    azure_deployment=DEPLOYMENT_NAME,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    temperature=0
)

embedding = AzureOpenAIEmbeddings(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=EMBEDDING_DEPLOYMENT_NAME,
    model=EMBEDDING_MODEL_NAME,
)

dir_path = os.path.dirname(os.path.abspath(__file__))
vectorstore = faiss.FAISS.load_local(dir_path, embedding)


# {"query": "count from 1 to 7"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
    #    verbose=True,
    )
    
    req_body = req.get_json()
    query = req_body['query']
    
    if query == '--reset':
        chat_history = []
        
        chat_history_bytes = pickle.dumps(chat_history)
        blob_name = 'chat_history.pkl'
        
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        chat_history_stream = io.BytesIO(chat_history_bytes)
        blob_client.upload_blob(chat_history_stream, overwrite=True)
        
        output = "chat conversation has been reset."
        return func.HttpResponse(output, status_code=200)
    
    try:
        blob_name = 'chat_history.pkl'
        
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        download_stream = blob_client.download_blob()
        blob_data = download_stream.readall()
        chat_history = pickle.loads(blob_data)
    
    except:
        chat_history = []

    result = chain({"question":query, "chat_history":chat_history})
    chat_history.append((query, result['answer']))

    chat_history_bytes = pickle.dumps(chat_history)
    blob_name = 'chat_history.pkl'

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)    

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    chat_history_stream = io.BytesIO(chat_history_bytes)
    blob_client.upload_blob(chat_history_stream, overwrite=True)

    output = result['answer']
    
    return func.HttpResponse(output, status_code=200)