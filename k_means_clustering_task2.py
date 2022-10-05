# -*- coding: utf-8 -*-
"""k_means_clustering_TASK2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TX1qSHeoHZXuDgqGvbr3CjddsIUF2rDf

##Importing the libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sklearn.metrics as sm
# %matplotlib inline

"""##Importing the dataset"""

iris = datasets.load_iris()
print(iris.data)

print(iris.target_names)

X = pd.DataFrame(iris.data,columns=['sepal length','sepal width','petal length','petal width'])
y = pd.DataFrame(iris.target,columns = ['species'])

X.head()

y.head()

"""##Exploratory Data Analysis"""

plt.figure(figsize=(16,5))
colors = np.array(['red', 'green', 'blue'])
iris_targets_legend = np.array(iris.target_names)
red_patch = mpatches.Patch(color='red', label='Setosa')
green_patch = mpatches.Patch(color='green', label='Versicolor')
blue_patch = mpatches.Patch(color='blue', label='Virginica')


plt.subplot(1, 2, 1)
plt.scatter(X['sepal length'], X['sepal width'], c=colors[y['species']])
plt.title('sepal length vs sepal width')
plt.legend(handles=[red_patch, green_patch, blue_patch])

plt.subplot(1,2,2)
plt.scatter(X['petal length'], X['petal width'], c= colors[y['species']])
plt.title('Petal Length vs Petal Width')
plt.legend(handles=[red_patch, green_patch, blue_patch])

#finding the optimum k value by WCSS graph
#it will create a elbow graph from that we will find the optimum k value

x = X.iloc[:, [0, 1, 2, 3]].values

from sklearn.cluster import KMeans
wcss = []

for i in range(1, 10):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', 
                    max_iter = 250, n_init = 10, random_state = 0)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)
    

plt.plot(range(1, 10), wcss)
plt.title('The elbow method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS') 
plt.show()

"""from the above graph we know that the optimum k value is 3. because on that side only the graph bends and tends towards 0.

##Model Tranining
"""

model = KMeans(n_clusters = 3, init = 'k-means++',max_iter = 250, n_init = 9, random_state = 42)
model.fit(x)

print(model.labels_)

print(model.cluster_centers_)

plt.figure(figsize=(16,5))

colors = np.array(['red', 'green', 'blue'])

pred_y = np.choose(model.labels_, [1, 0, 2]).astype(np.int64)

plt.subplot(1, 2, 1)
plt.scatter(X['petal length'], X['petal width'], c=colors[y['species']])
plt.title('Before classification')
plt.legend(handles=[red_patch, green_patch, blue_patch])

plt.subplot(1, 2, 2)
plt.scatter(X['petal length'], X['petal width'], c=colors[pred_y])
plt.title("Model's classification")
plt.legend(handles=[red_patch, green_patch, blue_patch])

"""##Performance Metrics"""

sm.confusion_matrix(pred_y, y['species'])

sm.accuracy_score(pred_y, y['species'])

target_names = ['setosa','versicolor','virginica']
print(sm.classification_report(pred_y,y['species'],target_names=target_names))