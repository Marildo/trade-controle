
exports.up = function(knex) {
    return knex.schema.createTable('acoes', table => {
        table.increments('id').primary()
        table.string('codigo',6).notNull().unique()
        table.string('empresa', 100)
        table.decimal('preco')
        table.integer('setor_id').unsigned()
        table.foreign('setor_id').references('id').inTable('setores')
        table.integer('subsetor_id').unsigned()
        table.foreign('subsetor_id').references('id').inTable('subsetores')
        table.integer('segmento_id').unsigned()
        table.foreign('segmento_id').references('id').inTable('segmentos')
    })
  };
  
  exports.down = function(knex) {
    return knex.schema.dropTable('acoes')
  };
  