
exports.up = function(knex) {
  return knex.schema.createTable('setores', table => {
    table.increments('id').primary()
    table.string('nome',100).notNull().unique()
  })
};

exports.down = function(knex) {
    return knex.schema.dropTable('setores')
};
