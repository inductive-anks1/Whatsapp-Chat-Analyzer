import streamlit as st
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import plotly.graph_objs as go


st.sidebar.title('Whatsapp Chat Analyzer')

upload_file = st.sidebar.file_uploader('Chosse a file')

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    #user_list.remove('None')
    #user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        num_messages, words, num_media_messages = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<h1 style="font-size:24px">Total Messages</h1>', unsafe_allow_html=True)
            st.write(f"<h2 style='font-size:24px'>{num_messages}</h2>", unsafe_allow_html=True)

        with col2:
            st.markdown('<h1 style="font-size:24px">Total Words</h1>', unsafe_allow_html=True)
            st.write(f"<h2 style='font-size:24px'>{words}</h2>", unsafe_allow_html=True)

        with col3:
            st.markdown('<h2 style="font-size:24px">Media Shared</h2>', unsafe_allow_html=True)
            st.write(f"<h2 style='font-size:24px'>{num_media_messages}</h2>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # finding the busiest users in the group(overall)

        if selected_user == 'Overall':
            st.title('Most Active Users')
            top_users, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                fig = make_subplots(rows=1, cols=1)

                # Create the bar plot using Plotly Express
                bar_fig = px.bar(top_users, x=top_users.index, y=top_users.values,
                                 labels={'x': 'Users', 'y': 'Message Count'},
                                 color_discrete_sequence=['#FC0080'])

                # Add the bar plot to the subplot
                fig.add_trace(bar_fig.data[0])

                fig.update_layout(title_text='Top Most Active Users')

                # Display the subplots using st.plotly_chart
                st.plotly_chart(fig)

        st.markdown("<br>", unsafe_allow_html=True)

        st.title('Word Cloud of the Messages')
        #Wordcloud
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.markdown("<br>", unsafe_allow_html=True)

        #Most common words
        st.title('Top 15 Most Common Words')

        most_common_df = helper.most_common_words(selected_user, df)

        fig = make_subplots(rows=1, cols=1)

        bar_fig = px.bar(most_common_df, x='Word', y='Count',
                         labels={'x': 'Word', 'y': 'Word Count'},
                         color_discrete_sequence=['#FC0080'])
        # Add the bar plot to the subplot
        fig.add_trace(bar_fig.data[0])
        fig.update_layout(title_text='Top 15 Most Common Words')

        # Display the subplots using st.plotly_chart
        st.plotly_chart(fig)

        st.markdown("<br>", unsafe_allow_html=True)

        st.title('Top Most Busy Months')


        #Most Busy Months
        top_months = helper.most_busy_months(df)
        fig = make_subplots(rows=1, cols=1)

        # Create the bar plot using Plotly Express
        bar_fig = px.bar(top_months, x=top_months.index, y=top_months.values,
                         labels={'x': 'Months', 'y': 'Message Count'},
                         color_discrete_sequence=['#FC0080'])

        # Add the bar plot to the subplot
        fig.add_trace(bar_fig.data[0])

        fig.update_layout(title_text='Most Active Months')

        # Display the subplots using st.plotly_chart
        st.plotly_chart(fig)