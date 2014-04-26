from sklearn import tree
from sklearn import ensemble

def decision_tree_classifier(data, labels):
	clf = tree.DecisionTreeClassifier()
	clf.fit(data, labels)
	return clf

def random_forest_classifier(data, labels):
	clf = ensemble.RandomForestClassifier()
	clf.fit(data, labels)
	return clf

def extremely_random_forest_classifier(data, labels):
	clf = ensemble.ExtraTreesClassifier()
	clf.fit(data, labels)
	return clf

def adaboost_classifier(data, labels):
	clf = ensemble.AdaBoostClassifier()
	clf.fit(data, labels)
	return clf

def predict_using_classifier(classifier, test_data):
	return classifier.predict(test_data)

def accuracy(predictions, labels):
	correct = 0.0
	for index, prediction in enumerate(predictions):
		if prediction == labels[index]:
			correct+=1
	return correct/len(labels)

