const { expect, assert } = require('../helpers')
const movimentacaoModel = require('../../model/movimentacaoModel')

describe('Movimentacao Model', () => {
  describe('#Save', () => {
    it('Save: Deve salvar e retornar object salvo com id', function (done) {
      const mov = {
        data_movimentacao: new Date(),
        tipo: 1,
        valor: 40,
        descricao: 'Save test',
        carteira_id: 1,
      }

      movimentacaoModel
        .save(mov)
        .then((resp) => assert.isNumber(resp.id))
        .then(done())
    })
  })

  describe('#FindById', () => {
    const id = 10
    it('Deve retorna pelo id', function (done) {
      movimentacaoModel
        .findById(id)
        .then((resp) => expect(resp.id).to.equal(id))
        .then(done())
    })

    it('Deve retorna undefined', (done) => {
      movimentacaoModel
        .findById(30466)
        .then((resp) => expect(resp).to.equal(undefined))
        .then(done())
    })
  })

  describe('#FindByIdCarteira', () => {
    it('FindByIdCarteira: Deve retorna todas as movimentacoes pelo id da carteira', function (done) {
      const idCarteira = 1
      movimentacaoModel
        .findByIdCarteira(idCarteira)
        .then((resp) =>
          expect(resp.filter((i) => i.carteira_id !== idCarteira).to.be.empty)
        )
        .then(done())
    })

    it('FindByIdCarteira: Deve retorna []', function (done) {
      const idCarteira = 1544
      movimentacaoModel
        .findByIdCarteira(idCarteira)
        .then((resp) => expect(resp.to.be.empty))
        .then(done())
    })
  })

  describe('#DeleteById', () => {
    it('DeleteById: Deve deletar e retornar sucesso(1)', function (done) {
        movimentacaoModel
        .deleteById(20)
        .then(resp => expect(resp).to.equal(1) )
        .then(done())
    })
    it('DeleteById: Deve deletar e retornar not falha(0)',  function (done) {
      movimentacaoModel
      .deleteById(20)
      .then(resp => expect(resp).to.equal(0) )
      .then(done())
    })
  })
})
