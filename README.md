### Asistente de Soporte Informático

Este proyecto implementa un chatbot de soporte en informática utilizando LangChain, Streamlit, FAISS y LangSmith.
El sistema integra RAG (Retrieval Augmented Generation) para responder preguntas basadas en material cargado (soporte_informatica.txt) y mantiene memoria de conversación para mejorar la interacción.


📌 Requisitos previos

Python 3.10+

Instalar dependencias:

pip install -r requirements.txt


Configurar variables de entorno (puedes usar un archivo .env):

GITHUB_TOKEN=tu_token_de_github_ai
LANGCHAIN_API_KEY=tu_api_key_de_langsmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=IA_Project

📂 Estructura del proyecto
📁 productos_app/pruebaIA
│── chat.py                   # Código principal del chatbot con Streamlit
│── soporte_informatica.txt   # Base de conocimiento para el RAG
│── requirements.txt          # Librerías necesarias
│── README.md                 # Este archivo

▶️ Ejecución del sistema

Asegúrate de tener activado el entorno virtual (si usas uno):

.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac


Ejecuta la aplicación con Streamlit:

streamlit run chat.py


Accede desde tu navegador:

http://localhost:8501

⚙️ Funcionalidades principales

✅ Carga automática del archivo soporte_informatica.txt como base vectorial con FAISS.

✅ Respuestas basadas en RAG, solo usando la información del material cargado.

✅ Memoria de conversación para mantener contexto entre preguntas.

✅ Streaming de respuestas en tiempo real.

✅ Integración con LangSmith para trazabilidad y monitoreo de las interacciones.

✅ Opciones en sidebar:

Mostrar estadísticas del chatbot.

Limpiar la memoria de la conversación.

📊 Integración con LangSmith

Si tienes LangSmith configurado, cada interacción será registrada con:

Proyecto: IA_Project

API Key: definida en LANGCHAIN_API_KEY

Esto permite trazar, depurar y analizar el rendimiento del asistente.

🧪 Validación

Escribir una pregunta en el campo de texto, por ejemplo:

¿Cómo configurar el correo corporativo en Outlook?


El asistente responde basado únicamente en soporte_informatica.txt.

Si la información no está en el material, responde:

"La información para responder a tu pregunta no se encuentra en el material disponible."

📌 Notas importantes

Si no se encuentra el archivo soporte_informatica.txt, el sistema mostrará un error.

Debes configurar correctamente GITHUB_TOKEN (para usar el modelo LLM y embeddings) y LANGCHAIN_API_KEY (para LangSmith).

Compatible con Windows, Linux y Mac.

✍️ Este proyecto fue desarrollado como asistente especializado en soporte informático de oficina, usando RAG + LangChain + LangSmith + Streamlit.