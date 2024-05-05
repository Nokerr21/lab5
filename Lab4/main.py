import ID3
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


def prepare_confusion_matrix(real_data, predicted_data, labels):
    matrix = confusion_matrix(real_data, predicted_data)
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Przewidywane")
    plt.ylabel("Rzeczywiste")
    plt.title("Macierz Pomyłek")
    plt.show()

def read_dataset_from_file(file):
    return pd.read_csv(file)


def retrieve_attributes_from_dataset(data):
    result = {}
    for attribute in data.columns[1:]:
        result[attribute] = []
        for value in data[attribute].unique():
            result[attribute].append(value)
    return result


def perform_mushrooms_training_and_test():
    mushrooms_dataset = read_dataset_from_file('agaricus-lepiota.data')
    mushrooms_dataset.columns = ["Class",
                                 "cap-shape",
                                 "cap-surface",
                                 "cap-color",
                                 "bruises",
                                 "odor",
                                 "gill-attachment",
                                 "gill-spacing",
                                 "gill-size",
                                 "gill-color",
                                 "stalk-shape",
                                 "stalk-root",
                                 "stalk-surface-above-ring",
                                 "stalk-surface-below-ring",
                                 "stalk-color-above-ring",
                                 "stalk-color-below-ring",
                                 "veil-type",
                                 "veil-color",
                                 "ring-number",
                                 "ring-type",
                                 "spore-print-color",
                                 "population",
                                 "habitat"]

    attributes = retrieve_attributes_from_dataset(mushrooms_dataset)
    training_set, test_set = divide_data_set(mushrooms_dataset)
    decision_tree = ID3.ID3Node(training_set, attributes)
    test_set.reset_index()

    return perform_decision_tree_test(decision_tree, test_set)

def perform_breast_cancer_training_and_test():
    breast_cancer_dataset = read_dataset_from_file('breast-cancer.data')
    breast_cancer_dataset.columns = ["Class",
                                     "age",
                                     "menopause",
                                     "tumor-size",
                                     "inv-nodes",
                                     "node-caps",
                                     "deg-malig",
                                     "breast",
                                     "breast-quad",
                                     "irradiat"]

    attributes = retrieve_attributes_from_dataset(breast_cancer_dataset)
    training_set, test_set = divide_data_set(breast_cancer_dataset)
    decision_tree = ID3.ID3Node(training_set, attributes)
    test_set.reset_index()

    return perform_decision_tree_test(decision_tree, test_set)


def divide_data_set(data_set):
    training_set_size = int(3 * len(data_set) / 5)
    random_indexes = np.random.choice(len(data_set), training_set_size, replace=False)
    training_set = data_set.iloc[random_indexes]
    test_set = data_set.drop(random_indexes)

    return training_set, test_set


def perform_decision_tree_test(decision_tree, test_set):
    counter = 0
    predictions = []
    for index, row in test_set.iterrows():
        prediction = decision_tree.predict(row[1:])
        predictions.append(prediction)
        if row['Class'] == prediction:
            counter += 1
    labels = test_set['Class'].unique().tolist()
    return counter, test_set['Class'].tolist(), predictions, labels


def perform_tests(number_of_runs):
    mushrooms_accuracy = 0
    mushrooms_test_set = []
    mushrooms_predict_set = []
    mushrooms_labels = []
    breast_cancer_accuracy = 0
    breast_cancer_test_set = []
    breast_cancer_predict_set = []
    breast_cancer_labels = []
    for i in range(number_of_runs):
        mushrooms_results = perform_mushrooms_training_and_test()
        mushrooms_accuracy += mushrooms_results[0]
        mushrooms_test_set.extend(mushrooms_results[1])
        mushrooms_predict_set.extend(mushrooms_results[2])
        mushrooms_labels = mushrooms_results[3]

        breast_cancer_results = perform_breast_cancer_training_and_test()
        breast_cancer_accuracy += breast_cancer_results[0]
        breast_cancer_test_set.extend(breast_cancer_results[1])
        breast_cancer_predict_set.extend(breast_cancer_results[2])
        breast_cancer_labels = breast_cancer_results[3]

    mushrooms_average_accuracy = mushrooms_accuracy / len(mushrooms_test_set)
    prepare_confusion_matrix(mushrooms_test_set, mushrooms_predict_set, mushrooms_labels)
    print(mushrooms_average_accuracy)

    breast_cancer_average_accuracy = breast_cancer_accuracy / len(breast_cancer_test_set)
    prepare_confusion_matrix(breast_cancer_test_set, breast_cancer_predict_set, breast_cancer_labels)
    print(breast_cancer_average_accuracy)


NUMBER_OF_RUNS = 20
perform_tests(NUMBER_OF_RUNS)