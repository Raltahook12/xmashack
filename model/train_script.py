import pickle
import pandas as pd
from catboost import CatBoostClassifier


def train_model(data: pd.DataFrame) -> None:
    X = data.drop(columns=['ЗСК'])
    y = data['ЗСК']

    categorical_features = [col for col in X.select_dtypes(include=['category']).columns]

    model = CatBoostClassifier(iterations=100, learning_rate=0.1, depth=4, verbose=0)

    model.fit(X, y, cat_features=categorical_features)

    with open("model/model_1.pkl", "wb") as f:
        pickle.dump(model, f)
