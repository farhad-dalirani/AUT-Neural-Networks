import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from tensorflow.python.client import device_lib
from keras.callbacks import TensorBoard
import threading
from keras.layers import Input, Dense
from keras.models import Model
from keras.datasets import mnist
import numpy as np
from auto_encoders import create_auto_encoder
from keras.models import Sequential
from keras.models import model_from_json
from stl10_input import read_all_images, images_gray_falt_version, read_labels, read_names_of_labels
import matplotlib.pyplot as plt
import keras
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import json
#################################################################################
#       Read Dataset
#################################################################################
# dataset paths
path_dataset = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary'
path_train_x = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary\\train_X.bin'
path_train_y = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary\\train_y.bin'
path_test_x = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary\\test_X.bin'
path_test_y = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary\\test_y.bin'
path_unlabeled = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary\\unlabeled_X.bin'
path_labels_name = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary\\class_names.txt'
path_save_directory = 'D:\\ANN\\dataset\\stl10_binary\\stl10_binary\\new\\new'

# Read images (train images)
# x_train = read_all_images(path_train_x)
# convert images to gray flatten
# x_train = images_gray_falt_version(images=x_train)
# convert type
# x_train = x_train.astype('float32') / 255.
# print(x_train.shape, type(x_train))

# Read images (test images)
x_test = read_all_images(path_test_x)
# convert images to gray flatten
x_test = images_gray_falt_version(images=x_test)
# convert type
x_test = x_test.astype('float32') / 255.
print(x_test.shape, type(x_test))

# Read images (unlabeled images)
x_unlabel = read_all_images(path_unlabeled)
# convert images to gray flatten
x_unlabel = images_gray_falt_version(images=x_unlabel)
# convert type
x_unlabel = x_unlabel.astype('float32') / 255.
print(x_unlabel.shape, type(x_unlabel))

# Read labels (train)
# y_train = read_labels(path_train_y)
# print(y_train.shape)

# Read labels (train)
# y_test = read_labels(path_test_y)
# print(y_test.shape)

# train and validation
# x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, train_size=0.80, random_state=64)
# print(x_train.shape, y_train.shape, x_valid.shape, y_valid.shape)

# Read name of labels
labels_name = read_names_of_labels(path=path_labels_name)
print('labels name: {}'.format(labels_name))
print(type(labels_name))

"""
# print some of images(train)
for i in range(0, 6):
    plt.figure()
    plt.imshow(x_train[i].reshape(96, 96), cmap='gray')
    plt.title(y_train[i])
plt.show()
# print some of images(test)
for i in range(0, 6):
    plt.figure()
    plt.imshow(x_test[i].reshape(96, 96), cmap='gray')
    plt.title(y_test[i])
plt.show()
"""
#################################################################################
#       Load Best autoencoder Autoencoder from file and transform images
#       by autoencoder
#################################################################################
# path of best auto encoder
path = 'C:\\Users\\Home\\Dropbox\\codes\\ANN\\Assignment_5\\autoencoder1\\'

# load json and create model
json_file = open(path + 'model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_autoencoder = model_from_json(loaded_model_json)
# load weights into new model
loaded_autoencoder.load_weights(path + "model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['mse'])
# evaluate the model
# scores = loaded_autoencoder.evaluate(x_train, x_train, verbose=0)
# print("Train Evaluation {}: {}".format(loaded_autoencoder.metrics_names[0], scores[0]))
# print("Train Evaluation {}: {}".format(loaded_autoencoder.metrics_names[1], scores[1]))

# scores = loaded_autoencoder.evaluate(x_test, x_test, verbose=0)
# print("Test Evaluation {}: {}".format(loaded_autoencoder.metrics_names[0], scores[0]))
# print("Test Evaluation {}: {}".format(loaded_autoencoder.metrics_names[1], scores[1]))

# scores = loaded_autoencoder.evaluate(x_valid, x_valid, verbose=0)
# print("Validation Evaluation {}: {}".format(loaded_autoencoder.metrics_names[0], scores[0]))
# print("Validation Evaluation {}: {}".format(loaded_autoencoder.metrics_names[1], scores[1]))

# use auto encoder to compress train and test data
# x_train = loaded_autoencoder.predict(x_train)
# x_valid = loaded_autoencoder.predict(x_valid)
# x_test = loaded_autoencoder.predict(x_test)
x_unlabel_coded = loaded_autoencoder.predict(x_unlabel)
#################################################################################
#       Read Center of clusters and cluster of each observation in unlabeled dataset
#
#################################################################################
with open('C:\\Users\\Home\\Dropbox\\codes\\ANN\\Assignment_5\\clustering\\centers_labeled.txt') as json_file:
    data = json.load(json_file)

clusters_kernel = np.array(data['centers'])
cluster_unlabel = np.array(data['cluster_unlabel'])
print('Shape of cluster lebels of unlabeled data', cluster_unlabel)


# cluster of each instance
#cluster_unlabel = kmeans.predict(x_unlabel_coded)
#cluster_unlabel = np.array(cluster_unlabel)

# put unlabel dataset to different clusters
unlabels_in_clusters = []
for k in range(0, 10):
    unlabels_in_clusters.append(x_unlabel[cluster_unlabel == k, :])

# put unlabel dataset to different clusters
unlabels_in_clusters_coded = []
for k in range(0, 10):
    unlabels_in_clusters_coded.append(x_unlabel_coded[cluster_unlabel == k, :])


#################################################################################
#       Plotting
#
#################################################################################
# test image
#test_images = x_test[100,:]
#test_images = x_test[200,:]
##test_images = x_test[300,:]
##test_images = x_test[500,:]
##test_images = x_test[600,:]
##test_images = x_test[700,:]
test_images = x_test[667,:]

# cluster test image
dist = []
for i in range(0, 10):
    dist.append(np.sqrt(np.sum(np.multiply((test_images - clusters_kernel[i, :]), (test_images - clusters_kernel[i, :])))))
cluster_unlabel = np.argmin(dist)


print('cluster of test image:', cluster_unlabel, type(cluster_unlabel))

# knn
nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(unlabels_in_clusters_coded[cluster_unlabel])
indices = nbrs.kneighbors([test_images], return_distance=False)
print(indices)

# plot 10 nearest neighbour image within cluster to test image
for res_i in range(0,2):

    if res_i == 0:
        k_neighbour = unlabels_in_clusters_coded[cluster_unlabel][indices][0]
        print(k_neighbour.shape)
    else:
        k_neighbour = unlabels_in_clusters[cluster_unlabel][indices][0]
        print(k_neighbour.shape)

    # plot ten instance of nearest neighbours
    fig = plt.figure(figsize=(96, 96))
    columns = 10
    rows = 2

    for row in range(0, 2):
        if row == 0:
            img = test_images.reshape(96, 96)
            fig.add_subplot(rows, columns, 1)
            plt.imshow(img, cmap='gray')
            continue

        for col in range(0, 10):
            img = k_neighbour[col, :]
            print(img.shape)
            img = img.reshape(96, 96)
            fig.add_subplot(rows, columns, row * (10) + col + 1)
            plt.imshow(img, cmap='gray')

plt.show()
