import numpy
import random

def cov(X,Y):
    """
    returns the covariance of the datasets X and Y
    """            
    if len(X) != len(Y):
        raise ValueError, 'X and Y must be the same size.'
    mean_X = numpy.mean(X)
    mean_Y = numpy.mean(Y)
    dev_X = [x-mean_X for x in X]
    #~ print dev_X
    dev_Y = [y-mean_Y for y in Y]
    #~ print dev_Y
    res = 0
    for i in range(len(X)):
        res += dev_X[i] * dev_Y[i]
    #or     res = sum([v1*v2 for v1,v2 in zip(dev_X,dev_Y)])
    return res/len(X)
#~ 
def corr(X,Y):
    """
    takes two datasets and returns their Pearson correlation
    """
    c = cov(X,Y)
    sig_X = numpy.std(X)
    sig_Y = numpy.std(Y)
    return c/(sig_X*sig_Y)
    
def std_scores(X):
    """
    returns the standard scores of the dataset X
    """
    mean = numpy.mean(X)
    std = numpy.std(X)
    return [(x-mean)/std for x in X]

def createSample(dist,lenSamp):
    """
    Creates a sample of lenSamp items from dist with replacement
    """
    return [random.choice(dist) for i in range(lenSamp)]

def getpvalue(distribution,sample1,sample2,condition,numiter=1000):
    """
    Takes a distribution, the size of two samples, a lambda condition,
    and the number of iterations, and returns the p value of the condition.
    """
    numTrue = 0
    for _ in range(numiter):
        if condition(createSample(distribution,sample1),createSample(distribution,sample2)):
            numTrue += 1
    return float(numTrue) / float(numiter)

def binData(data,numBins):
    maxVal = max(data)
    minVal = min(data)
    binSize = (maxVal - minVal) / float(numBins)
    binDict = {}
    returnDict = {}
    bins = [(minVal,minVal+binSize)]
    n = 2
    while minVal + (n-1)*binSize < maxVal:
        bins.append((minVal+((n-1)*binSize),minVal+(n*binSize)))
        n += 1
    for item in data:
        for b in bins:
            if item >= b[0] and item <= b[1]:
                binDict[b] = binDict.get(b,0) + 1
    for key,val in binDict.items():
        returnDict[key[0]] = val / float(len(data))
    return returnDict, binSize
    
def getNthPercentile(cdf,percentile):
    """
    Takes a CDF object and a percentile and returns all the
    values in the CDF below the percentile
    """
    res = []
    for val, prob in cdf.Items():
        if prob <= percentile:
            res.append(val)
    return res


if __name__ == '__main__':
    X = [1,2,3,4,5,6,7,8,9,10]
    print binData(X,10)
