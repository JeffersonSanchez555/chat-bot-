import os
import random
import re
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# 1. Importamos y cargamos dotenv para leer el archivo .env de forma segura
from dotenv import load_dotenv
load_dotenv()

# Importamos la librería oficial de Google GenAI
from google import genai
from google.genai import types

# Inicializamos el cliente de Gemini (detectará automáticamente el GEMINI_API_KEY del .env)
client = genai.Client()

app = FastAPI(title="Chatbot sangresia bot", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


async def generar_respuesta(mensaje: str) -> str:
    """Función para generar la respuesta utilizando Gemini."""
    try:
        # Prompt de sistema para darle personalidad a Shena / CeniChat
        system_instruction = (
            "Eres Shena, un asistente virtual experto en la oferta educativa "
            "del Centro para la Industria de la Comunicación Gráfica (CENIGRAF) del SENA en Colombia. "
            "Responde de forma amable, clara y concisa a preguntas sobre programas, inscripciones, "
            "requisitos, contratos de aprendizaje y contacto."
        )

        # Usamos el modelo recomendado (gemini-2.5-flash)
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=mensaje,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        print(f"Error al conectar con Gemini: {e}")
        return "Lo siento, ocurrió un error al procesar tu solicitud con la inteligencia artificial."


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # Agregamos 'await' porque las llamadas a la API de Gemini son asíncronas/externas
    respuesta = await generar_respuesta(request.message)
    return ChatResponse(reply=respuesta)


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CeniChat - Asistente CENIGRAF</title>
  <!-- Bootstrap 5 CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- FontAwesome para iconos -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
      body {
          background-color: #0b0b0e;
          color: #e4e4e7;
          height: 100vh;
          display: flex;
          flex-direction: column;
          margin: 0;
      }
      .chat-container {
          max-width: 800px;
          width: 100%;
          height: 100vh;
          margin: auto;
          display: flex;
          flex-direction: column;
          background: #141418;
          border: 1px solid #23232c;
          box-shadow: 0 4px 20px rgba(0,0,0,0.5);
          overflow: hidden;
      }
      .chat-header {
          background-color: #241930;
          color: #f3e8ff;
          padding: 15px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 1px solid #322342;
      }
      .chat-messages {
          flex: 1;
          padding: 15px;
          overflow-y: auto;
          background-color: #0e0e11;
          display: flex;
          flex-direction: column;
          gap: 10px;
      }
      .message {
          max-width: 75%;
          padding: 10px 15px;
          border-radius: 15px;
          font-size: 0.95rem;
          word-wrap: break-word;
          white-space: pre-wrap;
      }
      .message.user {
          background-color: #432c5c;
          color: #f3e8ff;
          align-self: flex-end;
          border-bottom-right-radius: 2px;
      }
      .message.bot {
          background-color: #1a1a21;
          color: #e4e4e7;
          align-self: flex-start;
          border: 1px solid #2e2e3d;
          border-bottom-left-radius: 2px;
      }
      .faq-container {
          padding: 10px 15px;
          background: #141418;
          border-top: 1px solid #23232c;
          display: flex;
          gap: 8px;
          overflow-x: auto;
          white-space: nowrap;
      }
      .faq-btn {
          background-color: #241930;
          border: 1px solid #3b284e;
          border-radius: 20px;
          padding: 5px 12px;
          font-size: 0.85rem;
          color: #d8b4fe;
          cursor: pointer;
          transition: all 0.2s;
      }
      .faq-btn:hover {
          background-color: #432c5c;
          color: white;
      }
      .typing-indicator {
          font-style: italic;
          color: #a1a1aa;
          font-size: 0.85rem;
          display: none;
          padding: 5px 15px;
          background-color: #0e0e11;
      }
      .chat-input-area {
          padding: 15px;
          background: #141418;
          border-top: 1px solid #23232c;
          display: flex;
          gap: 10px;
      }
      .form-control {
          background-color: #1a1a21;
          border: 1px solid #31313f;
          color: #fff;
      }
      .form-control:focus {
          background-color: #1a1a21;
          color: #fff;
          border-color: #5d3e80;
          box-shadow: 0 0 0 0.25rem rgba(93, 62, 128, 0.25);
      }
      .btn-purple {
          background-color: #432c5c;
          color: #f3e8ff;
          border: none;
      }
      .btn-purple:hover {
          background-color: #533772;
          color: white;
      }
      @media (min-width: 768px) {
          .chat-container {
              height: 90vh;
              border-radius: 10px;
              margin-top: 5vh;
          }
      }
  </style>
</head>
<body>

    <div class="chat-container">
        <!-- Encabezado -->
        <div class="chat-header">
            <div>
                <h5 class="mb-0"><i class="fas fa-robot me-2"></i>CeniChat - Shena</h5>
                <small class="text-purple-50">Asistente Oferta Educativa CENIGRAF</small>
            </div>
            <button id="clear-btn" class="btn btn-outline-light btn-sm" title="Limpiar chat">
                <i class="fas fa-trash-alt"></i> Limpiar
            </button>
        </div>

        <!-- Área de mensajes -->
        <div id="chat-messages" class="chat-messages">
            <div class="message bot">
                ¡Hola! Soy <strong>Shena</strong>, tu asistente virtual potenciada con Gemini. Escribe un mensaje o selecciona una pregunta frecuente para empezar.
            </div>
        </div>

        <!-- Indicador de respuesta (Escribiendo...) -->
        <div id="typing-indicator" class="typing-indicator">
            <i class="fas fa-spinner fa-spin me-1"></i> El chatbot está escribiendo...
        </div>

        <!-- Botones de Preguntas Frecuentes -->
        <div class="faq-container">
            <button class="faq-btn" onclick="sendFaq('¿Qué programas ofrece CENIGRAF?')">Programas CENIGRAF</button>
            <button class="faq-btn" onclick="sendFaq('Requisitos de inscripción')">Requisitos</button>
            <button class="faq-btn" onclick="sendFaq('Información de contacto')">Contacto</button>
            <button class="faq-btn" onclick="sendFaq('Contrato de aprendizaje')">Contrato de aprendizaje</button>
        </div>

        <!-- Campo de escritura -->
        <div class="chat-input-area">
            <input type="text" id="user-input" class="form-control" placeholder="Escribe tu mensaje…" required maxlength="2000" autocomplete="off">
            <button id="send-btn" class="btn btn-purple"><i class="fas fa-paper-plane"></i></button>
        </div>
    </div>

  <script>
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-btn');
    const typingIndicator = document.getElementById('typing-indicator');

    function appendMessage(senderType, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', senderType);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function toggleTyping(show) {
        typingIndicator.style.display = show ? 'block' : 'none';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage(text) {
        const message = text.trim();
        if (!message) return;

        appendMessage('user', message);
        userInput.value = '';
        toggleTyping(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) throw new Error('No se pudo obtener una respuesta del servidor.');

            const data = await response.json();
            toggleTyping(false);
            appendMessage('bot', data.reply);
        } catch (error) {
            toggleTyping(false);
            appendMessage('bot', `Error: ${error.message}`);
        }
    }

    function sendFaq(question) {
        sendMessage(question);
    }

    sendBtn.addEventListener('click', () => {
        sendMessage(userInput.value);
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage(userInput.value);
        }
    });

    clearBtn.addEventListener('click', () => {
        if (confirm('¿Estás seguro de que deseas limpiar la conversación?')) {
            chatMessages.innerHTML = `
                <div class="message bot">
                    ¡Hola! Soy <strong>Shena</strong>, tu asistente virtual. Escribe un mensaje o selecciona una pregunta frecuente para empezar.
                </div>
            `;
        }
    });
  </script>
  <!-- Bootstrap 5 JS Bundle -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""