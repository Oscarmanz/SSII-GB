import sqlite3
import json
import pandas as pd
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
        #cur.execute('INSERT INTO legal VALUES (?, ?, ?, ?, ?)', (url, cookies, aviso, proteccion, creacion))

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
        #cur.execute('INSERT INTO emails VALUES (?, ?, ?, ?)', (id, total, phising, clicados))
        #for fecha in fechas:
            #cur.execute('INSERT INTO fechas VALUES (?, ?, ?)', (id_fecha, usuario, fecha))
            #id_fecha = id_fecha + 1
        #for ip in ips:
            #cur.execute('INSERT INTO ips VALUES (?, ?)', (ip, usuario))
        #cur.execute('INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?)', (usuario, telefono, passwd, provincia, permisos, id))

con.commit()

# Fase de consultas

# Ejercicio 2
print("\n\n\nEJERCICIO 2\n")
n_usuarios = pd.read_sql_query("SELECT DISTINCT COUNT(*) FROM usuarios", con)
print("El número de muestras es: ")
print(n_usuarios['COUNT(*)'][0])
print("----------------------------------------")
l_fechas = pd.read_sql_query("SELECT COUNT(fecha) FROM fechas GROUP BY nombre", con)
print("La media de inicios de sesión es:")
print(l_fechas['COUNT(fecha)'].mean())
print("La desviación de inicios de sesión es:")
print(l_fechas['COUNT(fecha)'].std())
print("----------------------------------------")
l_ips = pd.read_sql_query("SELECT COUNT(ip) FROM ips GROUP BY nombre", con)
print("La media de ips por usuario es:")
print(l_ips['COUNT(ip)'].mean())
print("La desviación de ips es:")
print(l_ips['COUNT(ip)'].std())
print("----------------------------------------")
l_mails = pd.read_sql_query("SELECT total FROM emails", con)
print("La media de emails por usuarios es: ")
print(l_mails['total'].mean())
print("La desviación de emails es:")
print(l_mails['total'].std())
print("----------------------------------------")
print("El máximo número de inicios de sesión de un usuario es:")
print(l_fechas['COUNT(fecha)'].max())
print("El mínimo número de inicios de sesión de un usuario es:")
print(l_fechas['COUNT(fecha)'].min())
print("----------------------------------------")
print("El máximo número de emails recibidos es:")
print(l_mails['total'].max())
print("El mínimo número de emails recibidos es:")
print(l_mails['total'].min())

# Ejercicio 3
print("\n\n\nEJERCICIO 3\n")
e_permisos = pd.read_sql_query("SELECT u.permisos, SUM(e.phishing) FROM usuarios u join emails e ON u.emails = e.id GROUP BY u.permisos", con)
print("El número de phishings con permiso 0 es:", end=" ")
print(e_permisos['SUM(e.phishing)'][0])
print("El número de phishings con permiso 1 es:", end=" ")
print(e_permisos['SUM(e.phishing)'][1])
e_permisos2 = pd.read_sql_query("SELECT u.permisos, COUNT(e.phishing) FROM usuarios u join emails e ON u.emails = e.id WHERE (e.phishing = 0) GROUP BY u.permisos", con)
print("El número de valores ausentes por permiso es:")
print(e_permisos2)
e_permisos3_0 = pd.read_sql_query("SELECT phishing FROM usuarios u join emails e ON u.emails = e.id WHERE u.permisos = 0", con)
e_permisos3_1 = pd.read_sql_query("SELECT phishing FROM usuarios u join emails e ON u.emails = e.id WHERE u.permisos = 1", con)
print("La mediana de phishings con permiso 0 es:", end=" ")
print(e_permisos3_0['phishing'].median())
print("La mediana de phishings con permiso 1 es:", end=" ")
print(e_permisos3_1['phishing'].median())
print("La media de phishings con permiso 0 es:", end=" ")
print(e_permisos3_0['phishing'].mean())
print("La media de phishings con permiso 1 es:", end=" ")
print(e_permisos3_1['phishing'].mean())
print("La varianza de phishings con permiso 0 es:", end=" ")
print(e_permisos3_0['phishing'].var())
print("La varianza de phishings con permiso 1 es:", end=" ")
print(e_permisos3_1['phishing'].var())
print("El máximo de phishings con permiso 0 es:", end=" ")
print(e_permisos3_0['phishing'].max())
print("El mínimo de phishings con permiso 0 es:", end=" ")
print(e_permisos3_0['phishing'].min())
print("La máximo de phishings con permiso 1 es:", end=" ")
print(e_permisos3_1['phishing'].max())
print("La mínimo de phishings con permiso 1 es:", end=" ")
print(e_permisos3_1['phishing'].min())

print("-------------------------------------------")

e_emailm200 = pd.read_sql_query("SELECT SUM(phishing) FROM emails WHERE (total < 200)", con)
e_emailM200 = pd.read_sql_query("SELECT SUM(phishing) FROM emails WHERE (total >= 200)", con)
print("El número de observaciones para menos de 200 correos es:", end=" ")
print(e_emailm200['SUM(phishing)'][0])
print("El número de observaciones para igual o más de 200 correos es:", end=" ")
print(e_emailM200['SUM(phishing)'][0])
e_emailm200_2 = pd.read_sql_query("SELECT COUNT(phishing) FROM emails WHERE (total < 200 and phishing = 0)", con)
e_emailM200_2 = pd.read_sql_query("SELECT COUNT(phishing) FROM emails WHERE (total >= 200 and phishing = 0)", con)
print("El número de valores ausentes para menos de 200 correos es:", end=" ")
print(e_emailm200_2['COUNT(phishing)'][0])
print("El número de valores ausentes para igual o más de 200 correos es:", end=" ")
print(e_emailM200_2['COUNT(phishing)'][0])
e_emailm200_3 = pd.read_sql_query("SELECT phishing FROM emails WHERE (total < 200)", con)
e_emailM200_3 = pd.read_sql_query("SELECT phishing FROM emails WHERE (total >= 200)", con)
print("La mediana de phishings con menos de 200 emails es:", end=" ")
print(e_emailm200_3['phishing'].median())
print("La mediana de phishings con igual o más de 200 emails es:", end=" ")
print(e_emailM200_3['phishing'].median())
print("La media de phishings con menos de 200 emails es:", end=" ")
print(e_emailm200_3['phishing'].mean())
print("La media de phishings con igual o más de 200 emails es:", end=" ")
print(e_emailM200_3['phishing'].mean())
print("La varianza de phishings con menos de 200 es:", end=" ")
print(e_emailm200_3['phishing'].var())
print("La varianza de phishings con igual o más de 200 es:", end=" ")
print(e_emailM200_3['phishing'].var())
print("El máximo de phishings con menos de 200 emails es:", end=" ")
print(e_emailm200_3['phishing'].max())
print("El mínimo de phishings con menos de 200 emails es:", end=" ")
print(e_emailm200_3['phishing'].min())
print("El máximo de phishings con igual o más de 200 emails es:", end=" ")
print(e_emailM200_3['phishing'].max())
print("El máximo de phishings con igual o más de 200 emails es:", end=" ")
print(e_emailM200_3['phishing'].min())
con.close()
