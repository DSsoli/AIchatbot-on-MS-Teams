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
import numpy as np


columns = [
    "Buyer Category",
    "Survey Questions and Answers",
    "Q1: Did you know about our brand before visiting this page?_Total",
    "Q1_A1: No, I didn't know about it",
    "Q1_A2: Yes, I knew about it",
    "Q2: Have you ever used a smart home device before?_Total",
    "Q2_A1: Used to use it but not anymore",
    "Q2_A2: Never used one",
    "Q2_A3: Currently using one",
    "Q3: Which smart home manufacturer are you currently using/have used?_Total",
    "Q3_A1: Manufacturer A",
    "Q3_A2: Manufacturer B",
    "Q3_A3: Manufacturer C",
    "Q3_A4: Other",
    "Q4: How satisfied are you with your current smart home device?_Total",
    "Q4_A1: Very satisfied",
    "Q4_A2: Somewhat satisfied",
    "Q4_A3: Neutral",
    "Q4_A4: Dissatisfied",
    "Q4_A5: Very dissatisfied",
    "Q5: What information do you consider when buying smart home devices?_Total",
    "Q5_A1: Expert reviews",
    "Q5_A2: User reviews",
    "Q5_A3: Price comparison",
    "Q5_A4: Detailed specifications",
    "Q5_A5: Warranty services",
    "Q5_A6: None in particular",
    "Q6: How often do you use smart home devices?_Total",
    "Q6_A1: Daily",
    "Q6_A2: Weekly",
    "Q6_A3: Monthly",
    "Q6_A4: Rarely",
    "Q6_A5: Never",
    "Q7: What motivates you to use smart home devices?_Total",
    "Q7_A1: Convenience",
    "Q7_A2: Security",
    "Q7_A3: Energy efficiency",
    "Q7_A4: Health monitoring",
    "Q7_A5: Entertainment",
    "Q8: What concerns do you have about smart home devices?_Total",
    "Q8_A1: Privacy issues",
    "Q8_A2: Cost",
    "Q8_A3: Device compatibility",
    "Q8_A4: Technical complexity",
    "Q8_A5: Limited usefulness",
    "Q9: How would you describe your willingness to recommend smart home devices to others?_Total",
    "Q9_A1: Definitely",
    "Q9_A2: Probably",
    "Q9_A3: Neutral",
    "Q9_A4: Probably not",
    "Q9_A5: Definitely not",
    "Q10: How do you research smart home devices before purchasing?_Total",
    "Q10_A1: Online reviews",
    "Q10_A2: Friends or family recommendations",
    "Q10_A3: Manufacturer's website",
    "Q10_A4: Social media",
    "Q10_A5: Sales representatives",
    "Q10_A6: Don't research"
]


buyer_categories = [
    "01_Loyal Buyers", 
    "02_First-Time Buyers", 
    "03_Casual Buyers", 
    "04_Competitor Buyers", 
    "05_Non-Buyers"
]


np.random.seed(42)


def generate_answers_and_totals(num_answers):
    answers = np.random.randint(5, 50, num_answers)
    total = np.sum(answers)
    return [total] + answers.tolist()


data = []

for category in buyer_categories:
    q1 = generate_answers_and_totals(2)
    q2 = generate_answers_and_totals(3)
    q3 = generate_answers_and_totals(4)
    q4 = generate_answers_and_totals(5)
    q5 = generate_answers_and_totals(6)
    q6 = generate_answers_and_totals(5)
    q7 = generate_answers_and_totals(5)
    q8 = generate_answers_and_totals(5)
    q9 = generate_answers_and_totals(5)
    q10 = generate_answers_and_totals(6)

    row = [category, f"response aggregations for {category}"] + q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10
    data.append(row)


artificial_dataset = pd.DataFrame(data, columns=columns)


output_path = './data/artificial_survey_data.csv'
artificial_dataset.to_csv(output_path, index=False)