const axios = require('axios')

const {
  GraphQLObjectType,
  GraphQLString,
  GraphQLSchema,
  GraphQLList
} = require('graphql')

const URL_API_ESTADOS = 'http://localhost:3000/estados'

// Estado Type
const EstadoType = new GraphQLObjectType({
  name: 'Estado',
  fields: () => ({
    sigla: { type: GraphQLString },
    nome: { type: GraphQLString },
    capital: { type: GraphQLString },
    cidades: { type: new GraphQLList(GraphQLString) },
  })
})

// Root Query
const RootQuery = new GraphQLObjectType({
  name: 'RootQueryType',
  fields: {
    estado: {
      type: new GraphQLList(EstadoType),
      args: {
        sigla: { type: GraphQLString }
      },
      resolve(parent, args) {
        return getDadosAPIEstados(`${URL_API_ESTADOS}?sigla=${args.sigla}`)
      }
    },
    estados: {
      type: new GraphQLList(EstadoType),
      resolve(parent, args) {
        return getDadosAPIEstados(URL_API_ESTADOS)
      }
    }
  }
})

async function getDadosAPIEstados(URL) {
  try {
    const response = await axios.get(URL)
    return response.data
  } catch (error) {
    console.log(error)
  }
}

module.exports = new GraphQLSchema({
  query: RootQuery
})