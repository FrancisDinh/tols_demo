# Add prompting to include topic
import openai

def create_message_for_finetune(prompt):
    return [{'role': 'system',
  'content': "Your name is Tols, a careful buddy, you help to answer question about food and health. If you do not have the answer, then reply: sorry bud, I couldnt assist you with this bud"},
 {'role': 'user', 'content': 
  f"""Follow step by step before providing the answer to the below <question>:
  If <question> is about nutrient, food, health, obesity and diet, then you answer it.
  Else reply I dont know

  Do not make up the answer, if you do not have the answer, then reply: I dont know.

  ###
  <question>: {prompt}.
  """}]

def get_answer_from_finetune(messages, model="ft:gpt-3.5-turbo-0613:tols:tols-v1:8PdVprZq"):
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0.7, max_tokens=100
    )
    return response["choices"][0]["message"]["content"]