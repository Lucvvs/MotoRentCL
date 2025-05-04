from django.shortcuts import render
import requests

API_KEY = '96DbFvqidfnd56ps1VdwpA==KGJebGeaPxidodno'

def arrendar(request):
    modelos_deseados = [
        {'make': 'honda', 'model': 'cbr500r'},
        {'make': 'honda', 'model': 'xr150l'},
        {'make': 'honda', 'model': 'ADV150'},
        {'make': 'honda', 'model': 'Africa Twin'},

        {'make': 'yamaha', 'model': 'fzs 25'},
        {'make': 'yamaha', 'model': 'mt-09'},
        {'make': 'yamaha', 'model': 'aerox 155'},
        {'make': 'yamaha', 'model': 'FJR1300AE'},

        {'make': 'suzuki', 'model': 'dr 650 se'},
        {'make': 'suzuki', 'model': 'gsx-r1000'},
        {'make': 'suzuki', 'model': 'dr-z400sm'},
        {'make': 'suzuki', 'model': 'Burgman 400'},

        {'make': 'ktm', 'model': '1290 Super Duke GT'},
        {'make': 'ktm', 'model': '450 EXC-F'},
        {'make': 'ktm', 'model': '250 EXC TPI'},
        {'make': 'ktm', 'model': '125 SX'},

        {'make': 'kawasaki', 'model': 'Brute Force 300'},
        {'make': 'kawasaki', 'model': 'Concours 14'},
        {'make': 'kawasaki', 'model': 'KLR 650 Adventure'},
        {'make': 'kawasaki', 'model': 'Ninja 650'},

        {'make': 'bajaj', 'model': 'Avenger Cruise 220'},
        {'make': 'bajaj', 'model': 'Pulsar RS200'},
        {'make': 'bajaj', 'model': 'Pulsar NS200'},
        {'make': 'bajaj', 'model': 'Dominar 400'},

        {'make': 'bmw', 'model': 'F 850 GS Adventure'},
        {'make': 'bmw', 'model': 'G 310 R'},
        {'make': 'bmw', 'model': 'R 1250 R'},
        {'make': 'bmw', 'model': 'C 400 GT'},

        {'make': 'Husqvarna', 'model': '701 Supermoto'},
        {'make': 'Husqvarna', 'model': 'Svartpilen 125'},
        {'make': 'Husqvarna', 'model': 'FC 250'},
        {'make': 'Husqvarna', 'model': 'Svartpilen 701'},


        
    ]

    motos_combinadas = []

    for item in modelos_deseados:
        url = f"https://api.api-ninjas.com/v1/motorcycles?make={item['make']}&model={item['model']}"
        response = requests.get(url, headers={'X-Api-Key': API_KEY})

        if response.status_code == 200:
            datos = response.json()
            # Filtrar coincidencia exacta de modelo
            coincidencias = [
                m for m in datos
                if m['model'].strip().lower() == item['model'].strip().lower()
            ]
            # Elegir la más nueva (por año)
            if coincidencias:
                moto_mas_nueva = max(coincidencias, key=lambda m: m.get('year', 0))
                motos_combinadas.append(moto_mas_nueva)

    return render(request, 'arrendar.html', {
        'motocicletas': motos_combinadas
    })

def index(request):
    marcas = ['honda', 'yamaha', 'suzuki', 'bajaj', 'ktm', 'bmw', 'kawasaki', 'husqvarna']
    return render(request, 'index.html', {'marcas': marcas})

def contacto(request):
    return render(request, 'contacto.html')

def registro(request):
    return render(request, 'registro.html')

def login(request):
    return render(request, 'login.html')