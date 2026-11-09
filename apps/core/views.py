from django.shortcuts import render
from apps.Bodega.models import Figura, Categoria


def inicio(request):
    categorias = Categoria.objects.filter(activo=True)
    destacadas = Figura.objects.filter(activo=True, destacado=True).select_related('categoria')[:4]
    return render(request, 'core/index.html', {
        'categorias': categorias,
        'destacadas': destacadas,
    })


def nosotros(request):
    return render(request, 'core/nosotros.html')