import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import csv

def train_model(train_data_dir, model_dir, play_cat_dir):
    raw_data_set = pd.read_csv(train_data_dir)
    winners = filter_winner_results(raw_data_set)
    
    X = extract_X(winners)
    Y, play_cat = extract_Y(winners)
    
    model = fit_model(X, Y)
    
    save_model(model, model_dir)
    save_play_categories(play_cat, play_cat_dir)

def filter_winner_results(df):
    return (
        df
        .drop(df[df['result'] != "WINNER"].index)
        .drop("result", axis=1)
    )

def extract_X(df):
    return df.drop("play", axis=1)

def extract_Y(df):
    Y = df["play"]
    categories = Y.astype('category')

    Y = categories.cat.codes
    categories = categories.unique()

    return (Y, categories)

def fit_model(X, Y):
    clf = DecisionTreeClassifier()
    clf.fit(X,Y)
    return clf

def save_model(model, model_dir):
    with open(model_dir, "wb") as file:
        pickle.dump(model, file)

def save_play_categories(categories, dir):
    with open(dir, "w+") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(zip(range(len(categories)), categories))