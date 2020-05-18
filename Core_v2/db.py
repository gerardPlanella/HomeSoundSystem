#!/usr/bin/python
import psycopg2 as pg
import random
import operator as op
import datetime
import events as eve

"""
IMPORTANT:
The IP address 188.166.9.142 references a remote server which is owned by Miquel
Saula. If any issue with the server is found contact Miquel Saula (miquel.saula@students.salle.url.edu)
or change the PSQL server to localhost or create a new one.
"""

#Postgre SQL credentials
SQL_HOST = '188.166.9.142'
SQL_DATABASE = 'homesoundsystemdb'
SQL_USERNAME = 'homesound'
SQL_PASSWORD = 'homesound1234'
SQL_PORT = 5432

# Classe que permet interactuar amb la base de dades al servidor remot
class HomeSoundSystemDB():
    def __init__(self):
        #Create a connection to the database with our credentials.
        self.conn = pg.connect(dbname=SQL_DATABASE, user=SQL_USERNAME, password=SQL_PASSWORD, host=SQL_HOST, port=SQL_PORT, sslmode="prefer")

    #Funció per a aliberar els recursos i tancar la connexió amb la DB
    def closeDB(self):
        self.conn.close()

    #Elimina tot el contingut de les taules de la base de dades i les torna a generar
    def resetTables(self):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()

        #Creem la taula Plant (la buidem si ja existia)
        cursor.execute("""  DROP TABLE IF EXISTS EventLog CASCADE;
                            CREATE TABLE EventLog (
                                location varchar(255),
                                time timeStamp,
                                type int,
                                power numeric,
                                PRIMARY KEY (location, time, type)
                            );""", vars=None)

        #Afegim els canvis realitzats a la base de dades real
        self.conn.commit()
        #Tanquem l'objecte
        cursor.close()

    #Afegeix un conjunt de informació falsa per finalitats de testing del sistema
    def addTestData(self):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()

        # Creem i executem la query per carregar les plantes de prova
        queryLogs = """INSERT INTO EventLog (location, time, type, power)
                        VALUES ('kitchen', %s, 1, .5);"""
        cursor.execute(queryLogs, (str(datetime.datetime.now()), ))

        # Guardem els canvis a la DB
        self.conn.commit()

        # Tanquem el cursor
        cursor.close()

    # Funció per pintar per pantalla tot el contingut de la taula indicada
    def printTable(self, name):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM %s;', (name, ))

        for row in cursor:
            print(list(row))
        cursor.close()

    def addLog(self, event):
        cursor = self.conn.cursor()

        queryLogs = """INSERT INTO EventLog (location, time, type, power)
                        VALUES (%s, %s, %s, %s);"""
        cursor.execute(queryLogs, (event.location, event.time, str(event.type), str(event.confidence), ))
        self.conn.commit()
        cursor.close()

    """
    Retorna la quantitat de vegades que ha succeit un event en el periode de temps definit a partir de (timestamp - period) fins timestamp, on period s'indica en segons.
    A més a més, es comprova també la quantitat de vegades de ha succeit en els n dies anteriors a la mateixa franja horaria (quantitat de dies definits per amountOfDays)

    This function returns the amount of times that a given event has happened in a period of time defined since the moment (timeStamp - period) until timeStamp, where period
    is given in seconds unit. Furthermore, is checked also the amount of times that the event has happened at the same time slot of the day, the n days before (where n is
    defined by amountOfDays).

    If the amount returned is equal to -1, an error may have happened while executing.
    """
    def eventsHappened(self, eventType, timeStamp, period, amountOfDays):
        cursor = self.conn.cursor()
        cursor.execute("""  SELECT COUNT(*) AS nEvents
                            FROM EventLog
                            WHERE
                                type = %s AND
                                MOD((%s - time), 24*3600) > %s AND
                                (%s - time) / (24*3600) <= %s;""", (str(eventType), str(timeStamp), str(period), str(timeStamp), str(amountOfDays), ))

        resultat = -1
        for row in cursor: resultat = int(row[0])

        return resultat

    def eventsHappenedInLocation(self, eventType, timeStamp, period, amountOfDays, location):
        cursor = self.conn.cursor()
        cursor.execute("""  SELECT COUNT(*) AS nEvents
                            FROM EventLog
                            WHERE
                                type = %s AND
                                MOD((%s - time), 24*3600) > %s AND
                                (%s - time) / (24*3600) <= %s AND
                                location like '%s';""", (str(eventType), str(timeStamp), str(period), str(timeStamp), str(amountOfDays), location, ))

        resultat = -1
        for row in cursor: resultat = int(row[0])

        return resultat

    def lastEventHappened(self, eventType):
        cursor = self.conn.cursor()
        cursor.execute("""  SELECT location, time, type
                            FROM EventLog
                            WHERE type = %s
                            ORDER BY time DESC
                            LIMIT 1;""", (str(eventType), ))

        resultat = eve.Event()
        for row in cursor:
            resultat.location = row[0]
            resultat.time = row[1]
            resultat.type = int(row[2])

        return resultat

    def lastEventHappenedInLocation(self, eventType, location):
        cursor = self.conn.cursor()
        cursor.execute("""  SELECT location, time, type
                            FROM EventLog
                            WHERE type = %s AND location = %s
                            ORDER BY time DESC
                            LIMIT 1;""", (str(eventType), location, ))

        resultat = eve.Event()
        for row in cursor:
            resultat.location = row[0]
            resultat.time = row[1]
            resultat.type = int(row[2])

        return resultat

    def mostFrequentEvent(self, timeStamp, period, amountOfDays):
        cursor = self.conn.cursor()
        cursor.execute("""  SELECT type, COUNT(*) AS nEvents
                            FROM EventLog
                            WHERE
                                MOD((%s - time), 24*3600) > %s AND
                                (%s - time) / (24*3600) <= %s
                            GROUP BY type
                            LIMIT 1;""", (str(timeStamp), str(period), str(timeStamp), str(amountOfDays), ))

        resultat = {"type": -1, "nEvents": -1}
        for row in cursor:
            resultat["type"] = row[0]
            resultat["nEvents"] = row[1]

        return resultat

    def mostFrequentEventInLocation(self, timeStamp, period, amountOfDays, location):
        cursor = self.conn.cursor()
        cursor.execute("""  SELECT type, COUNT(*) AS nEvents
                            FROM EventLog
                            WHERE
                                MOD((%s - time), 24*3600) > %s AND
                                (%s - time) / (24*3600) <= %s AND
                                location like '%s'
                            GROUP BY type
                            LIMIT 1;""", (str(timeStamp), str(period), str(timeStamp), str(amountOfDays), location, ))

        resultat = {"type": -1, "nEvents": -1}
        for row in cursor:
            resultat["type"] = row[0]
            resultat["nEvents"] = row[1]

        return resultat

    def getAllLogs(self):
        cursor = self.conn.cursor()
        cursor.execute("""  SELECT location, time, type
                            FROM EventLog;""", vars=None)

        resultat = []
        for row in cursor:
            event = eve.Event(int(row[0]), row[2])
            event.time = datetime(row[1])
            resultat.append(event)

        return resultat


"""
## Test Code to reset table to tests values

db = HomeSoundSystemDB()

db.resetTables()
db.addTestData()

db.closeDB()
"""
