import graphviz
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn import tree
from subprocess import call, check_call
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import json
import pandas as pd
from sklearn.tree import export_graphviz, plot_tree

# Cargamos el json
with open('users_IA_clases.json') as file:
    data = json.load(file)

#print(data['usuarios'][0]['usuario'])

users_X = []
users_Y = []
for i in range(len(data['usuarios'])):
    users_X.append([data['usuarios'][i]['emails_phishing_recibidos'], data['usuarios'][i]['emails_phishing_clicados']])
    users_Y.append(data['usuarios'][i]['vulnerable'])

# Separamos en datos para test y
limit = int(len(users_X)*0.7)

users_X_train = users_X[:limit]
users_X_test = users_X[limit:]

users_Y_train = users_Y[:limit]
users_Y_test = users_Y[limit:]

#####REGRESIÓN LINEAL#####
regrUsers = linear_model.LinearRegression()
# Entrenar modelo
regrUsers.fit(users_X_train, users_Y_train)
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
print("El modelo de regresion lineal ha predicho:")
print(contCeros," vulnerables y ",contUnos," no vulnerables")
#Calculamos accuracy
accuracy = accuracy_score(users_Y_test, users_Y_pred)
print("El accuracy es de: ", accuracy*100, "%\n")

# Gráfico regresión lineal
x = []
y = []
m = r2_score(users_Y_test, users_Y_pred)
b = regrUsers.intercept_

for i in range(len(users_X_test)):
    if (users_X_test[i][0] != 0):
        x.append(users_X_test[i][1] / users_X_test[i][0])
    else:
        x.append(0)


y = np.array(x)*m + b
plt.scatter(x, users_Y_test)
plt.plot(y, x)
plt.savefig("regresionLineal.png")
plt.show()

with open('users_IA_predecir.json') as file:
    data = json.load(file)

users_X_predict = []

for i in range(len(data['usuarios'])):
    users_X_predict.append([data['usuarios'][i]['emails_phishing_recibidos'], data['usuarios'][i]['emails_phishing_clicados']])

users_y_predict = regrUsers.predict(users_X_predict)
contCeros = 0
contUnos = 0
for i in range(len(users_y_predict)):
    if(users_y_predict[i] < 0.5):
        users_y_predict[i] = 0
        contCeros += 1
    else:
        users_y_predict[i] = 1
        contUnos += 1

print("El modelo de regresion lineal sobre los datos reales ha predicho:")
print(contCeros," vulnerables y ",contUnos," no vulnerables")
print("-------------------------------------------------------------------------------------------")

#####DECISION TREE#####
#Creamos modelo del árbol
clf_modelUsers = tree.DecisionTreeClassifier()
clf_modelUsers.fit(users_X_train, users_Y_train)

# Hacemos predicciones
users_Y_pred = clf_modelUsers.predict(users_X_test)
contCeros = 0
contUnos = 0
for i in range(len(users_Y_pred)):
    if(users_Y_pred[i] < 0.5):
        users_Y_pred[i] = 0
        contCeros += 1
    else:
        users_Y_pred[i] = 1
        contUnos += 1
print("El modelo de arbol de decisión ha predicho:")
print(contCeros," vulnerables y ",contUnos," no vulnerables")
#Calculamos accuracy
accuracy = accuracy_score(users_Y_test, users_Y_pred)
print("El accuracy es de: ", accuracy*100, "%\n")

#Gráfico árbol de decisión
fig, ax = plt.subplots(figsize=(12, 5))
print(f"Profundidad del árbol: {clf_modelUsers.get_depth()}")
print(f"Número de nodos terminales: {clf_modelUsers.get_n_leaves()}\n")
plot = plot_tree(
            decision_tree = clf_modelUsers,
            feature_names = ['clicados', 'recibidos'],
            class_names   = ['vulnerable', 'no vulnerable'],
            filled        = True,
            impurity      = False,
            fontsize      = 9,
            precision     = 4,
            ax            = ax
       )
plt.savefig("decisionTree.png")
plt.show()

#Resultados reales
users_y_predict = clf_modelUsers.predict(users_X_predict)
contCeros = 0
contUnos = 0
for i in range(len(users_y_predict)):
    if(users_y_predict[i] < 0.5):
        users_y_predict[i] = 0
        contCeros += 1
    else:
        users_y_predict[i] = 1
        contUnos += 1

print("El modelo de arbol de decisión sobre los datos reales ha predicho:")
print(contCeros," vulnerables y ",contUnos," no vulnerables")
print("-------------------------------------------------------------------------------------------")




#####RANDOM FOREST#####
clfRandomForest = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clfRandomForest.fit(users_X_train, users_Y_train)

# Hacemos predicciones
users_Y_pred = clfRandomForest.predict(users_X_test)
contCeros = 0
contUnos = 0
for i in range(len(users_Y_pred)):
    if(users_Y_pred[i] < 0.5):
        users_Y_pred[i] = 0
        contCeros += 1
    else:
        users_Y_pred[i] = 1
        contUnos += 1
print("El modelo de random forest ha predicho:")
print(contCeros," vulnerables y ",contUnos," no vulnerables")
#Calculamos accuracy
accuracy = accuracy_score(users_Y_test, users_Y_pred)
print("El accuracy es de: ", accuracy*100, "%\n")

#Graficos random forest
for i in range(len(clfRandomForest.estimators_)):
    fig, ax = plt.subplots(figsize=(12, 5))
    plot = plot_tree(
        decision_tree=clfRandomForest.estimators_[i],
        feature_names=['clicados', 'recibidos'],
        class_names=['vulnerable', 'no vulnerable'],
        filled=True,
        impurity=False,
        fontsize=9,
        precision=4,
        ax=ax
    )
    plt.savefig("randomForestTrees/decisionTree" + str(i) + ".png")
    plt.show()


#Resultados reales
users_y_predict = clfRandomForest.predict(users_X_predict)
contCeros = 0
contUnos = 0
for i in range(len(users_y_predict)):
    if(users_y_predict[i] < 0.5):
        users_y_predict[i] = 0
        contCeros += 1
    else:
        users_y_predict[i] = 1
        contUnos += 1

print("El modelo de random forest sobre los datos reales ha predicho:")
print(contCeros," vulnerables y ",contUnos," no vulnerables")
print("-------------------------------------------------------------------------------------------")