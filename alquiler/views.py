import concurrent
from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Motocicleta, UsuarioRegistro, Reserva, AlteracionUsuario, TipoUsuario
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactoForm, ReservaForm, UsuarioForm
from datetime import timedelta

API_KEY = '96DbFvqidfnd56ps1VdwpA==KGJebGeaPxidodno'

modelos_deseados = [
    {'make': 'honda', 'model': 'cbr500r'},
    {'make': 'honda', 'model': 'xr150l'},
    {'make': 'honda', 'model': 'adv150'},
    {'make': 'honda', 'model': 'africa twin'},
    {'make': 'yamaha', 'model': 'fzs 25'},
    {'make': 'yamaha', 'model': 'mt-09'},
    {'make': 'yamaha', 'model': 'aerox 155'},
    {'make': 'yamaha', 'model': 'fjr1300ae'},
    {'make': 'suzuki', 'model': 'dr 650 se'},
    {'make': 'suzuki', 'model': 'gsx-r1000'},
    {'make': 'suzuki', 'model': 'dr-z400sm'},
    {'make': 'suzuki', 'model': 'burgman 400'},
    {'make': 'ktm', 'model': '1290 super duke gt'},
    {'make': 'ktm', 'model': '450 exc-f'},
    {'make': 'ktm', 'model': '250 exc tpi'},
    {'make': 'ktm', 'model': '125 sx'},
    {'make': 'kawasaki', 'model': 'brute force 300'},
    {'make': 'kawasaki', 'model': 'concours 14'},
    {'make': 'kawasaki', 'model': 'klr 650 adventure'},
    {'make': 'kawasaki', 'model': 'ninja 650'},
    {'make': 'bajaj', 'model': 'avenger cruise 220'},
    {'make': 'bajaj', 'model': 'pulsar rs200'},
    {'make': 'bajaj', 'model': 'pulsar ns200'},
    {'make': 'bajaj', 'model': 'dominar 400'},
    {'make': 'bmw', 'model': 'f 850 gs adventure'},
    {'make': 'bmw', 'model': 'g 310 r'},
    {'make': 'bmw', 'model': 'r 1250 r'},
    {'make': 'bmw', 'model': 'r 400 gt'},
    {'make': 'Husqvarna', 'model': '701 supermoto'},
    {'make': 'Husqvarna', 'model': 'svartpilen 125'},
    {'make': 'Husqvarna', 'model': 'fc 250'},
    {'make': 'Husqvarna', 'model': 'svartpilen 701'},
]

# Diccionario de precios personalizados por modelo
precios_modelos = {
    "cbr500r": 50000,
    "xr150l": 28000,
    "adv150": 31000,
    "africa twin": 87500,
    "fzs 25": 32000,
    "mt-09": 91500,
    "aerox 155": 29500,
    "fjr1300ae": 99000,
    "dr 650 se": 81000,
    "gsx-r1000": 84500,
    "dr-z400sm": 49000,
    "burgman 400": 40000,
    "1290 super duke gt": 115000,
    "450 exc-f": 67000,
    "250 exc tpi": 40000,
    "125 sx": 34500,
    "brute force 300": 45000,
    "concours 14": 98000,
    "klr 650 adventure": 87000,
    "ninja 650": 94000,
    "avenger cruise 220": 37500,
    "pulsar rs200": 60000,
    "pulsar ns200": 49000,
    "dominar 400": 58000,
    "f 850 gs adventure": 108000,
    "g 310 r": 50000,
    "r 1250 r": 135000,
    "c 400 gt": 56000,
    "701 supermoto": 82000,
    "svartpilen 125": 41500,
    "fc 250": 87000,
    "svartpilen 701": 78000,
}


tipos_modelos = {
    "cbr500r": "Deportiva",
    "xr150l": "Adventure",
    "adv150": "Ciudad",
    "africa twin": "Adventure",
    "fzs 25": "Ciudad",
    "mt-09": "Ciudad",
    "aerox 155": "Ciudad",
    "fjr1300ae": "Deportiva",
    "dr 650 se": "Enduro",
    "gsx-r1000": "Deportiva",
    "dr-z400sm": "Enduro",
    "burgman 400": "Ciudad",
    "1290 super duke gt": "Ciudad",
    "450 exc-f": "Enduro",
    "250 exc tpi": "Enduro",
    "125 sx": "Enduro",
    "brute force 300": "Enduro",
    "concours 14": "Deportiva",
    "klr 650 adventure": "Adventure",
    "ninja 650": "Deportiva",
    "avenger cruise 220": "Ciudad",
    "pulsar rs200": "Deportiva",
    "pulsar ns200": "Ciudad",
    "dominar 400": "Adventure",
    "f 850 gs adventure": "Adventure",
    "g 310 r": "Ciudad",
    "r 1250 r": "Deportiva",
    "c 400 gt": "Ciudad",
    "701 supermoto": "Enduro",
    "svartpilen 125": "Ciudad",
    "fc 250": "Enduro",
    "svartpilen 701": "Ciudad"
}


