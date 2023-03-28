Consumo asincrono da API Questor Zen
==========

# Este projeto

O objetivo deste projeto é implementar uma solução asyncrona da api do **Questor Zen**, à fim de possibilitar o envio em lote de dados em pouco tempo.

Seu objetivo não é ser executado com frequência para isso existe o Questor Connect, seu intíto é realizar o envio de XMLs legado para a plataforma uma única vez.

**Importante**: Este script causa um stress considerável nos servidores da Questor. Não utilize ele sem antes consultar o fornecedor, pois sem planejamento prévio, a sua chave de API poderá ser bloqueada.


# O que é o Questor Connect e o Questor Zen 🤓

O Questor Connect é uma ferramenta que alguns escritórios de contabilidade contratam para auxiliar no recebimento dos XMLs de Notas Fiscais, Conhecimento de Transporte, etc, que seus clientes teriam que enviar. Essas notas são essenciais para a correta escrituração fiscal, declarações fiscais ao fisco e apuração de impostos.

A ferramenta, possibilita a captura automática de XMLs por meio dos certificados A1 e A3 (emitidos pelo governo brasileiro). Além disso ele pode ser utilizado para capturar os XMLs que o cliente já possui (por exemplo os que ele emitiu), e repassalos ao escritório contábil através da aplicação Web **Questor Zen**.   

A ferramenta foi desenvolvida para funcionar 24/7, então possui limitações para evitar um envio massivo de dados em pouco tempo. Já que o objetivo é suavisar o envio reduzindo stress no servidor do fornecedor do produto (a Questor).  


# Requisitos
Instale os módulos abaixo:
```
pip install aiohttp
pip install peewee
pip install asyncio
pip install elementpath
pip install requests
```

# Execução ▶️
**Importante**: Lembre-se de executar fora do horário comecial brasileiro.

A Execução deste script é feita pelo arquivo ```main.py```, para executar, defina as variáveis ```root_dir```, ```main_url```, e ```token```. Exemplos:
1. ```main_url```: Caso o site que use para acessar seja: https://**escritorio**.app.questorpublico.com.br, informe "**escritorio**".
2. ```root_dir```: "C:\Pasta contendo XMLs"
3. ```token```: O mesmo utilizado na configuração do Questor Connect

Ao executar o script o seguinte será realizado:

1. Será criado um banco de dados para registrar o andamento do processo e as respostas recebidas ```files.db```.
2. Todos os arquivos XMLs presentes na pasta ```root_dir``` serão consultados, validados, e salvos no banco de dados.
3. Os XMLs serão enviados em pacotes grandes desincronizados para o servidor.

# 🏃 Resultados 🏃

Em meus testes, após o passo 2, o envio de 2.000 arquivos tomou cerca de 180 segundos. Em geral, neste mesmo tempo o Connect teria enviado cerca de 15 XMLs.

Em dois finais de semana, e um dia trabalhando no período da noite, pude realizar o envio de cerca de 1M de XMLs.   

# 😅 Problemas 🤔

Nem tudo são rosas. Em alguns momentos a API parou de responder retornando erro 500 para todas as chamadas. E após aguardar 24 horas, foi possível enviar estes mesmos arquivos sem nenhum erro.

Para realizar todo o envio, tive que reprocessar o comando 3 ou 4 vezes em dias distintos. Analisando, cheguei a conclusão de que não há nenhum problema com o código e sim uma restrição que o servidor do fornecedor impõe sobre as APIs, mesmo questionando a Questor sobre o caso não, eles negaram que tal restição existisse.

Talvez estes problemas realmente estivessem no meu código, entretanto como o seu objetivo é ser executado apenas uma vez migrando dados legado, mesmo que ele não seja estável, atendeu a demanda, e gostaria de compartilhar ele com todos, caso passem por uma situação parecida.

Usem a vontade! 😄