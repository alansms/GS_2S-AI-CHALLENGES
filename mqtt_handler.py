import paho.mqtt.client as mqtt
import logging
import json
from config import MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_TOPIC

# Configuração de log
logging.basicConfig(level=logging.INFO)

# Função de conexão com o broker MQTT
def on_connect(client, userdata, flags, rc):
    logging.info(f"Conectado ao broker MQTT com código {rc}")
    client.subscribe(MQTT_TOPIC)  # Assinando o tópico MQTT

# Função que é chamada quando uma mensagem é recebida no tópico
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        logging.info(f"Dados recebidos: {payload}")

        # Aqui você pode acessar os dados de consumo específicos
        if 'consumo' in payload:  # Ajuste para o campo correto no payload
            # Atualize a variável global ou session_state
            logging.info(f"Consumo total: {payload['consumo']} kWh")
        else:
            logging.warning("Mensagem sem dados de consumo")
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar a mensagem: {e}")

# Função para configurar o cliente MQTT
def setup_mqtt():
    client = mqtt.Client()  # Criação do cliente MQTT
    client.on_connect = on_connect  # Função chamada na conexão
    client.on_message = on_message  # Função chamada ao receber mensagem
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  # Autenticação
    client.connect(MQTT_HOST, MQTT_PORT, 60)  # Conexão com o broker
    return client

# Função para iniciar o cliente MQTT em uma thread separada
def start_mqtt():
    client = setup_mqtt()
    client.loop_start()  # Inicia a escuta do MQTT