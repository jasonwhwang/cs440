import numpy as np
from math import exp
import time
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)

    num_classes = 10
    x_train = 50000 train examples of size 784
    y_train = 50000 train labels
    w1.shape = (784, 256)
    w4.shape = (256, 10)
    b1.shape = (256)
    b4.shape = (10)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):
    batch_size = 200
    s = np.arange(y_train.shape[0])
    allLoss = []

    # 1. Run for Epoch
    for e in range(epoch):
        start = time.time()
        # 2. Shuffle Values(x_train) and Labels(y_train)
        xs = None
        ys = None
        if shuffle:
            np.random.shuffle(s)
            xs = x_train[s]
            ys = y_train[s]
        else:
            xs = x_train
            ys = y_train

        # 3. Split Dataset into Batches
        #xb = [xs[i:i+batch_size] for i in range(0, xs.shape[0], batch_size)]
        #yb = [xs[i:i+batch_size] for i in range(0, ys.shape[0], batch_size)]
        eLoss = 0.0
        for i in range(xs.shape[0]//batch_size - 1):
            xb = xs[i*batch_size :(i+1) * batch_size, :]
            yb = ys[i*batch_size :(i+1) * batch_size]
        # 4. Train on Batches

            #for batch in range(len(xb)):
            w1, w2, w3, w4, b1, b2, b3, b4, bLoss = four_nn(w1, w2, w3, w4, b1, b2, b3, b4, xb,
                                                                yb, num_classes, False)
            eLoss += bLoss
        allLoss.append(eLoss)
        print("%.2f sec" % (time.time()-start))

    #plt.plot(allLoss)
    #plt.show()
    return w1, w2, w3, w4, b1, b2, b3, b4, allLoss

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.get_cmap("Blues")):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):

    classifications = four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test,
                                                        y_test, num_classes, True)

    avg_class_rate = np.sum(classifications == y_test) / len(y_test)
    matrix = np.zeros((num_classes, num_classes))

    for i in range(len(classifications)):
        matrix[y_test[i], classifications[i]] += 1

    class_rate_per_class = []
    for i in range(num_classes):
        class_rate_per_class.append(matrix[i,i])

    for i in range(num_classes):
        sum = np.sum(matrix[i])
        matrix[i] = matrix[i] / sum
        class_rate_per_class[i] = class_rate_per_class[i] / sum

    print(matrix)
    print(class_rate_per_class)
    #print(avg_class_rate)

    #class_names = np.array(["T-shirt/top","Trouser","Pullover","Dress",
    #    "Coat","Sandal","Shirt","Sneaker","Bag","Ankle boot"])

    #plot_confusion_matrix(y_test, classifications, classes=class_names, normalize=True,
    #                  title='Confusion matrix, with normalization')

    #plt.show()

    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x, y, num_classes, test):
    eta = 0.1

    z1, a_cache_1 = affine_forward(x, w1, b1)
    a1, r_cache_1 = relu_forward(z1)
    z2, a_cache_2 = affine_forward(a1, w2, b2)
    a2, r_cache_2 = relu_forward(z2)
    z3, a_cache_3 = affine_forward(a2, w3, b3)
    a3, r_cache_3 = relu_forward(z3)
    f0, a_cache_4 = affine_forward(a3, w4, b4)

    if test:
        # perform classifications
        return np.argmax(f0, axis = 1)

    loss, df = cross_entropy(f0, y)
    da3, dw4, db4 = affine_backward(df, a_cache_4)
    dz3 = relu_backward(da3, r_cache_3)
    da2, dw3, db3 = affine_backward(dz3, a_cache_3)
    dz2 = relu_backward(da2, r_cache_2)
    da1, dw2, db2 = affine_backward(dz2, a_cache_2)
    dz1 = relu_backward(da1, r_cache_1)
    dx, dw1, db1 = affine_backward(dz1, a_cache_1)

    # update weights using gradient descent
    w1 -= eta * dw1
    w2 -= eta * dw2
    w3 -= eta * dw3
    w4 -= eta * dw4

    b1 -= eta * db1
    b2 -= eta * db2
    b3 -= eta * db3
    b4 -= eta * db4

    return w1, w2, w3, w4, b1, b2, b3, b4, loss

"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):
    Z = np.matmul(A, W)
    Z += b
    cache = (A, W, b)
    return Z, cache

def affine_backward(dZ, cache):
    w = np.transpose(cache[1])
    dA = np.matmul(dZ, w)

    a = np.transpose(cache[0])
    dW = np.matmul(a, dZ)

    dB = np.sum(dZ, axis=0)
    return dA, dW, dB

def relu_forward(Z):
    A = np.where(Z <=0, 0, Z)
    cache = Z
    return A, cache

def relu_backward(dA, cache):
    coors = np.where(cache >= 0, dA, 0)
    return coors

def cross_entropy(F, y):
    loss = 0.0
    dF = np.zeros((F.shape[0], F.shape[1]))
    for i in range(F.shape[0]):
        Fiy = F[i, int(y[i])]
        logVal = np.exp(F[i])
        logSum = np.sum(logVal)
        logTemp = np.log(logSum)
        loss += Fiy - logTemp

        for j in range(F.shape[1]):
            gradient = 0.0
            if j == y[i]:
                gradient = 1
            newVal = -(1/F.shape[0]) * (gradient - exp(F[i,j])/logSum)
            dF[i,j] = newVal


    loss = -1* loss/F.shape[0]

    return loss, dF
