const  expect  = require('../helpers')
const  movimentacaoModel = require('../../model/movimentacaoModel')

describe('Movimentacao Model', () => {
  describe('#Save', () => {
    it('Save: Deve salvar e retornar object salvo com id', () => {
      expect(20).to.equal(260)
    })
  })

  describe('#FindById', () => {
    it('Deve retorna pelo id', () => {
      expect(20).to.equal(260)
    })

    it('Deve retorna undefined', (done) => {
      movimentacaoModel.findById(30466)
       .then(resp => {
         expect(resp).to.equal(undefined)
         done()
       })
       .catch(error => done(error))
    })
  })

  it('FindByIdCarteira: Deve retorna todas as movimentacoes pelo id da carteira', () => {
    expect(20).to.equal(260)
  })

  it('DeleteById: Deve deletar e retornar  sucessos(1)', () => {
    expect(20).to.equal(260)
  })
})
