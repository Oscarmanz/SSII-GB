from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from sklearn.datasets import load_iris
from subprocess import call
import graphviz #https://graphviz.org/download/

#Split data
iris = load_iris()
X, y = iris.data, iris.target
clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clf.fit(X, y)
print(str(X[0]) + " " + str(y[0]))
print(clf.predict([X[0]]))

for i in range(len(clf.estimators_)):
    print(i)
    estimator = clf.estimators_[i]
    export_graphviz(estimator,
                    out_file='tree.dot',
                    feature_names=iris.feature_names,
                    class_names=iris.target_names,
                    rounded=True, proportion=False,
                    precision=2, filled=True)
    call(['dot', '-Tpng', 'tree.dot', '-o', 'tree'+str(i)+'.png', '-Gdpi=600'])