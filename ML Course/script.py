import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from numpy.linalg import det, inv
from math import sqrt, pi
import scipy.io
import matplotlib.pyplot as plt
import pickle
import sys

def ldaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmat - A single d x d learnt covariance matrix 
    
    # IMPLEMENT THIS METHOD
    y_list = np.array([])
    means = np.array([])
    x1_list = []
    x2_list = []
    x1_mean = []
    x2_mean = []
    for i in range(len(y)):
        if y[i][0] in y_list:
            continue
        else:
            if len(y_list) == 0:
               y_list = np.array(y[i])
            else:
               y_list = np.append(y_list,y[i])        
    
    y_list.sort()
    for iLoop in y_list:
        x1_list = []
        x2_list = []
        for jLoop in range(len(y)):
            if y[jLoop][0] == iLoop:
                x1_list.append(X[jLoop][0])
                x2_list.append(X[jLoop][1])
        
        x1_mean.append(sum(x1_list)/len(x1_list))
        x2_mean.append(sum(x2_list)/len(x2_list))
        
    means = np.array([x1_mean])
    means = np.append(means,[x2_mean],axis = 0)
    
    covmat = np.cov(X.T)
    return means,covmat

def qdaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmats - A list of k d x d learnt covariance matrices for each of the k classes
    
    # IMPLEMENT THIS METHOD
    y_list = np.array([])
    means = np.array([])
    x1_list = []
    x2_list = []
    x1_mean = []
    x2_mean = []
    covmats = []
    for i in range(len(y)):
        if y[i][0] in y_list:
            continue
        else:
            if len(y_list) == 0:
               y_list = np.array(y[i])
            else:
               y_list = np.append(y_list,y[i])        
    
    y_list.sort()
    for iLoop in y_list:
        x1_list = []
        x2_list = []
        for jLoop in range(len(y)):
            if y[jLoop][0] == iLoop:
                x1_list.append(X[jLoop][0])
                x2_list.append(X[jLoop][1])
        
        x1_mean.append(sum(x1_list)/len(x1_list))
        x2_mean.append(sum(x2_list)/len(x2_list))
        covmats.append(np.cov(np.matrix([x1_list,x2_list])))
        
    means = np.array([x1_mean])
    means = np.append(means,[x2_mean],axis = 0)
    
    return means,covmats

def ldaTest(means,covmat,Xtest,ytest):
    # Inputs
    # means, covmat - parameters of the LDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels

    # IMPLEMENT THIS METHOD
    
    #p(y)*1/((2π)^D/2*det(Σ)^1/2)*e^−((x−μ).T*inv(Σ)*(x−μ))/2
    ypred_list = []
    acc = 0
    ypred = np.array([])
    covdet = np.linalg.det(covmat)
    denominator = np.sqrt(covdet)
    for iLoop in range(len(Xtest)):
        ypred_list.append(0)
        max_pred = 0
        for jLoop in range(means.shape[1]):
            Xtest_Minus_Mean = Xtest[iLoop] - means[:,jLoop]
            res = np.matmul(Xtest_Minus_Mean.T,np.linalg.inv(covmat))
            res = np.matmul(res,Xtest_Minus_Mean)
            pred = (1/denominator)*np.exp(-res/2)
            if pred > max_pred:
                ypred_list[iLoop] = jLoop + 1
                max_pred = pred
    ypred = np.array([ypred_list]).T
    
    correct_pred = 0
    for iLoop in range(len(ytest)):
        if ytest[iLoop][0] == ypred[iLoop][0]:
            correct_pred += 1
    
    acc = (correct_pred / len(ytest)) * 100
    return acc,ypred

def qdaTest(means,covmats,Xtest,ytest):
    # Inputs
    # means, covmats - parameters of the QDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels

    # IMPLEMENT THIS METHOD
    ypred_list = []
    acc = 0
    ypred = np.array([])
    for iLoop in range(len(Xtest)):
        ypred_list.append(0)
        max_pred = 0
        for jLoop in range(means.shape[1]):
            covdet = np.linalg.det(covmats[jLoop])
            denominator = np.sqrt(covdet)
            Xtest_Minus_Mean = Xtest[iLoop] - means[:,jLoop]
            res = np.matmul(Xtest_Minus_Mean.T,np.linalg.inv(covmats[jLoop]))
            res = np.matmul(res,Xtest_Minus_Mean)
            pred = (1/denominator)*np.exp(-res/2)
            if pred > max_pred:
                ypred_list[iLoop] = jLoop + 1
                max_pred = pred
    ypred = np.array([ypred_list]).T
    
    correct_pred = 0
    for iLoop in range(len(ytest)):
        if ytest[iLoop][0] == ypred[iLoop][0]:
            correct_pred += 1
    
    acc = (correct_pred / len(ytest)) * 100
    return acc,ypred

