function range_date(){
    var date1 = format(document.querySelector('#inicio').value)
    var date2 = format(document.querySelector('#fin').value)
    var tabla = document.querySelector('#totales')
    var tabla2 = document.querySelector('#siniva')
    var cadena = ''
    var cadena2 = ''
    var param = {
        "INICIO" : date1,
        "FIN"    : date2
    }

    console.log(param)

    fetch(`http://localhost:3000/peticionr`, {
        	method: 'POST',
            body: JSON.stringify(param),
            headers:{
                'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',}})

			.then(res => res.json())
        	.catch(err => {
             console.error('Error:', err)
             alert("Ocurrio un error")
            })
			.then(response =>{
                
                console.log(response);
                var valores = [];
                var fechas=[];
                response.forEach(element => {
                   
                    console.log(element)
  
                    cadena += `<tr>
                      <td > ${element.Fecha} </td>
                      <td > ${element.Ref} </td>
                      <td > ${element.Total} </td>
                      <td > ${element.Codigo} </td>
                      </tr>`
                    cadena2 += `<tr>
                    <td > ${element.Fecha} </td>
                    <td > ${element.Ref} </td>
                    <td > ${element.Valor} </td>
                    <td > ${element.Codigo} </td>
                    </tr>`
                    valores.push({"fecha":element.Fecha,"total":element.Total,"valor":element.Valor})
                    fechas.push(element.Fecha)        
                });
                tabla.innerHTML = cadena
                tabla2.innerHTML = cadena2
                grafica(valores,fechas)
                $(document).ready(function(){
                    $('ul.tabs2 li a:first').addClass('active');
                    $('.secciones2 article').hide();
	                $('.secciones2 article:first').show()
                });

            })
    };

function format(date){
    return date.replace(/^(\d{4})-(\d{2})-(\d{2})$/g,'$3/$2/$1');
  }

function grafica(valores,fechas){
    const new_date=[]

    for (var i = 0; i < fechas.length; i++) {
        
        const elemento = fechas[i];
 
        if (!new_date.includes(fechas[i])) {
            new_date.push(elemento);
        }    
    }

    var totales = [], temp=0;
    for (var i = 0; i < new_date.length; i++) {  
        for (var j = 0; j < valores.length; j++) {
            if (valores[j].fecha == new_date[i]) {
                temp+=parseInt(valores[j].total);
            }
        }
        totales.push(temp);
        temp=0;
    }

    var siniva = [], temp=0;
    for (var i = 0; i < new_date.length; i++) {  
        for (var j = 0; j < valores.length; j++) {
            if (valores[j].fecha == new_date[i]) {
                temp+=parseInt(valores[j].valor);
            }
        }
        siniva.push(temp);
        temp=0;
    }

    var data = [{
        x: new_date,
        y: totales,
        type: 'bar'
        }];
    var data2 = [{
        x: new_date,
        y: siniva,
        type: 'bar'
        }];    
    Plotly.newPlot("grafico",data);
    Plotly.newPlot("grafico2",data2);
};

