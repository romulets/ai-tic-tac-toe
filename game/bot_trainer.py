import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle
import csv

def train_model(train_data_dir, model_dir, play_cat_dir, result_cat_dir):
    print("----")
    print("training model")

    df_plays = pd.read_csv(train_data_dir)
    df_plays, play_cat = transform_play_feat(df_plays)
    df_plays, result_cat = transform_result_feat(df_plays)
    
    X = extract_X(df_plays)
    Y = extract_Y(df_plays)
    
    model = fit_model(X, Y)
    
    save_model(model, model_dir)
    save_categories(play_cat, play_cat_dir)
    save_categories(result_cat, result_cat_dir)

def transform_play_feat(df):
    df = df.copy()
    play_cat = df["play"].astype('category')
    df["play"] = play_cat.cat.codes
    play_cat = play_cat.unique()
    return df, play_cat

def transform_result_feat(df):
    df = df.copy()
    result_cat = df["result"].astype('category')
    df["result"] = result_cat.cat.codes
    result_cat = result_cat.unique()
    return df, result_cat

def extract_X(df):
    return df.drop("result", axis=1)

def extract_Y(df):
    return df["result"]

def fit_model(X, Y):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

    parameters = {
        "class_weight": [None, "balanced"],
        "max_leaf_nodes": range(2, 21),
        "max_depth": [None] + list(range(1, 11))
    }

    print("Grid searching on DecisionTree", parameters)

    decision_tree_clf = DecisionTreeClassifier()
    clf = GridSearchCV(decision_tree_clf, parameters)

    clf.fit(X_train, Y_train)

    print("Best parameters were", clf.best_params_)
    print("Score on test chunk", clf.score(X_test, Y_test))

    return clf.best_estimator_

def save_model(model, model_dir):
    with open(model_dir, "wb") as file:
        pickle.dump(model, file)

def save_categories(categories, dir):
    with open(dir, "w+") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(zip(range(len(categories)), categories))