# 🎯 GUÍA DE PRESENTACIÓN DEL CÓDIGO (7 MINUTOS)

## **MINUTO 1: Introducción y Estructura General** ⏱️ 0:00-1:00

**"Mi código tiene 928 líneas organizadas en 4 bloques principales:"**

```
1. CONFIGURACIÓN Y HERRAMIENTAS (líneas 1-99)
   ├─ LangSmith para observabilidad
   ├─ Logging persistente (logs_agentes.log)
   └─ HerramientaSoporte con 3 funciones:
      • calculadora_matematica() - cálculos de hardware
      • buscar_informacion() - búsqueda por categoría
      • analizar_problema() - clasificación automática

2. SISTEMA DE MEMORIA AVANZADA (líneas 100-249)
   └─ 5 tipos de memoria LangChain integrados

3. AGENTE ESPECIALIZADO (líneas 250-449)
   └─ Clase base para los 5 agentes

4. ORQUESTADOR + INTERFAZ STREAMLIT (líneas 450-928)
   └─ Coordina agentes + UI multipágina
```

---

## **MINUTO 2: HerramientaSoporte (RA2)** ⏱️ 1:00-2:00

**"Implemento 3 herramientas compartidas entre agentes:"**

```python
class HerramientaSoporte:
    # 1. Calculadora para requisitos técnicos
    @staticmethod
    def calculadora_matematica(expresion: str):
        # Eval seguro con funciones permitidas
        # Ejemplo: "2*1024" → "2048 MB"
    
    # 2. Búsqueda categorizada
    @staticmethod
    def buscar_informacion(query: str, categoria: str):
        # Retorna info por categoría (hardware/software/etc)
    
    # 3. Análisis automático de consulta
    @staticmethod
    def analizar_problema(descripcion: str):
        # Detecta palabras clave → asigna categoría + prioridad
        # "mi wifi no funciona" → {"categoria": "redes", "prioridad": "alta"}
```

**Punto clave:** "Estas herramientas son el cerebro de la orquestación, clasifican automáticamente las consultas."

---

## **MINUTO 3: Sistema de Memoria (RA1)** ⏱️ 2:00-3:00

**"Implemento 5 tipos de memoria LangChain para contexto conversacional:"**

```python
class SistemaMemoriaAvanzada:
    def __init__(self, llm, embeddings):
        # 1. Buffer - Historial completo
        self.buffer_memory = ConversationBufferMemory(...)
        
        # 2. Summary - Resumen inteligente
        self.summary_memory = ConversationSummaryMemory(llm=llm)
        
        # 3. Window - Solo últimas 5 interacciones
        self.window_memory = ConversationBufferWindowMemory(k=5)
        
        # 4. Entity - Recuerda nombres, dispositivos
        self.entity_memory = ConversationEntityMemory(llm=llm)
        
        # 5. Vector - Memoria a largo plazo con FAISS
        self.vector_memory = VectorStoreRetrieverMemory(retriever=...)
```

**Punto clave:** "Cada agente tiene su propio sistema de memoria completo, permitiendo contexto personalizado."

---

## **MINUTO 4: Agente Especializado + RAG FAISS** ⏱️ 3:00-4:00

**"La clase AgenteEspecializado es el núcleo del sistema:"**

```python
class AgenteEspecializado:
    def __init__(self, nombre, especialidad):
        self.llm = ChatOpenAI(...)  # GPT-4o-mini con GitHub
        self.embeddings = OpenAIEmbeddings(...)
        self.memoria = SistemaMemoriaAvanzada(...)  # 5 tipos
        self.vectorstore_rag = None  # FAISS para RAG
    
    # Carga material de conocimiento con FAISS
    def cargar_material(self, contenido: str):
        chunks = self.text_splitter.split_documents([doc])
        self.vectorstore_rag = FAISS.from_documents(chunks, self.embeddings)
    
    # Búsqueda semántica con FAISS
    def buscar_contexto_faiss(self, consulta: str) -> str:
        docs = self.vectorstore_rag.similarity_search(consulta, k=3)
        return "\n\n".join([doc.page_content for doc in docs])
    
    # Procesa consulta con FAISS + Memoria + LLM
    def procesar_consulta(self, consulta: str):
        contexto_faiss = self.buscar_contexto_faiss(consulta)
        contexto_memoria = self.memoria.obtener_contexto_completo()
        # Construye prompt con ambos contextos → streaming
```

**Punto clave:** "Cada agente busca contexto relevante con FAISS antes de responder, combinando RAG + memoria para respuestas personalizadas."

---

## **MINUTO 5: Orquestador Multi-Agente** ⏱️ 4:00-5:00

**"El OrquestadorMultiagente coordina los 5 agentes:"**

```python
class OrquestadorMultiagente:
    def __init__(self):
        self.agentes = {
            "hardware": AgenteEspecializado("🔧 Agente Hardware", ...),
            "software": AgenteEspecializado("💻 Agente Software", ...),
            "redes": AgenteEspecializado("🌐 Agente Redes", ...),
            "seguridad": AgenteEspecializado("🔒 Agente Seguridad", ...),
            "general": AgenteEspecializado("⚙️ Agente General", ...)
        }
    
    # Proceso principal:
    def procesar_consulta_compleja(self, consulta: str):
        # 1. Analizar problema → categoría
        analisis = self.herramientas.analizar_problema(consulta)
        
        # 2. Seleccionar agente principal
        agente_principal = self.agentes[analisis["categoria"]]
        
        # 3. Procesar con agente principal
        respuesta = agente_principal.procesar_consulta(consulta)
        
        # 4. ¿Necesita colaboración?
        if self._necesita_colaboracion(consulta):
            # Obtener input de otros agentes
            agentes_colaboradores = self._obtener_agentes_colaboradores(...)
            # Integrar respuestas
        
        return respuesta_integrada
```

