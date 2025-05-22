# imports
import pandas as pd
import json

profiles = pd.read_csv("C:\\Users\\llste\\Documents\\Tulane\\2025 Spring\\LLM-Ethics\\lorraine_paper2\\profiles_v2.csv")

# Open and read the JSON file
with open('C:\\Users\\llste\\Documents\\Tulane\\2025 Spring\\LLM-Ethics\\lorraine_paper2\\questions.json', 'r') as file:
    questions = json.load(file)

# this is a weird way to do this but
baseline = pd.json_normalize(questions, record_path=['baseline'])
graham = pd.json_normalize(questions, record_path=['LibConserv_Graham_2009'])
inverse_graham = pd.json_normalize(questions, record_path=['Inverse_LibConserv_Graham_2009'])

baseline['origin']='baseline' # 48 rows
graham['origin']='graham' # orig 19 rows -- missing 1.4 (gov), added to even to 20
inverse_graham['origin']='inverse' # 20 rows

prompts = pd.concat([baseline, graham, inverse_graham], ignore_index=True) # 88 rows!
prompts.rename(columns={'text': 'prompt', 'number': "prompt_number"}, inplace=True)
prompts = prompts.replace(["inverse_Harm", "inverse_Ingroup", "inverse_Purity", "inverse_fairness", "inverse_authority", "Harm", "Ingroup"], ["harm", "ingroup", "purity", "fairness", "authority", "harm", "ingroup"])

graham_prompts = prompts.loc[prompts['origin'] != 'baseline']
graham_prompts = graham_prompts.reset_index(drop=True)

grahaminverse = graham_prompts.to_csv('graham_and_inverse.csv', index = True)