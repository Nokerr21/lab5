import ID3
import numpy as np
import pandas as pd


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

    print(perform_decision_tree_test(decision_tree, test_set) / len(test_set))


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

    print(perform_decision_tree_test(decision_tree, test_set) / len(test_set))


def divide_data_set(data_set):
    training_set_size = int(3 * len(data_set) / 5)
    random_indexes = np.random.choice(len(data_set), training_set_size, replace=False)
    training_set = data_set.iloc[random_indexes]
    test_set = data_set.drop(random_indexes)

    return training_set, test_set


def perform_decision_tree_test(decision_tree, test_set):
    counter = 0
    for index, row in test_set.iterrows():
        if row['Class'] == decision_tree.predict(row[1:]):
            counter += 1
    return counter


perform_mushrooms_training_and_test()
perform_breast_cancer_training_and_test()
