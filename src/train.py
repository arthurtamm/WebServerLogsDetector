import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

if __name__ == '__main__':
    df = pd.read_csv('../data/train.csv')

    X_train = df.drop('classification', axis=1)
    y_train = df['classification']

    model = RandomForestClassifier(
        max_depth=20,
        min_samples_split=12,
        n_estimators=10,
    )
    model.fit(X_train, y_train)
    
    with open("../models/random_forest", 'wb') as file:
        pickle.dump(model, file)
