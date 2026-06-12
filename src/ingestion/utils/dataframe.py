import pandas as pd

def clean_dataframe(df: pd.DataFrame):

    df = df.copy()

    df.columns = (
        df.columns
        .astype((str))
        .str.strip()
    )

    df = (
        df
        .dropna(how='all')
        .reset_index(drop=True)
    )

    return df