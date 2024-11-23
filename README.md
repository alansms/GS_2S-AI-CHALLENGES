# Documentação do Projeto: Uso de Visão Computacional para Otimização de Energia

Video de demostração: https://youtu.be/YO42yXDJGuU


## Introdução
Este projeto tem como objetivo explorar o potencial da visão computacional na otimização do consumo de energia em ambientes urbanos. A solução desenvolvida utiliza **OpenCV** e **MediaPipe** para processar gestos humanos capturados por uma câmera, permitindo o controle de dispositivos físicos via protocolo **MQTT**. Esta aplicação demonstra uma integração eficiente entre software de visão computacional e hardware IoT, resultando em um sistema inteligente de gestão energética.

---

## Descrição da Solução
A solução foca no reconhecimento de gestos humanos para ativar ou desativar dispositivos de iluminação. Utilizando uma câmera, o sistema analisa os gestos em tempo real. Quando o gesto de **“jóia”** (polegar para cima) é detectado, uma mensagem é enviada via **MQTT** para um dispositivo físico conectado, que acende ou apaga as luzes.

### Componentes do Sistema:
1. **Captura de Imagens**: Frames são obtidos a partir de uma câmera conectada via Wi-Fi.
2. **Processamento de Imagens**: MediaPipe detecta landmarks da mão no frame.
3. **Reconhecimento de Gesto**: A lógica avalia se o gesto de **“jóia”** foi realizado.
4. **Ação Física**: Um comando é enviado para o dispositivo de iluminação via **MQTT**.

### Aplicações:
A solução se aplica especialmente em ambientes públicos, como praças e parques, onde o acionamento de luzes é necessário apenas em momentos específicos, reduzindo o desperdício de energia.

---

## Pipeline da Solução
1. **Entrada**:
   - Frames capturados em tempo real por uma câmera conectada via Wi-Fi.

2. **Processamento**:
   - **MediaPipe** detecta landmarks das mãos.
   - A lógica verifica se o gesto de **“jóia”** foi identificado.

3. **Saída**:
   - Caso o gesto seja detectado, uma mensagem MQTT é publicada para ativar ou desativar as luzes.

4. **Hardware**:
   - Dispositivos IoT, como relés e controladores, executam a ação com base no comando recebido.

---

## Funcionamento e Impactos
O sistema é implementado em Python e utiliza bibliotecas como **OpenCV** para processamento de imagens e **MediaPipe** para reconhecimento de gestos. A comunicação com dispositivos físicos é feita através do protocolo **MQTT**.

### Impactos da Solução:
- **Eficiência Energética**: As luzes são acionadas apenas quando necessário, reduzindo o desperdício de energia.
- **Sustentabilidade**: Criação de ambientes inteligentes que consomem menos recursos.
- **Escalabilidade**: Pode ser adaptado para outros cenários, como controle de ar-condicionado ou segurança.

---

## Código-Fonte

### Configuração do MQTT
```python
# Configurações MQTT
MQTT_BROKER = "173.21.100.8"
MQTT_PORT = 1883
MQTT_USERNAME = "sms"
MQTT_PASSWORD = "23pipocas"
MQTT_TOPIC = "casa/luz"
MQTT_AVAILABILITY_TOPIC = "casa/luz/availability"

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
    except Exception as e:
        logging.error(f"Erro ao capturar a imagem: {e}")
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

# Função de envio de comando MQTT ao detectar gesto
def send_mqtt_command():
    client.publish(MQTT_TOPIC, "ON")
    logging.info("Comando MQTT enviado: ON")

# Função para exibir a detecção de movimento com MediaPipe
def show_camera():
    st.title("Detecção de Gesto com MediaPipe")
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
                        st.success("Gesto de 'Jóia' detectado!")
                        send_mqtt_command()

            stframe.image(frame, channels="BGR", use_column_width=True)

Conclusão

A solução apresentada demonstra como a visão computacional pode ser aplicada na otimização de energia em locais públicos. Apesar de ser uma implementação parcial, ela ilustra o potencial de escalabilidade e impacto sustentável desta abordagem. O uso de tecnologias como OpenCV, MediaPipe e MQTT cria um sistema autônomo eficiente, que pode ser integrado a outros dispositivos IoT.

📜 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

👨‍💻 Autores

Desenvolvido por: Alan de Souza Maximiano – 557088.
Danilo Ramalho Silva – 555183
João Vitor Pires da Silva – 556213

Contato: alan.maximiano@gmail.com

