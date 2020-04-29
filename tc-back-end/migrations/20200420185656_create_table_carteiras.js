
exports.up = function (knex) {
  return knex.schema.createTable('carteiras', table => {
    table.increments('id').primary()
    table.string('nome', 100).notNull().unique()
    table.decimal('saldo_ativos', 10, 2).defaultTo(0)
    table.decimal('saldo_caixa', 10, 2).defaultTo(0)
    table.decimal('resultado_diario', 10, 2).defaultTo(0)
    table.decimal('resultado_semanal', 10, 2).defaultTo(0)
    table.decimal('resultado_mensal', 10, 2).defaultTo(0)
    table.decimal('resultado_anual', 10, 2).defaultTo(0)
    table.decimal('resultado_total', 10, 2).defaultTo(0)
  })
};

exports.down = function (knex) {
  return knex.schema.dropTable('carteiras')
};