def obtener_moto(item):
    url = f"https://api.api-ninjas.com/v1/motorcycles?make={item['make']}&model={item['model']}"
    headers = {'X-Api-Key': API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            datos = response.json()
            coincidencias = [m for m in datos if m['model'].strip().lower() == item['model'].strip().lower()]
            if coincidencias:
                return max(coincidencias, key=lambda m: m.get('year', 0))
    except:
        pass
    return None

def llenar_db_si_vacia():
    if Motocicleta.objects.count() == 0:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            resultados = list(executor.map(obtener_moto, modelos_deseados))
        for moto in resultados:
            if moto:
                modelo_key = moto['model'].strip().lower()
                precio = int(precios_modelos.get(modelo_key, 45900))
                tipo = tipos_modelos.get(modelo_key, "Otro")  # Agregamos el tipo aquí

                Motocicleta.objects.create(
                    make=moto['make'],
                    model=moto['model'],
                    year=moto.get('year'),
                    power=moto.get('power', ''),
                    gearbox=moto.get('gearbox', ''),
                    cooling=moto.get('cooling', ''),
                    precio=precio,
                    tipo=tipo  
                )

def arrendar(request):
    llenar_db_si_vacia()


    # Obtener parámetros GET
    marca = request.GET.get('marca')
    estilo = request.GET.get('estilo')
    orden = request.GET.get('orden')

    # Base de datos de motos
    motocicletas = Motocicleta.objects.all()

    # Filtro por marca
    if marca:
        motocicletas = motocicletas.filter(make__iexact=marca)

    # Filtro por tipo de moto (estilo)
    if estilo:
        motocicletas = motocicletas.filter(tipo__iexact=estilo)

    # Orden por precio
    if orden == 'asc':
        motocicletas = motocicletas.order_by('precio')
    elif orden == 'desc':
        motocicletas = motocicletas.order_by('-precio')


        # ✅ Diccionario de traducción
    traducciones = {
        "5-speed": "5-Velocidades",
        "6-speed": "6-Velocidades",
        "Automatic": "Automática",
        "Liquid": "Líquida",
        "Air": "Aire",
        "Oil": "Aceite",
        "Water": "Agua"
    }

    # ✅ Aplicar traducción
    for moto in motocicletas:
        moto.gearbox = traducciones.get(moto.gearbox, moto.gearbox)
        moto.cooling = traducciones.get(moto.cooling, moto.cooling)

    # Obtener marcas y estilos únicos
    marcas = Motocicleta.objects.values_list('make', flat=True).distinct()
    estilos = Motocicleta.objects.values_list('tipo', flat=True).distinct()

    return render(request, 'arrendar.html', {
        'motocicletas': motocicletas,
        'marcas': marcas,
        'estilos': estilos
    })

def index(request):
    marcas = ['honda', 'yamaha', 'suzuki', 'bajaj', 'ktm', 'bmw', 'kawasaki', 'husqvarna']
    return render(request, 'index.html', {'marcas': marcas})

def contacto(request):
    return render(request, 'contacto.html')

def registro_usuario(request):
    if request.method == 'POST':
        # reCAPTCHA
        token = request.POST.get('g-recaptcha-response')
        secret_key = '6LdklC4rAAAAAKGtBkeNXxObeWSDnIyXDdzjS1z3'

        respuesta = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={'secret': secret_key, 'response': token}
        )
        resultado = respuesta.json()

        if not resultado.get('success'):
            messages.error(request, "Verifica que no eres un robot (captcha).")
            return redirect('registro')

        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        nacionalidad = request.POST.get('nacionalidad')
        contrasena = request.POST.get('contrasena')
        confirmar = request.POST.get('confirmar_contrasena')

        # Validaciones
        if contrasena != confirmar:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro')

        if UsuarioRegistro.objects.filter(correo=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect('registro')
        
        tipo_default = TipoUsuario.objects.get(codigo=0)


        nuevo_usuario = UsuarioRegistro(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            nacionalidad=nacionalidad,
            contrasena=contrasena,
            tipo_usuario=tipo_default
        )
        nuevo_usuario.save()

        messages.success(request, "Registro exitoso. ¡Bienvenido!")
        return redirect('login')

    return render(request, 'registro.html')


# login de usuario dioreccionado a inicio # login de usuario dioreccionado a inicio 
# login de usuario dioreccionado a inicio # login de usuario dioreccionado a inicio 
# login de usuario dioreccionado a inicio # login de usuario dioreccionado a inicio 

def login_usuario(request):
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '')

        try:
            usuario = UsuarioRegistro.objects.get(correo=correo)
        except UsuarioRegistro.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('login')

        # Validar con check_password
        if check_password(contrasena, usuario.contrasena):
            # Guardar datos mínimos en sesión
            request.session['usuario_id']     = usuario.id
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_correo'] = usuario.correo

            messages.success(request, f"¡Bienvenido de vuelta, {usuario.nombre}!")
            return redirect('index')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('login')

    return render(request, 'login.html')



