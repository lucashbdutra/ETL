import pandas as pd
import pandera as pa

valores_ausentes = ['*****','****','####','###!','**','NULL','***']
df = pd.read_csv('ocorrencia.csv', parse_dates=['ocorrencia_dia'], dayfirst=True, na_values=valores_ausentes) #fazer a leitura da tablea, parse_data: faz a conversão para data e dayfirst: faz com que o dia seja o primeiro número
df.head(10)
schema = pa.DataFrameSchema( #cria um esquema para o data frame para fazer as validações
    columns = {
    'codigo':pa.Column(pa.Int, required=False), # O valor required (necessário) é True por padrao, colocando assim essa passa a ser uma coluna opcional, em caso de ausência não havera erro.
    'codigo_ocorrencia':pa.Column(pa.Int),# diz que a primeira coluna tem que ser int
    'codigo_ocorrencia2':pa.Column(pa.Int), # e assim por diante, verificando o tipo de cada coluna
    'ocorrencia_classificacao':pa.Column(pa.String),
    'ocorrencia_cidade':pa.Column(pa.String),
    'ocorrencia_uf':pa.Column(pa.String, pa.Check.str_length(2,2), nullable=True), # verifica o tamanho min e max
    'ocorrencia_aerodromo':pa.Column(pa.String, nullable=True),
    'ocorrencia_dia':pa.Column(pa.DateTime),
    'ocorrencia_hora':pa.Column(pa.String, pa.Check.str_matches(r'([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$'),nullable=True), #nullable é pra permitir valores nulos
    'total_recomendacoes':pa.Column(pa.Int) #essa expressão recular acima faz a validação das horas, minutos e segundos
    }
)

schema.validate(df)





df.iloc[-1] #isso é uma pesquisa de índice, mas nesse caso o label e o índice tem o mesmo valor, tem como usar o recurso -1 para pegar o ultimo item como em arrays e listas em python

df['ocorrencia_uf'] # isso é a mesmas coisa que df.loc[:,'nome_da_coluna']

df.nome_da_coluna.isnull() # assim posso pegar todos o valores nulos dessa coluna, e talvez somalos com o .sum()

df.loc[df.nome_da_coluna.isnull()] # posso também localizar esses dados com um .loc

filtro = df.nome_da_coluna.isnull() # posso tabem atribuir os objetos de uma filtragem a uma variável, e depois usar a var dentro do df.loc[filtro]

df.count() #Soma os valores, mas por padrão não soma os nullos





filtro = df.total_recomendacoes > 10
df.loc[filtro] #assim eu consigo pesquisar todos os valores maior que 10 nessa coluna

# df.loc[filtro, 'nome_colunas'] assim ao inves de trazer a linha inteira, eu trago apenas os valores de uma coluna especifica que cumpra os requisitos do filtro, posso tambem passar uma lista de colunas ['','','']

# df.loc[filtro1 & filtro2] posso tambem unir duas variáveis de filtro com o '&'

# filtro = (condição == 'string') | (outra_coisa == 'outra string')  necessidade de parenteses para evitar erro com os valores boleanos

filtro = df.ocorrencia_classificacao.isin('valorQueEuQueroProcurar') # é um equivalente ao if var in '', eu posso passar também uma lista de valores caso seja mais de um ['','','']





#Tem como também pesquisar apenas uma parte de um valor da coluna, por exemplo começa com 'tal' letra

filtro = df.ocorrencia_cidade.str[0] == 'C' #Pego o índice '0' que seria a primeira letra e comparao com a letra 'C'
df.loc[filtro]

filtro = df.ocorrencia_cidade.str[-2:] == 'MA' # Do penúltimo (-2) até o fim (:) tem que ter MA

filtro = df.ocorrencia_cidade.contains('MA') # Aqui independente da posição vai conferir se TEM 'MA' na string

filtro = df.ocorrencia_cidade.contains('MA|AL') # Posso usar tambem dentro dessa string o 'ou'





#Filtros nas datas

filtro = df.ocorrencia_dia.dt.year == 2015  #operador dt é usado pra extrair parte da data, nesse caso o ano '2015'

filtro = (df.ocorrencia_dia.dt.year == 2015) & (df.ocorrencia_dia.dt.month == 12) # também posso usá-lo com operadores lógicos, não pode esquecer dos parenteses pra isolar as operações

filtro = (df.ocorrencia_dia.dt.year == 2015) & (df.ocorrencia_dia.dt.month == 12) & (df.ocorrencia_dia.dt.day == 8) # Assim eu pesquiso uma data completa




# Posso também mesclar colunas

df['ocorrencia_dia_hora'] = pd.to_datetime(df.ocorrencia_dia.astype(str) + ' ' + df.ocorrencia_hora)

# assim eu consigo concatenar as duas colunas separados por um espaço ''

# usando o método to_datetime eu converto as strings para o formato dia hora 





# Fazendo a concatenação com conversão pra data e hora me permite usar filtros nesse formato

filtro = df.ocorrencia_dia_hora >= '2015-12-03 11:00:00'

#torna o filtro bem mais preciso




#ocorrências do ano de 2015 e mês 3
filtro = (df.ocorrencia_dia.dt.year == 2015) & (df.ocorrencia_dia.dt.month == 3)
df201503 = df.loc[filtro]

# assim ele usa codigo_ocorrencia de base e conta quantos elementos tem nas outras colunas relacionadas a esse
df201503.groupby(['codigo_ocorrencia']).count() 

df201503.groupby(['ocorrencia_classificacao']).codigo_ocorrencia.count()
#assim eu conto as classificações mediante ao codigo_ocorrencia, ou seja pra cada ocorrencia, quantas classificações diferentes eu tenho







# Assim ao invés de contar se tem ou não registro, eu apenas conto se existe "algo" naquela linha, pois caso eu vá contar do modo acima e minha coluna base tenha valores nulos esses valores vão ser skipados na contagem

df201503.groupby(['ocorrencia_classificacao']).size()

#eles ainda podem ser agrupados em ordem crescente com o método .sort_values() ou decrescente com .sort_values(ascending=False)

# Nesse caso eu estou obtendo dentro de todas as ocorrencias do RIO DE JANEIRO, a soma da coluna recomendações.

filtro = df.ocorrencia_cidade == 'RIO DE JANEIRO'
df.loc[filtro].total_recomendacoes.sum()

#posso tambem fazer a soma  considerando os valores NA sem o uso da função size, colocando o dropna=False, pois por padra ele dropa todos os valores que são NA

df.groupby(['ocorrencia_aerodromo'], dropna=False).total_recomendacoes.sum()