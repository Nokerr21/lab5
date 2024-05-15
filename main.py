import matplotlib.pyplot as plt
import perceptron
import numpy as np

# ToDo tu prosze podac pierwsze cyfry numerow indeksow
p = [1, 7]

L_BOUND = -5
U_BOUND = 5
def q(x):
    return np.sin(x * np.sqrt(p[0] + 1)) + np.cos(x * np.sqrt(p[1] + 1))


if __name__ == '__main__':
    x = np.linspace(L_BOUND, U_BOUND, 100)
    y = q(x)

    np.random.seed(1)

    nn = perceptron.DlNet(x, y)
    nn.train(x, y, 30000)

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
