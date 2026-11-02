from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ClienteForm
from .models import Cliente


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente guardado: {cliente.nombre} ({cliente.correo})')
            return redirect('clientes_crear')
    else:
        form = ClienteForm()

    clientes = Cliente.objects.order_by('-id')
    return render(request, 'clientes/create.html', {
        'form': form,
        'clientes': clientes,
    })
