"""
TUTOR EXPERTO CON OLLAMA - VERSIÓN FINAL
- Responde preguntas directamente (NO método socrático)
- Mantiene contexto de conversación
- Da recomendaciones expertas
- Evalúa técnicas y métodos
- Se especializa en el tema que elijas
"""

import os
import json
from dotenv import load_dotenv
from typing import List, Dict
import requests

load_dotenv()


class TutorExperto:
    """
    Tutor Experto que responde preguntas directamente
    Se especializa en el tema que el usuario elija
    """
    
    def __init__(self, tema: str, modelo: str = "llama3", base_url: str = "http://localhost:11434"):
        self.tema = tema
        self.modelo = modelo
        self.base_url = base_url
        self.api_url = f"{base_url}/api/chat"
        
        self._verificar_ollama()
        self.historial = []
        self.system_prompt = self._construir_system_prompt()
        self.few_shot = self._crear_few_shot()
        self._inicializar_chat()
    
    def _verificar_ollama(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise Exception("Ollama no responde")
            print(f"✅ Ollama conectado")
        except Exception as e:
            print(f"\n❌ ERROR: Ollama no está corriendo")
            print(f"   Ejecuta: ollama serve")
            raise e
    
    def _construir_system_prompt(self) -> str:
        return f"""<system_instruction>
Eres un TUTOR EXPERTO en: {self.tema}

<especialidad>
Tu ÚNICA área de conocimiento es: {self.tema}
Eres un experto que responde preguntas, da recomendaciones y explica conceptos.
</especialidad>

<como_responder>
1. Para CUALQUIER pregunta sobre {self.tema}:
    Responde directamente y de forma clara
    Explica con ejemplos cuando sea necesario
    Da tu opinión experta
    Recomienda cuando te lo pidan
    Evalúa técnicas, ejercicios o métodos que mencionen

2. Si te piden RECOMENDACIONES:
    Evalúa lo que proponen
    Di si es bueno o no, y por qué
    Sugiere alternativas o mejoras
    Explica ventajas y desventajas

3. Si te preguntan DATOS/HECHOS:
    Da la respuesta directa
    Agrega contexto relevante
    Explica por qué es importante

4. Si te preguntan CONCEPTOS:
    Explica claramente qué es
    Usa ejemplos del mundo real
    Da aplicaciones prácticas
</como_responder>

<temas_fuera_alcance>
Si te preguntan sobre temas que NO son {self.tema}:
1. Aclara amablemente que tu especialidad es solo {self.tema}
2. Haz una conexión creativa entre ese tema y {self.tema} si es posible
3. Redirige a {self.tema}
</temas_fuera_alcance>

<manejo_contexto>
IMPORTANTE: Mantén el hilo de la conversación.
- Lee el contexto previo antes de responder
- NO repitas información ya dicha
- NO preguntes obviedades ya establecidas
- Continúa desde donde quedó la conversación
</manejo_contexto>

<tono>
- Sé claro, directo y útil
- Explica de forma accesible
- Comparte tu conocimiento experto
- Sé amigable y profesional
</tono>
</system_instruction>"""
    
    def _crear_few_shot(self) -> List[Dict]:
        return [
            {
                "role": "user",
                "content": f"¿Quién fue [persona/evento importante de {self.tema}]?"
            },
            {
                "role": "assistant",
                "content": f"""[Respuesta directa sobre la persona/evento]

Además, es importante saber que [contexto adicional relevante].

Esto es significativo en {self.tema} porque [explicación del impacto]."""
            },
            {
                "role": "user",
                "content": f"Encontré estos ejercicios/métodos para [objetivo en {self.tema}]. ¿Me los recomiendas?"
            },
            {
                "role": "assistant",
                "content": f"""Excelente que investigaste. Déjame evaluarlos como experto:

Los ejercicios/métodos que encontraste son [buenos/parcialmente buenos/no los recomiendo] porque:
✅ Ventajas:
   - [Ventaja 1]: Esto ayuda a...
   - [Ventaja 2]: Es efectivo para...

 Puntos a mejorar:
   - [Limitación 1]: Le falta...
   - [Sugerencia 1]: Te recomendaría complementar con...

Mi recomendación completa:
- Sí, úsalos para [aspecto específico]
- Agrega [ejercicio/método complementario] porque [razón]
- Evita [error común] que podría [consecuencia negativa]

En resumen: [conclusión clara y accionable]"""
            },
            {
                "role": "user",
                "content": "Hablemos de [tema diferente a la especialidad]"
            },
            {
                "role": "assistant",
                "content": f"""Interesante tema, pero debo aclarar:

Soy un tutor especializado ÚNICAMENTE en {self.tema}. No puedo enseñarte sobre [otro tema] porque podría darte información incorrecta.

Sin embargo, ya que lo mencionas... ¿sabías que [conexión creativa entre ese tema y {self.tema}]?

Por ejemplo: [analogía concreta]

Si tienes preguntas sobre {self.tema}, estaré encantado de ayudarte con:
- Conceptos y teoría de {self.tema}
- Técnicas y métodos de {self.tema}
- Recomendaciones sobre {self.tema}"""
            }
        ]
    
    def _inicializar_chat(self):
        self.historial.append({"role": "system", "content": self.system_prompt})
        for ejemplo in self.few_shot:
            self.historial.append(ejemplo)
        print(f"✅ Tutor de {self.tema} listo")
    
    def _obtener_contexto(self, ultimos_n: int = 3) -> str:
        """Obtiene contexto de la conversación para mantener el hilo"""
        inicio = 1 + len(self.few_shot)
        mensajes = self.historial[inicio:]
        
        if not mensajes:
            return "Primera pregunta."
        
        ultimos = mensajes[-(ultimos_n * 2):]
        contexto = "CONVERSACIÓN PREVIA:\n"
        
        for msg in ultimos:
            if msg["role"] == "user":
                contenido = msg["content"]
                if "<pregunta>" in contenido:
                    contenido = contenido.split("<pregunta>")[1].split("</pregunta>")[0].strip()
                contexto += f"Estudiante: {contenido}\n"
            else:
                resp = msg["content"][:150] + "..." if len(msg["content"]) > 150 else msg["content"]
                contexto += f"Tutor: {resp}\n"
        
        return contexto
    
    def enviar_mensaje(self, mensaje: str) -> str:
        contexto = self._obtener_contexto()
        
        mensaje_xml = f"""<pregunta>
{mensaje}
</pregunta>

<contexto_previo>
{contexto}
</contexto_previo>

<instrucciones>
1. LEE el contexto previo - mantén el hilo de la conversación
2. NO repitas información ya dicha
3. Responde de forma DIRECTA y CLARA
4. Da tu opinión experta cuando te la pidan
5. Recomienda cuando te pidan recomendaciones
6. Explica con ejemplos cuando sea necesario

Tu especialidad: {self.tema}
Responde como un experto que comparte su conocimiento.
</instrucciones>"""
        
        self.historial.append({"role": "user", "content": mensaje_xml})
        
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.modelo,
                    "messages": self.historial,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_predict": 512
                    }
                },
                timeout=60
            )
            
            if response.status_code != 200:
                return f" Error {response.status_code}"
            
            respuesta = response.json()["message"]["content"]
            self.historial.append({"role": "assistant", "content": respuesta})
            
            return respuesta
            
        except Exception as e:
            return f" Error: {e}"
    
    def reiniciar(self):
        self.historial = []
        self._inicializar_chat()
        print("🔄 Conversación reiniciada")
    
    def ver_historial(self):
        inicio = 1 + len(self.few_shot)
        print("\n" + "="*70)
        print("HISTORIAL")
        print("="*70)
        
        for msg in self.historial[inicio:]:
            if msg["role"] == "user":
                contenido = msg["content"]
                if "<pregunta>" in contenido:
                    contenido = contenido.split("<pregunta>")[1].split("</pregunta>")[0].strip()
                print(f"\n🎓 Estudiante:\n{contenido}")
            else:
                print(f"\n🤖 Tutor:\n{msg['content']}")
        
        print("\n" + "="*70)


