"""
Created on Mon Nov  8 16:51:50 2021

@author: Rafał Biedrzycki
Kodu tego mogą używać moi studenci na ćwiczeniach z przedmiotu Wstęp do Sztucznej Inteligencji.
Kod ten powstał aby przyspieszyć i ułatwić pracę studentów, aby mogli skupić się na algorytmach sztucznej inteligencji.
Kod nie jest wzorem dobrej jakości programowania w Pythonie, nie jest również wzorem programowania obiektowego, może zawierać błędy.

Nie ma obowiązku używania tego kodu.
"""

import numpy as np
import matplotlib.pyplot as plt

# ToDo tu prosze podac pierwsze cyfry numerow indeksow
p = [1, 7]

L_BOUND = -5
U_BOUND = 5


def q(x):
    return np.sin(x * np.sqrt(p[0] + 1)) + np.cos(x * np.sqrt(p[1] + 1))


x = np.linspace(L_BOUND, U_BOUND, 100)
y = q(x)

np.random.seed(1)


# f logistyczna jako przykład sigmoidalej
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# pochodna fun. 'sigmoid'
def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


# f. straty
def nloss(y_out, y):
    return (y_out - y) ** 2


# pochodna f. straty
def d_nloss(y_out, y):
    return 2 * (y_out - y)


class DlNet:
    def __init__(self, x, y):
        self.x = x.reshape(-1, 1)  # (100, ) -> (100, 1)
        self.y = y.reshape(-1, 1)
        self.y_out = 0

        self.HIDDEN_L_SIZE = 70
        self.INPUT_L_SIZE = 1
        self.OUTPUT_L_SIZE = 1
        self.LR = 0.1

        # Initialize weights and biases
        self.w1 = np.random.randn(self.INPUT_L_SIZE, self.HIDDEN_L_SIZE)
        self.b1 = np.zeros((1, self.HIDDEN_L_SIZE))
        self.w2 = np.random.randn(self.HIDDEN_L_SIZE, self.OUTPUT_L_SIZE)
        self.b2 = np.zeros((1, self.OUTPUT_L_SIZE))

    def forward(self, x):
        self.z1 = np.dot(x, self.w1) + self.b1
        self.a1 = sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.y_out = self.z2
        return self.y_out

    def predict(self, x):
        x = x.reshape(-1, 1)  # Ensure x is the correct shape
        return self.forward(x)

    def backward(self, x, y):
        m = y.shape[0]
        # TODO: można wywalić m, ale zmniejszyć lr

        # Calculate output layer error
        d_loss_y_out = d_nloss(self.y_out, y)  # d y_los_out / d y_out

        # Gradient for w2 and b2
        d_z2 = d_loss_y_out  # d y_los_out / d z2
        d_w2 = np.dot(self.a1.T, d_z2) / m  # d y_los_out / d z2 * d z2 / d w2
        d_b2 = np.sum(d_z2, axis=0, keepdims=True) / m  # sum along all samples

        # Calculate hidden layer error
        d_a1 = np.dot(d_z2, self.w2.T)  # [HL -> OL]: d y_los_out / d z2 * (d z2 / d a1 = w2)
        d_z1 = d_a1 * d_sigmoid(self.z1)  # d y_los_out / d z2 * (d z2 / d a1 = w2) * d a1 / d z1

        # Gradient for w1 and b1
        d_w1 = np.dot(x.T, d_z1) / m  # d y_los_out / d z2 * (d z2 / d a1 = w2) * d a1 / d z1 * (d z1 / d w1 = x)
        d_b1 = np.sum(d_z1, axis=0, keepdims=True) / m  # sum along all samples

        # Update weights and biases
        self.w1 -= self.LR * d_w1
        self.b1 -= self.LR * d_b1
        self.w2 -= self.LR * d_w2
        self.b2 -= self.LR * d_b2

    def train(self, x_set, y_set, iters):
        x_set = x_set.reshape(-1, 1)  # Ensure x_set is the correct shape
        y_set = y_set.reshape(-1, 1)  # Ensure y_set is the correct shape
        for i in range(iters):
            self.forward(x_set)
            self.backward(x_set, y_set)
            if i % 1000 == 0:
                loss = np.mean(nloss(self.y_out, y_set))
                print(f"Iteration {i}, loss: {loss}")


nn = DlNet(x, y)
nn.train(x, y, 15000)

# Get predictions
yh = nn.predict(x)

# Plotting the results
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.plot(x, y, 'r', label='Original function')
plt.plot(x, yh, 'b', label='Approximated function')
plt.legend()
plt.show()
