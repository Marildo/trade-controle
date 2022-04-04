 function update_carteira(carteira_id){         
     fetch("/carteiras/update/"+carteira_id)
     .then(resp =>         console.log(resp) )
 }