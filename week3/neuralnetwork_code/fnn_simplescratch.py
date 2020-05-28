# Rohitash Chandra, 2017 c.rohitash@gmail.conm

#https://github.com/rohitash-chandra
 

# ref: http://iamtrask.github.io/2015/07/12/basic-python-network/  
 

#Sigmoid units used in hidden and output  

# Numpy used: http://cs231n.github.io/python-numpy-tutorial/#numpy-arrays
 

 

import matplotlib.pyplot as plt
import numpy as np 
import random
import time
 
class Network:

	def __init__(self, Topo, Train, Test, MaxTime, Samples, MinPer): 
		self.Top  = Topo  # NN topology [input, hidden, output]
		self.Max = MaxTime # max epocs
		self.TrainData = Train
		self.TestData = Test
		self.NumSamples = Samples

		self.lrate  = 0 # will be updated later with BP call

		self.momenRate = 0
		self.useNesterovMomen = 0 #use nestmomentum 1, not use is 0

		self.minPerf = MinPer
																		#initialize weights ( W1 W2 ) and bias ( b1 b2 ) of the network
		np.random.seed() 
		self.W1 = np.random.randn(self.Top[0]  , self.Top[1])  / np.sqrt(self.Top[0] ) 
		self.B1 = np.random.randn(1  , self.Top[1])  / np.sqrt(self.Top[1] ) # bias first layer
		self.BestB1 = self.B1
		self.BestW1 = self.W1 
		self.W2 = np.random.randn(self.Top[1] , self.Top[2]) / np.sqrt(self.Top[1] )
		self.B2 = np.random.randn(1  , self.Top[2])  / np.sqrt(self.Top[1] ) # bias second layer
		self.BestB2 = self.B2
		self.BestW2 = self.W2 
		self.hidout = np.zeros((1, self.Top[1] )) # output of first hidden layer
		self.out = np.zeros((1, self.Top[2])) #  output last layer


	def sigmoid(self,x):
		return 1 / (1 + np.exp(-x))

	def sampleEr(self,actualout):
		error = np.subtract(self.out, actualout)
		sqerror= np.sum(np.square(error))/self.Top[2] 
		 
		return sqerror

	def ForwardPass(self, X ): 
		z1 = X.dot(self.W1) - self.B1  
		self.hidout = self.sigmoid(z1) # output of first hidden layer   
		z2 = self.hidout.dot(self.W2)  - self.B2 
		self.out = self.sigmoid(z2)  # output second hidden layer


	def ForwardPass_Simple(self, input ):  # Alternative implementation of ForwardPass(self, X )
		layer = 0 # input to hidden layer
		weightsum = 0
		for y in range(0, self.Top[layer+1]):
			for x in range(0, self.Top[layer]):

				print(input)
				weightsum  +=   input[x] * self.W1[x,y]

			self.hid_out[y] = self.sigmoid(weightsum - self.B1[y])
			weightsum = 0

		layer = 1 #   hidden layer to output
		weightsum = 0
		for y in range(0, self.Top[layer+1]):
			for x in range(0, self.Top[layer]):
				weightsum  +=   self.hid_out[x] * self.W2[x,y]
			self.out[y] = self.sigmoid(weightsum - self.B2[y])
			weightsum = 0


	def BackwardPass(self, Input, desired):   
		out_delta =   (desired - self.out)*(self.out*(1-self.out))  
		hid_delta = out_delta.dot(self.W2.T) * (self.hidout * (1-self.hidout))
		 
		self.W2+= (self.hidout.T.dot(out_delta) * self.lrate)  
		self.B2+=  (-1 * self.lrate * out_delta)
		self.W1 += (Input.T.dot(hid_delta) * self.lrate) 
		self.B1+=  (-1 * self.lrate * hid_delta)

	def BackwardPass_Simple(self, input, desired ):  # Alternative implementation of BackwardPass(self, Input, desired)

		# compute gradients for each layer (output and hidden layer)

		layer = 2 #output layer
		for x in range(0, self.Top[layer]):
			self.out_delta[x] =  (desired[x] - self.out[x])*(self.out[x]*(1-self.out[x]))

		layer = 1 # hidden layer
		temp = 0
		for x in range(0, self.Top[layer]):
			for y in range(0, self.Top[layer+1]):
				temp += ( self.out_delta[y] * self.W2[x,y]);
				self.hid_delta[x] =  (self.hid_out[x] * (1 - self.hid_out[x])) * temp
				temp = 0

				# update weights and bias
		layer = 1 # hidden to output

		for x in range(0, self.Top[layer]):
			for y in range(0, self.Top[layer+1]):
					self.W2[x,y] += self.learn_rate * self.out_delta[y] * self.hid_out[x]
			#print self.W2
			for y in range(0, self.Top[layer+1]):
				self.B2[y] += -1 * self.learn_rate * self.out_delta[y]

		layer = 0 # Input to Hidden

		for x in range(0, self.Top[layer]):
			for y in range(0, self.Top[layer+1]):
				self.W1[x,y] += self.learn_rate * self.hid_delta[y] * input[x]

		for y in range(0, self.Top[layer+1]):
			self.B1[y] += -1 * self.learn_rate * self.hid_delta[y]

			
 
	def TestNetwork(self, Data, testSize, erTolerance):
		Input = np.zeros((1, self.Top[0])) # temp hold input
		Desired = np.zeros((1, self.Top[2])) 
		nOutput = np.zeros((1, self.Top[2]))
		clasPerf = 0
		sse = 0  
		self.W1 = self.BestW1
		self.W2 = self.BestW2 #load best knowledge
		self.B1 = self.BestB1
		self.B2 = self.BestB2 #load best knowledge
 
		for s in range(0, testSize):
							
			Input[:]  =   Data[s,0:self.Top[0]] 
			Desired[:] =  Data[s,self.Top[0]:] 

			self.ForwardPass(Input ) 
			sse = sse+ self.sampleEr(Desired)  

			if(np.isclose(self.out, Desired, atol=erTolerance).any()):
				clasPerf =  clasPerf +1  

		return ( sse/testSize, float(clasPerf)/testSize * 100 )




	def saveKnowledge(self):
		self.BestW1 = self.W1
		self.BestW2 = self.W2
		self.BestB1 = self.B1
		self.BestB2 = self.B2  

	def BP_GD(self, learnRate):  

		self.lrate = learnRate 
 
		Input = np.zeros((1, self.Top[0])) # temp hold input
		Desired = np.zeros((1, self.Top[2])) 
		Er = []#np.zeros((1, self.Max)) 
		epoch = 0
		bestmse = 100
		bestTrain = 0
		while  epoch < self.Max and bestTrain < self.minPerf :
			sse = 0
			for s in range(0, self.NumSamples):
		
				Input[:]  =  self.TrainData[s,0:self.Top[0]]  
				Desired[:] = self.TrainData[s,self.Top[0]:]  

				self.ForwardPass_Simple(Input)  
				self.BackwardPass(Input , Desired)
				sse = sse+ self.sampleEr(Desired)
			 
			mse = np.sqrt(sse/self.NumSamples*self.Top[2])

			if mse < bestmse:
				 bestmse = mse
				 self.saveKnowledge() 
				 (x,bestTrain) = self.TestNetwork(self.TrainData, self.NumSamples, 0.2)

			Er = np.append(Er, mse)
			
			epoch=epoch+1  

		return (Er,bestmse, bestTrain, epoch) 



