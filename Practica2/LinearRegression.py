import graphviz
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn import tree
from subprocess import call
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import json
import pandas as pd
from sklearn.tree import export_graphviz


# Cargamos el json
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)
with open('users_IA_clases.json') as file:
    data = json.load(file)

#print(data['usuarios'][0]['usuario'])

users_X = []
users_Y = []
for i in range(len(data['usuarios'])):
    users_X.append([data['usuarios'][i]['emails_phishing_recibidos'], data['usuarios'][i]['emails_phishing_clicados']])
    users_Y.append(data['usuarios'][i]['vulnerable'])

# Separamos en datos para test y
limit = int(len(users_X)*0.6)

users_X_train = users_X[:limit]
users_X_test = users_X[limit:]

users_Y_train = users_Y[:limit]
users_Y_test = users_Y[limit:]

#####REGRESIÓN LINEAL#####
regrUsers = linear_model.LinearRegression()
# Entrenar modelo
regrUsers.fit(users_X_train, users_Y_train)
print(regrUsers.coef_)
# Hacemos predicciones
users_Y_pred = regrUsers.predict(users_X_test)
contCeros = 0
contUnos = 0
for i in range(len(users_Y_pred)):
    if(users_Y_pred[i] < 0.5):
        users_Y_pred[i] = 0
        contCeros += 1
    else:
        users_Y_pred[i] = 1
        contUnos += 1

print("Ha detectado ",contCeros," vulnerables y ",contUnos," no vulnerables")
#Calculamos accuracy
accuracy = int(accuracy_score(users_Y_test, users_Y_pred))
print("El accuracy es de: ", accuracy*100, "%")

# Gráfico regresión lineal
x = []
y = []
#m = regrUsers.coef_
m = r2_score(users_Y_test, users_Y_pred)
b = regrUsers.intercept_

for i in range(len(users_X_test)):
    x.append(users_X_test[i][1] / users_X_test[i][0])
    #y.append(x[i]*m + b)
    #y.append(b)

y = np.array(x)*m + b
plt.scatter(x, users_Y_test)
plt.plot(y, x)
plt.show()




#####DECISION TREE#####
#Creamos modelo del árbol
#clf_modelUsers = tree.DecisionTreeClassifier()
#clf_modelUsers.fit(users_X_train, users_Y_train)
#Gráfico árbol de decisión
#dot_data = tree.export_graphviz(clf_modelUsers, out_file=None)
#graph = graphviz.Source(dot_data)
#graph.render("users")
#dot_data = tree.export_graphviz(clf_modelUsers, out_file=None,
#                      feature_names=['recibidos', 'clicados'],
#                      class_names=['vulnerable', 'no vulnerable'],
#                     filled=True, rounded=True,
#                    special_characters=True)
#graph = graphviz.Source(dot_data)
#graph.render('test.gv', view=True).replace('\\', '/')


#####RANDOM FOREST#####
#clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
#clf.fit(users_X_train, users_Y_train)

#for i in range(len(clf.estimators_)):
#    estimator = clf.estimators_[i]
#    export_graphviz(estimator,
#                    out_file='tree.dot',
#                    #feature_names=iris.feature_names,
#                    #class_names=iris.target_names,
#                    rounded=True, proportion=False,
#                    precision=2, filled=True)
#    call(['dot', '-Tpng', 'tree.dot', '-o', 'tree'+str(i)+'.png', '-Gdpi=600'])



#Pseudocodigo solucion:
#array de [name,click, emails] y array de [0,1] con valor vulnerable o no
#predict devuelve array de valores con prob, luego recorrer con bucle y decir si esta por encima o debajo de 0,5
#error cuadratico medio no tiene sentido, mejor accuracy, pasarle array de predict y de valores correctos (test de y) y lo devuelve
#pintar la gráfica: eje y [0,1] eje x el array de probabilidades pa que pinte (pintar valores)