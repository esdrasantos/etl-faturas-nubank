import pandas as pd
import pdfplumber as pdfplumber
import re

# Função para extrair colunas com base no padrão Data, Compra e Valor
def extract_columns_from_row(row):
    # Padrão para Data: Dois dígitos seguidos por três letras (ex: '04 JUL')
    date_pattern = r'^\d{2} \w{3}'
    # Padrão para Valor: Um valor monetário no formato R$ xxx,xx
    value_pattern = r'R\$ \d{1,3}(?:\.\d{3})*,\d{2}'

    # Tenta encontrar Data no início da linha
    date_match = re.match(date_pattern, row)
    if date_match:
        date = date_match.group(0)  # '04 JUL'
        # Tenta encontrar o Valor no final da linha
        value_match = re.search(value_pattern, row)
        if value_match:
            value = value_match.group(0)  # 'R$ 52,51'
            # O que sobrou entre a Data e o Valor é a descrição da compra
            if date is not None and value_match is not None:
              purchase = row[len(date):value_match.start()].strip()
              return [date, purchase, value]
    return None


def read_pdf_as_dataframe(pdf_path):
    # Lista para armazenar as tabelas de todas as páginas
    all_tables = []

    # Abre o arquivo PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Itera sobre cada página do PDF
        for page_num, page in enumerate(pdf.pages):
            # Extrai a tabela da página
            table = page.extract_table()

            # Pula a primeira página
            if page_num == 1:
                continue

            # Se uma tabela for encontrada na página, adicione à lista
            if table:
                # Converte a tabela para DataFrame e adiciona à lista
                proc_data = [extract_columns_from_row(row[0]) for row in table if row]
                proc_data = list(filter(None, proc_data))
                df = pd.DataFrame(proc_data)
                all_tables.append(df)
                print(f"Tabela extraída da página {page_num + 1}")

    return pd.concat(all_tables, ignore_index=True)


def remove_nan_columns(dataframe):
    for column in dataframe.columns:
        if dataframe[column].isnull().all():
            dataframe.drop(columns=column, axis=1, inplace=True)


def remove_nan_lines(dataframe):
    dataframe.dropna(inplace=True)


def remove_lines(dataframe, condition_mask):
    return (dataframe[condition_mask]
            .reset_index(drop=True))


def reset_dataframe_column_indexes(dataframe):
    length = len(dataframe.columns)
    dataframe.columns = range(length)
    dataframe.rename(columns={0: DATE,
                              1: PURCHASE,
                              2: VALUE},
                     inplace=True)