def learnOLERegression(X,y):
    # Inputs:                                                         
    # X = N x d 
    # y = N x 1                                                               
    # Output: 
    # w = d x 1 
	
    # IMPLEMENT THIS METHOD
    w = np.array([])
    w = np.linalg.inv(np.matmul(X.T,X))
    w = np.matmul(w,X.T)
    w = np.matmul(w,y)
    #print(w.shape)                                                
    return w

def learnRidgeRegression(X,y,lambd):
    # Inputs:
    # X = N x d                                                               
    # y = N x 1 
    # lambd = ridge parameter (scalar)
    # Output:                                                                  
    # w = d x 1                                                                

    # IMPLEMENT THIS METHOD 
    I = np.identity(X.shape[1])
    w = lambd * I + np.matmul(X.T,X)
    w = np.matmul(np.linalg.inv(w),X.T)
    w = np.matmul(w,y)
    #print(w.shape)
    return w

def testOLERegression(w,Xtest,ytest):
    # Inputs:
    # w = d x 1
    # Xtest = N x d
    # ytest = X x 1
    # Output:
    # mse
    mse = 0
    # IMPLEMENT THIS METHOD
    for iLoop in range(len(Xtest)):
        mse += np.square(ytest[iLoop] - np.matmul(w.T,Xtest[iLoop])) 
    
    mse = (1/len(Xtest)) * mse
    return mse

def regressionObjVal(w, X, y, lambd):

    # compute squared error (scalar) and gradient of squared error with respect
    # to w (vector) for the given data X and y and the regularization parameter
    # lambda
    w = w.reshape(w.shape[0],1)
    term = (y-np.matmul(X,w))
    error = 0.5 * ((np.matmul(term.T,term)) + lambd * np.matmul(w.T,w))
    error_grad = -1* (np.matmul(X.T, term)) +  lambd * w
    
    error = error.flatten()
    error_grad = error_grad.flatten()
    #print(error)
    #print(error_grad)
    # IMPLEMENT THIS METHOD                                             
    return error, error_grad

def mapNonLinear(x,p):
    Xp = np.zeros((x.shape[0],p+1))
    for i in range(p+1):
        Xp[:,i] = np.power(x,i)
    #print(Xp)
    return Xp

# Main script

# Problem 1
# load the sample data                                                                 
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'),encoding = 'latin1')

# LDA
means,covmat = ldaLearn(X,y)
ldaacc,ldares = ldaTest(means,covmat,Xtest,ytest)
print('LDA Accuracy = '+str(ldaacc))
# QDA
means,covmats = qdaLearn(X,y)
qdaacc,qdares = qdaTest(means,covmats,Xtest,ytest)
print('QDA Accuracy = '+str(qdaacc))

# plotting boundaries
x1 = np.linspace(-5,20,100)
x2 = np.linspace(-5,20,100)
xx1,xx2 = np.meshgrid(x1,x2)
xx = np.zeros((x1.shape[0]*x2.shape[0],2))
xx[:,0] = xx1.ravel()
xx[:,1] = xx2.ravel()

fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)

zacc,zldares = ldaTest(means,covmat,xx,np.zeros((xx.shape[0],1)))
plt.contourf(x1,x2,zldares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest.ravel())
plt.title('LDA')

plt.subplot(1, 2, 2)

zacc,zqdares = qdaTest(means,covmats,xx,np.zeros((xx.shape[0],1)))
plt.contourf(x1,x2,zqdares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest.ravel())
plt.title('QDA')

plt.show()
# Problem 2
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'),encoding = 'latin1')

# add intercept
X_i = np.concatenate((np.ones((X.shape[0],1)), X), axis=1)
Xtest_i = np.concatenate((np.ones((Xtest.shape[0],1)), Xtest), axis=1)

