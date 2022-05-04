import json

from sklearn import tree
from sklearn.datasets import load_iris
import graphviz #https://graphviz.org/download/

#Split data
with open('users_IA_clases.json') as file:
    data = json.load(file)
users_X_caracteristicas = []
for element in range(len(data['usuarios'])):
        users_X_caracteristicas.append([data['usuarios'][element]['emails_phishing_recibidos'], data['usuarios'][element]['emails_phishing_clicados']])
users_Y_vuln = []
for element in range(len(data['usuarios'])):
        users_Y_vuln.append([data['usuarios'][element]['vulnerable']])

clfUsers = tree.DecisionTreeClassifier()
clfUsers = clfUsers.fit(users_X_caracteristicas, users_Y_vuln)
#Predict

clf_modelUsers = tree.DecisionTreeClassifier()
clf_modelUsers.fit(users_X_caracteristicas, users_Y_vuln)
#Print plot
dot_data = tree.export_graphviz(clfUsers, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("users")
dot_data = tree.export_graphviz(clfUsers, out_file=None,
                      feature_names=['recibidos', 'clicados'],
                      class_names=['vulnerable', 'no vulnerable'],
                     filled=True, rounded=True,
                    special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('test.gv', view=True).replace('\\', '/')
