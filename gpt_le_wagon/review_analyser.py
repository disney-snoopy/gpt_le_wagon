import pandas as pd
import numpy as np
import openai
import os
from gpt_le_wagon.get_summary import get_summary
from gpt_le_wagon.get_category import get_category
from gpt_le_wagon.get_sentiment import get_sentiment
from gpt_le_wagon.utils import *





def run_analysis(reviews, engine_summary = 'curie', engine_sentiment = 'curie', engine_category = 'curie', debug = False):

    # load sample dataframe
    df_training = pd.read_csv('raw_data/sentence_category-sentence_category_short.csv')
    categories = list(pd.unique(df_training['criteria']))

    # creating training samples for category classification
    examples_criteria = []
    for row in df_training.iterrows():
        example_criteria = []
        example_criteria.append(row[1]['review'].strip())
        example_criteria.append(row[1]['criteria'])
        examples_criteria.append(example_criteria)

    # creating training samples for sentiment classification
    examples_sentiment = []
    for row in df_training.iterrows():
        example_sentiment = []
        example_sentiment.append(row[1]['review'].strip())
        example_sentiment.append(row[1]['label'])
        examples_sentiment.append(example_sentiment)

    if debug:
        examples_sentiment = examples_sentiment[:3]
        examples_criteria = examples_criteria[:3]

    list_summaries = []
    list_category = []
    list_sentiment = []
    for review in reviews:
        summaries = get_summary(review, n_points=3, engine=engine_summary)
        for sentence in summaries:
            sentiment = get_sentiment(sentence, engine=engine_sentiment, examples_sentiment = examples_sentiment)
            category = get_category(sentence, examples_criteria, categories, engine=engine_category)
            list_summaries.append(sentence)
            list_sentiment.append(sentiment)
            list_category.append(category)

    df = pd.DataFrame()
    df['summary'] = np.array(list_summaries)
    df['category'] = np.array(list_category)
    df['sentiment'] = np.array(list_sentiment)

    return df


