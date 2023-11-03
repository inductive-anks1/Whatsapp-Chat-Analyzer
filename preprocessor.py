import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = df['message_date'].str.replace(' - ', '')
    df['message_date'] = df['message_date'].str.replace(' ', '')

    df[['date', 'Time']] = df['message_date'].str.split(',', expand=True)

    users = []
    messages = []

    for message in df['user_message']:
        try:
            entry = re.split(': ', message, 1)
            if len(entry) > 1:
                users.append(entry[0])
                messages.append(entry[1].strip())
            else:
                users.append(None)
                messages.append(None)
        except:
            users.append(None)
            messages.append(None)

    df['users'] = users
    df['messages'] = messages

    df.drop(columns=['user_message'], inplace=True)

    time_pattern = r'(\d+:\d+)\s([ap]m)'
    df[['Time', 'am/pm']] = df['Time'].str.extract(time_pattern)

    df = df[['users', 'messages', 'message_date', 'date', 'Time', 'am/pm']]
    df = df.drop(columns=['message_date'])

    df[['Day', 'Month', 'Year']] = df['date'].str.split('/', expand=True).astype(int)

    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    df['Month'] = df['Month'].replace(month_names)

    time_pattern = r'(\d+):(\d+)'

    df[['Hour', 'Minute']] = df['Time'].str.extract(time_pattern)

    df['Hour'] = df['Hour'].astype(int)
    df['Minute'] = df['Minute'].astype(int)

    return df
