import pickle

import pandas as pd


def predict(data: pd.DataFrame) -> list:
    with open("model/model_1.pkl", "rb") as f:
        model = pickle.load(f)

    return model.predict(data)


if __name__ == "__main__":
    df = pd.read_excel("data.xlsx")
    df = prepare(df)
    print(predict(df.head(10)))
