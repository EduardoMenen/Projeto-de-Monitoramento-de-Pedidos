![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.x-0C4B33?style=for-the-badge&logo=django)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.x-FF6600?style=for-the-badge&logo=rabbitmq)
![WebSockets](https://img.shields.io/badge/WebSockets-Enabled-4A90E2?style=for-the-badge&logo=websocket)

## 📚 Índice
- [Descrição do Projeto](#-descrição-do-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Configuração e comandos para rodar](#configuração-e-comandos-para-rodar)
- [Autor](#autor)

## 🎯 Descrição do Projeto

Este projeto implementa um sistema **distribuído de monitoramento de pedidos em tempo real**, utilizando mensageria e comunicação assíncrona entre serviços.

O objetivo é demonstrar uma arquitetura moderna onde:

- o envio de pedidos é desacoplado do processamento,
- os serviços se comunicam por meio de uma fila (RabbitMQ),
- um consumidor independente processa as mensagens,
- e o resultado aparece **instantaneamente** na interface usando WebSockets.

A solução foi projetada para ser simples, escalável e demonstrar conceitos reais de sistemas distribuídos utilizados na indústria.

## 🛠 Tecnologias Utilizadas

- **Python 3.10+**
- **Django 4.x** — Backend e envio de mensagens à fila
- **Django Channels** — Comunicação WebSocket em tempo real
- **RabbitMQ** — Fila de mensagens responsável pela comunicação assíncrona
- **Pika** — Cliente Python para integração com o RabbitMQ
- **HTML + CSS + JavaScript** — Interfaces de envio e monitoramento
- **ASGI** — Servidor assíncrono para WebSockets
- **Docker / Docker Compose (opcional)** — Conteiners para teste preciso

## Configuração e comandos para rodar

#### **Clonar o repositório**:
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO

#### **Criar ambiente virtual**:
Windows:
python -m venv venv
venv\Scripts\activate

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

#### **Instalar dependências**:
pip install -r requirements.txt

#### **Iniciar o RabbitMQ:**
Windows:
net start RabbitMQ

Linux:
sudo systemctl start rabbitmq-server

#### **Iniciar o Servidor ASGI (Django + Channels) com Daphne**

Como o projeto utiliza **WebSockets** através do Django Channels, o servidor padrão (`runserver`) não é indicado para produção.  
Por isso, utilizamos o **Daphne**, o servidor ASGI oficial do Django Channels.

Para iniciar o servidor:

daphne -p 8000 order_monitor.asgi:application

## 👨‍💻 Autores

**Eduardo Menegazzo**

**Eduardo Zambenedetti**

**Vitor Valduga Modesti**

Sempre aberto a colaboração e novas ideias!