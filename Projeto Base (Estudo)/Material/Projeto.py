import pandas as pd
import pandera as pa

df = pd.read_csv('ocorrencia.csv', parse_dates=['ocorrencia_dia'], dayfirst=True) #fazer a leitura da tablea, parse_data: faz a conversão para data e dayfirst: faz com que o dia seja o primeiro número
df.head(10)

schema = pa.DataFrameSchema( #cria um esquema para o data frame para fazer as validações
    columns = {
    'codigo':pa.Column(pa.Int, required=False), # O valor required (necessário) é True por padrao, colocando assim essa passa a ser uma coluna opcional, em caso de ausência não havera erro.
    'codigo_ocorrencia':pa.Column(pa.Int),# diz que a primeira coluna tem que ser int
    'codigo_ocorrencia2':pa.Column(pa.Int), # e assim por diante, verificando o tipo de cada coluna
    'ocorrencia_classificacao':pa.Column(pa.String),
    'ocorrencia_cidade':pa.Column(pa.String),
    'ocorrencia_uf':pa.Column(pa.String, pa.Check.str_length(2,2)), # verifica o tamanho min e max
    'ocorrencia_aerodromo':pa.Column(pa.String),
    'ocorrencia_dia':pa.Column(pa.DateTime),
    'ocorrencia_hora':pa.Column(pa.String, pa.Check.str_matches(r'([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$'),nullable=True), #nullable é pra permitir valores nulos
    'total_recomendacoes':pa.Column(pa.Int) #essa expressão recular acima faz a validação das horas, minutos e segundos
    }
)

schema.validate(df)