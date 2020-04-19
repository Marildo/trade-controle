
exports.up = function(knex) {
  return knex.schema.createTable('acoes', table => {
      table.increments('id').primary()
      table.string('sigla',6).notNull().unique()
      table.string('empresa', 100)
      table.decimal('cotacao')
  })
};

exports.down = function(knex) {
  return knex.schema.dropTable('acoes')
};