w = learnOLERegression(X,y)
mle = testOLERegression(w,Xtest,ytest)

w_i = learnOLERegression(X_i,y)
mle_i = testOLERegression(w_i,Xtest_i,ytest)

print('MSE without intercept '+str(mle))
print('MSE with intercept '+str(mle_i))
print('OLE Regression Weights:\n', w_i)
# Problem 3
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
mses3_train = np.zeros((k,1))
mses3 = np.zeros((k,1))
mintest = 10000000
mintesttrain = 10000000
mintesttotal = 10000000
mintestlambd = 5
mintot = 10000000
mintotlambd = 5
for lambd in lambdas:
    w_l = learnRidgeRegression(X_i,y,lambd)
    mses3_train[i] = testOLERegression(w_l,X_i,y)
    mses3[i] = testOLERegression(w_l,Xtest_i,ytest)
    if mses3[i] < mintest:
        mintesttotal = (mses3[i] + mses3_train[i])
        mintest = mses3[i]
        mintesttrain = mses3_train[i]
        mintestlambd = lambd
    if (mses3[i] + mses3_train[i]) < mintot:
        mintot = (mses3[i] + mses3_train[i])
        mintotlambd = lambd
    i = i + 1

print('Minimum test lambda = ', mintestlambd)
print('Minimum test lambda Test Error = ', mintest)
print('Minimum test lambda Train Error = ', mintesttrain)
print('Minimum test lambda Total Error = ', mintesttotal)
print('Minimum total lambda = ', mintotlambd)
print('Minimum total lambda Error = ', mintot)


fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.subplot(1, 2, 2)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')

plt.show()
# Problem 4
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
mses4_train = np.zeros((k,1))
mses4 = np.zeros((k,1))
opts = {'maxiter' : 20}    # Preferred value.                                                
w_init = np.ones((X_i.shape[1],1))
minlambd = 5
mintest = 1000000
mintesttrain = 1000000
for lambd in lambdas:
    args = (X_i, y, lambd)
    w_l = minimize(regressionObjVal, w_init, jac=True, args=args,method='CG', options=opts)
    w_l = np.transpose(np.array(w_l.x))
    w_l = np.reshape(w_l,[len(w_l),1])
    mses4_train[i] = testOLERegression(w_l,X_i,y)
    mses4[i] = testOLERegression(w_l,Xtest_i,ytest)
    if mses4[i] < mintest:
        mintest = mses4[i]
        mintesttrain = mses4_train[i]
        minlambd = lambd
    i = i + 1
    
print('Gradient Best Lambda: ', minlambd)
print('Gradient Best Lambda Test: ', mintest)
print('Gradient Best Lambda Train: ', mintesttrain)
fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses4_train)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.legend(['Using scipy.minimize','Direct minimization'])

plt.subplot(1, 2, 2)
plt.plot(lambdas,mses4)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')
plt.legend(['Using scipy.minimize','Direct minimization'])
plt.show()

# Problem 5
pmax = 7
lambda_opt = 0.06  # REPLACE THIS WITH lambda_opt estimated from Problem 3
mses5_train = np.zeros((pmax,2))
mses5 = np.zeros((pmax,2))
for p in range(pmax):
    Xd = mapNonLinear(X[:,2],p)
    Xdtest = mapNonLinear(Xtest[:,2],p)
    w_d1 = learnRidgeRegression(Xd,y,0)
    mses5_train[p,0] = testOLERegression(w_d1,Xd,y)
    mses5[p,0] = testOLERegression(w_d1,Xdtest,ytest)
    w_d2 = learnRidgeRegression(Xd,y,lambda_opt)
    mses5_train[p,1] = testOLERegression(w_d2,Xd,y)
    mses5[p,1] = testOLERegression(w_d2,Xdtest,ytest)

print('MSE for Train data:\n', mses5_train)
print('MSE for Test data:\n', mses5)
fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(range(pmax),mses5_train)
plt.title('MSE for Train Data')
plt.legend(('No Regularization','Regularization'))
plt.subplot(1, 2, 2)
plt.plot(range(pmax),mses5)
plt.title('MSE for Test Data')
plt.legend(('No Regularization','Regularization'))
plt.show()
