from flask import Flask,jsonify,request
from flask_cors import CORS
from solicitud import *
from datetime import datetime
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origin": "*"}})

root=''
root_s=''
solicitudes = []
autorizaciones = []
error_s = error_dte()

@app.route('/file', methods=['GET'])
def get_file():
    global root
    if root!='' and root_s!='':
        save_file = open(root, 'r')
        data=save_file.readlines()
        save_file.close()

        save_file2=open(root_s,'r')
        data2=save_file2.readlines()
        save_file2.close()

        return(jsonify({"ENTRADA":data,
                        "SALIDA":data2}))
    else:
        return(jsonify({"ENTRADA":"Ingrese un archivo de entrada",
                        "SALIDA":"Esperando..."}))


@app.route('/file', methods=['POST'])
def post_data():
    global root,root_s
    global solicitudes,autorizaciones,error_s

    if root=='':
        root='Backend\data\data.xml'
        url=request.json['URL']
        save_file=open(root,'w')
        data=str(url)
        print(data)
        data=data.replace('\\t','')
        print(data)
        save_file.write(data)
        save_file.close()
        save_data(root)
    else:
        new = request.json['URL']
        new = new.replace('<SOLICITUD_AUTORIZACION>','')
        save_ndata = open(root,'r')
        temp = save_ndata.read()
        save_ndata.close()
        temp = temp.replace('</SOLICITUD_AUTORIZACION>','')
        print('TEMP ANTES DE AÑADIR NUEVO')
        print(temp)
        temp+=new
        print(temp)
        new_data=open(root,'w')
        new_data.write(temp)
        new_data.close()
        solicitudes=[]
        autorizaciones=[]
        error_s=error_dte
        root_s=''

        save_data(root)

    return (jsonify({"MENSAJE":"archivo cargado"}))

@app.route('/file', methods=['DELETE'])
def delete_data():
    global root,root_s,solicitudes,autorizaciones,error_s

    d_file=open(root,'w')
    d_file.close()
    a_file=open(root_s,'w')
    a_file.close()
    
    root = ''
    root_s = ''
    solicitudes=[]
    autorizaciones=[]
    error_s = error_dte()   

    return jsonify({'Mensaje':'Se ha reseteado las entradas de autorizaciones'})

@app.route('/peticion', methods=['GET'])
def get_aprove():
    global root,root_s,solicitudes,autorizaciones

    if root!='' and root_s!='':
        dte_tabla=[]
        for aut in autorizaciones:
            for dte in solicitudes:
                if aut.fecha == dte.tiempo and aut.ref == dte.referencia:
                    data={"FECHA":dte.tiempo,
                          "REF":dte.referencia,
                          "EMISOR": dte.n_emisor,
                          "RECEPTOR":dte.n_receptor,
                          "VALOR":dte.valor,
                          "IVA":dte.iva,
                          "TOTAL":dte.total,
                          "CODIGO":aut.codigo}
                    dte_tabla.append(data)

        return(jsonify(dte_tabla))
    else:
        return(jsonify({"MENSAJE":"No hay autorizaciones disponibles"}))


@app.route('/peticionr', methods=['POST'])
def get_range_date():
    global root,root_s,solicitudes,autorizaciones
    
    date1 = datetime.strptime(request.json['INICIO'],'%d/%m/%Y')
    date2 = datetime.strptime(request.json['FIN'],'%d/%m/%Y')

    if root!='' and root_s!='':
        dte_tabla=[]
        for aut in autorizaciones:
            for dte in solicitudes:
                if aut.fecha == dte.tiempo and aut.ref == dte.referencia:
                    if date1 <= datetime.strptime(dte.tiempo,'%d/%m/%Y') <= date2:
                        data={"Fecha":dte.tiempo,
                              "Ref":dte.referencia,
                              "Valor":dte.valor,
                              "Total":dte.total,
                              "Codigo":aut.codigo}
                        dte_tabla.append(data)

        if dte_tabla:
            return(jsonify(dte_tabla))
        else:
            return(jsonify({"MENSAJE":"No hay autorizaciones disponibles"}))
    else:
        return(jsonify({"MENSAJE":"No hay autorizaciones disponibles"}))


