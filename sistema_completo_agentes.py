"""
Sistema Completo de Agentes Múltiples con Orquestación y Multi-Agente
=====================================================================

"""

import os
from dotenv import load_dotenv
load_dotenv()
import time
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_classic.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory, ConversationEntityMemory, VectorStoreRetrieverMemory
from langchain_community.vectorstores import FAISS
from langsmith import Client

# -------------------- Configuración --------------------
client = Client()
print("✓ LangSmith conectado al proyecto:", os.getenv("LANGCHAIN_PROJECT"))

# -------------------- Herramientas Especializadas (RA1 y RA2) --------------------

class HerramientaSoporte:
    """Conjunto de herramientas para soporte informático"""
    
    @staticmethod
    def calculadora_matematica(expresion: str) -> str:
        """Calcula expresiones matemáticas para hardware y capacidad"""
        try:
            funciones_permitidas = {
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'pow': pow, 'sqrt': lambda x: x**0.5,
                'len': len
            }
            resultado = eval(expresion, {"__builtins__": {}, **funciones_permitidas})
            return f"Resultado: {resultado}"
        except Exception as e:
            return f"Error en el cálculo: {str(e)}"
    
    @staticmethod
    def buscar_informacion(query: str, categoria: str = "general") -> str:
        """Busca información categorizada por tipo de soporte"""
        # Esta función ahora se basa únicamente en el material cargado por los agentes
        return f"Información sobre {query} para la categoría {categoria}"
    
    @staticmethod
    def analizar_problema(descripcion: str) -> Dict[str, Any]:
        """Analiza la descripción del problema y sugiere una categoría"""
        palabras_hardware = ["cpu", "ram", "disco", "hardware", "procesador", "memoria"]
        palabras_software = ["programa", "aplicación", "software", "instalación", "bug", "error"]
        palabras_redes = ["internet", "wifi", "conexión", "red", "router"]
        palabras_seguridad = ["virus", "malware", "seguridad", "antivirus", "firewall"]
        
        desc_lower = descripcion.lower()
        
        categoria = "general"
        prioridad = "media"
        
        if any(palabra in desc_lower for palabra in palabras_hardware):
            categoria = "hardware"
            prioridad = "alta"
        elif any(palabra in desc_lower for palabra in palabras_software):
            categoria = "software"
            prioridad = "media"
        elif any(palabra in desc_lower for palabra in palabras_redes):
            categoria = "redes"
            prioridad = "alta"
        elif any(palabra in desc_lower for palabra in palabras_seguridad):
            categoria = "seguridad"
            prioridad = "crítica"
        
        return {
            "categoria": categoria,
            "prioridad": prioridad,
            "sugerencias": [f"Verificar {categoria}", f"Contactar especialista en {categoria}"]
        }

# -------------------- Sistema de Memoria Avanzada --------------------

