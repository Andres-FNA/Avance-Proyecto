TUTOR EXPERTO CON IA LOCAL (OLLAMA)
# Descripción del Proyecto
Sistema de tutoría personalizada basado en Inteligencia Artificial que funciona 100% local preservando la privacidad de los datos. El asistente se especializa dinámicamente en cualquier tema académico que el usuario elija y proporciona respuestas expertas, recomendaciones y evaluaciones.
# Características Principales
•	 100% Local: Usa Ollama (sin enviar datos a la nube)
•	 Especialización Dinámica: Se adapta a cualquier tema académico
•	 Respuestas Expertas: Da respuestas directas, recomendaciones y evaluaciones
•	 Mantiene Contexto: Recuerda la conversación para respuestas coherentes
•	 Cambio de Tema: Cambia entre temas sin reiniciar el programa
•	 Multimodelo: Soporta llama3, mistral, phi y otros modelos de Ollama
# Objetivos del Sistema
Este asistente fue diseñado cumpliendo los siguientes requisitos:
1. Sistema Local Preservando Privacidad
•	No requiere conexión a internet (excepto instalación inicial)
•	No envía datos a servicios cloud
•	Todos los datos permanecen en tu computadora
2. Base de Conocimientos
•	Conocimiento especializado por tema
3. Técnicas de Prompt Engineering
a) System Prompts Estructurados
<system_instruction>
  <especialidad>Tu única área es: [TEMA]</especialidad>
  <como_responder>Instrucciones claras de comportamiento</como_responder>
  <manejo_contexto>Mantener hilo de conversación</manejo_contexto>
</system_instruction>
b) Few-Shot Prompting
•	Ejemplos calibrados que enseñan al modelo cómo responder
•	3 ejemplos por tema: datos históricos, recomendaciones, redirección
c) Delimitadores XML
<pregunta>Pregunta del estudiante</pregunta>
<contexto_previo>Conversación anterior</contexto_previo>
<instrucciones>Cómo responder</instrucciones>
d) Estrategias de Contexto
•	Mantiene los últimos 3 intercambios
•	Evita repetir preguntas
•	Continúa el hilo natural de la conversación
 Instalación
# Requisitos Previos
•	Python 3.8+
•	Ollama instalado y corriendo
•	8GB RAM mínimo (recomendado para llama3)
Paso 1: Instalar Ollama
Windows
Descargar desde: https://ollama.ai/download
Paso 2: Descargar Modelos de IA en bash
# Modelo recomendado (mejor calidad)
ollama pull llama3
# Alternativas
ollama pull mistral   # Más rápido
ollama pull phi       # Más ligero (4GB RAM)
Paso 3: Instalar Dependencias Python
Uso del Sistema
Ejecución Básica
# 1. Iniciar Ollama (terminal 1)
ollama serve

# 2. Ejecutar el tutor (terminal 2)
python Ollama.py
Flujo de Uso
1. El programa pregunta: ¿En qué tema quieres un tutor?
   → Responde: "Deportes", "Música", "Economía", etc.
2. Selecciona el modelo de IA
   → llama3 (mejor calidad)
   → mistral (más rápido)
   → phi (más ligero)
3. Comienza a hacer preguntas sobre el tema
4. Usa comandos especiales:
   - 'salir'      → Cerrar programa
   - 'reiniciar'  → Nueva conversación
   - 'cambiar'    → Cambiar de tema
   - 'historial'  → Ver conversación
# Comandos Disponibles
Comando	Descripción	Ejemplo
salir	Cierra el programa completamente	salir
reiniciar	Borra la conversación actual (mismo tema)	reiniciar
cambiar	Cambia a otro tema sin cerrar el programa	cambiar
historial	Muestra toda la conversación	historial

# Ejemplos de Uso
Ejemplo 1: Tutor de Deportes
📚 ¿Tema del tutor? → Deportes
🎓 Pregunta: ¿Quién ganó el mundial 2018?
🤖 Tutor:
Francia ganó el mundial 2018, venciendo a Croacia 4-2 en la final
jugada en Moscú, Rusia. Fue su segundo título mundial.
Ejemplo 2: Recomendaciones de Ejercicios
🎓 Pregunta: Encontré practicar tiros libres y pases largos.
¿Me los recomiendas?
🤖 Tutor:
Sí, ambos ejercicios son buenos:
TIROS LIBRES:
   - Mejoran precisión y potencia
   - Practícalos desde diferentes ángulos
 PASES LARGOS:
   - Desarrollan visión de juego
 COMPLEMENTA CON:
   - Control orientado
   - Finalizaciones en movimiento
