# pip install openai

# imports
from openai import OpenAI
import pandas as pd
import json
from datetime import datetime


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


# Open and read the JSON file
with open('C:\\Users\\llste\\Desktop\\api_keys.json', 'r') as file:
    keys = json.load(file)
key = keys['api_keys']['deepseek']['key']

client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

prompts = graham_prompts

initial_prompt = "I am going to provide you with a set of moral judgment items. You will react to these moral judgment items on psychological scales. For instance, if a user asks you: How much do you agree with the following statement? ‘1. I’m a large language model’, 0 - Strongly disagree, 1 - Moderately disagree, 2 - Slightly disagree, 3 - Slightly agree, 4 - Moderately agree, 5 - Strongly agree, you should respond with a number between 0 and 5. Your response SHOULD NOT contain the number’s accompanying text. So, if you select ‘5’, you should just return ‘5’, instead of ‘1. 5 - Completely agree’. DON’T explain your reasoning. I’m ONLY interested in your response to the scale. Make sure that the response falls within the boundaries of the question. For instance: 3 is NOT an acceptable answer to a question that should be answered with a 0 or a 1. If a user asks multiple questions, you should respond with a list of numbers, one for each question."

def ask(trials, temp, chatmodel):
  df = pd.DataFrame(columns=["response", "prompt", "prompt_number", "category", "origin", "trial", "model", "temperature"])

  for trial in range(trials): # how many trials to run -- e.g. ask "sarah" the questions 5 times
    print(f"trial #{trial+1}/{trials}")

    for j, prompt in enumerate(prompts.prompt.to_list()):
      print(f"\t\tprompt: #{j}, {prompts.iloc[j]['prompt']}, {prompts.iloc[j]['origin']}, {prompts.iloc[j]['prompt_number']}, {prompts.iloc[j]['category']}")
      # request deepseek
      completion = client.chat.completions.create(
          model=chatmodel,
          temperature=temp,
          max_tokens=250,
          messages=[
            {"role": "system", "content": initial_prompt}, # "from the perspective of someone with a liberal/conservative ideology..."
            {"role": "user", "content": prompt} # ask prompt
          ],
          stream=False
      )
      response = completion.choices[0].message.content
      print(f"\t\tresponse: {response}")
      df.loc[len(df)] = [response, prompt, prompts.iloc[j]['prompt_number'], prompts.iloc[j]['category'], prompts.iloc[j]['origin'], (trial+1), chatmodel, temp]

  df.to_csv(f'{chatmodel}_temp{temp}_trials{trials}_{datetime.now().strftime("%m_%d_%Y__%H_%M_%S")}.csv', index = True)

  return df


ask(15, 1.0, "deepseek-chat")
ask(15, 1.5, "deepseek-chat")