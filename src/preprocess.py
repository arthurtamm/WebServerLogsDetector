import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from urllib.parse import urlparse
import re

def extract_url_info(df):
    def detect_patterns(text):
        return {
            "sql_injection": bool(re.search(r"\b(SELECT|DROP|INSERT|UPDATE|DELETE)\b\s*[\(\)=;'\"-]", text, re.IGNORECASE)),
            "xss_attack": bool(re.search(r"(<script>|alert|onload)", text, re.IGNORECASE)),
            "path_traversal": bool(re.search(r"(\.\./|%2e%2e)", text, re.IGNORECASE)),
            "hex_encoding": bool(re.search(r"%27|%3B|%3D|%22", text, re.IGNORECASE)),
        }

    # Aplicar a detecção de padrões tanto na URL quanto no content
    attack_flags_url = df['URL'].apply(lambda url: pd.Series(detect_patterns(url)))
    attack_flags_content = df['content'].apply(
        lambda content: pd.Series(detect_patterns(content)) if pd.notna(content) else pd.Series({
            "sql_injection": False,
            "xss_attack": False,
            "path_traversal": False,
            "hex_encoding": False
        })
    )

    # Combinar os resultados das colunas URL e content
    df['sql_injection'] = (attack_flags_url['sql_injection'] | attack_flags_content['sql_injection']).astype(int)
    df['xss_attack'] = (attack_flags_url['xss_attack'] | attack_flags_content['xss_attack']).astype(int)
    df['path_traversal'] = (attack_flags_url['path_traversal'] | attack_flags_content['path_traversal']).astype(int)
    df['hex_encoding'] = (attack_flags_url['hex_encoding'] | attack_flags_content['hex_encoding']).astype(int)

    # Contar parâmetros na URL
    df['param_count'] = df['URL'].apply(lambda url: len(urlparse(url).query.split('&')) if urlparse(url).query else 0)
    
    return df.drop(columns=['URL'])

def accept_transformation(df):
    df['accept_present'] = df['accept'].notna().astype(int)
    return df.drop(columns=['accept'])

def content_transformation(df):
    df = df.copy()
    df['content'] = df['content'].fillna('')

    # Calcular o comprimento do conteúdo
    df['content_length'] = df['content'].apply(len)
    
    # Contar o número de parâmetros no conteúdo
    df['param_count_content'] = df['content'].apply(
        lambda x: len(urlparse(x).query.split('&')) if urlparse(x).query else 0
    )
    
    return df.drop(columns=['content'])
    
def method_one_hot(df):
    encoder = OneHotEncoder(sparse_output=False, drop='if_binary')
    encoded = encoder.fit_transform(df[['method']])
    encoded_df = pd.DataFrame(
        encoded, 
        columns=encoder.get_feature_names_out(['method']),
        index=df.index
    )
    return pd.concat([df.drop(columns=['method']), encoded_df], axis=1)

def bool_to_int(df):
    for column in df.columns:
        if df[column].dtype == bool:
            df[column] = df[column].astype(int)
    return df

def preprocess_pipeline(include_label=True):
    """
    Cria a pipeline de pré-processamento.
    - include_label: Define se a coluna 'classification' será selecionada (para treino).
    """
    steps = [
        ('select_columns', FunctionTransformer(lambda df: 
            df[['method', 'URL', 'content', 'accept'] + (['classification'] if include_label else [])]
        )),
        ('extract_url_info', FunctionTransformer(extract_url_info)),
        ('accept_transformation', FunctionTransformer(accept_transformation)),
        ('content_transformation', FunctionTransformer(content_transformation)),
        ('method_encoding', FunctionTransformer(method_one_hot)),
        ('bool_to_int', FunctionTransformer(bool_to_int)),
    ]
    return Pipeline(steps)

# Ajustar a função de preprocessamento de treino
def preprocess(data, include_label=True):
    """
    Preprocessa dados para treino ou predição.
    - data: DataFrame de entrada.
    - include_label: Define se inclui a coluna 'classification'.
    """
    pipeline = preprocess_pipeline(include_label=include_label)
    return pipeline.fit_transform(data)

if __name__ == "__main__":
    data = pd.read_csv('../data/logs.csv')
    preprocessed_data = preprocess(data)
    preprocessed_data.to_csv('../data/train.csv', index=False)