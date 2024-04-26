import numpy as np

CLASS_NAME = 'Class'


class ID3Node:
    def __init__(self, training_set, attributes, is_terminal=False, predicted_class=None):
        self.isTerminal = is_terminal
        self.attribute = None
        self.children = {}
        self.predicted_class = predicted_class

        if predicted_class is None:
            self.build_node(training_set, attributes)

    def build_node(self, training_set, attributes):
        if len(training_set[CLASS_NAME].unique()) == 1:  # jeśli klasa ma tylko jedną unikalną wartość
            self.isTerminal = True
            self.predicted_class = training_set[CLASS_NAME].iloc[0]  # przypisz tę wartość jako najczęstszą
            return

        if len(training_set.columns) == 1:  # jeśli zbiór treningowy posiada tylko klasę
            self.isTerminal = True
            self.predicted_class = training_set[CLASS_NAME].mode()[0]  # przypisz najczęściej występującą wartość klasy
            return

        calculated_attribute_information_gains = {}
        #Oblicz przyrost informacji dla każdego atrybutu
        for column in training_set.columns[1:]:
            calculated_attribute_information_gains[column] = calculate_information_gain(column, training_set)

        #Wybierz największy przyrost
        best_attribute = max(calculated_attribute_information_gains, key=calculated_attribute_information_gains.get)

        #Przypisz najlepszą kolumnę jako atrybut tego węzła
        self.attribute = best_attribute
        self.add_child(training_set, attributes)

    def add_child(self, training_set, attributes):
        for value in attributes[self.attribute]:
            # Znajdź rekordy, które mają daną wartość w zbiorze treningowym
            current_best_attribute_value_rows = training_set.loc[training_set[self.attribute] == value]
            # Usuń kolumnę, która daje najwyższy aktualny infGain
            current_best_attribute_value_rows = current_best_attribute_value_rows.drop(columns=[self.attribute])
            reduced_attributes = attributes.copy()
            reduced_attributes.pop(self.attribute)
            if current_best_attribute_value_rows.shape[0] == 0:
                predicted_class = training_set[CLASS_NAME].mode()[0]
                self.children[value] = ID3Node(current_best_attribute_value_rows, reduced_attributes, True, predicted_class)
            else:
                self.children[value] = ID3Node(current_best_attribute_value_rows, reduced_attributes)

    def predict(self, data_to_predict):
        if self.isTerminal:
            return self.predicted_class
        #Wejdź do poddrzewa, które ma daną wartość w self.attribute
        best_attribute_data_value = data_to_predict[self.attribute]
        next_node_to_visit = self.children[best_attribute_data_value]
        return next_node_to_visit.predict(data_to_predict)


def calculate_attribute_entropy(training_set):
    entropy = 0.0
    for current_class in training_set[CLASS_NAME].unique():
        class_frequency = len(training_set.loc[training_set[CLASS_NAME] == current_class]) / len(training_set)
        entropy += -class_frequency * np.log(class_frequency)
    return entropy


def calculate_set_entropy(column, training_set):
    entropy = 0.0
    for attribute in training_set[column].unique():
        selected_rows = training_set.loc[training_set[column] == attribute]
        entropy += (len(selected_rows) / len(training_set)) * calculate_attribute_entropy(selected_rows)
    return entropy


def calculate_information_gain(column, training_set):
    return calculate_attribute_entropy(training_set) - calculate_set_entropy(column, training_set)
