import numpy as np
import matplotlib.pyplot as plt

# Setting the student index digits
p = [1, 7]

# Define the range for input values
L_BOUND = -5
U_BOUND = 5

# Function J(x) to approximate
def q(x):
    return np.sin(x * np.sqrt(p[0] + 1)) + np.cos(x * np.sqrt(p[1] + 1))

# Input data for training
x = np.linspace(L_BOUND, U_BOUND, 100)
y = q(x)

np.random.seed(1)

# Sigmoid function and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Mean squared error loss function and its derivative
def mse_loss(y_out, y):
    return (y_out - y) ** 2

def d_mse_loss(y_out, y):
    return 2 * (y_out - y)

# Neural network class
class DlNet:
    def __init__(self, input_size, hidden_layer_size, output_size):
        self.w1 = np.random.random((input_size, hidden_layer_size))
        self.w1 = self.w1 * 2 - 1
        self.b1 = np.zeros(hidden_layer_size)
        # self.b1 = np.random.random((1, hidden_layer_size))
        # self.b1 = self.b1 * 2 - 1

        self.w2 = np.random.random((hidden_layer_size, output_size))
        self.w2 = self.w2 * 2 - 1
        self.b2 = np.zeros(output_size)
        # self.b2 = np.random.random((1, output_size))
        # self.b2 = self.b2 * 2 - 1

        self.LR = 0.1

    def forward(self, x):
        self.z1 = np.dot(x, self.w1) + self.b1
        self.a1 = sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2

    def backward(self, x, y):
        # self.output_err = d_mse_loss(self.a2, y)
        # self.output_delta = self.output_err * d_sigmoid(self.a2)
        #
        # self.a1_err = self.output_delta.dot(self.w2.T)
        # self.a1_delta = self.a1_err * d_sigmoid(self.a1)
        #
        # self.w1 -= self.LR * x.T.dot(d_sigmoid(self.a1_delta))
        # self.w2 -= self.LR * self.a1.T.dot(self.output_delta)
        #
        # self.b1 -= self.LR * np.sum(self.a1_delta, axis=0)
        #
        # self.b2 -= self.LR * np.sum(self.output_delta, axis=0)
        # print(self.b2)

                   # d Etot/d a2             d a2 / d z2
        a2_delta = d_mse_loss(self.a2, y) * d_sigmoid(self.z2)  # z2 -> a2
                   # d Etot / d a1 * d z1 / d a1                d a1 / a z1
        a1_delta = np.dot(d_mse_loss(self.a1, y), self.w1.T) * d_sigmoid(self.z1)  # z1 -> a1

        # print(a2_delta.shape)
        # print(a1_delta.shape)

        self.w2 -= self.LR * np.dot(self.a1.T, a2_delta)  # d z2 / d w2 * a2_delta
        self.b2 -= self.LR * np.sum(a2_delta, axis=0)  # (d z2 / d b2) = 1 * a2_delta
        # print(np.sum(a2_delta, axis=0))
        # print(self.b2)
        self.w1 -= self.LR * np.dot(x.T, a1_delta)  # d z1 / d w1 * a1_delta
        self.b1 -= self.LR * np.sum(a1_delta, axis=0)  # (d z1 / d b1) = 1 * a1_delta
        # print(a1_delta)
        # print(np.sum(a1_delta, axis=0))
        # print("asdasdasd", self.b1)

    def train(self, x, y, epochs):
        for epoch in range(epochs):
            y_out = self.forward(x)
            self.backward(x, y)
            if epoch % 100 == 0:
                loss = np.mean(mse_loss(y_out, y))
                print(f'Epoch {epoch}, Loss: {loss}')


# Prepare the data for training
x = x.reshape(-1, 1)  # Reshape x to fit the neural network input
nn = DlNet(1, 12, 1)
nn.train(x, y.reshape(-1, 1), 15000)

# Predict using the trained network
yh = nn.forward(x)

# Plot the original and the predicted functions
fig, ax = plt.subplots()
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.plot(x.flatten(), y, 'r', label='Original')
plt.plot(x.flatten(), yh.flatten(), 'b', label='Predicted')
plt.legend()
plt.show()
