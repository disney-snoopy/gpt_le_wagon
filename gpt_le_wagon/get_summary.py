from gpt_le_wagon.utils import *
import openai

# load api key
openai.api_key = API_KEY

def get_summary(review, n_points = 5, engine = 'curie'):
  '''
  return bullet point summary of a review
  '''
  response = openai.Completion.create(
    engine=engine,
    prompt=f"I need to summarise it in {n_points} sentences:\n\"\"\"\n{review}.\n\"\"\"\nI rephrased it in {n_points} bulletpoints:\n\"\"\"\n",
    temperature=0.2,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0,
    stop=["\"\"\""]
    )
  return response['choices'][0]['text'].split('. ')