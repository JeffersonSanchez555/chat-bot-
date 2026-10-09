"""Chatbot básico con API HTTP y una interfaz web mínima."""

from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Chatbot básico", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


def responder(mensaje: str) -> str:
    """Genera una respuesta por reglas; reemplaza esta función para usar un LLM."""
    texto = mensaje.strip().lower()

    # --- Respuestas por defecto ---
    if any(saludo in texto for saludo in ("hola", "buenas", "hey", "parcerito")):
        return "HOLA, ¿En que te puedo ayudar mi sangreee?"
    if "nombre" in texto:
        return "Soy cule bot insano programado en el piton XD."
    if any(palabra in texto for palabra in ("adiós", "chao", "hasta luego")):
        return "La re buena mi sg, Dios lo bendiga ."
    if "ayuda" in texto:
        return "Que quiere saber mi sg sobre los programas del rio SENA XD, tecnicos o tecnologos??"

    
    
    
    if any(p in texto for p in ("inscripcion", "inscripciones", "inscrito", "abierta", "abiertas")):
        return "Actualmente todas las inscripciones se encuentran en estado: 'Inscripciones NO abiertas'."

   
    if any(p in texto for p in ("software", "adso", "programacion")):
        return "El programa 'Análisis y desarrollo de software' (Código: 228118) dura 27 meses (Tecnólogo Virtual/Presencial) y el 'Programación de software' dura 15 meses (Técnico Presencial)."

    
    if "tecnologo virtual" in texto or "tecnico virtual" in texto or "tecnologo" in texto or "tecnico" in texto:
        return "Los Tecnicos Virtuales incluyen: Análisis y desarrollo de software, Animación 3D, Animación digital, Desarrollo de medios gráficos visuales, Desarrollo publicitario, Desarrollo multimedia y web, Desarrollo de videojuegos y Coordinación de procesos logísticos (duración: 27 meses)."

    
    if any(p in texto for p in ("animacion", "multimedia", "grafico", "videojuego", "videojuegos")):
        return "Contamos con programas como Animación 3D, Animación digital, Desarrollo de videojuegos, Producción multimedia y Desarrollo de medios gráficos visuales."

    
    if "tecnico presencial" in texto or "tecnicos presenciales" in texto:
        return "Entre los Técnicos Presenciales (duración: 15 meses) tenemos: Preprensa digital, Impresión (offset, flexográfica, serigráfica, digital), Programación de software, Sistemas teleinformáticos, Elaboración de audiovisuales y Encuadernación."
    


    return f"Entiendo. Cuéntame un poco más sobre: «{mensaje.strip()}»"


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=responder(request.message))


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chatbot básico</title>
  <style>
    body { font: 16px system-ui, sans-serif; max-width: 680px; margin: 3rem auto; padding: 0 1rem; color: #202124; }
    #chat { min-height: 260px; border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
    .message { margin: .6rem 0; white-space: pre-wrap; }
    form { display: flex; gap: .5rem; }
    input { flex: 1; padding: .8rem; border: 1px solid #aaa; border-radius: 8px; }
    button { padding: .8rem 1rem; border: 0; border-radius: 8px; background: #1459c7; color: white; cursor: pointer; }
  </style>
</head>
<body>
  <h1>Aladino</h1>
  <div id="chat" aria-live="polite"><p class="message">Sangresita: ¡Hola! Escribe un mensaje para empezar.</p></div>
  <form id="form">
    <input id="message" autocomplete="off" placeholder="Escribe tu mensaje…" required maxlength="2000">
    <button type="submit">Enviar</button>
  </form>
  <script>
    const chat = document.querySelector('#chat');
    const form = document.querySelector('#form');
    const input = document.querySelector('#message');
    function addMessage(who, text) {
      const p = document.createElement('p');
      p.className = 'message';
      p.textContent = `${who}: ${text}`;
      chat.appendChild(p);
      chat.scrollTop = chat.scrollHeight;
    }
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;
      addMessage('Tú', message);
      input.value = '';
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        if (!response.ok) throw new Error('No se pudo obtener una respuesta.');
        const data = await response.json();
        addMessage('Sangresita', data.reply);
      } catch (error) {
        addMessage('Sangresita', `Error: ${error.message}`);
      }
    });
  </script>
</body>
</html>"""