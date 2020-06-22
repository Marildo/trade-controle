const { expect, assert } = require('../helpers')
const model = require('../../model/carteiraModel')

describe('Carteira Model', () => {
  describe('#Save', () => {
    it('Save: Deve salvar e retornar object salvo com id', function (done) {
      const cart = {
        nome: 'Cart' + Math.random(),
      }
      model
        .save(cart)
        .then((resp) => {
          assert.isNumber(resp.id)
          done()
        })
        .catch((err) => done(err))
    })

    it('Save: Deve levante excecao nome ja existe', function (done) {
      const cart = {
        nome: 'CartDupli',
      }
      model
        .save(cart)
        .then(() => {
          assert.fail()
          done()
        })
        .catch((err) => {
          expect(err).eql('Key (nome)=(CartDupli) already exists.')
          done()
        })
    })
  })

  describe('#FindById', () => {
    const id = 1
    it('Deve retorna pelo id', function (done) {
      model
        .findById(id)
        .then((resp) => {
          expect(resp).to.not.undefined
          expect(resp).to.not.empty
          done()
        })
        .catch((err) => done(err))
    })

    it('Deve retorna undefined', (done) => {
      model
        .findById(30466)
        .then((resp) => expect(resp).to.be.undefined)
        .then(done())
        .catch((err) => done(err))
    })
  })

  describe('#CalculateSaldoAcoes', () => {
    it('Deve retorna saldo = 10', function (done) {
      model
        .calculateSaldoAcoes(1)
        .then(resp => {
          assert.equal(10, parseInt(resp))
          done()
        })
        .catch(err => done(err))
    })

    it('Deve retorna 0', function (done) {
      const idCarteira = 1454
      model
        .calculateSaldoAcoes(idCarteira)
        .then((resp) => {
          assert.equal(0, parseInt(resp))
          done()
        })
        .catch((err) => done(err))
    })
  })

  describe('#CalculateSaldoCaixa', () => {
    it('Deve retorna saldo = 10', function (done) {
      const idCarteira = 1
      model
        .calculateSaldoCaixa(idCarteira)
        .then(resp => {
          assert.equal(10, parseInt(resp))
          done()
        })
        .catch(err => done(err))
    })

    it('Deve retorna 0', function (done) {
      const idCarteira = 1454
      model
        .calculateSaldoCaixa(idCarteira)
        .then(resp => {
          assert.equal(0, parseInt(resp))
          done()
        })
        .catch(err => done(err))
    })
  })
})
