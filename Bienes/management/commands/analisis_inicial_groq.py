# management/commands/analisis_inicial_groq.py
from django.core.management.base import BaseCommand
from django.db import transaction
from Bienes.models import Bienes
from services.groq_service import GroqService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'ANÁLISIS INICIAL: Determina cuántos componentes debe tener cada bien (solo ejecutar UNA VEZ)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--usar-groq',
            action='store_true',
            help='Usar Groq API para análisis más preciso (recomendado)'
        )
    
    def handle(self, *args, **options):
        groq_service = GroqService()
        usar_groq = options['usar_groq']
        
        bienes = Bienes.objects.filter(total_componentes__isnull=True)  # Solo los no analizados
        total = bienes.count()
        
        self.stdout.write(f"Analizando {total} bienes para determinar componentes requeridos...")
        
        actualizados = 0
        for bien in bienes:
            try:
                if usar_groq:
                    resultado = groq_service.analizar_con_groq(bien.description)
                else:
                    resultado = groq_service.determinar_componentes_requeridos(bien.description)
                
                # Actualizar el bien con la información determinada
                bien.tipo_bien = resultado['tipo']
                bien.total_componentes = resultado['total_requerido']
                bien.part = resultado['part_inicial']  # Ej: "0/4"
                
                # Inicializar campos de componentes según el tipo
                if resultado['tipo'] == 'COMPUTADOR':
                    bien.cpu_registrado = False
                    bien.monitor_registrado = False
                    bien.teclado_registrado = False
                    bien.mouse_registrado = False
                    bien.cornetas_registrado = (resultado['total_requerido'] == 5)
                
                bien.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ {bien.bm} -> {bien.part} ({resultado['tipo']})")
                )
                actualizados += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Error en {bien.bm}: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Análisis completado: {actualizados} bienes actualizados")
        )