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


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

storage_account_name = ''
storage_account_key = ''
container_name = ''

connection_string = ''

aggregation_data_dir = "./data/artificial_survey_data.csv"
total_q_number = 10


def save_chart_local(data_dir, question_num: int):
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')
    
    survey_data = pd.read_csv(data_dir)
    
    sns.set(style="whitegrid")
    question_num_str = f"Q{question_num}"

    question_prefix = f"{question_num_str}_"
    total_col = next((col for col in survey_data.columns if col.startswith(question_num_str) and "Total" in col), None)
    if not total_col:
        print(f"Total data not found for question number: {question_num_str}")
        return None
    
    question_name = total_col.split(':', 1)[-1].strip().replace('_Total', '')
    
    options_cols = [col for col in survey_data.columns if col.startswith(question_prefix) and "Total" not in col]
    if not options_cols:
        print(f"No options data found for question number: {question_num_str}")
        return None

    data = survey_data[options_cols].sum()
    clean_labels = [col.split(':', 1)[-1].strip() for col in options_cols]
    plt.figure(figsize=(12, 8))
    bars = plt.bar(clean_labels, data, color=sns.color_palette("Blues_d"), edgecolor='grey')
    
    for bar in bars:
        bar.set_edgecolor("black")
        bar.set_linewidth(1)
        bar.set_alpha(0.7)  # Slight transparency
    
    plt.title(f'Responses Distribution for {question_num_str}:\n{question_name}', fontsize=16, fontweight='bold')
    plt.xlabel('Answer Options', fontsize=14)
    plt.ylabel('Response Count', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig(f"./figs/Q_{question_num}.png", bbox_inches='tight')
    plt.show()
    

def upload_to_storage(connection_string, container_name, local_dir_path, filename):
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    upload_path = local_dir_path + filename

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(upload_path))

    with open(upload_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)    


def main():
    
    for i in range(1, total_q_number+1):
        # save all figures locally
        save_chart_local(aggregation_data_dir, i)
        upload_to_storage(connection_string, container_name, './figs/', f'Q_{i}.png')
    
    print(f"""\
        all figs saved locally at figs/
        all figs uploaded to blob storage container: {container_name}\
        """)


if __name__ == "__main__":
    main()
