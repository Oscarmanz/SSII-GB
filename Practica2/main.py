import sqlite3

import pandas as pd
from flask import Flask
from flask import render_template
from flask import request
import requests
from json2html import *


import json
import plotly.graph_objects as go

app = Flask(__name__)


@app.route('/')
def main():
   return render_template('main.html')
@app.route('/usC')
def return_users():
   return render_template('topUsersCrit.html')
@app.route('/wIn')
def return_webs():
   return render_template('pagsVul.html')
@app.route('/vt10')
def return_vuln():
   #Recuperamos el texto de la pagina y lo pasamos a JSON
   url = requests.get("https://cve.circl.lu/api/last/10")
   text = url.text
   data = json.loads(text)
   #Para acceder a un dato concreto data[elemento]['campo'] -> data[0]['Modified']
   #Lo parseamos para que se vea en una tabla
   scan0utput = json2html.convert(json=data)
   #Devolvemos la tabla
   return render_template('top10vuln.html', text=scan0utput)

@app.route('/opcional', methods=["GET", "POST"])
def opcional():
   dominio = request.form['url']
   dominio_total = "https://urlscan.io/api/v1/search/?q=domain:" + dominio
   print(dominio_total)
   url = requests.get(dominio_total)
   text = url.text
   data = json.loads(text)
   scan0utput = json2html.convert(json=data)
   return render_template('opcional.html', text=scan0utput)


@app.route('/infoUrl')
def infoUrl():
   return render_template('infoUrl.html')

if __name__ == '__main__':
   app.run(debug = True)

@app.route('/critUsers', methods=["GET", "POST"])
def usuarios_criticos():
   num = request.form['numero']
   opcion = request.form['opcion']
   con = sqlite3.connect('bdSqlLite.db')
   cur = con.cursor()
   cont = pd.read_sql_query("SELECT contraseña FROM usuarios", con)
   cont_ponz = pd.DataFrame(columns=['cont'])
   cont_ponz.loc[0] = [cont['contraseña'][2]]
   cont_ponz.loc[1] = [cont['contraseña'][3]]
   cont_ponz.loc[2] = [cont['contraseña'][6]]
   cont_ponz.loc[3] = [cont['contraseña'][7]]
   cont_ponz.loc[4] = [cont['contraseña'][8]]
   cont_ponz.loc[5] = [cont['contraseña'][11]]
   cont_ponz.loc[6] = [cont['contraseña'][12]]
   cont_ponz.loc[7] = [cont['contraseña'][14]]
   cont_ponz.loc[8] = [cont['contraseña'][19]]
   cont_ponz.loc[9] = [cont['contraseña'][22]]
   cont_ponz.loc[10] = [cont['contraseña'][25]]
   cont_ponz.loc[11] = [cont['contraseña'][26]]
   cont_ponz.loc[12] = [cont['contraseña'][27]]
   cont_ponz.loc[13] = [cont['contraseña'][29]]

   usuarios_inseguros = pd.DataFrame(columns=['nombre', 'total', 'phishing', 'clicados'])
   for i in range(len(cont_ponz['cont'])):
      cur.execute('SELECT nombre, total, phishing, cliclados FROM usuarios u JOIN emails e ON u.emails = e.id WHERE contraseña = ?', [cont_ponz['cont'][i]])
      usuarios_inseguros.loc[i] = cur.fetchone()

   usuarios_inseguros['prob_pincharSpam'] = round(usuarios_inseguros['clicados'] / usuarios_inseguros['phishing'], 4) * 100
   usuarios_inseguros = usuarios_inseguros.fillna(0)

   for i in range(len(usuarios_inseguros['nombre'])):
      if(opcion == "Menos del 50% de spam clicado" and usuarios_inseguros.loc[i]['prob_pincharSpam'] > 50):
         usuarios_inseguros = usuarios_inseguros.drop(index=i)
      elif((opcion == "Más del 50% de spam clicado" and usuarios_inseguros.loc[i]['prob_pincharSpam'] <= 50)):
         usuarios_inseguros = usuarios_inseguros.drop(index=i)

   usuarios_inseguros = usuarios_inseguros.sort_values('prob_pincharSpam', ascending=False)
   usuarios_insegurosTopX = usuarios_inseguros.head(int(num))
   usuarios_insegurosTopX.reset_index(drop=True, inplace=True)

   fig = go.Figure(
      data=[go.Bar(x=usuarios_insegurosTopX['nombre'], y=usuarios_insegurosTopX['prob_pincharSpam'])],
      layout_title_text="Figura"
   )
   import plotly
   a = plotly.utils.PlotlyJSONEncoder
   graphJSON = json.dumps(fig, cls=a)
   con.close()
   return render_template('topUsersCrit.html', graphJSON=graphJSON)

@app.route('/critPags', methods=["GET", "POST"])
def webs_criticas():
   con = sqlite3.connect('bdSqlLite.db')
   cur = con.cursor()
   num = request.form['numero']

   cur.execute('SELECT url, cookies, aviso, protección_de_datos FROM legal')
   aux = cur.fetchall()
   webs_inseg = pd.DataFrame(aux, columns=['url', 'cookies', 'aviso', 'proteccion'])
   webs_inseg['n_desact'] = webs_inseg['cookies'] + webs_inseg['aviso'] + webs_inseg['proteccion']
   webs_inseg = webs_inseg.sort_values('n_desact', ascending=True)
   webs_insegTopX = webs_inseg.head(int(num))

   fig = go.Figure(
         data=[go.Bar(x=webs_insegTopX['url'], y=webs_insegTopX['n_desact'])],
         layout_title_text="Figura"
      )
   import plotly
   a = plotly.utils.PlotlyJSONEncoder
   graphJSON = json.dumps(fig, cls=a)
   con.close()
   return render_template('pagsVul.html', graphJSON=graphJSON)
