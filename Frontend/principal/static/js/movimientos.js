function movimientos(){
    var date1 = format(document.querySelector('#movf').value)
    var tabla = document.querySelector('#Movimientos')
    var cadena = ''
    var param = {
        "MOV" : date1
    }

    console.log(param)

    fetch(`http://localhost:3000/peticionm`, {
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
                var nits=[];
                response.forEach(element => {
                   
                    console.log(element)
  
                    cadena += `<tr>
                      <td > ${element.Fecha} </td>
                      <td > ${element.Nit} </td>
                      <td > ${element.Emitido} </td>
                      <td > ${element.Recibido} </td>
                      </tr>`
                    nits.push(String(element.Nit))
                    valores.push({"emitido":element.Emitido,"recibido":element.Recibido,"nit":element.Nit})
                });
                tabla.innerHTML = cadena
                grafica2(nits,valores)
                
            })
    };

function format(date){
    return date.replace(/^(\d{4})-(\d{2})-(\d{2})$/g,'$3/$2/$1');
  }

function grafica2(nits,valores){
    const new_nits=[]

    for (var i = 0; i < nits.length; i++) {
        
        const elemento = nits[i];
 
        if (!new_nits.includes(nits[i])) {
            new_nits.push(elemento);
        }    
    }

    var emitido = [], temp=0;
    for (var i = 0; i < new_nits.length; i++) {  
        for (var j = 0; j < valores.length; j++) {
            if (valores[j].nit == new_nits[i]) {
                temp+=parseFloat(valores[j].emitido);
            }
        }
        emitido.push(temp);
        temp=0;
    }

    var recibido = [], temp=0;
    for (var i = 0; i < new_nits.length; i++) {  
        for (var j = 0; j < valores.length; j++) {
            if (valores[j].nit == new_nits[i]) {
                temp+=parseFloat(valores[j].recibido);
            }
        }
        recibido.push(temp);
        temp=0;
    }

    var data = {
        x: new_nits,
        y: emitido,
        name: 'Emitido',
        type: 'bar'
        };
    var data2 = {
        x: new_nits,
        y: recibido,
        name: 'Recibido',
        type: 'bar'
        }; 
    var data3 = [data,data2];  
    var type = {barmode: 'group'}; 
    
    Plotly.newPlot("ultima",data3,type);
};

