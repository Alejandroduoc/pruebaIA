# Sistema Multi-Agente con Orquestación Inteligente

## 🎯 Descripción del Proyecto

Este proyecto implementa un sistema avanzado de soporte informático utilizando múltiples agentes especializados con orquestación inteligente. El sistema integra conceptos de RA1 (Recuperación y Memoria) y RA2 (Agentes y Orquestación) para crear una solución completa de asistencia técnica.

### Características Principales

- **5 Agentes Especializados**: Hardware, Software, Redes, Seguridad y General
- **Orquestación Inteligente**: Coordinación automática entre agentes
- **Memoria Avanzada**: 5 tipos de memoria de LangChain implementados
- **Colaboración Multi-Agente**: Agentes trabajan juntos cuando es necesario
- **Interfaz Web**: Dashboard interactivo con Streamlit
- **Métricas en Tiempo Real**: Monitoreo de rendimiento por agente

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8+
- Token de GitHub AI

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/Alejandroduoc/pruebaIA.git
cd sistema-multi-agente

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirement.txt

# Configurar variables de entorno
export GITHUB_TOKEN="tu_token_aqui"
export LANGCHAIN_PROJECT="sistema-multi-agente"
```

### Ejecución
```bash
streamlit run sistema_completo_agentes.py
```

Accede desde tu navegador: `http://localhost:8501`

## 🏗️ Arquitectura del Sistema

### Componentes Principales
- **OrquestadorMultiagente**: Coordina todos los agentes
- **Agentes Especializados**: 5 agentes con especialidades específicas
- **SistemaMemoriaAvanzada**: 5 tipos de memoria integrados
- **HerramientaSoporte**: Herramientas compartidas entre agentes

### Tipos de Memoria Implementados
- **ConversationBufferMemory**: Historial completo
- **ConversationSummaryMemory**: Resumen inteligente
- **ConversationBufferWindowMemory**: Últimas 5 interacciones
- **ConversationEntityMemory**: Entidades recordadas
- **VectorStoreRetrieverMemory**: Memoria semántica a largo plazo con FAISS

### 🔍 RAG Principal con FAISS
- **Material vectorizado**: `soporte_informatica.txt` con embeddings
- **Búsqueda semántica**: `similarity_search()` por consulta
- **Contexto relevante**: Top 3 chunks más similares por agente
- **Especialización**: Material específico por especialidad
- **Integración completa**: FAISS en prompts y memoria

## 🤖 Agentes Especializados

| Agente | Especialidad | Ejemplo de Consulta |
|--------|-------------|-------------------|
| 🔧 **Hardware** | Componentes físicos | "Mi computadora tiene solo 4GB de RAM" |
| 💻 **Software** | Aplicaciones y programas | "No puedo instalar Microsoft Office" |
| 🌐 **Redes** | Conectividad | "No puedo conectarme al WiFi" |
| 🔒 **Seguridad** | Protección y malware | "Mi antivirus detectó un virus" |
| ⚙️ **General** | Soporte general | Consultas diversas |

## 🔧 Herramientas Especializadas

### HerramientaSoporte
- **`calculadora_matematica()`**: Cálculos técnicos
- **`buscar_informacion()`**: Búsqueda contextual
- **`analizar_problema()`**: Clasificación automática

## 📊 Métricas y Monitoreo

### Métricas por Agente
- Consultas atendidas
- Tiempo promedio de respuesta
- Problemas resueltos

### Métricas Globales
- Total de consultas procesadas
- Distribución por agente
- Número de colaboraciones multi-agente

### Métricas de Memoria
- Buffer: Historial completo
- Summary: Resumen inteligente
- Window: Últimas interacciones
- Entities: Entidades recordadas
- Vector: Memoria a largo plazo con FAISS

### Métricas de FAISS
- **FAISS activo**: Indica si se usó búsqueda semántica
- **Contexto encontrado**: Chunks relevantes por consulta
- **Material vectorizado**: Chunks por agente especializado
- **Búsquedas semánticas**: Número de similarity_search() ejecutadas

## 🔄 Ejemplos de Uso

### Consulta Simple (1 Agente)
```
Usuario: "Mi computadora está lenta"
→ Agente Hardware procesa
→ Respuesta: Solución de rendimiento
```

### Consulta Compleja (Multi-Agente)
```
Usuario: "Mi computadora tiene virus y no puedo conectarme a WiFi"
→ Agente Seguridad (principal)
→ Colaboración con Agente Redes
→ Respuesta coordinada de ambos agentes
```

## 📁 Estructura del Proyecto

```
sistema-multi-agente/
├── sistema_completo_agentes.py    # Sistema principal
├── chat.py                        # Chatbot original
├── requirement.txt                # Dependencias
├── soporte_informatica.txt        # Material de conocimiento
├── README.md                      # Este archivo
├── README_DETALLADO.md           # Documentación completa
├── DOCUMENTACION_COMPLETA_SISTEMA_AGENTES.md
├── INFORME_COMPLETO.md
├── MEMORIA_AVANZADA_IMPLEMENTADA.md
├── DIAGRAMAS_ARQUITECTURA.md
├── REFERENCIAS_BIBLIOGRAFICAS.md
├── ANALISIS_CUMPLIMIENTO.md
├── MEJORAS_ICONOS.md

```

## 🧪 Validación del Sistema

### Casos de Prueba
1. **Consulta Simple**: "Mi computadora está lenta"
2. **Consulta Compleja**: "Virus y problemas de WiFi"
3. **Memoria Persistente**: Múltiples consultas relacionadas

### Métricas de Rendimiento
- **Tiempo de respuesta**: < 3 segundos promedio
- **Precisión de categorización**: > 90%
- **Colaboración exitosa**: > 85%

## 📚 Documentación Adicional

- **[README Detallado](README_DETALLADO.md)**: Documentación completa
- **[Diagramas de Arquitectura](DIAGRAMAS_ARQUITECTURA.md)**: Diagramas Mermaid
- **[Memoria Avanzada](MEMORIA_AVANZADA_IMPLEMENTADA.md)**: Sistema de memoria
- **[Referencias Bibliográficas](REFERENCIAS_BIBLIOGRAFICAS.md)**: Formato APA
- **[Análisis de Cumplimiento](ANALISIS_CUMPLIMIENTO.md)**: Verificación de requisitos

## 🎓 Integración RA1 y RA2

### RA1 - Recuperación y Memoria ✅
- **RAG completo con FAISS**: Búsqueda semántica implementada
- **Memoria avanzada**: 5 tipos de memoria de LangChain
- **VectorStoreRetrieverMemory**: Memoria a largo plazo con FAISS
- **similarity_search()**: Búsqueda semántica por consulta
- **Material vectorizado**: soporte_informatica.txt con embeddings
- **Streaming de respuestas**: Respuestas en tiempo real
- **Integración con LLM**: Prompts con FAISS y memoria

### RA2 - Agentes y Orquestación ✅
- Agentes especializados independientes
- Sistema de orquestación centralizado
- Colaboración inter-agente
- Herramientas especializadas


