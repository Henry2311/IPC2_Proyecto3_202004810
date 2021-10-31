class solicitud_dte:
    def __init__(self,tiempo,referencia,n_emisor,n_receptor,valor,iva,total):
        self.tiempo=tiempo
        self.referencia = referencia
        self.n_emisor = n_emisor
        self.n_receptor = n_receptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.autorizacion=False
        self.list_e=[]

class aprobadas:
    def __init__(self,fecha,ref,codigo,emisor,receptor,iva):
        self.fecha = fecha
        self.ref = ref
        self.codigo = codigo
        self.emisor = emisor
        self.receptor = receptor
        self.iva = iva
    
class error_dte:
    def __init__(self):
        self.e_iva=0
        self.e_nitE=0
        self.e_nitR=0
        self.e_total=0
        self.r_duplex=0

    def analizar_datos(self,lista_dte):
        aux=list(set(lista_dte))
        for dte in lista_dte:
            self.mod11(dte.n_emisor,'E',dte.list_e)
            self.mod11(dte.n_receptor,'R',dte.list_e)
            self.iva(dte.iva,dte.valor,dte.list_e)
            self.total(dte.iva,dte.valor,dte.total,dte.list_e)

            duplex=len(lista_dte)-len(aux)

            if duplex == 0:
                print('referencias correctas')
            else:
                self.r_duplex+=1
                dte.list_e.append('Error en referencias')
                print('referencia duplicada')
            
            if len(dte.list_e) == 0:
                dte.autorizacion = True
            else:
                dte.autorizacion = False

    def mod11(self,nit,type,lista_e):
        val = 0
        pos=1

        for c in range(len(nit)-2,-1,-1):
            val+=pos*int(nit[c])
            pos+=1

            if pos==8:
                pos=1
        
        mod=11-(val%11)

        i=len(nit)-1
        if mod < 10:
            if nit[i]=='K' or nit[i]=='k':
                if type == 'E':
                    self.e_nitE+=1
                elif type == 'R':
                    self.e_nitR+=1
                lista_e.append('Error')
                print('error nit invalido')
            elif mod != int(nit[i]): 
                if type == 'E':
                    self.e_nitE+=1
                elif type == 'R':
                    self.e_nitR+=1
                lista_e.append('Error')
                print('error nit invalido')
            else:
                print('nit valido')
        elif mod == 10:
            if nit[i] == 'k' or nit[i] == 'K':
                print('nit valido')
            else:
                if type == 'E':
                    self.e_nitE+=1
                elif type == 'R':
                    self.e_nitR+=1
                lista_e.append('Error')
                print('error nit invalido')
        elif mod == 11:
            if int(nit[i]) == 0:
                print('nit valido')
            else:
                if type == 'E':
                    self.e_nitE+=1
                elif type == 'R':
                    self.e_nitR+=1
                lista_e.append('Error')
                print('error nit invalido')
        
    def iva(self,iva,valor,lista_e):
        verify = round(float(valor)*0.12,2)
        if verify == float(iva):
            print('iva correcto')
        else:
            self.e_iva+=1
            lista_e.append('Error')
            print('error iva invalido')

    def total(self,iva,valor,total,lista_e):
        verify = float(iva)+float(valor)
        if verify == float(total):
            print('total correcto')
        else:
            self.e_total+=1
            lista_e.append('Error')
            print('error iva invalido')


    
    