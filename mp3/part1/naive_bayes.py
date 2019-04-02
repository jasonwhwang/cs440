import numpy as np
from math import log10


class NaiveBayes(object):
    def __init__(self, num_class, feature_dim, num_value):
        """Initialize a naive bayes model. 

        This function will initialize prior and likelihood, where 
        prior is P(class) with a dimension of (# of class,)
                that estimates the empirical frequencies of different classes in the training set.
        likelihood is P(F_i = f | class) with a dimension of 
                (# of features/pixels per image, # of possible values per pixel, # of class),
                that computes the probability of every pixel location i being value f for every class label.  

        Args:
            num_class(int): number of classes to classify
            feature_dim(int): feature dimension for each example 
            num_value(int): number of possible values for each pixel 
        """

        self.num_value = num_value
        self.num_class = num_class
        self.feature_dim = feature_dim

        self.prior = np.zeros((num_class))
        self.likelihood = np.zeros((feature_dim, num_value, num_class))

    def train(self, train_set, train_label):
        """ Train naive bayes model (self.prior and self.likelihood) with training dataset. 
                self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
                self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
                        (# of features/pixels per image, # of possible values per pixel, # of class).
                You should apply Laplace smoothing to compute the likelihood. 

        Args:
            train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
            train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
        """

        # self.num_value = 256; the feature/pixel can take on intensity values from 0 to 255
        # self.num_class = 10; the class/labels: T-shirt, Trouser, Pullover, Dress,
        # 						Coat, Sandal, Shirt, Sneaker, Bag, and Ankle boot
        # self.feature_dim = 784; each image is 28X28 pixels represented as a flattened array of size 784
        # self.prior

        # train_set = 50000 * 784; 5000 examples for each class
        # train_label = 50000

        laplace = 0.1
        laplaceD = laplace*self.num_value

        for i in range(0, train_label.size):
            imgClass = train_label[i]
            for j in range(0, self.feature_dim):
                self.likelihood[j, train_set[i, j], imgClass] += 1
            self.prior[imgClass] += 1

        for i in range(0, self.feature_dim):
            for j in range(0, self.num_value):
                for k in range(0, self.num_class):
                    self.likelihood[i, j, k] = (
                        self.likelihood[i, j, k]+laplace)/(self.prior[k]+laplaceD)

        for i in range(0, self.num_class):
            self.prior[i] = self.prior[i]/train_label.size

    def test(self, test_set, test_label):
        """ Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
                by performing maximum a posteriori (MAP) classification.  
                The accuracy is computed as the average of correctness 
                by comparing between predicted label and true label. 

        Args:
            test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
            test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

        Returns:
                accuracy(float): average accuracy value  
                pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
        """

        accuracy = 0
        pred_label = np.zeros((test_label.size))

        for i in range(0, test_label.size):
            arr = np.zeros((self.num_class))
            for j in range(0, self.num_class):
                arr[j] = log10(self.prior[j])
                for k in range(0, self.feature_dim):
                    arr[j] = arr[j] + log10(self.likelihood[k, test_set[i, k], j])

            pred_label[i] = arr.argmax()
            if pred_label[i] == test_label[i]:
                accuracy += 1

        accuracy = accuracy/test_label.size
        print(accuracy)

        return accuracy, pred_label

    def save_model(self, prior, likelihood):
        """ Save the trained model parameters 
        """

        np.save(prior, self.prior)
        np.save(likelihood, self.likelihood)

    def load_model(self, prior, likelihood):
        """ Load the trained model parameters 
        """

        self.prior = np.load(prior)
        self.likelihood = np.load(likelihood)

    def intensity_feature_likelihoods(self, likelihood):
        """
        Get the feature likelihoods for high intensity pixels for each of the classes,
            by sum the probabilities of the top 128 intensities at each pixel location,
            sum k<-128:255 P(F_i = k | c).
            This helps generate visualization of trained likelihood images. 

        Args:
            likelihood(numpy.ndarray): likelihood (in log) with a dimension of
                (# of features/pixels per image, # of possible values per pixel, # of class)
        Returns:
            feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
                (# of features/pixels per image, # of class)
        """

        feature_likelihoods = np.zeros(
            (likelihood.shape[0], likelihood.shape[2]))

        for i in range(0, likelihood.shape[0]):
            for k in range(0, likelihood.shape[2]):
                sum = 0
                for j in range(127, likelihood.shape[1]):
                    sum += self.likelihood[i, j, k]
                feature_likelihoods[i, k] = sum

        return feature_likelihoods