def main():
    print("="*70)
    print("🎓 TUTOR EXPERTO ESPECIALIZADO")
    print("="*70)
    print("\nEste tutor se especializará en UN tema que elijas.")
    print("Responderá tus preguntas de forma directa y clara.\n")
    
    print("Ejemplos de temas:")
    print("  • Deportes")
    print("  • Música")
    print("  • Economía")
    print("  • Matemáticas")
    print("  • Programación")
    print("  • O cualquier otro tema\n")
    
    tema = ""
    while not tema:
        tema = input("📚 ¿Tema del tutor? → ").strip()
        if not tema:
            print("⚠️  Debes ingresar un tema\n")
    
    print(f"\n✅ Crearé un tutor experto en: {tema}")
    print(f"   El tutor SOLO responderá sobre {tema}\n")
    
    print("Modelos:")
    print("1. llama3")
    print("2. mistral")
    print("3. phi\n")
    
    opcion = input("🤖 Modelo (1/2/3) [Enter = llama3]: ").strip()
    modelos = {"1": "llama3", "2": "mistral", "3": "phi", "": "llama3"}
    modelo = modelos.get(opcion, "llama3")
    
    print(f"\n⏳ Iniciando tutor de {tema}...\n")
    
    try:
        tutor = TutorExperto(tema=tema, modelo=modelo)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Loop principal que permite cambiar de tema
    while True:
        print("\n" + "="*70)
        print(f"✅ TUTOR DE {tema.upper()} LISTO")
        print("="*70)
        print("\nComandos:")
        print("  • 'salir'       → Terminar programa")
        print("  • 'reiniciar'   → Nueva conversación (mismo tema)")
        print("  • 'cambiar'     → Cambiar de tema")
        print("  • 'historial'   → Ver conversación completa\n")
        print(f"Ahora puedes preguntar sobre {tema}")
        print("="*70 + "\n")
        
        cambiar_tema = False
        
        while not cambiar_tema:
            try:
                entrada = input(f"🎓 Pregunta sobre {tema}: ").strip()
                
                if not entrada:
                    continue
                
                if entrada.lower() == "salir":
                    print("\n👋 ¡Hasta pronto!\n")
                    print("="*70)
                    print("FIN DE SESIÓN")
                    print(f"Último tema: {tema} | Modelo: {modelo}")
                    print("="*70 + "\n")
                    return  # Salir del programa completamente
                
                if entrada.lower() == "cambiar":
                    print("\n🔄 Cambiando de tema...\n")
                    cambiar_tema = True
                    break
                
                if entrada.lower() == "reiniciar":
                    tutor.reiniciar()
                    continue
                
                if entrada.lower() == "historial":
                    tutor.ver_historial()
                    continue
                
                print("\n⏳ Pensando...\n")
                respuesta = tutor.enviar_mensaje(entrada)
                print(f"🤖 Tutor:\n{respuesta}\n")
                print("-"*70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n✋ Interrumpido")
                return
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        # Si llegamos aquí, es porque eligió "cambiar"
        if cambiar_tema:
            print("Ejemplos de temas:")
            print("  • Deportes")
            print("  • Música")
            print("  • Economía")
            print("  • Matemáticas")
            print("  • Programación")
            print("  • O cualquier otro tema\n")
            
            nuevo_tema = ""
            while not nuevo_tema:
                nuevo_tema = input("📚 ¿Nuevo tema del tutor? → ").strip()
                if not nuevo_tema:
                    print("⚠️  Debes ingresar un tema\n")
            
            tema = nuevo_tema
            print(f"\n✅ Cambiando a: {tema}")
            print(f"⏳ Iniciando nuevo tutor...\n")
            
            try:
                tutor = TutorExperto(tema=tema, modelo=modelo)
            except Exception as e:
                print(f"\n❌ Error al cambiar tema: {e}")
                return


if __name__ == "__main__":
    main()