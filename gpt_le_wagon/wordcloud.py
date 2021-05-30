from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_wordcloud(df):
    text = " ".join(review for review in df['reviews'])
    wordcloud = WordCloud().generate(text)
    # Create and generate a word cloud image
    wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white").generate(text)
    fig, ax = plt.subplots(1,1, figsize = (20, 8))
    # Display the generated image
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    return fig