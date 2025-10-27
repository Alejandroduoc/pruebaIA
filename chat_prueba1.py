import os
import time
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langsmith import Client





client = Client()
print("✓ LangSmith conectado al proyecto:", os.getenv("LANGCHAIN_PROJECT"))
# -------------------- Clase Chatbot --------------------
class ChatbotSoporte:
    def __init__(self):
        # Configuración del modelo LLM
        self.llm = ChatOpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("GITHUB_TOKEN"),
            model="openai/gpt-4o-mini",
            temperature=0.7,
            streaming=True
        )
        
        
        # Configuración del modelo de embeddings
        self.embeddings = OpenAIEmbeddings(
         model="text-embedding-3-small",
         api_key=os.getenv("GITHUB_TOKEN")
        )
        # Memoria de conversación
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        
        self.vectorstore = None
        
        # Divisor de texto
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def cargar_material_automatico(self):
        """Carga automáticamente el archivo soporte_informatica.txt"""
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_txt = os.path.join(dir_actual, "soporte_informatica.txt")
        if not os.path.exists(ruta_txt):
            st.error(f"No se encontró el archivo: {ruta_txt}")
            return
        
        with open(ruta_txt, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        doc = Document(page_content=contenido, metadata={"source": "soporte_informatica"})
        chunks = self.text_splitter.split_documents([doc])
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        st.success(f"Archivo '{ruta_txt}' cargado automáticamente con {len(chunks)} chunks.")

    def generar_respuesta_con_streaming(self, pregunta: str, mostrar_contexto: bool = False):
        """Genera respuesta con streaming integrando RAG y memoria"""
        contexto = ""
        if self.vectorstore:
            docs = self.vectorstore.similarity_search(pregunta, k=3)
            contexto = "\n\n".join([doc.page_content for doc in docs])
            if mostrar_contexto:
                st.info("📚 Contexto relevante:\n" + contexto[:500] + "...")
        
   
        system_prompt = f"""
Eres un asistente de soporte informático experto para oficinas. 
Tu conocimiento se basa exclusivamente en el siguiente material (extraído de soporte_informatica.txt):


{contexto}


Directrices:
1. Responde de manera clara, concisa y profesional.
2. Solo utiliza la información contenida en el material mostrado arriba; no inventes respuestas ni uses conocimiento externo.
3. Si la pregunta no puede ser respondida con el material, responde amablemente:
   "La información para responder a tu pregunta no se encuentra en el material disponible."
4. Prioriza la seguridad informática y buenas prácticas.
5. Para problemas técnicos, proporciona pasos prácticos y ordenados.
6. Mantén un tono amigable y de ayuda.
"""
        messages = [SystemMessage(content=system_prompt)]
        historial = self.memory.load_memory_variables({})["chat_history"]
        for msg in historial:
            messages.append(msg)
        messages.append(HumanMessage(content=pregunta))
        
        respuesta_completa = ""
        try:
            placeholder = st.empty()
            respuesta_texto = "🤖 **Asistente:** "
            for chunk in self.llm.stream(messages):
                respuesta_texto += chunk.content
                placeholder.markdown(respuesta_texto + "▌")
                respuesta_completa += chunk.content
                time.sleep(0.02)
            placeholder.markdown(respuesta_texto)
            self.memory.save_context({"input": pregunta}, {"output": respuesta_completa})
            return respuesta_completa
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return f"Error: {e}"

# -------------------- Aplicación Streamlit --------------------
def main():
    st.set_page_config(page_title="Asistente Soporte Informática", page_icon="🤖", layout="wide")
    st.title("🤖 Asistente de Soporte en Informática")
    st.markdown("Haz tus consultas sobre soporte informático en oficinas.")

    # Inicializa chatbot en sesión
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatbotSoporte()
        st.session_state.chatbot.cargar_material_automatico()  # Carga automática al iniciar

    # Barra lateral
    with st.sidebar:
        st.header("Opciones")
        if st.button("📊 Mostrar estadísticas"):
            historial = st.session_state.chatbot.memory.load_memory_variables({})["chat_history"]
            st.subheader("📊 Estadísticas del Chatbot")
            st.write(f"💬 Mensajes en memoria: {len(historial)}")
            st.write(f"📚 Base vectorial: {'✓ Cargada' if st.session_state.chatbot.vectorstore else '✗ No disponible'}")
            if st.session_state.chatbot.vectorstore:
                st.write(f"📖 Documentos indexados: {st.session_state.chatbot.vectorstore.index.ntotal}")
        if st.button("🗑️ Limpiar memoria"):
            st.session_state.chatbot.memory.clear()
            st.success("Memoria limpiada")

    # Área principal de Chat
    st.header("💬 Chat")
    historial = st.session_state.chatbot.memory.load_memory_variables({})["chat_history"]
    if historial:
        with st.expander("📜 Historial de conversación"):
            for msg in historial:
                if isinstance(msg, HumanMessage):
                    st.write(f"**🧑 Usuario:** {msg.content}")
                elif isinstance(msg, AIMessage):
                    st.write(f"**🤖 Asistente:** {msg.content}")

    pregunta = st.text_area("Escribe tu pregunta:", placeholder="¿En qué puedo ayudarte?")
    col1, col2 = st.columns([1, 5])
    with col1:
        mostrar_contexto = st.checkbox("Mostrar contexto", value=False)
    with col2:
        if st.button("🚀 Enviar pregunta"):
            if pregunta.strip():
                with st.spinner("Generando respuesta..."):
                    st.session_state.chatbot.generar_respuesta_con_streaming(
                        pregunta, mostrar_contexto=mostrar_contexto
                    )
            else:
                st.warning("Por favor, escribe una pregunta")

    st.markdown("---")
    st.markdown("*Asistente basado en RAG con memoria de conversación*")

# -------------------- inico del programa  --------------------
if __name__ == "__main__":
    if not os.getenv("GITHUB_TOKEN"):
        st.error("⚠️ Configura la variable de entorno GITHUB_TOKEN")
    else:
        main()
