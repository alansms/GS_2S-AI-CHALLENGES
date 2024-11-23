Documentação do Projeto: Uso de Visão Computacional para Otimização de Energia

Introdução

Este projeto tem como objetivo explorar o potencial da visão computacional na otimização do consumo de energia em ambientes urbanos. A solução desenvolvida utiliza OpenCV e MediaPipe para processar gestos humanos capturados por uma câmera, permitindo o controle de dispositivos físicos via protocolo MQTT. Esta aplicação demonstra uma integração eficiente entre software de visão computacional e hardware IoT, resultando em um sistema inteligente de gestão energética.

Descrição da Solução

A solução foca no reconhecimento de gestos humanos para ativar ou desativar dispositivos de iluminação. Utilizando uma câmera, o sistema analisa os gestos em tempo real. Quando o gesto de “jóia” (polegar para cima) é detectado, uma mensagem é enviada via MQTT para um dispositivo físico conectado, que acende ou apaga as luzes.

Este sistema foi projetado para:
	1.	Captura de Imagens: Frames são obtidos a partir de uma câmera conectada.
	2.	Processamento de Imagens: MediaPipe detecta landmarks da mão no frame.
	3.	Reconhecimento de Gesto: A lógica avalia se o gesto de “jóia” foi realizado.
	4.	Ação Física: Um comando é enviado para o dispositivo de iluminação via MQTT.

A solução se aplica especialmente em ambientes públicos, como praças e parques, onde o acionamento de luzes é necessário apenas em momentos específicos, reduzindo o desperdício de energia.

Pipeline da Solução

	1.	Entrada: Frames são capturados em tempo real por uma câmera conectada via Wi-Fi.
	2.	Processamento:
	•	MediaPipe detecta landmarks das mãos.
	•	Uma lógica verifica se o gesto de “jóia” foi identificado.
	3.	Saída:
	•	Caso o gesto seja detectado, uma mensagem MQTT é publicada para ativar ou desativar as luzes.
	4.	Hardware:
	•	Dispositivos IoT, como relés e controladores, executam a ação com base no comando recebido.

Funcionamento e Impactos

O sistema é implementado em Python e utiliza bibliotecas como OpenCV para processamento de imagens e MediaPipe para reconhecimento de gestos. A comunicação com dispositivos físicos é feita através do protocolo MQTT.

Impactos da solução:
	•	Eficiência Energética: As luzes são acionadas apenas quando necessário, reduzindo o desperdício de energia.
	•	Sustentabilidade: Criação de ambientes inteligentes que consomem menos recursos.
	•	Escalabilidade: Pode ser adaptado para outros cenários, como controle de ar-condicionado ou segurança.

Código-Fonte

O código-fonte integra captura de imagens, reconhecimento de gestos e envio de comandos MQTT. Ele está dividido em três partes principais:
	1.	Captura de Frames: Frames são obtidos de uma câmera conectada via Wi-Fi.
	2.	Processamento de Gesto: MediaPipe detecta landmarks e verifica o gesto de “jóia”.
	3.	Envio de Comandos: Comandos MQTT são enviados para dispositivos IoT.

Conclusão

A solução apresentada demonstra como a visão computacional pode ser aplicada na otimização de energia em locais públicos. Apesar de ser uma implementação parcial, ela ilustra o potencial de escalabilidade e impacto sustentável desta abordagem. O uso de tecnologias como OpenCV, MediaPipe e MQTT cria um sistema autônomo eficiente, que pode ser integrado a outros dispositivos IoT.

Link do Vídeo