**Punto clave:** "El orquestador analiza, enruta, coordina colaboración y registra todo en logs + métricas."

---

## **MINUTO 6: Interfaz Streamlit Multi-Página** ⏱️ 5:00-6:00

**"La interfaz tiene navegación con 3 páginas:"**

```python
# Streamlit configurado como multipágina
st.set_page_config(page_title="Sistema Multi-Agente", layout="wide")

# Sidebar con navegación
pagina = st.sidebar.radio("Navegación", ["🏠 Chat", "📊 Métricas", "📋 Logs"])

if pagina == "🏠 Chat":
    # Interfaz principal de chat
    # Historial conversacional + streaming
    # Botones para funciones especiales
    
elif pagina == "📊 Métricas":
    # Dashboard con:
    # - Métricas por agente (consultas, tiempo, resolución)
    # - Métricas globales (total consultas, colaboraciones)
    # - Gráficos Plotly interactivos
    # - Métricas de LangSmith (traces, latencia)
    
elif pagina == "📋 Logs":
    # Últimos eventos del sistema
    # logs_agentes.log parseado
    # Filtros por nivel (INFO, WARNING, ERROR)
```

**Punto clave:** "Todo está visualizado: el usuario ve chat, métricas en tiempo real y logs del sistema."

---

## **MINUTO 7: Flujo Completo + Demo** ⏱️ 6:00-7:00

**"Flujo end-to-end de una consulta:"**

```
Usuario escribe: "Mi computadora está lenta y no puedo conectarme a WiFi"
    ↓
1. HerramientaSoporte.analizar_problema()
   → Detecta 2 categorías: hardware + redes
    ↓
2. OrquestadorMultiagente.procesar_consulta_compleja()
   → Selecciona agente principal: Hardware
    ↓
3. AgenteEspecializado.procesar_consulta()
   ├─ buscar_contexto_faiss("computadora lenta") → contexto RAM/CPU
   ├─ memoria.obtener_contexto_completo() → historial usuario
   ├─ Construye prompt con FAISS + memoria
   └─ llm.stream() → respuesta en tiempo real
    ↓
4. Orquestador detecta necesidad colaboración
   → Consulta a Agente Redes sobre WiFi
    ↓
5. Integra ambas respuestas
    ↓
6. Guarda en memoria de ambos agentes
    ↓
7. Registra en logs + actualiza métricas + envía a LangSmith
    ↓
Usuario recibe respuesta completa con solución hardware + redes
```

**Frase de cierre:**
*"928 líneas que implementan un sistema completo: clasificación automática, 5 agentes con RAG+FAISS, 5 tipos de memoria, orquestación inteligente, colaboración multi-agente y observabilidad total. Todo funcional en Streamlit."*

---

## 📝 **TIPS PARA LA PRESENTACIÓN:**

1. **Abre el archivo en VS Code** y señala las líneas mientras explicas
2. **Ten Streamlit corriendo** para mostrar interfaz rápidamente
3. **Prepara una demo rápida** (30 seg): una consulta compleja en vivo
4. **Enfatiza los números:** 928 líneas, 5 agentes, 5 memorias, 3 herramientas
5. **Usa términos técnicos clave:** FAISS, RAG, streaming, embeddings, orquestación

---

## 🔍 **REFERENCIAS RÁPIDAS (Si te preguntan por alguna parte específica):**

| Componente | Líneas | Descripción |
|---|---|---|
| **Configuración** | 1-99 | LangSmith, logging, HerramientaSoporte |
| **Memoria** | 100-249 | SistemaMemoriaAvanzada (5 tipos) |
| **RAG FAISS** | 290-320 | cargar_material(), buscar_contexto_faiss() |
| **Agente** | 250-449 | AgenteEspecializado completo |
| **Orquestador** | 450-600 | OrquestadorMultiagente |
| **Streamlit** | 600-928 | UI multipágina + dashboard |

---

## 💡 **FRASES CLAVE PARA IMPRESIONAR:**

- "Implemento RAG con FAISS para búsqueda semántica en el material de conocimiento"
- "Cada agente tiene 5 tipos de memoria LangChain para contexto enriquecido"
- "El orquestador analiza automáticamente la consulta y coordina colaboración multi-agente"
- "Todo observable: LangSmith para traces, logs persistentes y dashboard Streamlit"
- "928 líneas que integran RA1 (RAG + memoria) y RA2 (agentes + orquestación)"

---

## 🎯 **POSIBLES PREGUNTAS Y RESPUESTAS:**

**P: "¿Por qué 5 agentes y no más o menos?"**  
R: "Cubren las categorías principales de soporte IT: hardware, software, redes, seguridad y general. Más agentes aumentarían complejidad sin mejora significativa en cobertura."

**P: "¿Cómo garantizas que el agente correcto responde?"**  
R: "La función `analizar_problema()` usa análisis de palabras clave para clasificar. Si hay ambigüedad, el orquestador puede activar múltiples agentes en colaboración."

**P: "¿Por qué FAISS y no otra base vectorial?"**  
R: "FAISS es rápida, local (sin costos API) y suficiente para el tamaño actual del material. Para producción, consideraría Pinecone o Weaviate."

**P: "¿Cuál es el bottleneck del sistema?"**  
R: "Las llamadas al LLM. Por eso uso streaming para mejor UX. En las propuestas de mejora documento cache multi-nivel para reducir latencia 70%."

---

¡Éxito en tu presentación! 🚀
