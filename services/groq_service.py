# tu_app/services/groq_service.py
import os
from groq import Groq
from dotenv import load_dotenv
import logging
import re
import time

load_dotenv()

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv('GROQ_API_KEY')
        )
        self.model = "mixtral-8x7b-32768"
    
    def analizar_con_groq(self, descripcion):
        """
        Usa Groq para determinar cuántos componentes DEBE tener un bien
        Versión mejorada con categorías específicas
        """
        
        # Categorías y sus componentes esperados
        categorias = {
            'LAPTOP': {
                'palabras_clave': ['LAPTOP', 'NOTEBOOK', 'PORTATIL', 'MACBOOK'],
                'componentes': 2,  # Laptop + cargador
                'descripcion': 'Laptop (incluye cargador)'
            },
            'COMPUTADOR_COMPLETO': {
                'palabras_clave': ['COMPUTADOR', 'PC', 'DESKTOP', 'EQUIPO', 'VIT', 'PENTIUM', 'CORE', 'CPU'],
                'componentes': 4,  # CPU, monitor, teclado, mouse
                'descripcion': 'Computador de escritorio completo'
            },
            'COMPUTADOR_CON_CORNETAS': {
                'palabras_clave': ['CORNETA', 'PARLANTE', 'SPEAKER', 'AUDIFONO'],
                'componentes': 5,  # CPU, monitor, teclado, mouse, cornetas
                'descripcion': 'Computador con cornetas'
            },
            'CPU_SOLO': {
                'palabras_clave': ['CPU', 'GABINETE', 'TORRE'],
                'componentes': 1,  # Solo la CPU
                'descripcion': 'CPU/torre sola'
            },
            'MONITOR': {
                'palabras_clave': ['MONITOR', 'LCD', 'LED', 'PANTALLA'],
                'componentes': 1,  # Monitor solo
                'descripcion': 'Monitor individual'
            },
            'TECLADO': {
                'palabras_clave': ['TECLADO', 'KEYBOARD'],
                'componentes': 1,  # Teclado solo
                'descripcion': 'Teclado individual'
            },
            'MOUSE': {
                'palabras_clave': ['MOUSE', 'RATON'],
                'componentes': 1,  # Mouse solo
                'descripcion': 'Mouse individual'
            },
            'IMPRESORA': {
                'palabras_clave': ['IMPRESORA', 'PRINTER', 'MULTIFUNCIONAL'],
                'componentes': 1,  # Impresora sola
                'descripcion': 'Impresora'
            },
            'SILLA': {
                'palabras_clave': ['SILLA', 'CHAIR', 'SILLON'],
                'componentes': 1,  # Silla sola
                'descripcion': 'Silla'
            },
            'ESCRITORIO': {
                'palabras_clave': ['ESCRITORIO', 'MESA', 'DESK'],
                'componentes': 1,  # Escritorio solo
                'descripcion': 'Escritorio'
            },
            'OTRO': {
                'palabras_clave': [],
                'componentes': 1,  # Por defecto
                'descripcion': 'Bien individual'
            }
        }
        
        # Prompt mejorado para Groq
        prompt = f"""
        Analiza la siguiente descripción de un bien de inventario y determina QUÉ TIPO de equipo es y CUÁNTOS componentes físicos debería tener.

        Descripción: "{descripcion}"

        REGLAS DE CLASIFICACIÓN:
        1. LAPTOP/NOTEBOOK: Siempre debe tener 2 componentes (la laptop y su cargador)
        2. COMPUTADOR DE ESCRITORIO COMPLETO: Debe tener 4 componentes (CPU, monitor, teclado, mouse)
        3. COMPUTADOR CON CORNETAS: Debe tener 5 componentes (CPU, monitor, teclado, mouse, cornetas)
        4. CPU SOLA (sin monitor): Debe tener 1 componente (solo la CPU)
        5. MONITOR SOLO: Debe tener 1 componente
        6. TECLADO SOLO: Debe tener 1 componente
        7. MOUSE SOLO: Debe tener 1 componente
        8. IMPRESORA: Debe tener 1 componente
        9. SILLA: Debe tener 1 componente
        10. ESCRITORIO: Debe tener 1 componente
        11. CUALQUIER OTRO BIEN: Debe tener 1 componente

        Responde ÚNICAMENTE con el número de componentes (1, 2, 4 o 5) y la categoría, en este formato:
        [número]|[categoría]
        
        Ejemplos:
        - "Laptop Dell Latitude" -> 2|LAPTOP
        - "Computador VIT Pentium Dual Core con monitor, teclado y mouse" -> 4|COMPUTADOR_COMPLETO
        - "CPU VIT modelo 3500" -> 1|CPU_SOLO
        - "Monitor Samsung 20 pulgadas" -> 1|MONITOR
        - "Silla ergonómica negra" -> 1|SILLA
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en clasificación de inventarios. Debes ser preciso en determinar el tipo de equipo y sus componentes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=30
            )
            
            respuesta = response.choices[0].message.content.strip()
            logger.info(f"Respuesta de Groq: {respuesta}")
            
            # Parsear la respuesta
            if '|' in respuesta:
                partes = respuesta.split('|')
                total = int(partes[0].strip())
                categoria = partes[1].strip()
            else:
                # Si no viene con formato, intentar extraer solo el número
                numeros = re.findall(r'\d+', respuesta)
                if numeros:
                    total = int(numeros[0])
                    categoria = "DETECTADA"
                else:
                    total = self._determinar_manual(descripcion)
                    categoria = "MANUAL"
            
            # Validar que sea un número válido
            if total in [1, 2, 4, 5]:
                return total, categoria
            else:
                logger.warning(f"Número inválido {total}, usando método manual")
                return self._determinar_manual(descripcion), "MANUAL"
                
        except Exception as e:
            logger.error(f"Error con Groq: {e}")
            return self._determinar_manual(descripcion), "MANUAL_FALLBACK"
    
    def _determinar_manual(self, descripcion):
        """
        Método manual mejorado con más categorías
        """
        descripcion_upper = descripcion.upper()
        
        # 1. Detectar LAPTOP
        if any(p in descripcion_upper for p in ['LAPTOP', 'NOTEBOOK', 'PORTATIL', 'MACBOOK']):
            logger.info(f"Detectado LAPTOP: {descripcion[:50]}")
            return 2
        
        # 2. Detectar COMPUTADOR COMPLETO (con mención de componentes)
        if any(pc in descripcion_upper for pc in ['COMPUTADOR', 'PC', 'DESKTOP', 'EQUIPO', 'VIT', 'PENTIUM', 'CORE']):
            # Verificar si menciona componentes específicos
            if 'MONITOR' in descripcion_upper or 'TECLADO' in descripcion_upper or 'MOUSE' in descripcion_upper:
                # Verificar si tiene cornetas
                if any(p in descripcion_upper for p in ['CORNETA', 'PARLANTE', 'SPEAKER']):
                    logger.info(f"Detectado COMPUTADOR CON CORNETAS: {descripcion[:50]}")
                    return 5
                else:
                    logger.info(f"Detectado COMPUTADOR COMPLETO: {descripcion[:50]}")
                    return 4
        
        # 3. Detectar CPU SOLA
        if 'CPU' in descripcion_upper and not any(comp in descripcion_upper for comp in ['MONITOR', 'TECLADO', 'MOUSE']):
            logger.info(f"Detectado CPU SOLA: {descripcion[:50]}")
            return 1
        
        # 4. Detectar MONITOR SOLO
        if 'MONITOR' in descripcion_upper and not any(pc in descripcion_upper for pc in ['COMPUTADOR', 'CPU']):
            logger.info(f"Detectado MONITOR SOLO: {descripcion[:50]}")
            return 1
        
        # 5. Detectar COMPONENTES INDIVIDUALES
        componentes_individuales = ['TECLADO', 'MOUSE', 'IMPRESORA', 'SILLA', 'ESCRITORIO', 'MESA']
        for comp in componentes_individuales:
            if comp in descripcion_upper:
                logger.info(f"Detectado {comp}: {descripcion[:50]}")
                return 1
        
        # 6. Por defecto
        logger.info(f"Tipo no detectado, asumiendo bien individual: {descripcion[:50]}")
        return 1