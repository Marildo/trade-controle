
exports.up = function (knex) {
    return knex.schema.createTable('movimentacoes_carteiras', table => {
        table.increments('id').primary()
        table.datetime('data_movimentacao', { precision: 6 }).defaultTo(knex.fn.now(6))
        table.integer('tipo').unsigned().notNullable()
        table.decimal('valor', 12, 2).defaultTo(0)
        table.string('descricao')
        table.integer('carteira_id').unsigned()
        table.foreign('carteira_id').references('id').inTable('carteiras')
    })
};

exports.down = function (knex) {
    return knex.schema.dropTable('movimentacoes_carteiras')
};
