import sqlite3
import json
import pandas as pd
import numpy
import random

con = sqlite3.connect('example.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS legal (url text, cookies integer, aviso integer, protección_de_datos integer, creacion integer, primary key (url))')
cur.execute('CREATE TABLE IF NOT EXISTS emails (id integer, total integer, phishing integer, cliclados integer, primary key (id))')
cur.execute('CREATE TABLE IF NOT EXISTS fechas (id integer, nombre text, fecha text, primary key (id), foreign key (nombre) references usuarios(nombre))')
cur.execute('CREATE TABLE IF NOT EXISTS ips (ip text, nombre text, primary key (ip), foreign key (nombre) references usuarios(nombre))')
cur.execute('CREATE TABLE IF NOT EXISTS usuarios (nombre text, telefono integer, contraseña text, provincia text, permisos text, emails integer, primary key (nombre), foreign key (emails) references emails(id))')
con.commit()

with open('legal.json') as file:
    data = json.load(file)

for element in range(len(data['legal'])):
    for web in data['legal'][element].keys():
        url = web
        cookies = data['legal'][element][web]['cookies']
        aviso = data['legal'][element][web]['aviso']
        proteccion = data['legal'][element][web]['proteccion_de_datos']
        creacion = data['legal'][element][web]['creacion']
        cur.execute('INSERT INTO legal VALUES (?, ?, ?, ?, ?)', (url, cookies, aviso, proteccion, creacion))

con.commit()

with open('users.json') as file:
    data = json.load(file)

id_fecha = 0
for element in range(len(data['usuarios'])):
    for nombre in data['usuarios'][element].keys():
        usuario = nombre
        telefono = data['usuarios'][element][nombre]['telefono']
        passwd = data['usuarios'][element][nombre]['contrasena']
        provincia = data['usuarios'][element][nombre]['provincia']
        permisos = data['usuarios'][element][nombre]['permisos']
        email = data['usuarios'][element][nombre]['emails']
        fechas = data['usuarios'][element][nombre]['fechas']
        ips = data['usuarios'][element][nombre]['ips']
        total = email['total']
        phising = email['phishing']
        clicados = email['cliclados']
        id = random.randint(1, 9999)
        cur.execute('INSERT INTO emails VALUES (?, ?, ?, ?)', (id, total, phising, clicados))
        for fecha in fechas:
            cur.execute('INSERT INTO fechas VALUES (?, ?, ?)', (id_fecha, usuario, fecha))
            id_fecha = id_fecha + 1
        for ip in ips:
            cur.execute('INSERT INTO ips VALUES (?, ?)', (ip, usuario))
        cur.execute('INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?)', (usuario, telefono, passwd, provincia, permisos, id))

con.commit()

#Fase de consultas
n_usuarios = pd.read_sql_query("SELECT DISTINCT COUNT(*) FROM usuarios", con)
print("El número de muestras es: ")
print(n_usuarios['COUNT(*)'][0])
n_fechas = pd.read_sql_query("SELECT COUNT(*) FROM fechas", con)
print("La media de inicios de sesión es:")
print(n_fechas['COUNT(*)'][0] / n_usuarios['COUNT(*)'][0])
print("La desviación de inicios de sesión es:")
print("continuara...")



n_mails = pd.read_sql_query("SELECT SUM(total) FROM emails", con)
print("La media de emails por usuarios es: ")
print(n_mails['SUM(total)'][0] / n_usuarios['COUNT(*)'][0])



con.close()
