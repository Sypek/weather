import streamlit as st
from utils.mocks import MockedKafkaOutputMessage
from src.consumer import consumer


st.set_page_config(layout="wide")
st.title(f"Weather dashboard :sunny::sun_small_cloud::sun_behind_cloud::sun_behind_rain_cloud:")
placeholder = st.empty()

def update_dashboard(message):
    weather = message.value['weather']
    metadata = message.value['metadata']
    last_update = metadata['close_time']

    with placeholder.container():
        col1, col2 = st.columns(2)
        col1.subheader('Temperature')
        col2.subheader('Pressure')

        col1.metric('Min', weather['temp']['min_val'])
        col1.metric('Max', weather['temp']['max_val'])
        col1.metric('Avg', weather['temp']['avg_val'])

        col2.metric('Min', weather['pressure']['min_val'])
        col2.metric('Max', weather['pressure']['max_val'])
        col2.metric('Avg', weather['pressure']['avg_val'])

        st.success(f'Last update: {last_update}', icon="✅")


def consume_weather_from_kafka():
    for message in consumer:
        update_dashboard(message)


if __name__ == '__main__':
    # m = MockedKafkaOutputMessage()
    consume_weather_from_kafka()