const db = require('../config/db')
const { save, update } = require('./baseModel')

const table = () => db('summary_acoes')

function SummaryAcoesModel() {

    this.save = (summary) => save(table, summary)

    this.updateSummary = async (trade) => {
        try {
            const idCarteira = trade.idCarteira
            const idAcao = trade.acao.id
           
            const select =
                `SELECT
                 SUM(quantidade * preco_compra) / SUM(quantidade) prCompra, 
                 SUM(quantidade * preco_venda) / SUM(quantidade) prVenda,
                 SUM(quantidade) qtd
                FROM trade_acoes
                 WHERE acao_id = ? AND carteira_id = ? AND finalizada = false`

            const query = await db.raw(select, [idAcao, idCarteira])
            const row = query.rows[0]

            const summary = await this.findByAcaoAndIdCarteira(idAcao, idCarteira)
            if (row) {
                summary.quantidade = row.qtd
                summary.preco_medio = row.prcompra > 0 ? row.prcompra : row.prvenda
            } else {
                summary.quantidade = 0
                summary.preco_medio = 0
            }

            return update(table, summary)
        } catch (error) {
            console.log(error)
        }
    }

    this.findByAcaoAndIdCarteira = (acao_id, carteira_id) => {
        return new Promise((resolve, reject) => {
            table()
                .select()
                .where('acao_id', acao_id)
                .andWhere('carteira_id', carteira_id)
                .then(resp => {
                    if (resp.length !== 0) {
                        resolve(resp[0])
                    } else {
                        const summary = {
                            acao_id,
                            carteira_id,
                            quantidade: 0,
                            preco_medio: 0
                        }
                        resolve(this.save(summary))
                    }
                })
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }

    this.findAllByIdCarteira = (idCarteira) => {
        return new Promise((resolve, reject) => {
            table()
                .select(['summary_acoes.*',
                    'acoes.codigo',
                    'acoes.empresa',
                    'acoes.preco',
                    'acoes.setor_id',
                    'acoes.subsetor_id',
                    'acoes.segmento_id'])
                .innerJoin('acoes', 'acao_id', 'acoes.id')
                .where('carteira_id', idCarteira)
                .andWhere('quantidade', '<>', 0)
                .then(resp => resolve(resp))
                .catch(error => {
                    console.log(error)
                    reject(error.detail)
                })
        })
    }
}

module.exports = SummaryAcoesModel