const axios = require('axios')
const baseURL = 'http://cotacoes.economia.uol.com.br/ws/asset/';


async function locateAcao(sigla) {
    try {
        const resp = await axios.get(baseURL + 'stock/list')
        const acoes = resp.data.data;
        const acao = acoes
            .filter(a => a.code.replace(".SA", "").toUpperCase() === sigla.toUpperCase())[0]
        if (!acao) {
            return null
        }

        const code = acao.code.replace(".SA", "")
        return {
            ...acao,
            code
        }
    } catch (err) {
        console.log(err)
        return new Error(err)
    }
}

async function findCotacao(id) {
    try {
        const resp = await axios.get(baseURL + id + '/intraday?replicate=true')
        const cotacoes = resp.data.data
        if (!cotacoes) {
            return null
        }
        return cotacoes[0];
    } catch (err) {
        console.log(err)
        return null
    }
}

module.exports = { locateAcao, findCotacao }