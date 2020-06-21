const { expect } = require('../helpers')
const { movimentacaoModel } = require('../../model/')

describe('Movimentacao Model', () => {
  it('Save: Deve salvar e retornar object salvo com id', () => {
    expect(20).to.equal(260)
  })

  it('FindById: Deve retorna pelo id', () => {
   expect(20).to.equal(260)
  })

  it('FindByIdCarteira: Deve retorna todas as movimentacoes pelo id da carteira', () => {
   expect(20).to.equal(260)
  })

  it('DeleteById: Deve deletar e retornar  sucessos(1)', () => {
   expect(20).to.equal(260)
  })
})
