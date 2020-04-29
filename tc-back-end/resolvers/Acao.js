
module.exports = {
    quantidade(acao) {
        return Math.floor(
            Math.random() * (1000 - 1) + 1
        )
    },

    setor(acao){         
       return {id:acao.setor_id,
               nome:acao.setor
              }
    },

    subsetor({subsetor_id,subsetor}){
        return {id:subsetor_id,
                nome:subsetor
               }
     },

     segmento({segmento_id,segmento}){
        return {id:segmento_id,
                nome:segmento
               }
     }
}