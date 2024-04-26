import numpy as np


class DecisionTree:
    def __init__(self, training_set, attributes, terminal=False, predicted_class=None):
        if terminal and predicted_class is not None:
            self.isTerminal = True
            self.predicted_class = predicted_class
            self.attribute = None
            self.children = {}
        else:
            self.isTerminal = False
            self.predicted_class = None
            self.attribute = None
            self.children = {}

            self.build(training_set, attributes)

    def build(self, training_set, attributes):
        if len(training_set['Class'].unique()) == 1:  # jeśli klasa ma tylko jedną unikalną wartość
            self.isTerminal = True
            self.predicted_class = training_set['Class'].iloc[0]  # przypisz najczęściej tę wartość
            return

        if len(training_set.columns) == 1:  # jeśli zbiór treningowy posiada tylko klasę
            self.isTerminal = True
            self.predicted_class = training_set['Class'].mode()[0]  # przypisz najczęściej występującą wartość klasy
            return

        calculated_attribute_information_gains = {}
        for column in training_set.columns[1:]:
            calculated_attribute_information_gains[column] = calculate_information_gain(column, training_set)
        best_attribute = max(calculated_attribute_information_gains, key=calculated_attribute_information_gains.get)
        self.attribute = best_attribute
        for value in attributes[best_attribute]:
            # Znajdź rekordy, które mają daną wartość w zbiorze treningowym
            selected_rows = training_set.loc[training_set[best_attribute] == value]
            #Usuń kolumnę, która daje najwyższy aktualny infGain
            selected_rows = selected_rows.drop(columns=[best_attribute])
            new_attributes = attributes.copy()
            new_attributes.pop(best_attribute)
            #TODO tu chyba jest coś nie tak
            if selected_rows.shape[0] == 0:
                predicted_class = training_set['Class'].mode()[0]
                self.children[value] = DecisionTree(selected_rows, new_attributes, True, predicted_class)
            else:
                self.children[value] = DecisionTree(selected_rows, new_attributes)

    def predict(self, item):
        if self.isTerminal:
            return self.predicted_class
        #Wejdź do poddrzewa, które ma największy infGain
        return self.children[item[self.attribute]].predict(item)


def calculate_attribute_entropy(training_set):
    E = 0.0
    for current_class in training_set['Class'].unique():
        fi = len(training_set.loc[training_set['Class'] == current_class]) / len(training_set)
        E += -fi * np.log(fi)
    return E


def calculate_set_entropy(d, training_set):
    E = 0.0
    for attr in training_set[d].unique():
        Uj = training_set.loc[training_set[d] == attr]
        E += (len(Uj) / len(training_set)) * calculate_attribute_entropy(Uj)
    return E


def calculate_information_gain(d, training_set):
    return calculate_attribute_entropy(training_set) - calculate_set_entropy(d, training_set)
