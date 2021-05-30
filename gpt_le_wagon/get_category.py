from gpt_le_wagon.utils import *
import openai

# load api key
openai.api_key = API_KEY

def get_category(input_sentence, examples_criteria, labels, engine = 'curie'):
  response = openai.Classification.create(
                examples = examples_criteria,
                labels = labels,
                query = input_sentence,
                search_model = engine,
                model = engine
                )
  return response['label']