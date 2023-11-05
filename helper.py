from wordcloud import WordCloud
import pandas as pd
from collections import Counter

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    #Num of Messages
    num_messages = df.shape[0]

    #Num of Words
    words = []

    for message in df['messages']:
        if message is not None:
            words.extend(message.split())

    #Num of Media Messages
    num_media_messages = df[df['messages'] == '<Media omitted>'].shape[0]


    return num_messages, len(words), num_media_messages

def most_busy_users(df):
    top_users = df['users'].value_counts().head()

    new_df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'precent'})

    return top_users, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=400, height=400, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=' '))

    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['messages'] != '<Media omitted>']

    words = []

    for message in temp['messages']:
        if message is not None:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(15))
    return_df.columns = ['Word', 'Count']

    return return_df


def most_busy_months(df):
    top_months = df['Month'].value_counts().head()

    return top_months

def most_busy_hours(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['Hour', 'am/pm']).count()['messages'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(str(timeline['Hour'][i]) + " " + str(timeline['am/pm'][i]))

    timeline['Time'] = time

    custom_order = ['12 am', '1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am', '10 am', '11 am',
                    '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm']

    timeline['Time'] = pd.Categorical(timeline['Time'], categories=custom_order, ordered=True)

    timeline = timeline.sort_values(by='Time')

    timeline = timeline.reset_index(drop=True)

    return timeline