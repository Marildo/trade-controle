const db = require('../config/db')
const { save, findAll } = require('./baseModel')

const table = () => db('trade_acoes')

function TradeAcaoModel() {

    this.save = (trade) => save(table, trade)

    this.findAll = () => findAll(table)

    this.findByMovimentacaoId = async (idMov) => {
        const trade = await table()
            .select()
            .where('movimentacao_id', idMov)
        if (trade.length > 0) {
            return { 
                acao: { id: trade[0].acao_id },
                idCarteira: trade[0].carteira_id
            }
        }
        return undefined
    }

    this.findByIdCarteiraIdAndIdAcao = (idCarteira, idAcao) => {
        const trade =  table()
            .select()
            .where('carteira_id', idCarteira)
            .andWhere('acao_id', idAcao)
        return trade
    }
}

module.exports = TradeAcaoModel