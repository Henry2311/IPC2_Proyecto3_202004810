from django.shortcuts import render, redirect
import requests
# Create your views here.

port = 'http://localhost:3000{}'

def index(request):
    if request.method == 'GET':
        url = port.format('/file')  # http://localhost:3000/file
        data = requests.get(url).json()  # consulta a la API
        context = {
            'data': data,
        }
        return render(request, 'index.html', context)

    elif request.method == 'POST':
        docs = str(request.FILES['document'].read())
        docs=docs.replace("b'",'')
        docs=docs.replace("'",'')
        docs=docs.replace("\\r\\n",'\n')
        data = {'URL': str(docs)}
        url = port.format('/file')
        requests.post(url, json=data)
        return redirect('index')

def peticiones(request):
    if request.method == 'GET':
        url = port.format('/peticion')  # http://localhost:3000/file
        data = requests.get(url).json()  # consulta a la API
        context = {
            'data': data,
        }
        return render(request, 'peticiones.html',context)
