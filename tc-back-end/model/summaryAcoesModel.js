const db = require('../config/db')
const { save, update } = require('./baseModel')

const table = () => db('summary_acoes')

function SummaryAcoesModel() {

    this.save = (summary) => save(table, summary)

    this.updateSummary = (dados) => {
        this.updateQuantidade(dados)
    }

    this.updateQuantidade = async (trade) => {
        try {
            const idCarteira = trade.idCarteira
            const idAcao = trade.acao.id

            const summary = await this.findByAcaoAndIdCarteira(idAcao, idCarteira)
            const quantidade = parseFloat(summary.quantidade)
            const precoMedio = parseFloat(summary.preco_medio)
            const quantidadeOperacao = trade.quantidade * (trade.compra ? 1 : -1)

            const newQtd = quantidade + quantidadeOperacao

            if (newQtd > 0 && trade.compra) {
                summary.preco_medio =
                    ((quantidade * precoMedio) + (trade.quantidade * trade.valor)) / newQtd
            } else if (newQtd < 0 && !trade.compra) {
                summary.preco_medio =
                    (((quantidade * -1) * precoMedio) + (trade.quantidade * trade.valor)) / (newQtd * -1)
            } else if (newQtd === 0) {
                summary.preco_medio = 0
            }

            summary.quantidade = newQtd
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
                            carteira_id
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