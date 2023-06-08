import numpy as np
from math import log, floor

class Automaton:  
    radius=1
    rule_book=[0,0,1,1,0,1,1,0]

    @classmethod
    def nextLayer(self, curLayer):
        output = np.array([0 for i in range(len(curLayer))])
        array = np.array([])
        if self.radius == 1:
            array = 7 - np.sum(np.vstack((np.roll(curLayer, 1) * 4, curLayer * 2, np.roll(curLayer, -1))), axis=0)
        elif self.radius == 2:
            array = 31 - np.sum(np.vstack((np.roll(curLayer, 2) * 16, np.roll(curLayer, 1) * 8,
                                        curLayer * 4, np.roll(curLayer, -1) * 2, np.roll(curLayer, -2))), axis=0)
        elif self.radius == 3:
            array = 127 - np.sum(np.vstack((np.roll(curLayer, 3) * 64, np.roll(curLayer, 2) * 32,
                                            np.roll(curLayer, 1) * 16, curLayer * 8, np.roll(curLayer, -1) * 4,
                                            np.roll(curLayer, -2) * 2, np.roll(curLayer, -3))), axis=0)

        for i in range(len(array)):
            if self.rule_book[array[i]] == 1:
                output[i] = 1
            else:
                output[i] = 0

        return output

    @classmethod
    def getRuleByLangton(self, langtonFactor):
        rule_book = [0 for _ in range(2**(2*self.radius+1))]
        for _ in range(floor(2**(2*self.radius+1)*langtonFactor)):
            index = np.random.randint(0, 2**(2*self.radius+1))
            while rule_book[index] != 0:
                index = np.random.randint(0, 2**(2*self.radius+1))
            rule_book[index] = 1

        return rule_book

    @classmethod
    def getLangton(self):
        return sum(self.rule_book) # chyba to powinno być jeszcze podzielone przez długość listy
    
    @classmethod
    def returnString(array):
        arr = list(array.flatten())
        strings = [str(x) for x in arr]

        return ' '.join(strings)
    
    @classmethod
    def sumEntropy(self, line, radius):
        dic = {}
        lineSize = line.size
        key = self.returnString(line[0:5])
        dic[key] = 1

        for i in range(lineSize - 1):
            line = np.roll(line, -1)
            key = self.returnString(line[0:5])
            if not key in dic:
                dic[key] = 1
            else:
                dic[key] += 1

        entropy = 0
        for key in dic:
            entropy += (dic[key] / lineSize) * log(dic[key] / lineSize, 2)

        return -entropy

    @classmethod
    def newEntropy(self, ruleBinary, layerWidth):
        field = np.array([])
        gen = 0
        if self.radius == 1:
            field = np.zeros([100, layerWidth], dtype=np.int8)
            gen = 100
        elif self.radius == 2:
            field = np.zeros([200, layerWidth], dtype=np.int8)
            gen = 200
        elif self.radius == 3:
            field = np.zeros([500, layerWidth], dtype=np.int8)
            gen = 500

        field[0, layerWidth // 2] = 1
        averageEntropy = 0
        averageEntropy += self.sumEntropy(field[0, :], self.radius)

        for i in range(gen + 99):
            field[i + 1, :] = self.nextLayer(field[i, :])
            if i - gen + 1 >= 0:
                averageEntropy += self.sumEntropy(field[i + 1, :], self.radius)

        return averageEntropy/100
