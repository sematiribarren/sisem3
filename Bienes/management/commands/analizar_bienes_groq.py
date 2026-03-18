# management/commands/analizar_bienes_groq.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q  # Importamos Q para las consultas complejas
from Bienes.models import Bienes  # Reemplaza 'tu_app' con el nombre real de tu app
from services.groq_service import GroqService
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'ANÁLISIS INICIAL: Determina cuántos componentes debe tener cada bien y establece part (0/X)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=20,
            help='Cantidad de registros a procesar por lote'
        )
        parser.add_argument(
            '--sin-groq',
            action='store_true',
            help='Usar solo método manual (sin API)'
        )
        parser.add_argument(
            '--bm',
            type=str,
            help='Analizar solo un BM específico'
        )
    
    def handle(self, *args, **options):
        # Crear instancia del servicio Groq
        if not options['sin_groq']:
            groq_service = GroqService()
        else:
            groq_service = None
            
        batch_size = options['batch_size']
        bm_especifico = options.get('bm')
        
        # Filtrar bienes (solo los que no tienen part o tienen part vacío)
        if bm_especifico:
            bienes = Bienes.objects.filter(bm=bm_especifico)
            self.stdout.write(f"Analizando bien específico: {bm_especifico}")
        else:
            # CORREGIDO: Usamos Q en lugar de models.Q
            bienes = Bienes.objects.filter(
                Q(part__isnull=True) | 
                Q(part='')
            )
        
        total = bienes.count()
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No hay bienes pendientes de análisis"))
            return
        
        self.stdout.write(f"Analizando {total} bienes para determinar componentes requeridos...")
        
        actualizados = 0
        errores = []
        
        # Procesar en lotes
        for i in range(0, total, batch_size):
            lote = bienes[i:i+batch_size]
            
            with transaction.atomic():
                for bien in tqdm(lote, desc=f"Lote {i//batch_size + 1}"):
                    try:
                        # Determinar total de componentes
                        if groq_service:
                            total_componentes = groq_service.analizar_con_groq(bien.description)
                        else:
                            # Si no hay servicio Groq, usar método manual
                            if groq_service:
                                total_componentes = groq_service._determinar_manual(bien.description)
                            else:
                                # Si groq_service es None, crear instancia temporal para método manual
                                temp_service = GroqService()
                                total_componentes = temp_service._determinar_manual(bien.description)
                        
                        # Establecer part inicial (0/total)
                        bien.part = f"0/{total_componentes}"
                        
                        # Actualizar condition según el tipo
                        if total_componentes > 1:
                            bien.condition = 'Incompleto'  # Inicialmente incompleto
                        
                        bien.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ {bien.bm}: {bien.description[:50]}... -> {bien.part}")
                        )
                        actualizados += 1
                        
                    except Exception as e:
                        errores.append(f"{bien.bm}: {str(e)}")
                        self.stdout.write(
                            self.style.ERROR(f"✗ Error en {bien.bm}: {str(e)}")
                        )
                        logger.error(f"Error procesando {bien.bm}: {str(e)}")
        
        # Resumen
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Análisis completado:\n"
                f"   Actualizados: {actualizados}\n"
                f"   Errores: {len(errores)}"
            )
        )
        
        if errores:
            self.stdout.write(self.style.WARNING("\nDetalle de errores:"))
            for error in errores:
                self.stdout.write(self.style.WARNING(f"  - {error}"))