@app.route('/peticionm', methods=['POST'])
def get_movimientos():
    global root,root_s,solicitudes,autorizaciones
    
    date1 = datetime.strptime(request.json['MOV'],'%d/%m/%Y')
    n_temp=[]
    for n in autorizaciones:
        if datetime.strptime(n.fecha,'%d/%m/%Y')==date1:
            n_temp.append(n.emisor)
            n_temp.append(n.receptor)
    
    n_temp = list(set(n_temp))
    if root!='' and root_s!='':
        dte_tabla=[]
        iva_r=0
        iva_e=0
        for n in n_temp:
            for dte in autorizaciones:
                if datetime.strptime(dte.fecha,'%d/%m/%Y')==date1:
                    if n == dte.emisor:
                        iva_e+=float(dte.iva)
                    elif n == dte.receptor:
                        iva_r+=float(dte.iva)
            
            fecha_temp=''
            for dte in autorizaciones:
                if datetime.strptime(dte.fecha,'%d/%m/%Y')==date1:
                    fecha_temp=dte.fecha
                    break

            data={"Fecha":fecha_temp,
                  "Nit":str(n)+'*',
                  "Emitido":str(iva_e),
                  "Recibido":str(iva_r)
            }        
            dte_tabla.append(data)
            iva_r=0
            iva_e=0

        if dte_tabla:
            return(jsonify(dte_tabla))
        else:
            return(jsonify({"MENSAJE":"No hay autorizaciones disponibles"}))
    else:
        return(jsonify({"MENSAJE":"No hay autorizaciones disponibles"}))

def save_data(path):
    global solicitudes

    mytree = ET.parse(path)
    file = mytree.getroot()

    time=[]
    ref=[]
    nit_e=[]
    nit_r=[]
    val=[]
    iva=[]
    total=[]

    for c in file.findall('./DTE/TIEMPO'):
        d=c.text.replace(' ','')
        patron=r'(\d{2})/(\d{2})/(\d{4})'
        fecha = re.findall(patron,d)
        tiempo=''

        for f in fecha[0]:
            tiempo+=str(f)+'/'

        tiempo=tiempo[:-1]

        time.append(tiempo)
    
    for c in file.findall('./DTE/REFERENCIA'):
        d=c.text.replace(' ','')
        ref.append(d)

    for c in file.findall('./DTE/NIT_EMISOR'):
        d=c.text.replace(' ','')
        d=d.replace('k','K')
        nit_e.append(d)

    for c in file.findall('./DTE/NIT_RECEPTOR'):
        d=c.text.replace(' ','')
        d=d.replace('k','K')
        nit_r.append(d)

    for c in file.findall('./DTE/VALOR'):
        d=c.text.replace(' ','')
        val.append(d)

    for c in file.findall('./DTE/IVA'):
        d=c.text.replace(' ','')
        iva.append(d)

    for c in file.findall('./DTE/TOTAL'):
        d=c.text.replace(' ','')
        total.append(d)

    for i in range(len(time)):
        print('*')
        solicitudes.append(solicitud_dte(time[i],ref[i],nit_e[i],nit_r[i],val[i],iva[i],total[i]))

    for c in solicitudes:
        print(c.n_emisor,c.n_receptor, c.tiempo)
    
    
    write_xml(solicitudes,time,nit_e,nit_r)

