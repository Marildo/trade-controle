const tableName = 'historicos_carteiras'
exports.up = function (knex) {
  return knex.schema.createTable(tableName, table => {
    table.increments('id').primary()
    table.date('data_historico').defaultTo(knex.fn.now())
    table.decimal('saldo_ativos', 10, 2).defaultTo(0)
    table.decimal('saldo_caixa', 10, 2).defaultTo(0)
    table.integer('carteira_id').unsigned()
    table.foreign('carteira_id').references('id').inTable('carteiras')
    table.unique(['data_historico','carteira_id'])
  })
};

exports.down = function (knex) {
  return knex.schema.dropTable(tableName)
};
