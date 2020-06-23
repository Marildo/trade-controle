const config = require('../knexfile')
const knex = require('knex')(config)
//knex.on('query', query => console.log(query))

module.exports = knex