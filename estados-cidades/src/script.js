const estadosSelect = document.getElementById('estados-select')
const cidadesList = document.getElementById('cidades-list')

queryFetch(`
  query {
    estados {
      sigla
      nome
    }
  }
  `).then(dados => {
  dados.data.estados.forEach(estado => {
    const option = document.createElement('option')
    option.value = estado.sigla
    option.innerText = estado.nome
    estadosSelect.append(option)
  })
})

estadosSelect.addEventListener('change', async e => {
  const siglaEstado = e.target.value
  const cidades = await getCidadesEstado(siglaEstado)
  cidadesList.innerHTML = ''

  cidades.forEach(item => {
    const element = document.createElement('div')
    element.innerText = item
    cidadesList.append(element)
  })
})

function getCidadesEstado(siglaEstado) {
  return queryFetch(`
    query ($sigla: String) {
      estado(sigla: $sigla) {
        cidades
      }
    }
  `, { sigla: siglaEstado })
    .then(dados => {
      return (dados.data.estado[0].cidades)
    })
}

function queryFetch(query, variables) {
  return fetch('http://localhost:4000/graphql', {
    method: 'POST',
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: query,
      variables: variables
    })
  }).then(res => res.json())
}