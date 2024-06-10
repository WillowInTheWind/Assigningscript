import pandas as pd
import numpy as np


def read_in_data(filename, relevant_columns):
    df = load_data_as_dataframe(filename)
    df = read_relevant_data(df, relevant_columns)
    return df


def load_data_as_dataframe(filename):
    dataframe = pd.read_csv(f'{filename}.csv')
    return dataframe


def read_relevant_data(dataframe: pd.DataFrame, relevant_columns: list) -> pd.DataFrame:
    columns = dataframe.columns.tolist()
    irrelevantcolumns = []
    for column in columns:
        if column not in relevant_columns:
            irrelevantcolumns.append(column)

    dataframe = dataframe.drop(columns=irrelevantcolumns)
    return dataframe


if __name__ == "__main__":
    print("Data Processing Started")
    dataf = load_data_as_dataframe("testcsv2")
    dataf = read_relevant_data(dataf, ["School Name","How many delegates would you like to register for FWPMUN VIII? (Delegate counts may be altered as needed.)", "Index"])
    print(dataf.head())