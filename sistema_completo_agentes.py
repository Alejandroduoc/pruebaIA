"""
Sistema Completo de Agentes Múltiples con Orquestación y Multi-Agente
=====================================================================
Integra RA1 y RA2 con agentes especializados, orquestación y comunicación entre agentes
"""

import os
import time
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
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
        base_datos = {
            "hardware": {
                "cpu": "El CPU (procesador) es el cerebro del computador...",
                "ram": "La RAM es memoria de acceso aleatorio temporal...",
                "disco": "Los discos duros almacenan datos permanentemente..."
            },
            "software": {
                "windows": "Windows requiere mínimo 4GB RAM y 64GB espacio...",
                "instalacion": "Para instalar software: 1) Ejecutar setup, 2) Siguiente, 3) Aceptar..."
            },
            "redes": {
                "wifi": "Para conectar WiFi: verificar contraseña y alcance...",
                "ethernet": "Cable Ethernet proporciona conexión estable..."
            }
        }
        
        query_lower = query.lower()
        categoria_lower = categoria.lower()
        
        if categoria_lower in base_datos:
            for palabra, info in base_datos[categoria_lower].items():
                if palabra in query_lower:
                    return info
        
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
        self.historial = []
        self.metricas = {
            "consultas_atendidas": 0,
            "tiempo_promedio": 0,
            "problemas_resueltos": 0
        }
        self.material_cargado = ""
    
    def cargar_material(self, contenido: str):
        """Carga material de conocimiento para el agente"""
        self.material_cargado = contenido
    
    def procesar_consulta(self, consulta: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Procesa una consulta y devuelve respuesta"""
        inicio = time.time()
        
        # Construir prompt especializado
        system_prompt = f"""
Eres {self.nombre}, un agente especializado en {self.especialidad}.

Conocimiento del área:
{self.material_cargado[:3000]}

Directrices:
1. Responde específicamente sobre {self.especialidad}
2. Proporciona soluciones prácticas y paso a paso
3. Si necesitas colaborar con otro agente, indícalo
4. Mantén un tono profesional y útil
"""
        
        # Preparar mensajes
        messages = [SystemMessage(content=system_prompt)]
        
        # Agregar historial reciente
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
        
        # Guardar en historial
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
            "categoria": self.especialidad
        }
    
    def colaborar(self, info: str) -> str:
        """Permite que el agente comparta información con otros agentes"""
        return f"{self.nombre} ({self.especialidad}): {info}"

# -------------------- Sistema de Orquestación --------------------

class OrquestadorMultiagente:
    """Sistema que orquesta múltiples agentes especializados"""
    
    def __init__(self):
        # Crear agentes especializados
        self.agentes = {
            "hardware": AgenteEspecializado("Agente Hardware", "hardware y componentes físicos"),
            "software": AgenteEspecializado("Agente Software", "aplicaciones y programas"),
            "redes": AgenteEspecializado("Agente Redes", "conectividad y redes informáticas"),
            "seguridad": AgenteEspecializado("Agente Seguridad", "seguridad informática y protección"),
            "general": AgenteEspecializado("Agente General", "soporte técnico general")
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
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Sistema Multi-Agente de Soporte Informático")
    st.markdown("Sistema con orquestación, agentes especializados y colaboración entre agentes")
    
    # Inicializar orquestador
    if "orquestador" not in st.session_state:
        st.session_state.orquestador = OrquestadorMultiagente()
        
        # Cargar material base para todos los agentes
        material_base = """
        Hardware: Componentes físicos del computador (CPU, RAM, discos).
        Software: Programas y aplicaciones (Windows, Office, navegadores).
        Redes: Conectividad (WiFi, Ethernet, routers, switches).
        Seguridad: Protección contra amenazas (antivirus, firewall, malware).
        """
        
        for agente_nombre, agente in st.session_state.orquestador.agentes.items():
            agente.cargar_material(material_base)
        
        st.session_state.historial_consultas = []
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Panel de Control")
        st.markdown("### Agentes Disponibles:")
        for nombre, agente in st.session_state.orquestador.agentes.items():
            metricas = agente.metricas
            st.write(f"**{nombre.upper()}**: {metricas['consultas_atendidas']} consultas")
        
        st.markdown("---")
        if st.button("🗑️ Limpiar Memoria"):
            for agente in st.session_state.orquestador.agentes.values():
                agente.historial = []
            st.success("Memoria limpiada")
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat Multi-Agente")
        
        # Input
        consulta = st.text_area(
            "Describe tu problema técnico:",
            placeholder="Ej: Mi computadora tiene virus y la pantalla se congela",
            height=100
        )
        
        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1:
            enviar = st.button("🚀 Enviar", type="primary")
        with col_btn2:
            ejemplo = st.button("💡 Ejemplo Complejo")
        
        if ejemplo:
            consulta = "Mi computadora está lenta, tiene virus y no puedo conectarme a WiFi"
        
        # Procesar consulta
        if enviar and consulta.strip():
            with st.spinner("🤖 Procesando con múltiples agentes especializados..."):
                # Usar orquestador para procesar consulta
                resultado = st.session_state.orquestador.procesar_consulta_compleja(consulta)
                
                # Mostrar resultado
                st.markdown("### 🤖 Respuesta del Sistema")
                st.info(f"🎯 **Agente Principal**: {resultado['agente_principal']}")
                st.info(f"👥 **Agentes Involucrados**: {', '.join(resultado['agentes_involucrados'])}")
                st.info(f"⏱️ **Tiempo**: {resultado['tiempo_respuesta']:.2f}s")
                
                if "colaboracion" in resultado:
                    with st.expander("🤝 Colaboración Multi-Agente"):
                        st.markdown(resultado["colaboracion"])
                
                st.markdown("#### 💬 Respuesta:")
                st.markdown(resultado["respuesta"])
                
                # Guardar
                st.session_state.historial_consultas.append({
                    "consulta": consulta,
                    "resultado": resultado,
                    "timestamp": datetime.now()
                })
    
    with col2:
        st.header("📊 Métricas Globales")
        
        metricas = st.session_state.orquestador.metricas_globales
        st.metric("Total Consultas", metricas["total_consultas"])
        st.metric("Colaboraciones", metricas["colaboraciones"])
        
        st.markdown("### 📈 Uso de Agentes")
        for agente, count in metricas["agentes_involucrados"].items():
            st.write(f"**{agente}**: {count}")
        
        # Historial de comunicación
        if st.session_state.orquestador.comunicacion_agentes:
            st.markdown("### 📡 Última Comunicación")
            ultima = st.session_state.orquestador.comunicacion_agentes[-1]
            st.write(f"Agentes: {', '.join(ultima['agentes'])}")
            st.caption(f"{ultima['consulta']}")
    
    # Footer
    st.markdown("---")
    st.markdown("*Sistema Multi-Agente con Orquestación y Colaboración Inter-Agente*")

if __name__ == "__main__":
    if not os.getenv("GITHUB_TOKEN"):
        st.error("⚠️ Configura la variable de entorno GITHUB_TOKEN")
    else:
        main()
