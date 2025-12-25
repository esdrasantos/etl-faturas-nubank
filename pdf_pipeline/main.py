import os
import warnings
import pandas as pd
import cleaner
import constants as const
import classifier
import datefixer as dfix

def main_function(event, context):

    warnings.simplefilter(action='ignore')
    pdf_folder = '/workspaces/etl-faturas-nubank/faturas_nu_pdf'
    output_dir = '/workspaces/etl-faturas-nubank/faturas_nu_csv'

    pdf_files  = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    for pdf in pdf_files:
        print(f'Processing {pdf}')
        pdf_path = f'{pdf_folder}/{pdf}'
        dataframe = cleaner.read_pdf_as_dataframe(pdf_path)
        dataframe.columns = [const.DATE, const.PURCHASE, const.VALUE]

        # Máscara que identifica linhas de 'Pagamento' na tabela de compras
        is_payment_line = (dataframe[const.PURCHASE]
                        .str.
                        startswith(const.PAYMENT))

        # Prepara uma tabela apenas com as linhas de 'Pagamento'
        payments = cleaner.remove_lines(dataframe, is_payment_line)

        # Remove linhas de pagamento de entre as linhas de compras
        dataframe = cleaner.remove_lines(dataframe, ~is_payment_line)
        dataframe[const.CATEGORY] = dataframe[const.PURCHASE].apply(classifier.classify_purchases) # É facil 'estender' os objetos em python

        # Adiciona nome do arquivo de origem
        dataframe[const.SOURCEFILE] = pdf

        # Adiciona data de fechamento da fatura
        dataframe[const.INVOICECLOSE] = (
                                            dataframe[const.SOURCEFILE]
                                            .str.rsplit('_', n=1).str[1]
                                            .str.split('.').str[0]
                                        )

        dfix.add_purchase_date_column(dataframe)

        print(dataframe.head())

        # Define o caminho de saída para o CSV
        csv_file_name = pdf.replace('.pdf', '.csv')  # Troca a extensão para .csv

        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, csv_file_name)

        # Salva o DataFrame como CSV
        dataframe.to_csv(output_path, index=False)

        print(f'CSV file saved at {output_path}')

main_function("","")