import numpy as np


class MultiClassPerceptron(object):
    def __init__(self, num_class, feature_dim):
        """Initialize a multi class perceptron model. 

        This function will initialize a feature_dim weight vector,
        for each class. 

        The LAST index of feature_dim is assumed to be the bias term,
                self.w[:,0] = [w1,w2,w3...,BIAS] 
                where wi corresponds to each feature dimension,
                0 corresponds to class 0.  

        Args:
            num_class(int): number of classes to classify
            feature_dim(int): feature dimension for each example 
        """

        self.w = np.zeros((feature_dim+1, num_class))

    def train(self, train_set, train_label):
        """ Train perceptron model (self.w) with training dataset. 

        Args:
            train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
            train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
        """
        # self.w.shape[0] = number of features + 1 = 784 + 1(bias) = 785
        # self.w.shape[1] = number of classes = 10
        # train_set = 50000 examples * 784 features
        # train_set.shape[0] = 50000
        # train_set.shape[1] = 784
        # train_label = 50000
        bias = 1
        learnRate = 1
        epochs = 1
        allSums = np.zeros(10)

        for init in range(0, self.w.shape[1]):
            self.w[self.w.shape[0]-1,init] = 1

        for epoch in range(0, epochs):
            for example in range(0, train_set.shape[0]):
                trainExample = train_set[example]
                trainExample = np.append(trainExample, bias)
                actualClass = train_label[example]
                for aClass in range(0, self.w.shape[1]):
                    allSums[aClass] = np.dot(trainExample, self.w[:,aClass])
                prediction = np.argmax(allSums)

                # if misclassified, update weights
                if prediction != actualClass:
                    # update both the true class and misclassified class
                    self.w[:,actualClass] += learnRate * trainExample
                    self.w[:,prediction] -= learnRate * trainExample

    def test(self, test_set, test_label):
        """ Test the trained perceptron model (self.w) using testing dataset. 
                The accuracy is computed as the average of correctness 
                by comparing between predicted label and true label. 

        Args:
            test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
            test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

        Returns:
                accuracy(float): average accuracy value 
                pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
        """
        bias = 1
        allSums = np.zeros(10)
        correct = 0

        accuracy = 0
        pred_label = np.zeros((len(test_set)))

        for example in range(0, test_set.shape[0]):
            testExample = test_set[example]
            testExample = np.append(testExample, bias)
            actualClass = test_label[example]
            for aClass in range(0, self.w.shape[1]):
                allSums[aClass] = np.dot(testExample, self.w[:,aClass])
            pred_label[example] = np.argmax(allSums)
            
            if pred_label[example] == actualClass:
                correct += 1
        accuracy = correct/test_set.shape[0]
        print(accuracy)

        return accuracy, pred_label

    def save_model(self, weight_file):
        """ Save the trained model parameters 
        """

        np.save(weight_file, self.w)

    def load_model(self, weight_file):
        """ Load the trained model parameters 
        """

        self.w = np.load(weight_file)
