# tu_app/management/commands/analizar_todos_groq.py
from django.core.management.base import BaseCommand
from django.db import transaction
from Bienes.models import Bienes
from services.groq_service import GroqService
import logging
from tqdm import tqdm
import time

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Analiza TODOS los bienes con Groq (versión mejorada)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Cantidad de registros a procesar por lote'
        )
        parser.add_argument(
            '--desde',
            type=int,
            help='Comenzar desde este ID'
        )
        parser.add_argument(
            '--solo-pendientes',
            action='store_true',
            help='Procesar solo los que no tienen part'
        )
        parser.add_argument(
            '--categoria',
            type=str,
            help='Filtrar por categoría específica'
        )
    
    def handle(self, *args, **options):
        groq_service = GroqService()
        batch_size = options['batch_size']
        desde_id = options.get('desde')
        solo_pendientes = options['solo_pendientes']
        categoria = options.get('categoria')
        
        # Construir query
        bienes_query = Bienes.objects.all()
        
        if desde_id:
            bienes_query = bienes_query.filter(id__gte=desde_id)
        
        if solo_pendientes:
            bienes_query = bienes_query.filter(part__isnull=True) | bienes_query.filter(part='')
        
        # Obtener total
        total = bienes_query.count()
        
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(f"ANÁLISIS DE BIENES CON GROQ")
        self.stdout.write(f"{'='*50}")
        self.stdout.write(f"Total a procesar: {total}")
        if categoria:
            self.stdout.write(f"Categoría: {categoria}")
        self.stdout.write(f"Batch size: {batch_size}")
        self.stdout.write(f"{'='*50}\n")
        
        if total == 0:
            self.stdout.write(self.style.WARNING("No hay bienes para procesar"))
            return
        
        # Estadísticas
        estadisticas = {
            'LAPTOP': 0,
            'COMPUTADOR_COMPLETO': 0,
            'COMPUTADOR_CON_CORNETAS': 0,
            'CPU_SOLO': 0,
            'MONITOR': 0,
            'TECLADO': 0,
            'MOUSE': 0,
            'IMPRESORA': 0,
            'SILLA': 0,
            'ESCRITORIO': 0,
            'OTRO': 0,
            'ERRORES': 0
        }
        
        procesados = 0
        errores = []
        
        # Procesar en lotes
        for i in range(0, total, batch_size):
            lote = bienes_query[i:i+batch_size]
            
            self.stdout.write(f"\nProcesando lote {i//batch_size + 1}/{(total+batch_size-1)//batch_size}")
            
            with transaction.atomic():
                for bien in tqdm(lote, desc="Bienes"):
                    try:
                        # Llamar a Groq
                        total_componentes, categoria_detectada = groq_service.analizar_con_groq(bien.description)
                        
                        # Actualizar el bien
                        part_anterior = bien.part or "vacío"
                        bien.part = f"0/{total_componentes}"
                        
                        # Actualizar condición según tipo
                        if total_componentes > 1:
                            bien.condition = 'Incompleto'
                        
                        bien.save()
                        
                        # Actualizar estadísticas
                        if categoria_detectada in estadisticas:
                            estadisticas[categoria_detectada] += 1
                        else:
                            estadisticas['OTRO'] += 1
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✓ {bien.bm}: {part_anterior} → {bien.part} [{categoria_detectada}]"
                            )
                        )
                        
                        procesados += 1
                        
                        # Pequeña pausa para no saturar la API
                        time.sleep(0.5)
                        
                    except Exception as e:
                        errores.append(f"{bien.bm}: {str(e)}")
                        estadisticas['ERRORES'] += 1
                        self.stdout.write(
                            self.style.ERROR(f"✗ Error en {bien.bm}: {str(e)}")
                        )
        
        # Mostrar estadísticas finales
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(self.style.SUCCESS("✅ ANÁLISIS COMPLETADO"))
        self.stdout.write(f"{'='*50}")
        self.stdout.write(f"\n📊 ESTADÍSTICAS:")
        self.stdout.write(f"   Total procesados: {procesados}")
        self.stdout.write(f"   Errores: {len(errores)}")
        self.stdout.write(f"\n📋 CLASIFICACIÓN:")
        
        for categoria, cantidad in estadisticas.items():
            if cantidad > 0 and categoria != 'ERRORES':
                porcentaje = (cantidad / procesados) * 100
                self.stdout.write(f"   {categoria}: {cantidad} ({porcentaje:.1f}%)")
        
        if estadisticas['ERRORES'] > 0:
            self.stdout.write(f"   ERRORES: {estadisticas['ERRORES']}")
        
        if errores:
            self.stdout.write(self.style.WARNING("\n⚠️ DETALLE DE ERRORES:"))
            for error in errores[:10]:  # Mostrar solo los primeros 10
                self.stdout.write(self.style.WARNING(f"   {error}"))
        
        self.stdout.write(f"{'='*50}")