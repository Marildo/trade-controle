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
        .then((resp) => {
          assert.isNotEmpty(resp)
          done()
        })
        .catch((err) => done(err))
    })
  })

  describe('#FindById', () => {
    const id = 10
    it('Deve retorna pelo id', function (done) {
      movimentacaoModel
        .findById(id)
        .then((resp) => {
          assert.equal(id, resp.id)
          done()
        })
        .catch((err) => done(err))
    })

    it('Deve retorna undefined', (done) => {
      movimentacaoModel
        .findById(30466)
        .then((resp) => {
          assert.equal(resp, undefined)
          done()
        })
        .catch((err) => done(err))
    })
  })

  describe('#FindByIdCarteira', () => {
    it('FindByIdCarteira: Deve retorna todas as movimentacoes pelo id da carteira', function (done) {
      const idCarteira = 1
      movimentacaoModel
        .findByIdCarteira(idCarteira)
        .then((resp) => {          
          assert.equal(resp[0].carteira_id, idCarteira)
          done()
        })
        .catch((err) => done(err))
    })

    it('Deve retorna []', function (done) {
      const idCarteira = 1544
      movimentacaoModel
        .findByIdCarteira(idCarteira)
        .then((resp) => {
          assert.isEmpty(resp)
          done()
        })
        .catch((err) => done(err))
    })
  })

  describe('#DeleteById', () => {
    it('Deve deletar e retornar sucesso(1)', function (done) {
      movimentacaoModel
        .deleteById(42)
        .then((resp) => {
          expect(resp).to.equal(1)
          done()
        })
        .catch((err) => done(err))
    })
    it('Deve deletar e retornar not falha(0)', function (done) {
      movimentacaoModel
        .deleteById(2660)
        .then((resp) => {
          expect(resp).to.equal(0)
          done()
        })
        .catch((err) => done(err))
    })
  })
})
