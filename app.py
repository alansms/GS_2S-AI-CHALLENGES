import requests
from PIL import Image, UnidentifiedImageError
import numpy as np
import cv2
import mediapipe as mp
import streamlit as st
import paho.mqtt.client as mqtt
import logging
import time
from io import BytesIO
import plotly.graph_objs as go
import pandas as pd

# Configurações MQTT
MQTT_BROKER = "173.21.100.8"
MQTT_PORT = 1883
MQTT_USERNAME = "sms"
MQTT_PASSWORD = "23pipocas"
MQTT_TOPIC = "casa/luz"
MQTT_AVAILABILITY_TOPIC = "casa/luz/availability"

# Configuração de logs
logging.basicConfig(level=logging.INFO)

# Callback para conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado ao MQTT Broker com sucesso.")
        client.publish(MQTT_AVAILABILITY_TOPIC, "online", retain=True)
    else:
        logging.error(f"Erro ao conectar ao MQTT. Código: {rc}")

# Callback para publicação
def on_publish(client, userdata, mid):
    logging.info(f"Mensagem publicada com sucesso. ID: {mid}")

# Callback para desconexão
def on_disconnect(client, userdata, rc):
    logging.warning("Desconectado do MQTT Broker.")
    if rc != 0:
        logging.error("Desconexão inesperada. Tentando reconectar...")
    client.publish(MQTT_AVAILABILITY_TOPIC, "offline", retain=True)

# Configuração do cliente MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Conectando ao broker MQTT
logging.info("Tentando conectar ao MQTT Broker...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Função para capturar frames da câmera
def get_frame_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.verify()
        img = Image.open(BytesIO(response.content))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame
    except UnidentifiedImageError:
        logging.error("O conteúdo retornado pelo URL não é uma imagem válida.")
        st.error("Erro: O conteúdo retornado pelo URL não é uma imagem válida.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na conexão com o stream: {e}")
        st.error(f"Erro ao conectar ao stream: {e}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao capturar a imagem: {e}")
        st.error(f"Erro inesperado ao capturar a imagem: {e}")
        return None

# Função para verificar se o gesto de "jóia" foi detectado
def is_thumb_up(landmarks, width, height):
    try:
        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]
        wrist = landmarks[0]

        thumb_up = thumb_tip.y < index_mcp.y and thumb_tip.y < wrist.y
        thumb_positioned = abs(thumb_tip.x - wrist.x) > 0.1
        return thumb_up and thumb_positioned
    except Exception as e:
        logging.error(f"Erro ao verificar o gesto 'jóia': {e}")
        return False

# Função para exibir a detecção de movimento com MediaPipe
def show_camera():
    st.title("Detecção de Gesto com MediaPipe")
    st.text("Insira o URL da câmera para começar.")

    camera_url = st.text_input("Endereço do stream (URL ou IP):", value="http://192.168.4.1/cam-hi.jpg")
    if not camera_url:
        st.warning("Insira o endereço do stream para iniciar.")
        return

    stframe = st.empty()
    stop_button = st.button("Parar", key="stop_button")

    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
        while not stop_button:
            frame = get_frame_from_url(camera_url)
            if frame is None:
                st.error("Erro ao capturar frames. Verifique o stream.")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if is_thumb_up(hand_landmarks.landmark, frame.shape[1], frame.shape[0]):
                        st.success("Gesto de 'Jóia' detectado! Enviando comando MQTT...")
                        logging.info("Gesto de 'Jóia' detectado!")
                        client.publish(MQTT_TOPIC, "ON")
                        st.balloons()
                        thumb_tip = hand_landmarks.landmark[4]
                        thumb_tip_x = int(thumb_tip.x * frame.shape[1])
                        thumb_tip_y = int(thumb_tip.y * frame.shape[0])
                        cv2.circle(frame, (thumb_tip_x, thumb_tip_y), 10, (0, 255, 0), -1)

            stframe.image(frame, channels="BGR", use_column_width=True)

    st.info("Monitoramento encerrado.")

# Funções para gráficos e sugestões de economia de energia
def generate_sample_data():
    dates = pd.date_range(start="2023-03-01", periods=31, freq="D")
    energy_data = np.random.randint(5000, 7000, size=(31,))
    return dates, energy_data

def show_graphs():
    st.title("Painel de Monitoramento de Energia")
    dates, energy_data = generate_sample_data()

    st.subheader("Perfil de Carga")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=energy_data, mode='lines+markers', name="Demanda"))
    fig.update_layout(
        title="Perfil de Carga",
        xaxis_title="Data",
        yaxis_title="Consumo (kW)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_suggestions():
    st.title("Sugestões de Economia de Energia")
    total_consumption = st.number_input("Digite o consumo total de energia (kWh):", min_value=1)
    time_period = st.text_input("Digite o período de tempo:", value="Mar/2024")
    if st.button("Gerar Sugestão"):
        st.subheader("Sugestão de Economia de Energia")
        st.write(f"Sugestões para {time_period} com {total_consumption} kWh consumidos.")

# Navegação entre páginas
page = st.sidebar.radio("Escolha uma opção", ["Detecção de Gesto", "Gráficos", "Sugestões de Economia"])

if page == "Detecção de Gesto":
    show_camera()
elif page == "Gráficos":
    show_graphs()
elif page == "Sugestões de Economia":
    show_suggestions()