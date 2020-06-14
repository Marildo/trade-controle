
const tableName = 'trade_acoes'

exports.up = function(knex) {
  return knex.schema.createTable(tableName, table => {
     table.increments('id').primary()
     table.datetime('data_compra', { precision: 6 }).defaultTo(knex.fn.now(6)).notNullable()
     table.datetime('data_venda', { precision: 6 }).defaultTo(knex.fn.now(6)).notNullable()
     table.integer('quantidade').unsigned().notNullable()
     table.decimal('preco_compra', 12, 2).defaultTo(0).notNullable()
     table.decimal('preco_venda', 12, 2).defaultTo(0).notNullable()
     table.decimal('corretagem', 12, 2).defaultTo(0).notNullable()
     table.decimal('impostos', 12, 2).defaultTo(0).notNullable()
     table.boolean('finalizada').notNullable().defaultTo()
     table.integer('movimentacao_id').unsigned().notNullable()
     table.foreign('movimentacao_id').references('id').inTable('movimentacoes_carteiras').onUpdate('CASCADE').onDelete('CASCADE') 
     table.integer('carteira_id').unsigned().notNullable()
     table.foreign('carteira_id').references('id').inTable('carteiras')
     table.integer('acao_id').unsigned().notNullable()
     table.foreign('acao_id').references('id').inTable('acoes')
  })
};

exports.down = function(knex) {
    return knex.schema.dropTable(tableName)
};
