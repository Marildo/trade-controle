const { expect, assert } = require('../helpers')
const dateUtils = require('../../lib/dateUtils')

describe('DateUtils', () => {
  it('Should to return 01/06/2020', () => {
    const dateExpect = new Date(2020, 06, 01)
    const start = dateUtils.startOfMonth(new Date(2020, 06, 30))
    expect(dateExpect.getTime()).to.equal(start.getTime())
  })

  it('Expect to equal Invalid Date', () => {
    try {
      dateUtils.startOfMonth('202/25/36')
    } catch (error) {
      expect(error).to.equal('Invalid Date')
    }
  })

  it('Expect to equal Invalid Date', () => {
    try {
      dateUtils.startOfMonth('1592168091161')
    } catch (error) {
      expect(error).to.equal('Invalid Date')
    }
  })
})
