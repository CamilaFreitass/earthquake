# Earthquakes (Terremotos) - API

Essa api foi criada com objetivo de mostrar onde
ocorreu o terremoto mais próximo, com magnitude 
igual ou superior a 5, em relação a uma determinada
cidade dentro de um determinado período. Para isso
foi utilizado dados públicos disponíveis em:

<https://www.usgs.gov/programs/earthquake-hazards>

A aplicação também salva os resultados sempre que
executamos uma pesquisa com novos parâmetros. 

Os parâmetros que são utilizados para realizar a 
pesquisa são: a cidade de referência `cidade_base`
que se deseja fazer a pesquisa, data inicial `data_inicio`
que é onde começa o período da pesquisa e data final
`data_fim` que é onde acaba o período da pesquisa. 

Obs.: o espaço de tempo para a pesquisa foi estabelecido
para um período de no máximo dois anos, pois para períodos
muito grandes a api pública de onde estamos consumindo os
dados não obteve uma resposta satisfatória. 

## Desenvolvimento

Para desenvolver essa aplicação foi utilizado Python,
FastAPI e SQLite. Além disso foi utilizado uma API do 
Google Maps para ajudar na localização da cidade em 
relação a localização do terremoto. 


## Passo a passo para ambiente local

    git clone https://github.com/CamilaFreitass/earthquake.git

    pip install requirements.txt

    python make.py

    * Substituir na chave google no arquivo .env