class SistemaMemoriaAvanzada:
    """Sistema que integra múltiples tipos de memoria de LangChain"""
    
    def __init__(self, llm, embeddings):
        self.llm = llm
        self.embeddings = embeddings
        
        # 1. ConversationBufferMemory - Historial completo
        self.buffer_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 2. ConversationSummaryMemory - Resume cuando es largo
        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="summary_history",
            return_messages=True
        )
        
        # 3. ConversationBufferWindowMemory - Solo últimas N interacciones
        self.window_memory = ConversationBufferWindowMemory(
            k=5,  # Últimas 5 interacciones
            memory_key="window_history",
            return_messages=True
        )
        
        # 4. ConversationEntityMemory - Recuerda entidades
        self.entity_memory = ConversationEntityMemory(
            llm=self.llm,
            memory_key="entity_history",
            return_messages=True
        )
        
        # 5. VectorStoreRetrieverMemory - Memoria a largo plazo
        self.vectorstore = None
        self.vector_memory = None
        self._inicializar_vectorstore()
    
    def _inicializar_vectorstore(self):
        """Inicializa el vectorstore para memoria a largo plazo"""
        try:
            # Crear documentos iniciales vacíos
            docs = [Document(page_content="Memoria inicial del sistema")]
            self.vectorstore = FAISS.from_documents(docs, self.embeddings)
            
            # Crear retriever
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            
            # Crear VectorStoreRetrieverMemory
            self.vector_memory = VectorStoreRetrieverMemory(
                retriever=retriever,
                memory_key="vector_history",
                return_messages=True
            )
        except Exception as e:
            print(f"⚠️ Error inicializando vectorstore: {e}")
            self.vectorstore = None
            self.vector_memory = None
    
    def agregar_interaccion(self, entrada: str, salida: str):
        """Agrega una nueva interacción a todos los tipos de memoria"""
        # Buffer Memory (completo)
        self.buffer_memory.save_context(
            {"input": entrada}, 
            {"output": salida}
        )
        
        # Summary Memory (resumen)
        self.summary_memory.save_context(
            {"input": entrada}, 
            {"output": salida}
        )
        
        # Window Memory (ventana deslizante)
        self.window_memory.save_context(
            {"input": entrada}, 
            {"output": salida}
        )
        
        # Entity Memory (entidades)
        self.entity_memory.save_context(
            {"input": entrada}, 
            {"output": salida}
        )
        
        # Vector Memory (a largo plazo)
        if self.vector_memory:
            try:
                self.vector_memory.save_context(
                    {"input": entrada}, 
                    {"output": salida}
                )
            except Exception as e:
                print(f"⚠️ Error guardando en vector memory: {e}")
    
    def obtener_contexto_completo(self) -> Dict[str, Any]:
        """Obtiene contexto de todos los tipos de memoria"""
        contexto = {}
        
        try:
            # Buffer Memory
            buffer_vars = self.buffer_memory.load_memory_variables({})
            contexto["buffer"] = buffer_vars.get("chat_history", [])
        except:
            contexto["buffer"] = []
        
        try:
            # Summary Memory
            summary_vars = self.summary_memory.load_memory_variables({})
            contexto["summary"] = summary_vars.get("summary_history", [])
        except:
            contexto["summary"] = []
        
        try:
            # Window Memory
            window_vars = self.window_memory.load_memory_variables({})
            contexto["window"] = window_vars.get("window_history", [])
        except:
            contexto["window"] = []
        
        try:
            # Entity Memory
            entity_vars = self.entity_memory.load_memory_variables({})
            contexto["entities"] = entity_vars.get("entity_history", [])
        except:
            contexto["entities"] = []
        
        try:
            # Vector Memory
            if self.vector_memory:
                vector_vars = self.vector_memory.load_memory_variables({})
                contexto["vector"] = vector_vars.get("vector_history", [])
            else:
                contexto["vector"] = []
        except:
            contexto["vector"] = []
        
        return contexto
    
    def limpiar_memoria(self):
        """Limpia todos los tipos de memoria"""
        self.buffer_memory.clear()
        self.summary_memory.clear()
        self.window_memory.clear()
        self.entity_memory.clear()
        if self.vector_memory:
            self.vector_memory.clear()

# -------------------- Clase Agente Especializado --------------------