def write_xml(data,fechas,emisor,receptor):
    global root_s
    global error_s
    global autorizaciones   
    root_s='Backend\\data\\autorizaciones.xml'
    DTE=[]

    time_aux=[]
    result = []
    for item in fechas:
        if item not in result:
            result.append(item)

    #AGRUPACION POR FECHAS
    for i in range(len(result)):
        for j in range(len(data)):
            
            if result[i]==data[j].tiempo:
                time_aux.append(data[j]) #lista de autorizaciones
        DTE.append(time_aux) #lista de listas por fecha
        time_aux=[]

    error_s=error_dte()
    raiz=ET.Element('LISTAAUTORIZACIONES')
    for i in range(len(DTE)):
        autorizacion=ET.SubElement(raiz,'AUTORIZACION')
        fecha=ET.SubElement(autorizacion,'FECHA')
        fecha.text = str(DTE[i][0].tiempo)

        fac_r = ET.SubElement(autorizacion,'FACTURAS_RECIBIDAS')
        fac_r.text = str(len(DTE[i]))

        error_s.analizar_datos(DTE[i])

        errores = ET.SubElement(autorizacion,'ERRORES')
        n_emisor = ET.SubElement(errores,'NIT_EMISOR')
        n_emisor.text = str(error_s.e_nitE)

        n_receptor = ET.SubElement(errores,'NIT_RECEPTOR')
        n_receptor.text = str(error_s.e_nitR)

        e_iva = ET.SubElement(errores,'IVA')
        e_iva.text = str(error_s.e_iva)

        e_total = ET.SubElement(errores,'TOTAL')
        e_total.text = str(error_s.e_total)

        e_ref = ET.SubElement(errores,'REFERENCIA_DUPLICADA')
        e_ref.text = str(error_s.r_duplex)

        error_s=error_dte()

        correctas = 0
        cant_e = len(list(set(emisor)))
        cant_r = len(list(set(receptor)))

        for j in DTE[i]:
            if j.autorizacion == True:
                correctas+=1

        correct = ET.SubElement(autorizacion,'FACTURAS_CORRECTAS')
        correct.text = str(correctas)

        emi = ET.SubElement(autorizacion,'CANTIDAD_EMISORES')
        emi.text = str(cant_e)

        recep = ET.SubElement(autorizacion,'CANTIDAD_RECEPTORES')
        recep.text = str(cant_r)

        listado_a = ET.SubElement(autorizacion,'LISTADO_AUTORIZACIONES')
        fac=1
        
        for k in DTE[i]:
            if k.autorizacion == True:
                aprobacion = ET.SubElement(listado_a,'APORBACION')
                nit_emisor = ET.SubElement(aprobacion,'NIT_EMISOR',ref=str(k.referencia))
                nit_emisor.text = str(k.n_emisor)

                #codigo de aprobacion aaaammdd######## 8char maximo
                
                code_a = cod_aprobacion(DTE[i][0].tiempo,fac)
            
                codigo = ET.SubElement(aprobacion,'CODIGO_APROBACION')
                codigo.text = str(code_a)

                autorizaciones.append(aprobadas(DTE[i][0].tiempo,str(k.referencia),code_a,k.n_emisor,k.n_receptor,k.iva))

                fac+=1

        error_s=error_dte()


    structure(raiz)
    doc=ET.ElementTree(raiz)
    try:
        doc.write(root_s)
    except IOError as e:
        print(e)

def structure(root, tab='  '):
    aux = [(0, root)]
    while aux:
        line, e = aux.pop(0)
        lista = [(line + 1, c) for c in list(e)]
        if lista:
            e.text = '\n' + tab * (line+1)
        if aux:
            e.tail = '\n' + tab * aux[0][0]
        else:
            e.tail = '\n' + tab * (line-1) 
        aux[0:0] = lista

def cod_aprobacion(fecha,i):
    fecha=fecha.split('/')
    fecha=fecha[::-1]
    first=''
    for x in fecha:
        first+=x
    n=i
    second=''
    if n<=99999999:
        if n<=9:
            second='0000000'+str(n)
        elif n<=99:
            second='000000'+str(n)
        elif n<=999:
            second='00000'+str(n)
        elif n<=9999:
            second='0000'+str(n)
        elif n<=99999:
            second='000'+str(n)
        elif n<=999999:
            second='00'+str(n)
        elif n<=9999999:
            second='0'+str(n)
        else:
            second=str(n)

    aprobacion = first+second
    print(aprobacion)
    return aprobacion

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)