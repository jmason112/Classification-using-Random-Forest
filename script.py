#!/usr/bin/env python3


import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import classification_report, confusion_matrix
import graphviz

# Read the data from the dataset.csv file
data = pd.read_csv('dataset.csv')

# Drop the MD5 hash and label columns
features_only = data.drop(['MD5', 'label'], axis=1)

# Separate the features (X) and the target (y)
X = features_only.drop('Target', axis=1)
y = features_only['Target']

# Split the data into training and test sets (50% for training)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.5, random_state=42)

# Calculate the variance threshold
selector = VarianceThreshold(threshold=(0.2 * (1 - 0.2)))
selector.fit_transform(X_train)

# Get the indices of the selected features
selected_features = X_train.columns[selector.get_support()]

# Modify the X_train and X_test datasets to select only the filtered features
X_train = X_train[selected_features]
X_test = X_test[selected_features]

# Create and train a decision tree classifier with criterion=entropy
clf = DecisionTreeClassifier(criterion='entropy')
clf.fit(X_train, y_train)

# Predict the output
y_pred = clf.predict(X_test)

# Generate a classification report and confusion matrix
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save the decision tree as an image
dot_data = export_graphviz(clf, out_file=None, feature_names=selected_features, class_names=['benign', 'malware'], filled=True, rounded=True, special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("classifier")