class AgenteEspecializado:
    """Agente individual especializado en un área de soporte"""
    
    def __init__(self, nombre: str, especialidad: str):
        self.nombre = nombre
        self.especialidad = especialidad
        self.llm = ChatOpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("GITHUB_TOKEN"),
            model="openai/gpt-4o-mini",
            temperature=0.7,
            streaming=True
        )
        
        # Inicializar embeddings para memoria vectorial
        self.embeddings = OpenAIEmbeddings(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("GITHUB_TOKEN"),
            model="text-embedding-3-small"
        )
        
        # Sistema de memoria avanzada
        self.memoria = SistemaMemoriaAvanzada(self.llm, self.embeddings)
        
        # Historial simple (mantener para compatibilidad)
        self.historial = []
        
        # Text splitter para RAG
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Vectorstore para RAG principal
        self.vectorstore_rag = None
        
        self.metricas = {
            "consultas_atendidas": 0,
            "tiempo_promedio": 0,
            "problemas_resueltos": 0
        }
        self.material_cargado = ""
    
    def cargar_material(self, contenido: str):
        """Carga material de conocimiento para el agente usando FAISS"""
        self.material_cargado = contenido
        
        try:
            # Crear documento
            doc = Document(page_content=contenido, metadata={"source": f"material_{self.especialidad}"})
            
            # Dividir en chunks
            chunks = self.text_splitter.split_documents([doc])
            
            # Crear vectorstore FAISS
            self.vectorstore_rag = FAISS.from_documents(chunks, self.embeddings)
            
            print(f"✓ {self.nombre}: Material cargado con FAISS ({len(chunks)} chunks)")
            
        except Exception as e:
            print(f"⚠️ Error cargando material FAISS para {self.nombre}: {e}")
            self.vectorstore_rag = None
    
    def buscar_contexto_faiss(self, consulta: str) -> str:
        """Busca contexto relevante usando FAISS"""
        if self.vectorstore_rag:
            try:
                # Búsqueda semántica con FAISS
                docs = self.vectorstore_rag.similarity_search(consulta, k=3)
                contexto = "\n\n".join([doc.page_content for doc in docs])
                return contexto
            except Exception as e:
                print(f"⚠️ Error en búsqueda FAISS para {self.nombre}: {e}")
                return ""
        return ""
    
    def procesar_consulta(self, consulta: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Procesa una consulta y devuelve respuesta"""
        inicio = time.time()
        
        # Obtener contexto de memoria avanzada
        contexto_memoria = self.memoria.obtener_contexto_completo()
        
        # Obtener contexto FAISS para RAG
        contexto_faiss = self.buscar_contexto_faiss(consulta)
        
        # Construir prompt especializado con contexto de memoria y FAISS
        system_prompt = f"""
Eres {self.nombre}, un agente especializado en {self.especialidad}.

Conocimiento del área (FAISS RAG):
{contexto_faiss if contexto_faiss else self.material_cargado[:2000]}

Contexto de memoria:
- Resumen de conversaciones anteriores: {self._formatear_memoria(contexto_memoria.get('summary', []))}
- Entidades recordadas: {self._formatear_memoria(contexto_memoria.get('entities', []))}
- Últimas interacciones: {self._formatear_memoria(contexto_memoria.get('window', []))}
- Memoria vectorial: {self._formatear_memoria(contexto_memoria.get('vector', []))}

Directrices:
1. Responde específicamente sobre {self.especialidad}
2. Proporciona soluciones prácticas y paso a paso
3. Si necesitas colaborar con otro agente, indícalo
4. Mantén un tono profesional y útil
5. Usa el contexto de memoria y FAISS para respuestas más personalizadas
6. Si no tienes información específica, indícalo claramente
"""
        
        # Preparar mensajes
        messages = [SystemMessage(content=system_prompt)]
        
        # Agregar historial reciente (mantener compatibilidad)
        for msg in self.historial[-3:]:
            messages.append(msg)
        
        # Mensaje del usuario con contexto si existe
        consulta_completa = consulta
        if contexto:
            consulta_completa += f"\n\nContexto colaborativo: {contexto.get('info', '')}"
        
        messages.append(HumanMessage(content=consulta_completa))
        
        # Generar respuesta
        respuesta = ""
        for chunk in self.llm.stream(messages):
            respuesta += chunk.content
        
        # Guardar en memoria avanzada
        self.memoria.agregar_interaccion(consulta, respuesta)
        
        # Guardar en historial simple (compatibilidad)
        self.historial.append(HumanMessage(content=consulta))
        self.historial.append(AIMessage(content=respuesta))
        
        if len(self.historial) > 10:
            self.historial = self.historial[-10:]
        
        # Actualizar métricas
        tiempo_respuesta = time.time() - inicio
        self.metricas["consultas_atendidas"] += 1
        self.metricas["tiempo_promedio"] = (
            (self.metricas["tiempo_promedio"] * (self.metricas["consultas_atendidas"] - 1) + tiempo_respuesta)
            / self.metricas["consultas_atendidas"]
        )
        self.metricas["problemas_resueltos"] += 1
        
        return {
            "agente": self.nombre,
            "respuesta": respuesta,
            "tiempo_respuesta": tiempo_respuesta,
            "categoria": self.especialidad,
            "faiss_usado": bool(contexto_faiss),
            "contexto_faiss": contexto_faiss[:200] if contexto_faiss else "",
            "memoria_usada": {
                "buffer": len(contexto_memoria.get('buffer', [])),
                "summary": len(contexto_memoria.get('summary', [])),
                "window": len(contexto_memoria.get('window', [])),
                "entities": len(contexto_memoria.get('entities', [])),
                "vector": len(contexto_memoria.get('vector', []))
            }
        }
    
    def _formatear_memoria(self, memoria_messages: List) -> str:
        """Formatea los mensajes de memoria para el prompt"""
        if not memoria_messages:
            return "Ninguna información previa"
        
        formatted = []
        for msg in memoria_messages[-3:]:  # Últimos 3 mensajes
            if hasattr(msg, 'content'):
                formatted.append(msg.content[:200])  # Limitar longitud
        
        return " | ".join(formatted) if formatted else "Ninguna información previa"
    
    def colaborar(self, info: str) -> str:
        """Permite que el agente comparta información con otros agentes"""
        return f"{self.nombre} ({self.especialidad}): {info}"

# -------------------- Sistema de Orquestación --------------------

class OrquestadorMultiagente:
    """Sistema que orquesta múltiples agentes especializados"""
    
    def __init__(self):
        # Crear agentes especializados
        self.agentes = {
            "hardware": AgenteEspecializado("🔧 Agente Hardware", "hardware y componentes físicos"),
            "software": AgenteEspecializado("💻 Agente Software", "aplicaciones y programas"),
            "redes": AgenteEspecializado("🌐 Agente Redes", "conectividad y redes informáticas"),
            "seguridad": AgenteEspecializado("🔒 Agente Seguridad", "seguridad informática y protección"),
            "general": AgenteEspecializado("⚙️ Agente General", "soporte técnico general")
        }
        
        # Herramientas compartidas
        self.herramientas = HerramientaSoporte()
        
        # Historial de comunicación entre agentes
        self.comunicacion_agentes = []
        
        # Métricas globales
        self.metricas_globales = {
            "total_consultas": 0,
            "agentes_involucrados": {},
            "colaboraciones": 0
        }
    
    def determinar_agente_principal(self, consulta: str) -> str:
        """Determina qué agente debe manejar la consulta"""
        analisis = self.herramientas.analizar_problema(consulta)
        return analisis["categoria"]
    
    def procesar_consulta_compleja(self, consulta: str) -> Dict[str, Any]:
        """Procesa consulta con orquestación multi-agente"""
        self.metricas_globales["total_consultas"] += 1
        
        # Paso 1: Análisis inicial
        agente_principal = self.determinar_agente_principal(consulta)
        
        # Paso 2: Consulta principal al agente especializado
        resultado = self.agentes[agente_principal].procesar_consulta(consulta)
        resultado["agente_principal"] = agente_principal
        
        # Paso 3: Determinar si se necesita colaboración
        necesita_colaboracion = self._evaluar_colaboracion(consulta, agente_principal)
        
        if necesita_colaboracion:
            # Paso 4: Solicitar opinión de otros agentes
            agentes_colaboradores = self._identificar_colaboradores(consulta, agente_principal)
            contexto_colaboracion = self._obtener_contexto_colaborativo(agentes_colaboradores, consulta)
            
            # Paso 5: Agregar contexto de colaboración
            resultado["colaboracion"] = contexto_colaboracion
            resultado["agentes_involucrados"] = [agente_principal] + agentes_colaboradores
            self.metricas_globales["colaboraciones"] += 1
        else:
            resultado["agentes_involucrados"] = [agente_principal]
        
        # Actualizar métricas de agentes involucrados
        for agente in resultado["agentes_involucrados"]:
            self.metricas_globales["agentes_involucrados"][agente] = \
                self.metricas_globales["agentes_involucrados"].get(agente, 0) + 1
        
        return resultado
    
    def _evaluar_colaboracion(self, consulta: str, agente_principal: str) -> bool:
        """Determina si la consulta requiere colaboración multi-agente"""
        palabras_multiple = ["y también", "además", "también necesito", "complejo", "varios problemas"]
        return any(palabra in consulta.lower() for palabra in palabras_multiple)
    
    def _identificar_colaboradores(self, consulta: str, agente_principal: str) -> List[str]:
        """Identifica qué otros agentes pueden colaborar"""
        colaboradores = []
        
        # Lógica simple: si habla de hardware y software, involucrar ambos
        if "hardware" in consulta.lower() and "software" in consulta.lower():
            if agente_principal == "hardware":
                colaboradores.append("software")
            else:
                colaboradores.append("hardware")
        
        # Siempre agregar agente general como backup
        if "general" not in colaboradores and agente_principal != "general":
            colaboradores.append("general")
        
        return colaboradores
    
    def _obtener_contexto_colaborativo(self, colaboradores: List[str], consulta: str) -> str:
        """Obtiene información de agentes colaboradores"""
        contexto_completo = []
        
        for agente_nombre in colaboradores:
            agente = self.agentes[agente_nombre]
            respuesta = agente.colaborar(f"Perspectiva sobre: {consulta[:100]}")
            contexto_completo.append(respuesta)
        
        # Registrar comunicación entre agentes
        self.comunicacion_agentes.append({
            "timestamp": datetime.now(),
            "consulta": consulta[:100],
            "agentes": colaboradores
        })
        
        return "\n\n".join(contexto_completo)

# -------------------- Aplicación Streamlit --------------------

def main():
    st.set_page_config(
        page_title="Sistema Multi-Agente con Orquestación",
        page_icon="⚙️",
        layout="wide"
    )
    
    st.title("⚙️ Sistema Multi-Agente de Soporte Informático")
    st.markdown("Sistema con orquestación, agentes especializados y colaboración entre agentes")
    
    # Inicializar orquestador
    if "orquestador" not in st.session_state:
        st.session_state.orquestador = OrquestadorMultiagente()
        
        # Cargar material de soporte desde archivo
        try:
            with open("soporte_informatica.txt", "r", encoding="utf-8") as f:
                material_soporte = f.read()
            
            # Cargar material específico por agente
            materiales_especificos = {
                "hardware": f"""
                {material_soporte}
                
                ESPECIALIDAD HARDWARE:
                - Componentes físicos del computador (CPU, RAM, discos, tarjetas gráficas)
                - Problemas de rendimiento y capacidad
                - Instalación y configuración de hardware
                - Diagnóstico de fallos físicos
                """,
                "software": f"""
                {material_soporte}
                
                ESPECIALIDAD SOFTWARE:
                - Programas y aplicaciones (Windows, Office, navegadores)
                - Instalación y desinstalación de software
                - Problemas de compatibilidad
                - Configuración de aplicaciones
                """,
                "redes": f"""
                {material_soporte}
                
                ESPECIALIDAD REDES:
                - Conectividad (WiFi, Ethernet, routers, switches)
                - Configuración de red
                - Problemas de conectividad
                - Seguridad de red
                """,
                "seguridad": f"""
                {material_soporte}
                
                ESPECIALIDAD SEGURIDAD:
                - Protección contra amenazas (antivirus, firewall, malware)
                - Configuración de seguridad
                - Detección de amenazas
                - Mejores prácticas de seguridad
                """,
                "general": f"""
                {material_soporte}
                
                ESPECIALIDAD GENERAL:
                - Soporte técnico general
                - Consultas diversas
                - Coordinación entre especialidades
                - Información general de TI
                """
            }
            
            for agente_nombre, agente in st.session_state.orquestador.agentes.items():
                material = materiales_especificos.get(agente_nombre, material_soporte)
                agente.cargar_material(material)
                
            st.success("✅ Material de soporte cargado con FAISS para todos los agentes")
            
        except FileNotFoundError:
            st.error("❌ Archivo soporte_informatica.txt no encontrado. Por favor, crea este archivo con el material de soporte técnico.")
            st.stop()
        
        st.session_state.historial_consultas = []
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Panel de Control")
        st.markdown("### Agentes Disponibles:")
        for nombre, agente in st.session_state.orquestador.agentes.items():
            metricas = agente.metricas
            st.write(f"**{nombre.upper()}**: {metricas['consultas_atendidas']} consultas")
        
        st.markdown("---")
        if st.button("🔄 Limpiar Memoria"):
            for agente in st.session_state.orquestador.agentes.values():
                # Limpiar memoria avanzada
                agente.memoria.limpiar_memoria()
                # Limpiar historial simple (compatibilidad)
                agente.historial = []
            st.success("✅ Memoria avanzada limpiada")
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Consulta Multi-Agente")
        
        # Input
        consulta = st.text_area(
            "Describe tu problema técnico:",
            placeholder="Describe tu problema técnico aquí...",
            height=100
        )
        
        enviar = st.button("▶️ Enviar", type="primary")
        
        # Procesar consulta
        if enviar and consulta.strip():
            with st.spinner("⚙️ Procesando con múltiples agentes especializados..."):
                # Usar orquestador para procesar consulta
                resultado = st.session_state.orquestador.procesar_consulta_compleja(consulta)
                
                # Mostrar resultado
                st.markdown("### 🔧 Respuesta del Sistema")
                st.info(f"🎯 **Agente Principal**: {resultado['agente_principal']}")
                st.info(f"👥 **Agentes Involucrados**: {', '.join(resultado['agentes_involucrados'])}")
                st.info(f"⏱️ **Tiempo**: {resultado['tiempo_respuesta']:.2f}s")
                
                if "colaboracion" in resultado:
                    with st.expander("🔗 Colaboración Multi-Agente"):
                        st.markdown(resultado["colaboracion"])
                
                st.markdown("#### 📋 Respuesta:")
                st.markdown(resultado["respuesta"])
                
                # Mostrar información de FAISS
                if "faiss_usado" in resultado and resultado["faiss_usado"]:
                    with st.expander("🔍 FAISS RAG Utilizado"):
                        st.success("✅ Búsqueda semántica FAISS activa")
                        if resultado.get("contexto_faiss"):
                            st.markdown("**Contexto encontrado:**")
                            st.text(resultado["contexto_faiss"])
                        else:
                            st.info("Contexto FAISS disponible pero no mostrado")
                
                # Mostrar información de memoria utilizada
                if "memoria_usada" in resultado:
                    with st.expander("🧠 Memoria Utilizada"):
                        memoria_info = resultado["memoria_usada"]
                        col_mem1, col_mem2, col_mem3 = st.columns(3)
                        
                        with col_mem1:
                            st.metric("Buffer", memoria_info.get("buffer", 0))
                            st.caption("Historial completo")
                        with col_mem2:
                            st.metric("Summary", memoria_info.get("summary", 0))
                            st.caption("Resumen inteligente")
                        with col_mem3:
                            st.metric("Window", memoria_info.get("window", 0))
                            st.caption("Últimas interacciones")
                        
                        col_mem4, col_mem5 = st.columns(2)
                        with col_mem4:
                            st.metric("Entities", memoria_info.get("entities", 0))
                            st.caption("Entidades recordadas")
                        with col_mem5:
                            st.metric("Vector", memoria_info.get("vector", 0))
                            st.caption("Memoria a largo plazo")
                
                # Guardar
                st.session_state.historial_consultas.append({
                    "consulta": consulta,
                    "resultado": resultado,
                    "timestamp": datetime.now()
                })
    
    with col2:
        st.header("📈 Métricas Globales")
        
        metricas = st.session_state.orquestador.metricas_globales
        st.metric("Total Consultas", metricas["total_consultas"])
        st.metric("Colaboraciones", metricas["colaboraciones"])
        
        st.markdown("### 📊 Uso de Agentes")
        for agente, count in metricas["agentes_involucrados"].items():
            st.write(f"**{agente}**: {count}")
        
        # Historial de comunicación
        if st.session_state.orquestador.comunicacion_agentes:
            st.markdown("### 🔄 Última Comunicación")
            ultima = st.session_state.orquestador.comunicacion_agentes[-1]
            st.write(f"Agentes: {', '.join(ultima['agentes'])}")
            st.caption(f"{ultima['consulta']}")
    
    # Footer
    st.markdown("---")
    st.markdown("*Sistema Multi-Agente con Orquestación Inteligente y Colaboración Inter-Agente*")

if __name__ == "__main__":
    if not os.getenv("GITHUB_TOKEN"):
        st.error("🔧 Configura la variable de entorno GITHUB_TOKEN")
    else:
        main()
