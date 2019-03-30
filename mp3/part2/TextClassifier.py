from math import log

# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0
        self.prior = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.likelihood = [dict(), dict(), dict(), dict(), dict(), dict(
        ), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()]
        self.words = set()

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """
        # self.prior length = 14 classes
        # self.likelihood length = 14 dictionaries
        # train_set, train_label length = 3865 examples

        laplace = 1

        mostCommonFeatures = []

        for example in range(0, len(train_label)):
            textClass = train_label[example] - 1
            self.prior[textClass] += 1
            for word in train_set[example]:
                if word in self.likelihood[textClass]:
                    self.likelihood[textClass][word] += 1
                else:
                    self.likelihood[textClass][word] = 1
                
                if word not in self.words:
                    self.words.add(word)

        for textClass in range(0, len(self.likelihood)):
            d = self.likelihood[textClass]
            d = sorted(d.items(), key=lambda x: x[1], reverse=True)
            common = d[:20]
            mostCommonFeatures.append(common)

        # for feature in mostCommonFeatures:
        #     print(feature)
        #     print()
        # input("-->")

        for textClass in range(0, len(self.likelihood)):
            for feature in self.likelihood[textClass]:
                self.likelihood[textClass][feature] = log((self.likelihood[textClass][feature]+laplace)/(len(self.likelihood[textClass])+ len(self.words)))

        for textClass in range(0, len(self.prior)):
            self.prior[textClass] = log(self.prior[textClass]/len(train_label))

    def predict(self, x_set, dev_label, lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """

        accuracy = 0.0
        result = []

        for example in range(0, len(dev_label)):
            predVal=[]
            for textClass in range(0, len(self.prior)):
                val=self.prior[textClass]
                for word in x_set[example]:
                    if word in self.likelihood[textClass]:
                        val += self.likelihood[textClass][word]
                    else:
                        val -= 10
                predVal.append(val)
            maxVal=max(predVal)
            prediction=predVal.index(maxVal)

            if prediction+1 == dev_label[example]:
                accuracy += 1

            # print(predVal)
            # print(prediction+1)
            # print(dev_label[example])
            # input("-->")

            result.append(prediction + 1)

        accuracy=accuracy/len(dev_label)

        return accuracy, result
