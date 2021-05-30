import streamlit as st
import pandas as pd
import altair as alt
from gpt_le_wagon.review_analyser import run_analysis
from gpt_le_wagon.wordcloud import get_wordcloud


# setting wide screen
st.set_page_config(layout="wide")

with st.beta_expander(label='🤗Creators of this App🤗', expanded=False):
    c1, c2, c3 = st.beta_columns((1,1,1))
    c1.image('https://res.cloudinary.com/dbxctsqiw/image/upload/v1622389459/gpt/T02NE0241-U01UPSN2MA7-142110bca3da-512_d8fcst.jpg', use_column_width=True)
    c2.image('https://res.cloudinary.com/dbxctsqiw/image/upload/v1622389455/gpt/Renato_Boemer_-_BW_ckccyj.jpg',  use_column_width=True)
    c3.image('https://res.cloudinary.com/dbxctsqiw/image/upload/v1622391317/profile_elwgth.jpg',  use_column_width=True)
    c1, c2, c3 = st.beta_columns((1,1,1))
    c1.markdown('''Zak Song''')
    c1.markdown('''[Linked In](https://www.linkedin.com/in/zak-gei-song-010725157/), [Github](https://github.com/songzeji)''')
    c2.markdown('''Renato Boemer''')
    c2.markdown('''[Linked In](https://www.linkedin.com/in/renatoboemer/), [Github](https://github.com/boemer00?tab=repositories)''')
    c3.markdown('''Jae Kim''')
    c3.markdown('''[Github](https://github.com/disney-snoopy/)''')

with st.beta_expander(label='💌Introduction💌', expanded=False):
    st.markdown('''
                ## Motivation
                Game developing companies are constantly improving the gaming experience so as to increase engagement and revenue.
                However, traditional approaches to understanding user experience and feedback, such as research, are expensive and time-consuming. Also, reading reviews to identify the criteria by which players evaluate the game experience, as well as their overall feeling towards the game, is challenging, if not completely unreliable. This is because people might have a different (or contrasting) interpretation of a review -- let alone how difficult it is for players to express their opinion through writing. Therefore, a human reviewer makes it difficult to reach reliable conclusions that support game development and business decisions.
                ## Out Solution
                ReviewRaven is powered by GPT-3 autoregressive language model that uses deep learning to interpret a human-like text. ReviewRaven creates clustering and sentiment analysis based on game reviews. It is a simple and easy online tool for game developers and companies that need quick text review interpretation and a sense of direction of what the customers think about a product. ReviewRaven saves time, money and offers consistent and reliable reports based on what customers/players say and feel.
                Just upload a CSV file and ReviewRaven outputs a dashboard with key stats and visual representation of the reviews. ReviewRaven will transform the way developers interact with gamers, enabling them to create a unique gaming experience whilst increasing revenue for the company.
                We are just starting, so watch this space!

                ''')


# sidebar for page navigation
st.sidebar.title('ReviewRaven with GPT-3')
# st.sidebar.subheader('Navigation')
# PAGES = ['Batch Analysis',
#          'Single Review Analysis']
# selection = st.sidebar.radio("Go to", list(PAGES))

engine_summary = st.sidebar.radio("Choose the language model for summary generation",
                                 ('davinci', 'curie', 'ada'))
engine_sentiment = st.sidebar.radio("Choose the language model for sentiment classification",
                                 ('davinci', 'curie', 'ada'))
engine_category = st.sidebar.radio("Choose the language model for category classification",
                                 ('davinci', 'curie', 'ada'))
st.sidebar.write('davinci is the most powerful and the most costly engine and ada is the fastest and the most affordable engine.')


c1, c2 = st.beta_columns((1,3))

uploaded_file = c1.file_uploader(label = 'Upload your game review excel file.', type=['csv'], accept_multiple_files=False)


if uploaded_file != None:
    df_reviews = pd.read_csv(uploaded_file)

    reviews = list(df_reviews.iloc[:, 0])
    df_result = run_analysis(reviews, engine_summary = engine_summary, engine_sentiment = engine_sentiment, engine_category = engine_category, debug = False)
#    st.write(df_result.shape)

    df_result['score'] = df_result['sentiment']
    df_result['score'] = df_result['score'].replace({'Positive':1, 'Neutral':0, 'Negative':-1})
#    st.write(df_result)

    a = df_result.groupby('category').mean().reset_index()
    a.columns = ['category', 'avg_score']


    chart_category = alt.Chart(df_result).mark_bar().encode(
                                                            x=alt.X('sentiment:N', title = None),
                                                            y=alt.Y('count(sentiment):Q', title = 'Sentiment Count'),
                                                            color=alt.Color('sentiment:N'),
                                                            column= alt.Column('category:N', title = 'Review Sentiment by Category')
                                                            ).properties(width = 400, height = 400)

    c1, c2, c3, c4 = st.beta_columns((1,1,1,1))
    c1.write(chart_category)
    c1, c2 = st.beta_columns((1,1))
    category_list =list(pd.unique(df_result['category']))
    for category in category_list:
        with st.beta_expander(label=f'{category}', expanded=False):
            c1, c2 = st.beta_columns((1,1))
            c1.subheader('Positive Reviews')
            c2.subheader('Negative Reviews')
            df_temp = df_result[df_result['category'] == f'{category}'][['summary', 'sentiment']]
            df_temp_pos = df_temp[df_temp['sentiment'] == 'Positive'][['summary']].drop_duplicates()['summary']
            df_temp_neg = df_temp[df_temp['sentiment'] == 'Negative'][['summary']].drop_duplicates()['summary']
            if df_temp_pos.shape[0] > 0:
                for row in df_temp_pos:
                    c1.markdown(f'''
                                - {row}
                                ''')
            else:
                c1.write('No Positive reviews')

            if df_temp_neg.shape[0] > 0:
                for row in df_temp_neg:
                    c2.markdown(f'''
                                - {row}
                                ''')
            else:
                c2.write('No Positive reviews')

    fig_wordcloud = get_wordcloud(df_reviews)
    st.write(fig_wordcloud)










