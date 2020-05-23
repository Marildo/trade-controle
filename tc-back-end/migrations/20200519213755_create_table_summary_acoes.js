const tableName = 'summary_acoes'

exports.up = function (knex) {
    return knex.schema.createTable(tableName, table => {
        table.increments('id').primary()
        table.decimal('quantidade', 12, 2).defaultTo(0).notNullable()
        table.decimal('preco_medio', 12, 2).defaultTo(0).notNullable()
        table.decimal('preco_atual', 12, 2).defaultTo(0).notNullable()
        table.decimal('resultado', 12, 2).defaultTo(0).notNullable()
        table.decimal('percentual', 12, 2).defaultTo(0).notNullable()
        table.integer('carteira_id').unsigned().notNullable()
        table.foreign('carteira_id').references('id').inTable('carteiras')
        table.integer('acao_id').unsigned().notNullable()
        table.foreign('acao_id').references('id').inTable('acoes')
    })
};

exports.down = function (knex) {
    return knex.schema.dropTable(tableName)
};
