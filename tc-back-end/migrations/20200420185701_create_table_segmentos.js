exports.up = function(knex) {
    return knex.schema.createTable('segmentos', table => {
      table.increments('id').primary()
      table.string('nome',100).notNull()
    })
  };
  
  exports.down = function(knex) {
      return knex.schema.dropTable('segmentos')
  };
  