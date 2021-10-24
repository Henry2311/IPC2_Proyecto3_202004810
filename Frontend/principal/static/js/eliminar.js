function ELIMINAR(){
    var obj = {'Del':"yes"}

    fetch(`http://localhost:3000/file`,{
      method: 'DELETE',
      body: JSON.stringify(obj),
      headers:{
        'Content-Type':'aplication/json',
        'Access-Control-Allow-Origin':'*',}})

        .then(res => res.json())
        .catch(err => {
          console.error('Error:',err)
          alert("Ocurrio un error, ver consola")
        })
        .then(response => {
          console.log(response);
          alert(response.Mensaje)
        })
        location.reload()
      }