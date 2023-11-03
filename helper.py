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
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]




    return num_messages, len(words), num_media_messages