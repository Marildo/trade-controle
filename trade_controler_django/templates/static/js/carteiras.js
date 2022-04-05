function update_ativos(){
     console.log('resp')
     fetch("/ativos/update_prices/")
     .then(resp =>         console.log(resp) )
}