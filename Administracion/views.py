from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.cache import cache
from Bienes.models import Bienes
from .models import *
from .forms import *
import requests


def obtener_tasas_api():
    cache_key = 'tasas_cambio_completas'
    tasas = cache.get(cache_key)
    
    if not tasas:
        try:
            # Usar Frankfurter API (gratuita y confiable)
            url = 'https://api.frankfurter.app/latest?from=USD&to=VES'
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                dolar = data['rates']['VES']
                
                # Obtener euro desde USD
                url_eur = 'https://api.frankfurter.app/latest?from=EUR&to=USD,VES'
                response_eur = requests.get(url_eur, timeout=5)
                
                if response_eur.status_code == 200:
                    data_eur = response_eur.json()
                    euro_usd = data_eur['rates']['USD']
                    euro_ves = data_eur['rates']['VES']
                    
                    tasas = {
                        'dolar': f"{dolar:.2f}",
                        'euro': f"{euro_ves:.2f}",
                        'euro_usd': f"{euro_usd:.2f}",
                    }
                    
                    # Cache por 1 hora
                    cache.set(cache_key, tasas, 3600)
                else:
                    tasas = {
                        'dolar': f"{dolar:.2f}",
                        'euro': "No disponible",
                    }
            else:
                tasas = obtener_tasas_fallback()
                
        except Exception as e:
            print(f"Error en API: {e}")
            tasas = obtener_tasas_fallback()
    
    return tasas

def obtener_tasas_fallback():
    """API de respaldo"""
    try:
        # Usar ExchangeRate-API
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            dolar_ves = data['rates'].get('VES', 'N/A')
            
            # Obtener EUR
            url_eur = 'https://api.exchangerate-api.com/v4/latest/EUR'
            response_eur = requests.get(url_eur, timeout=5)
            
            if response_eur.status_code == 200:
                data_eur = response_eur.json()
                euro_ves = data_eur['rates'].get('VES', 'N/A')
                
                return {
                    'dolar': str(dolar_ves),
                    'euro': str(euro_ves),
                }
    except:
        pass
    
    return {
        'dolar': "No disponible",
        'euro': "No disponible",
    }

def Home(request):
    empleados = Empleado.objects.all().count()
    bienes = Bienes.objects.all().count()

    user = request.user

    tasas = obtener_tasas_api()
    
    context = {
        'empleados': empleados,
        'bienes': bienes,
        'euro': tasas.get('euro', 'No disponible'),
        'dolar': tasas.get('dolar', 'No disponible'),
        'user': user,
    }
    return render(request, 'home.html', context)

def Funcionarios(request):

    return render(request,"administracion/funcionarios.html")

@never_cache
@login_required
def lista_funcionarios(request):

    usuario_actual = request.user
    rol = get_user_role(usuario_actual)

    if rol == 'admin':

        entity = Empleado.objects.all()
        data = [
            {
                'cedula': c.document,
                'nombre': c.names, 
                'telefono': c.phone,
                'status': c.condition.capitalize(),
                'cargo': c.position,
                'area': c.area.name,
                'id': c.id,
                } for c in entity
            ]
        return JsonResponse({'data':data}, safe=False)
    
    elif rol[0] == 'encargado_bienes':
        area = rol[1]
        
        entity = Empleado.objects.filter(area=area)
        data = [
            {
                'cedula': c.document,
                'nombre': c.names, 
                'telefono': c.phone,
                'status': c.condition.capitalize(),
                'cargo': c.position,
                'area': c.area.name,
                'id': c.id,
                } for c in entity
            ]
        return JsonResponse({'data':data}, safe=False)
    
    else:

        entity = Empleado.objects.filter(user = usuario_actual)
        data = [
            {
                'cedula': c.document,
                'nombre': c.names, 
                'telefono': c.phone,
                'status': c.condition.capitalize(),
                'cargo': c.position,
                'area': c.area.name,
                'id': c.id,
                } for c in entity
            ]
        return JsonResponse({'data':data}, safe=False)

@never_cache
@login_required
def crear_funcionario(request):

    usuario_actual = request.user
    rol = get_user_role(usuario_actual)
    
    context = {
        'form': EmpleadoForm()
    }

    if rol == 'admin' or rol[0] == 'encargado_bienes':

        if request.method == 'POST':
            formulario = EmpleadoForm(request.POST, user=usuario_actual)
            if formulario.is_valid():
                empleado = formulario.save(commit=False)

                if rol[0] == 'encargado_bienes':
                    empleado.area = rol[1]  # Asignar el área del encargado
                
                empleado.save()
                messages.success(request, 'Empleado registrado exitosamente')

                return redirect('funcionarios')
            else:
                context['form'] = formulario
        return render(request, 'administracion/new_func.html', context)

def profile(request, id):


    employee = Empleado.objects.filter(user = id).first()

    context = {
        'employee': employee
    }
    
    return render(request, 'profile.html', context)


