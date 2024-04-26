from time import sleep
import pandas as pd
import numpy as np


class Node:
    def __init__(self, U, ATTR, terminal=False, cls=None):
        if terminal and cls is not None:
            self.isTerminal = True
            self.cls = cls
            self.attribute = None
            self.children = {}
        else:
            self.isTerminal = False
            self.cls = None
            self.attribute = None
            self.children = {}

            self.build(U, ATTR)

    def build(self, U, ATTR):
        if len(U['Class'].unique()) == 1:  # jeśli liczba unikatowych klas jest równa 1, czyli jedna klasa
            self.isTerminal = True
            self.cls = U['Class'].iloc[0]  # zwraca klasę o zerowej pozycji w U
            return

        if len(U.columns) == 1:  # jeśli liczba kolumn w U jest równa 1, czyli mamy samą klasę
            self.isTerminal = True
            self.cls = U['Class'].mode()[0]  # najczęściej występująca klasa
            return

        D = {}
        for d in U.columns[1:]:
            D[d] = infGain(d, U)
        dj = max(D, key=D.get)
        self.attribute = dj
        for val in ATTR[dj]:
            Uj = U.loc[U[dj] == val]
            Uj = Uj.drop(columns=[dj])
            new_attr = ATTR.copy()
            new_attr.pop(dj)
            if Uj.shape[0] == 0:
                cls = U['Class'].mode()[0]
                self.children[val] = ID3(Uj, new_attr, True, cls)
            else:
                self.children[val] = ID3(Uj, new_attr)

