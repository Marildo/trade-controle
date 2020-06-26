const db = require('../config/db')
const baseModel = require('./baseModel')

const table = () => db('carteiras')

const findAll = () => baseModel.findAll(table)

const findById = (id) => baseModel.findById(table, id)

const save = (carteira) => baseModel.save(table, carteira)

const updateCarteiras = () => {
  findAll().then((resp) => {
    for (let { id } of resp) {
      updateCarteira(id)
    }
  })
}

const updateCarteira = async (id) => {
  await updateHistorico(id)
  await updateSaldos(id)
  await updateHistorico(id)
}

const updateHistorico = (id) => {
  const script = `DELETE FROM historicos_carteiras WHERE data_historico = CURRENT_DATE AND carteira_id = ${id};
  INSERT INTO historicos_carteiras(data_historico, saldo_ativos,saldo_caixa, carteira_id)  
    SELECT CURRENT_DATE, saldo_ativos sa, saldo_caixa, ${id} FROM carteiras WHERE id = ${id};`

  return db.raw(script)
}

const updateSaldos = (id) => {
  const script = `
    UPDATE carteiras SET 
      saldo_ativos = (SELECT COALESCE(SUM(quantidade * a.preco),0) AS total
                      FROM summary_acoes 
                      	INNER JOIN acoes a ON acao_id = a.id
                      WHERE carteira_id = ${id}) , 

      saldo_caixa = (SELECT COALESCE(
                		 SUM(CASE WHEN tipo IN (1,3,5,7) THEN valor ELSE 0 END) -
                 		 SUM(CASE WHEN tipo IN (0,2,4,6) THEN valor ELSE 0 END), 0) saldo 
                    FROM movimentacoes_carteiras WHERE carteira_id = ${id}) ,

      resultado_diario = (SELECT t-l AS rs FROM
      					(SELECT saldo_ativos + saldo_caixa t
      					FROM historicos_carteiras
      					WHERE data_historico = CURRENT_DATE AND carteira_id= ${id}) a,
      					(SELECT saldo_ativos + saldo_caixa l
      					FROM historicos_carteiras
      					WHERE data_historico = CURRENT_DATE - 1 AND carteira_id = ${id}) b),
                
      resultado_semanal = (SELECT t-l AS rs FROM
      					(SELECT saldo_ativos + saldo_caixa t
      					FROM historicos_carteiras
      					WHERE data_historico = CURRENT_DATE AND carteira_id = ${id}) a,
      					(SELECT saldo_ativos + saldo_caixa l
      					FROM historicos_carteiras
      					WHERE data_historico = (
        						SELECT MAX(data_historico) FROM historicos_carteiras
        						WHERE data_historico < cast(date_trunc('week', current_date) as DATE)
      					)
       					AND carteira_id= ${id}) b),
                
      resultado_mensal = (SELECT t-l AS rs FROM
      					(SELECT saldo_ativos + saldo_caixa t
      					FROM historicos_carteiras
      					WHERE data_historico = CURRENT_DATE AND carteira_id = ${id}) a,
      					(SELECT saldo_ativos + saldo_caixa l
      					FROM historicos_carteiras
      					WHERE data_historico = (
       						SELECT MIN(data_historico)
      				      FROM historicos_carteiras
       						WHERE 
      						 EXTRACT(MONTH FROM data_historico) = EXTRACT(MONTH FROM CURRENT_DATE)
      						AND 
      						 EXTRACT(YEAR FROM data_historico) = EXTRACT(YEAR FROM CURRENT_DATE)
      					) AND carteira_id= ${id}) b),
                
      resultado_anual = (SELECT t-l AS rs FROM
      						(SELECT saldo_ativos + saldo_caixa t
      						FROM historicos_carteiras
      						WHERE data_historico = CURRENT_DATE AND carteira_id = ${id}) a,
      						(SELECT saldo_ativos + saldo_caixa l FROM historicos_carteiras
      						WHERE data_historico =
      						  (SELECT MIN(data_historico) FROM historicos_carteiras
        							 WHERE  EXTRACT(YEAR FROM data_historico) = EXTRACT(YEAR FROM CURRENT_DATE)
      						 ) AND carteira_id= ${id}) b ),
                  
      resultado_total = (SELECT t-l AS rs FROM
      						(SELECT saldo_ativos + saldo_caixa t
      						FROM historicos_carteiras
      						WHERE data_historico = CURRENT_DATE AND carteira_id = ${id}) a,
      						(SELECT saldo_ativos + saldo_caixa l
      						FROM historicos_carteiras
      						WHERE data_historico =
      						  (SELECT MIN(data_historico) FROM historicos_carteiras
      						) AND carteira_id = ${id}) b )
    WHERE id = ${id};`

  return db.raw(script)
}

module.exports = {
  findAll,
  findById,
  save,
  updateCarteira,
  updateCarteiras,
}
