import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializar cliente de Gemini con la SDK oficial
client = None
if GEMINI_API_KEY.strip():
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error al inicializar el cliente de Gemini: {e}")

def analizar_sentimiento(comentario: str) -> str:
    """Evalúa el comentario en español con Gemini y determina si es Positivo, Neutral o Negativo."""
    if not client:
        return "Neutral (Falta API Key)"

    try:
        # Prompt en español especificando la interpretación del idioma
        prompt = (
            "Eres un experto analista de sentimientos de reseñas de clientes en idioma ESPAÑOL.\n"
            "Analiza detenidamente el siguiente comentario en español sobre un negocio local y evalúa su intención emocional.\n"
            "REGLA OBLIGATORIA: Debes responder ÚNICAMENTE con una de estas tres palabras exactas: 'Positivo', 'Neutral', o 'Negativo'.\n"
            "No incluyas explicaciones, puntuación, signos ni palabras adicionales.\n\n"
            f"Comentario del cliente: \"{comentario}\"\n"
            "Sentimiento:"
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        
        texto_respuesta = response.text.strip().capitalize()
        
        # Filtro estricto para retornar el valor esperado
        if "Positivo" in texto_respuesta:
            return "Positivo"
        elif "Negativo" in texto_respuesta:
            return "Negativo"
        elif "Neutral" in texto_respuesta:
            return "Neutral"
        
        return "Neutral"
    except Exception as err:
        print(f"Excepción al analizar sentimiento con Gemini: {err}")
        return "Neutral"

def generar_resumen_opiniones(lista_resenas: list) -> str:
    """Genera una síntesis en español de todas las opiniones registradas."""
    if not lista_resenas:
        return "No hay reseñas registradas para generar un resumen."

    if not client:
        return "Falta configurar GEMINI_API_KEY en el archivo .env."

    comentarios_str = "\n".join([f"- [{r.calificacion}/5 estrellas] {r.cliente}: {r.comentario}" for r in lista_resenas])

    try:
        prompt = (
            "Eres un consultor de negocios locales. A continuación tienes un listado de opiniones de clientes escritas en español:\n"
            f"{comentarios_str}\n\n"
            "Redacta un resumen analítico en español (máximo 3 párrafos) que identifique los puntos fuertes principales y las áreas de mejora sugeridas por los clientes."
        )
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as err:
        return f"Error al generar el resumen con Gemini: {str(err)}"