def normalisedata(data, inputsize, outsize): # normalise the data between [0,1]
	traindt = data[:,np.array(range(0,inputsize))]	
	dt = np.amax(traindt, axis=0)
	tds = abs(traindt/dt) 
	return np.concatenate(( tds[:,range(0,inputsize)], data[:,range(inputsize,inputsize+outsize)]), axis=1)

def main(): 
					
		
	problem = 3 # [1,2,3] choose your problem (Iris classfication or 4-bit parity or XOR gate)
				

	if problem == 1:
		TrDat  = np.loadtxt("data/train.csv", delimiter=',') #  Iris classification problem (UCI dataset)
		TesDat  = np.loadtxt("data/test.csv", delimiter=',') #  
		Hidden = 6
		Input = 4
		Output = 2 #https://stats.stackexchange.com/questions/207049/neural-network-for-binary-classification-use-1-or-2-output-neurons
		TrSamples =  110
		TestSize = 40
		learnRate = 0.1 
		mRate = 0.01   
		TrainData  = normalisedata(TrDat, Input, Output) 
		TestData  = normalisedata(TesDat, Input, Output)
		MaxTime = 500


		 

	elif problem == 2:
		TrainData = np.loadtxt("data/4bit.csv", delimiter=',') #  4-bit parity problem
		TestData = np.loadtxt("data/4bit.csv", delimiter=',') #  
		Hidden = 4
		Input = 4
		Output = 1 #  https://stats.stackexchange.com/questions/207049/neural-network-for-binary-classification-use-1-or-2-output-neurons
		TrSamples =  16
		TestSize = 16
		learnRate = 0.9 
		mRate = 0.01
		MaxTime = 3000

	elif problem == 3:
		TrainData = np.loadtxt("data/xor.csv", delimiter=',') #  XOR  problem
		TestData = np.loadtxt("data/xor.csv", delimiter=',') #  
		Hidden = 3
		Input = 2
		Output = 2  # one hot encoding: https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
		TrSamples =  4
		TestSize = 4
		learnRate = 0.9 
		mRate = 0.01
		MaxTime = 500 

	#print(TrainData)

	# todo: softmax: https://stats.stackexchange.com/questions/207049/neural-network-for-binary-classification-use-1-or-2-output-neurons


	Topo = [Input, Hidden, Output] 
	MaxRun = 3 # number of experimental runs 
	 
	MinCriteria = 95 #stop when learn 95 percent

	trainTolerance = 0.2 # [eg 0.15 would be seen as 0] [ 0.81 would be seen as 1]
	testTolerance = 0.4

	useStocasticGD = 1 # 0 for vanilla BP. 1 for Stocastic BP
	useVanilla = 1 # 1 for Vanilla Gradient Descent, 0 for Gradient Descent with momentum (either regular momentum or nesterov momen) 
	useNestmomen = 0 # 0 for regular momentum, 1 for Nesterov momentum
	 


	trainPerf = np.zeros(MaxRun)
	testPerf =  np.zeros(MaxRun)

	trainMSE =  np.zeros(MaxRun)
	testMSE =  np.zeros(MaxRun)
	Epochs =  np.zeros(MaxRun)
	Time =  np.zeros(MaxRun)

	for run in range(0, MaxRun  ):
		print(run, ' is experimental run') 

		fnn = Network(Topo, TrainData, TestData, MaxTime, TrSamples, MinCriteria)
		start_time=time.time()
		(erEp,  trainMSE[run] , trainPerf[run] , Epochs[run]) = fnn.BP_GD(learnRate)   

		Time[run]  =time.time()-start_time
		(testMSE[run], testPerf[run]) = fnn.TestNetwork(TestData, TestSize, testTolerance)
	print(' print classification performance for each experimental run') 
	print(trainPerf)
	print(testPerf)
	print(' print RMSE performance for each experimental run') 
	print(trainMSE)
	print(testMSE)
	print(' print Epocs and Time taken for each experimental run') 
	print(Epochs)
	print(Time)
	print(' print mean and std of training performance') 
	

	print(np.mean(trainPerf), np.std(trainPerf))
	print(np.mean(testPerf), np.std(testPerf))

	print(' print mean and std of computational time taken') 
	
	print(np.mean(Time), np.std(Time))
	
	
				 
	plt.figure()
	plt.plot(erEp )
	plt.ylabel('error')  
	plt.savefig('out.png')
			 
 
if __name__ == "__main__": main()