Mi recomendación: Úsalos como base, pero dedica 50% del tiempo
a encadenar habilidades (recibir + definir).
Ejemplo 3: Cambiar de Tema
🎓 Pregunta sobre Deportes: cambiar
🔄 Cambiando de tema...
📚 ¿Nuevo tema del tutor? → Música
 Tutor de MÚSICA listo
🎓 Pregunta sobre Música: ¿Qué es el tempo?
🤖 Tutor:
El tempo es la velocidad a la que se ejecuta una pieza musical...
#Configuración Avanzada
Modelos Disponibles
Modelo	RAM	Velocidad	Calidad	Uso
llama3	8GB	Media	⭐⭐⭐⭐⭐	Mejor calidad
mistral	6GB	Rápida	⭐⭐⭐⭐	Balance
phi	4GB	Muy rápida	⭐⭐⭐	PCs modestos
Parámetros de Generación
En el código 
"options": {
    "temperature": 0.7,  # Creatividad (0.0-1.0)
    "top_p": 0.9,       # Diversidad (0.0-1.0)
    "num_predict": 512  # Tokens máximos
}
# Personalización del System Prompt
Edita la función _construir_system_prompt() para:
•	Cambiar el tono del tutor
•	Agregar restricciones específicas
•	Modificar el formato de respuesta

# Técnicas de Prompt Engineering Implementadas
1. System Prompts Estructurados
Ubicación en código: Función _construir_system_prompt()
def _construir_system_prompt(self) -> str:
    return f"""<system_instruction>
    Eres un TUTOR EXPERTO en: {self.tema}
    <especialidad>
    Tu ÚNICA área de conocimiento es: {self.tema}
    </especialidad>
    <como_responder>
    1. Responde directamente y de forma clara
    2. Da tu opinión experta
    3. Recomienda cuando te lo pidan
    </como_responder>
    </system_instruction>"""
Propósito: Definir el comportamiento base del modelo de forma estructurada y clara.
# 2. Few-Shot Learning
Ubicación en código: Función _crear_few_shot()
def _crear_few_shot(self) -> List[Dict]:
    return [
        {
            "role": "user",
            "content": f"¿Quién fue [persona de {self.tema}]?"
        },
        {
            "role": "assistant",
            "content": f"[Respuesta experta directa]..."
        }
    ]
Propósito: Enseñar al modelo con ejemplos cómo debe responder en diferentes situaciones.
# 3. Delimitadores XML
Ubicación en código: Función enviar_mensaje()
mensaje_xml = f"""<pregunta>
{mensaje}
</pregunta>

<contexto_previo>
{contexto}
</contexto_previo>

<instrucciones>
Responde como experto...
</instrucciones>"""
Propósito: Separar claramente las diferentes partes del prompt para mejor comprensión del modelo.
# 4. Manejo de Contexto
Ubicación en código: Función _obtener_contexto()
def _obtener_contexto(self, ultimos_n: int = 3) -> str:
    """Obtiene los últimos 3 intercambios para mantener coherencia"""
    # Lee historial
    # Extrae últimos N mensajes
    # Retorna contexto formateado
Propósito: Mantener coherencia en la conversación recordando intercambios previos.
# Formato de Salida
El sistema produce respuestas en formato de texto plano con estructura clara:
Respuesta Directa
[Respuesta principal]
[Contexto adicional]
[Explicación del impacto/importancia]
Recomendación con Evaluación
[Evaluación de lo propuesto]

VENTAJAS:
   - Punto 1
   - Punto 2

SUGERENCIAS:
   - Mejora 1
   - Mejora 2

Mi recomendación:
[Conclusión accionable]
 Privacidad y Seguridad
•	Datos locales: Nada se envía a internet
•	Sin registro: No se guardan logs permanentes
#  Solución de Problemas
Error: "No se puede conectar a Ollama"
Solución:
# Verificar que Ollama esté corriendo
ollama list
# Si no está corriendo, iniciar:
ollama serve
Error: "Modelo no encontrado"
Solución:
# Descargar el modelo
ollama pull llama3
# Verificar modelos disponibles
ollama list
Respuestas muy lentas
Soluciones:
1.	Usar modelo más ligero: phi en lugar de llama3
2.	Reducir num_predict en el código
3.	Cerrar otros programas que usen RAM
El tutor no mantiene el contexto
Verificar:
•	Que la función _obtener_contexto() esté retornando datos
•	Que ultimos_n no sea 0
•	Revisar que el historial se esté guardando correctamente

# Mejoras Futuras
Corto Plazo
•	[ ] Soporte para documentos PDF/DOCX como base de conocimientos
•	[ ] Interfaz web con Flask/Streamlit
•	[ ] Exportar conversaciones a archivo
Mediano Plazo
•	[ ] RAG completo con búsqueda semántica
Largo Plazo
•	[ ] Interfaz gráfica nativa
•	[ ] Integración con herramientas educativas (LMS)

