from django.shortcuts import render, redirect
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

    bien = Bienes.objects.get(id=id)
    form = addBien_form()
    if request.method == 'POST':
      
        if form.is_valid():
            form.save()
            return redirect('bienes')
    
    context = {
        'form': form,
        'bien': bien
    }
    return render(request, 'bienes/add_bien_det.html', context)
