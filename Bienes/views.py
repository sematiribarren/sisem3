from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *

# Create your views here.


def bienes(request):
    return render(request, 'bienes/bienes.html')

def lista_bienes(request):

    entity = Bienes.objects.all()
    data = [
        {
            'bm': c.bm,
            'descripcion': c.description,
            'partes': c.part,
            'status': c.condition.capitalize(),
            'id': c.id,
            } for c in entity
        ]
    return JsonResponse({'data':data}, safe=False)

def add_bien(request, id):
    import logging
    logger = logging.getLogger(__name__)
    
    bien_fisico = get_object_or_404(Bienes, id=id)
    
    if request.method == 'POST':
        form = addBien_form(request.POST)
        
        condition_bien = request.POST.get('condition') 
        
        print("="*50)
        print("Datos POST recibidos:", request.POST)
        print("Condición de bien recibida:", condition_bien)
        print("="*50)
        
        if form.is_valid():
            print("Formulario válido, procesando...")
            
            if bien_fisico.part and '/' in bien_fisico.part:
                try:
                    actual, total = map(int, bien_fisico.part.split('/'))
                    
                    if actual < total:
                        actual += 1
                        nuevo_part = f"{actual}/{total}"
                        
                        if actual == total:
                            bien_fisico.condition = 'Completo'
                            print("Bien físico marcado como Completo")
                        else:
                            bien_fisico.condition = 'Incompleto'
                            print("Bien físico marcado como Incompleto")
                        
                        bien_fisico.part = nuevo_part
                        bien_fisico.save()
                        print(f"Part actualizado: {nuevo_part}")
                        
                except ValueError as e:
                    print(f"Error al procesar part: {e}")
            
            try:
                form.instance.bm_worker = bien_fisico.bm
                form.instance.id_bien = bien_fisico
                
                if condition_bien:
                    form.instance.condition = condition_bien
                    print(f"Asignando condición: {condition_bien} a la instancia")
                
                asignacion = form.save()
                
                print(f"Asignación guardada exitosamente con ID: {asignacion.id}")
                print(f"Condición guardada: {asignacion.condition}")
                print(f"Condición en BD: {Bienes_persona.objects.get(id=asignacion.id).condition}")
                
                return redirect('bienes')
                
            except Exception as e:
                print(f"Error al guardar asignación: {e}")
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = addBien_form()
    
    context = {
        'form': form,
        'bien': bien_fisico, 
        'form_errors': form.errors if hasattr(form, 'errors') else None
    }
    
    return render(request, 'bienes/add_bien_det.html', context)


def bienes_detallado(request, id):
    bien = get_object_or_404(Bienes, id=id)
    bienes_asignados = Bienes_persona.objects.filter(id_bien=bien)
    context = {
        'bienes_asignados': bienes_asignados,
        'bienes': bien
    }
    return render(request, 'bienes/bienes_det.html', context)
