function exportarpdf(){
    var element = document.getElementById("rango")
    var fecha1 = document.querySelector('#inicio').value
    var fecha2 = document.querySelector('#fin').value
    let date = "Rango: "+format(String(fecha1))+" - "+format(String(fecha2))

    var ePDF = element.outerHTML
    console.log(ePDF)
    ePDF = ePDF.replace('<article id="tab11" style="">','<h6 style="text-align: center; font-size: 24px;">Resumen por Rango de Fechas</h6><h6 style="text-align: center; font-size: 18px;">'+date+'</h6><h6>Ver Totales:</h6><article id="tab11" style="">')
    ePDF = ePDF.replace('<article id="tab22" style="display: none;">','<h6>Ver sin IVA:</h6><article id="tab22" style="display: none;">')
    ePDF = ePDF.replace('display: none;','')
    var opt = {
        margin:       [2,2,1,2],
        filename:     'rango_fechas.pdf',
        image:        { type: 'jpeg', quality: 0.99 },
        html2canvas:  { scale: 4 },
        jsPDF:        { unit: 'cm', format: 'letter', orientation: 'portrait' }
      };
     
    html2pdf().set(opt).from(ePDF).save();
    
}

function format(date){
    return date.replace(/^(\d{4})-(\d{2})-(\d{2})$/g,'$3/$2/$1');
  }

function exportarpdf2(){
    var element = document.getElementById("contenedorpdf2")
    var fecha1 = document.querySelector('#movf').value
    let date = "Busqueda: "+format(String(fecha1))
    //2021-01-15 --> 15/01/2021
  
    var ePDF = element.outerHTML
    console.log(ePDF)
    ePDF = ePDF.replace('<div id="main-container">','<h6 style="text-align: center; font-size: 24px;">Movimientos de Nits</h6><h6 style="text-align: center; font-size: 18px;">'+date+'</h6><div id="main-container">')
    
    var opt = {
        margin:       [1,2,1,2],
        filename:     'rango_fechas.pdf',
        image:        { type: 'jpeg', quality: 0.99 },
        html2canvas:  { scale: 4 },
        jsPDF:        { unit: 'cm', format: 'letter', orientation: 'portrait' }
      };
     
    html2pdf().set(opt).from(ePDF).save();
}