import pandas as pd

df = pd.read_csv('ocorrencia.csv', parse_dates=['ocorrencia_dia'], dayfirst=True) #fazer a leitura da tablea, parse_data: faz a conversão para data e dayfirst: faz com que o dia seja o primeiro número
df.head(5)



df.loc[1,'ocorrencia_cidade'] #usado em forma de matriz, como linha e o nome da coluna, loc de localize

df.loc[3] #pega todos os dados da linha 3, e pode ser usado na forma de [1:3] por exemplo pra pegar um intervalo

df.loc[[10,40]] # pra passa uma lista de linhas que eu quero, no caso os índices 10 e 40

df.loc[:,'ocorrencia_cidade'] #os dois pontos é o range das linhas (como se eu estivesse copiando uma lista em python) no caso está vazio então são todas, e de 'tal_coluna'

df.codigo_ocorrencia.is_unique #pra verificar se o valor não se repete e pode ser usado como índice

df.set_index('codigo_ocorrencia', inplace=True) # ao inves de usar o índice padrão do sistema, eu troco pelo valor que eu ja tenho na tabela e que NÃO se repete.

# Pra que a mudança seja efetivada tem que usar o inplace=True, se não vai mudar apenas momentaneamente

df.reset_index(drop=True, inplace=True) # E aqui eu estou resetando o índice do data frame para o padrão





df.loc[0,'ocorrencia_aerodromo'] = '' # isso seria pra mudar os dados de um local específico

df['ocorrencia_uf_bkp'] = df.ocorrencia_uf # Ja assim eu consigo criar uma nova coluna e copiar os dados de uma ja existente

df.loc[df.ocorrencia_uf == 'SP', ['ocorrencia_classificação',]] = 'GRAVE' #Assim eu crio um filtro onde eu digo que todas as ocorrencias que forem igual a SP, vao ter seu estado em classificação alterado pra GRAVE. Caso necessário posso adicionar mais filtros de acordo com minha necessidade.



# Agora o que precisamos limpar nessa tabela:

# Ocorrencia_uf = **
# Ocorrencia_aerodromo = ####, ###!, ****, *****
# Ocorrencia_hora = NULL

df.replace(['*****','****','####','###!','**','NULL', '***'], pd.NA, inplace=True) 
# Mais uma vez o parâmetro inplace pra fazer a alteração dentro do df e não so no momento da exucução para visualização

df.loc[df.ocorrencia_aerodromo == '****', ['ocorrencia_aerodromo']] = pd.NA # NA são valores não informados
#essa seria a forma de trocar um erro por vez


df.isna().sum() # função pra somar por coluna todos os dados NA
df.isnull().sum() # função pra somar por coluna todos os dados NA/NULL





df.fillna("valor que eu quero colocar nos dados NA", inplace=True) # Sempre lembrar do inplace=True

df.fillna(value={'total_recomendacoes':10}, inplace=True) # Nesse caso eu pego os valor que estão como NA em uma coluna específica e altero eles para 10, então eles não serão mais contabilizados como NA

df.drop(['passo aqui', 'uma lista de colunas', 'para apagar'], axis=1, inplace=True) # temos que mudar o eixo, ele por padrão é '0' que é o das linhas, temos que mudar pra '1' no caso de colunas

df.dropna(inplace=True) #exclui todos os valores não informados (NA), mas CUIDADO, ele não tem como tirar apenas uma célula, ele exclui a linha toda

df.dropna(subset=['ocorrencia_uf']) # assim ele vai dropar a linha que tiver NA apenas nessa coluna específica 




df.drop_duplicates(inplace=True) #procura linhas duplicadas e as exclui