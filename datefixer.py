import pandas as pd
import constants as const 

def add_purchase_date_column(df):

    dia_mes_ano = df['Data'].str.split(' ')
    
    df['Dia'] = dia_mes_ano.str[0].str.strip()
    df['Mes'] = dia_mes_ano.str[1].str.strip()
    df['Ano'] = df[const.INVOICECLOSE].str\
                .split('-').str[0]\
                .str.strip()
    meses = {
        "JAN": 1,
        "FEV": 2,
        "MAR": 3,
        "ABR": 4,
        "MAI": 5,
        "JUN": 6,
        "JUL": 7,
        "AGO": 8,
        "SET": 9,
        "OUT": 10,
        "NOV": 11,
        "DEZ": 12
    }

    df['N Mes'] = df['Mes'].map(meses)

    df['Data_Compra_Aux'] = df.Ano + "-"\
                            + df['N Mes'].astype(str) + "-"\
                            + df.Dia

    dtdiff = pd.to_datetime(df[const.INVOICECLOSE])-pd.to_datetime(df['Data_Compra_Aux'])
    df['Dias_Compra'] = dtdiff.dt.days
    df['Data'] = pd.to_datetime(df['Data_Compra_Aux'])

    filtro = df['Dias_Compra'] < 0
    df.loc[filtro, 'Data'] = df.loc[filtro, 'Data'] - pd.DateOffset(years=1)

    df['Mes Compra'] = df['Data'].dt.month
    df['Semana Compra'] = df['Data'].dt.isocalendar().week

    df.drop(columns=['Data_Compra_Aux', 'Dias_Compra'],inplace=True)

    df[const.INVOICECLOSE] = pd.to_datetime(
        df[const.INVOICECLOSE],
        format="%Y-%m-%d",
        errors="raise"
    )
    df["Dia"] = df["Dia"].astype(str).str.zfill(2)
    df["Mes"] = df["Mes"].astype(str).str.zfill(2)