# cerrar sesion# cerrar sesion# cerrar sesion# cerrar sesion
# cerrar sesion# cerrar sesion# cerrar sesion# cerrar sesion


@csrf_exempt  # solo si no estás usando {% csrf_token %}, aunque aquí sí lo usamos
def logout_usuario(request):
    if request.method == 'POST':
        request.session.flush()  # Elimina toda la sesión
        messages.success(request, "Sesión cerrada correctamente.")
        return redirect('index')
    return redirect('index')



def contacto_usuario(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save()
            messages.success(request,
                f"Gracias por tu mensaje, {contacto.nombre}. Te contactaremos al correo y/o teléfono ingresado dentro de las próximas 48 horas!"
            )
            return redirect('index')
    else:
        # Cargar datos del usuario si hay sesión
        inicial = {}
        if request.session.get('usuario_id'):
            try:
                from .models import UsuarioRegistro
                usuario = UsuarioRegistro.objects.get(id=request.session['usuario_id'])
                inicial['nombre'] = usuario.nombre
                inicial['correo'] = usuario.correo
                inicial['celular'] = usuario.telefono  # ✅ Aquí va el celular
            except UsuarioRegistro.DoesNotExist:
                pass

        form = ContactoForm(initial=inicial)

    return render(request, 'contacto.html', {'form': form})


def reserva_moto(request, moto_id):
    moto = get_object_or_404(Motocicleta, id=moto_id)

    # Traducciones de gearbox y cooling
    traducciones = {
        "5-speed": "5-Velocidades",
        "6-speed": "6-Velocidades",
        "Automatic": "Automática",
        "Liquid": "Líquida",
        "Air": "Aire",
        "Oil": "Aceite",
        "Water": "Agua"
    }
    moto.gearbox = traducciones.get(moto.gearbox, moto.gearbox)
    moto.cooling  = traducciones.get(moto.cooling, moto.cooling)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.motocicleta   = moto
            reserva.nombre_cliente = request.session.get('usuario_nombre', '')
            reserva.correo         = request.session.get('usuario_correo', '')
            reserva.total          = reserva.total_pagar()

            # Detectar botón presionado
            accion = request.POST.get('accion')
            if accion == 'reservar':
                reserva.estado_pago = 'PENDIENTE'
                messages.success(request, '🔥 Reserva realizada con éxito. ¡Gracias por preferir MotoRentCL! 🏍️')
            elif accion == 'pagar':
                reserva.estado_pago = 'PAGADO'
                messages.success(request, '💳 Pago realizado con éxito. Revisa tu correo para más detalles. ¡Gracias! 🔥🏍️💨')

            reserva.save()
            return redirect('index')

    else:
        # GET — precargamos nombre y correo
        form = ReservaForm(initial={
            'nombre_cliente': request.session.get('usuario_nombre', ''),
            'correo':         request.session.get('usuario_correo', '')
        })

    return render(request, 'reserva.html', {
        'moto': moto,
        'form': form
    })
def mi_perfil(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario = UsuarioRegistro.objects.get(id=request.session['usuario_id'])

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_modificado = form.save(commit=False)

            nueva_contrasena = form.cleaned_data.get('contrasena')
            if nueva_contrasena:
                usuario_modificado.contrasena = make_password(nueva_contrasena)

            usuario_modificado.save()
            request.session['usuario_nombre'] = usuario_modificado.nombre
            request.session['usuario_correo'] = usuario_modificado.correo

            AlteracionUsuario.objects.create(usuario=usuario_modificado, tipo='modificacion')

            messages.success(request, "¡Datos actualizados correctamente!")
            return redirect('index')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'mi_perfil.html', {'form': form})




def eliminar_usuario(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    try:
        usuario = UsuarioRegistro.objects.get(id=request.session['usuario_id'])
    except UsuarioRegistro.DoesNotExist:
        return redirect('login')

    # Registrar la eliminación
    AlteracionUsuario.objects.create(usuario=usuario, tipo='eliminacion')

    # Eliminar usuario y cerrar sesión
    usuario.delete()
    request.session.flush()

    return redirect('index')