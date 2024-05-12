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


import warnings
warnings.filterwarnings("ignore")

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import faiss # chroma, 


AZURE_OPENAI_API_KEY  = ""
AZURE_OPENAI_ENDPOINT = ""
DEPLOYMENT_NAME       = ""
OPENAI_API_VERSION    = ""
MODEL_NAME = ""
API_TYPE = ""

EMBEDDING_DEPLOYMENT_NAME = ""
EMBEDDING_MODEL_NAME = ""

aggregation_data = 'data/artificial_survey_data.csv'
destination_api_dir = '../funcs/embedding_conversation_model_api'


def generate_model():
    
    embedding = AzureOpenAIEmbeddings(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=EMBEDDING_DEPLOYMENT_NAME,
        model=EMBEDDING_MODEL_NAME,
    )
    return embedding


def save_vectorestore_to_api(embedding_model, aggregation_data, api_path):
    
    loader = CSVLoader(aggregation_data)
    data = loader.load()
    # text_splitter = CharacterTextSplitter() #chunk_size=500, chunk_overlap=20   # -- to decrease # of tokens concerning token limits
    text_splitter = RecursiveCharacterTextSplitter()
    text_chunks = text_splitter.split_documents(data)
    vectorstore = faiss.FAISS.from_documents(text_chunks, embedding_model) # -- to decrease # of tokens concerning token limits
    vectorstore.save_local(api_path)
    print("vectorstore db loaded to destination api dir")


def main():
    embedding = generate_model()
    save_vectorestore_to_api(embedding, 
                             aggregation_data, 
                             destination_api_dir)
    
    
if __name__ == "__main__":
    main()