# estados-cidades
Desenvolvi este sitema para aprender mais sobre GraphQL.

**Estados - Cidades** consulta os estados e cidades do Brasil a partir de um servidor GraphQL usando Express e JSON-Server.

Os estados e cidades estão armazenados no arquivo **db.json**

Meu principal objetivo era construir um servidor **GraphQL** para obter os dados utilizando essa linguagem.


## Configuração

### Criar package.json
``` node
npm init
```

### Alterar package.json
``` json
"scripts": {
  "start-json": "json-server --watch src/db.json",
  "start-node": "nodemon src/server.js"
}
```

### Instalar Dependências
``` node
npm install axios
npm install cors
npm install express
npm install express-graphql
npm install graphql
npm install json-server
npm install nodemon --save-dev
```

### Iniciar Servidores
``` node
npm start-json
npm start-node
```

### Acessar
* JSON-Server (Porta 3000) = http://localhost:3000/estados
* GraphiQL IDE (Porta 4000) = http://localhost:4000/graphql
