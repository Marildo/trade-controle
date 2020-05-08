
const tableName = 'trade_acoes'

exports.up = function(knex) {
  return knex.schema.createTable(tableName, table => {
     table.increments('id').primary()
     table.datetime('data_trade', { precision: 6 }).defaultTo(knex.fn.now(6)).notNullable()
     table.boolean('compra').notNullable()
     table.integer('quantidade').unsigned().notNullable()
     table.decimal('valor', 10, 2).defaultTo(0).notNullable()
     table.decimal('corretagem', 10, 2).defaultTo(0).notNullable()
     table.decimal('impostos', 10, 2).defaultTo(0).notNullable()
     table.integer('movimentacao_id').unsigned().notNullable()
     table.integer('carteira_id').unsigned().notNullable()
     table.foreign('carteira_id').references('id').inTable('carteiras')
     table.integer('acao_id').unsigned().notNullable()
     table.foreign('acao_id').references('id').inTable('acoes')
  })
};

exports.down = function(knex) {
    return knex.schema.dropTable(tableName)
};
