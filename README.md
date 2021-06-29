# Trade Controle

 ### Tecnologias
  - Node
  - Vue
  - Quasar
  - GraphQl

 * Projeto pessoal para aprendizado;
 * O TradeControle tem por finalidade o controle de investimentos em bolsa de valores e renda fixa;
 
------------------------------------------------------------------------------------------------------------------

### Requisitos Não Funcionais

- RNF01 -> Teconlogias: Sistema deve ser desenvolvido em linguagem Javascript utilizando NodeJs, ExpressJS, Knex, Apollo, GraphGL, VueJS,  HTML e CSS.

- RNF02 -> Bando de dados: O banco de dados deve ser desenvolvido no PostgreSQL.

- RNF03 -> Interface: A interface deve ser agradável e de fácil utilização.

- RNF04 -> Responsividade: Interface deve ser ajustar a qualquer tamanho de tela.

------------------------------------------------------------------------------------------------------------------

### Requisitos Funcionais

- RF01 -> Cadastrar ações: Este requisito deve prover  o cadastro de ações, possibilitando inserção, edição e exclusão de ações sem movimentação e o cadastro compras, vendas, dividendos, juros sob capital e taxas.
- RF02 -> Cadastro de carteira: Este requisito deve prover o cadastro carteiras  e relacioná-las com ações, títulos do tesouro direto, renda fixas e fundos de investimentos,  além de fornecer gráficos de pizza mostrando a proporção de cada ação na respectiva carteira.
- RF03 -> Gerenciamento de risco: Este requisito deve prover o gerenciamento de risco das ações em carteiras, calculando  o gain/stop  e fornecendo alertas.
- RF04 -> Cálculo de performance: Este requisito deve prover os cálculos da performance dos investimentos, exibindos o resultados em gráficos permitindo a fácil comparação entres carteiras, IBOVESPA, CDI  e IPCA.
- RF05 -> Cadastro de títulos do Tesouro Direto: Este requisito deve prover o cadastro de títulos do tesouro direto, inserindo  dados da compra e resgate, além de possibilitar  separá-los por SELIC, Prefixados e inflação.
- RF06 -> Cadastro de títulos de rendas fixas: Este requisito deve prover o cadastro de títulos de CDB, LCI/LCA, CRI/CRA, debentures e poupança.
- RF07 -> Cadastro de fundos de investimentos: Este requisito deve prover o cadastro de fundos de investimentos.
- RF08 -> Patrimônio: Este requisito deve prover uma visão rápida do patrimônio líquido, bem como aportes, ganhos e perdas por períodos determinados pelo usuário. 
- RF09 -> Cadastro de Objetivos: Este requisito deve prover o cadastro de objetos, permitindo o agrupamentos da carteiras em objetivos e fornecedores gráficos e estimativas para alcance dos objetivos.
- RF10 -> Cotação em tempo real: Este requisito deve prover a cotação em tempo real das ações e fornecer o resultado diário.
- RF11 -> Cadastro de setores: Este requisito deve prover o cadastro de setores e subsetores e relacioná-los entre sim e com o cadastro de ações.
- RF12 -> Cadastro de Corretoras: Este requisito deve prover o cadastro de corretoras e relacioná-las aos ativos cadastrado.
- RF13 -> Busca de informação no CEI: Este requisito deve possibilitar a busca de informação diretamente no Canal Eletrônico do Investidor.


# trade-controle-front-end

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your unit tests
```
npm run test:unit
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
