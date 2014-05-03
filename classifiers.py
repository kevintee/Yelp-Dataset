from sklearn import tree, ensemble, neighbors, naive_bayes, multiclass, svm, cross_validation, grid_search, lda, qda

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

def k_nearest_neighbor_classifier(data, labels):
	clf = neighbors.KNeighborsClassifier()
	clf.fit(data, labels)
	return clf

def gaussian_naive_bayes_classifier(data, labels):
	clf = naive_bayes.GaussianNB()
	clf.fit(data, labels)
	return clf

def one_vs_rest_classifier(data, labels):
	clf = multiclass.OneVsRestClassifier(svm.LinearSVC())
	clf.fit(data, labels)
	return clf

def one_vs_one_classifier(data, labels):
	clf = multiclass.OneVsOneClassifier(svm.LinearSVC())
	clf.fit(data, labels)
	return clf

def LDA_classifer(data, labels):
    clf = lda.LDA()
    clf.fit(data, labels)
    return clf

def QDA_classifer(data, labels):
    clf = qda.QDA()
    clf.fit(data, labels)
    return clf

def cross_validate(classifier, data, labels):
	scores = cross_validation.cross_val_score(classifier, data, labels, cv=5)
	return scores

def grid_srch(classifier, data, labels, parameters):
	clf = grid_search.GridSearchCV(classifier, parameters)
	clf.fit(data, labels)
	return clf

def prediction_confidence(classifier, test_data):
	return classifier.predict_proba(test_data)

def predict_using_classifier(classifier, test_data):
	return classifier.predict(test_data)

def accuracy(predictions, labels):
    return sklearn.metrics.accuracy_score(predictions, labels)
