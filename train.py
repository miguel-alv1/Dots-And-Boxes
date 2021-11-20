# Neural Network for Dots and Boxes
# References:
#   https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/
#   applsci-11-02056-v2%20.pdf

from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

# load the dataset
dataset = loadtxt('data.csv', delimiter=',')

# split into input (X) and output (y) variables
X = dataset[:,0:56]
y = dataset[:,56]
# define the keras model

model = Sequential()
model.add(Dense(100, input_dim=56, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(X, y, epochs=150, batch_size=10)

model.save("DB_Model")

# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))