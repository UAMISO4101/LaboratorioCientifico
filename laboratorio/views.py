from django.shortcuts import render

# Create your views here.
def ir_index(request):
    return render(request,"laboratorio/index.html")
def ir_pie(request):
    return render(request,"laboratorio/pie.html")
def ir_encabezado(request):
    return render(request,"laboratorio/encabezado.html")