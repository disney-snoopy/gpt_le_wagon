from gpt_le_wagon.utils import *
import openai

# load api key
openai.api_key = API_KEY

def get_sentiment(sentence, examples_sentiment, engine = 'curie'):
  response = openai.Classification.create(
                examples = examples_sentiment,
                labels = ["positive", "negative", "neutral"],
                query = sentence,
                search_model = "ada",
                model = engine
                )
  return response['label']