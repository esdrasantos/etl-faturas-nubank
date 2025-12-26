from flask import Flask, request, jsonify
import warnings
import pandas as pd
import cleaner
import constants as const
import classifier
import datefixer as dfix
from google.cloud import storage, bigquery
import tempfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
BQ_TABLE = "powerbi-drive-458204.controle_gastos.fatura_nu"

def download_pdf(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    blob.download_to_filename(tmp.name)
    logger.info(f"PDF baixado em {tmp.name}")

    return tmp.name

def process_pdf(pdf, pdf_name):
    
    print(f'Processing {pdf}')

    pdf_path = pdf
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
    dataframe[const.SOURCEFILE] = pdf_name

    # Adiciona data de fechamento da fatura
    dataframe[const.INVOICECLOSE] = (
                                        dataframe[const.SOURCEFILE]
                                        .str.rsplit('_', n=1).str[1]
                                        .str.split('.').str[0]
                                    )

    dfix.add_purchase_date_column(dataframe)

    # print(dataframe.head())

    return dataframe

def pipeline(bucket, file_name):
    pdf_path = download_pdf(bucket, file_name)
    # For testing locally
    # pdf_path = '/workspaces/etl-faturas-nubank/faturas_nu_pdf/Nubank_2025-01-11.pdf'
    df = process_pdf(pdf_path, file_name)
    return df

def load_bigquery_table(df, table_id):
    client = bigquery.Client()

    job = client.load_table_from_dataframe(
        df,
        table_id
    )

    job.result()

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "service": "etl-faturas-nubank",
        "message": "Cloud Run is up"
    }), 200

@app.route("/process", methods=["POST"])
def process():

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "status": "error",
                "message": "JSON inválido ou ausente"
            }), 400

        bucket = data.get("bucket")
        name = data.get("name")

        if not bucket or not name:
            return jsonify({
                "status": "error",
                "message": "Campos 'bucket' e 'name' são obrigatórios"
            }), 400

        logger.info(f"Processando arquivo {name} do bucket {bucket}")

        df = pipeline(bucket, name)
        df[const.PROCDATE] = pd.Timestamp.utcnow()

        load_bigquery_table(df, BQ_TABLE)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        logger.exception("Erro em /process")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)