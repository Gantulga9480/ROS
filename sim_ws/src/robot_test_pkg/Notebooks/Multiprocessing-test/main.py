import os
from multiprocessing import Pool
from keras.models import load_model
from keras.utils import to_categorical
from keras.datasets import mnist
#download mnist data and split into train and test sets

(X_train, y_train), (X_test, y_test) = mnist.load_data()
processes=('process1.py','process2.py')
model=load_model('model_cnn.h5')

def run_process(process):
    os.system('python {}'.format(process))
def main():
	#reshape data to fit model
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train = X_train.reshape(60000,28,28,1)
    X_test = X_test.reshape(10000,28,28,1)

    #one-hot encode target column
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)


    pool=Pool(processes=2)
    pool.map(run_process,processes)


    
if __name__== "__main__":
    main()
