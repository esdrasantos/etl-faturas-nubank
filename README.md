# etl-faturas-nubank

Deployed on Google Cloud Run. Curl to test:

curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "bucket": "faturas_nu_pdf",
    "name": "faturas_nu/Nubank_2025-02-11.pdf"
  }' \
  https://etl-faturas-nubank-10698316802.southamerica-east1.run.app/process
