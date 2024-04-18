import streamlit as st
from utils.mocks import MockedKafkaOutputMessage
from src.front.consumer import consumer

st.set_page_config(layout="wide")
st.title(f"Weather dashboard :sunny::sun_small_cloud::sun_behind_cloud::sun_behind_rain_cloud:")
placeholder = st.empty()


def update_dashboard(message, prev_message = None):
    weather = message.value['weather']
    metadata = message.value['metadata']
    last_update = metadata['close_time']

    min_temp = weather['temp']['min_val']
    max_temp = weather['temp']['max_val']
    avg_temp = weather['temp']['avg_val']

    min_pressure = weather['pressure']['min_val']
    max_pressure = weather['pressure']['max_val']
    avg_pressure = weather['pressure']['avg_val']

    delta_min_temp = None
    delta_max_temp = None
    delta_avg_temp = None
    delta_min_pressure = None
    delta_max_pressure = None
    delta_avg_pressure = None

    if prev_message:
        prev_weather = prev_message.value['weather']

        delta_min_temp = min_temp - prev_weather['temp']['min_val']
        delta_max_temp = max_temp - prev_weather['temp']['max_val']
        delta_avg_temp = avg_temp - prev_weather['temp']['avg_val']

        delta_min_pressure = min_pressure - prev_weather['pressure']['min_val']
        delta_max_pressure = max_pressure - prev_weather['pressure']['max_val']
        delta_avg_pressure = avg_pressure - prev_weather['pressure']['avg_val']


    with placeholder.container():
        col1, col2 = st.columns(2)
        col1.subheader('Temperature')
        col2.subheader('Pressure')

        col1.metric('Min', min_temp, delta=delta_min_temp)
        col1.metric('Max', max_temp, delta=delta_max_temp)
        col1.metric('Avg', avg_temp, delta=delta_avg_temp)

        col2.metric('Min', min_pressure, delta=delta_min_pressure)
        col2.metric('Max', max_pressure, delta=delta_max_pressure)
        col2.metric('Avg', avg_pressure, delta=delta_avg_pressure)

        st.success(f'Last update: {last_update}', icon="✅")


def consume_weather_from_kafka():
    """
    TODO: desc
    Storing previous message to calculate delta.
    """
    for message in consumer:
        if 'prev_message' in st.session_state:
            update_dashboard(message, st.session_state['prev_message'])
        else:
            update_dashboard(message)
            
        st.session_state['prev_message'] = message


if __name__ == '__main__':
    # m = MockedKafkaOutputMessage()
    consume_weather_from_kafka()