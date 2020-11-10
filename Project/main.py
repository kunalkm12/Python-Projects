# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:15:54 2020

@author: Kk
"""
#setwd("C:/Users/kunal/Desktop/Buffalo/Python/Project")
import os
import re
from IPython.display import display, HTML
import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
os.chdir("C:/Users/kunal/Desktop/Buffalo/Python/Project")

def create_connection(db_file, delete_db = False):
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn

def create_database(dataset_filename):
    conn = create_connection('C:/Users/kunal/Desktop/Buffalo/Python/Project/database.db')
    cur = conn.cursor()

    with conn:
        drop = "DROP TABLE IF EXISTS maindata"
        cur.execute(drop)

    #####
    ### MAIN DATA TABLE
    #####

    table = """CREATE TABLE maindata (
                    CaseNumber VARCHAR NOT NULL PRIMARY KEY,
                    Dat DATE,
                    Sex VARCHAR,
                    Race VARCHAR,
                    Age INT,
                    Residence_City VARCHAR,
                    Residence_State VARCHAR,
                    Residence_County VARCHAR,
                    Death_City VARCHAR,
                    Death_State VARCHAR,
                    Death_County VARCHAR,
                    Location VARCHAR,
                    DescriptionofInjury VARCHAR,
                    InjuryPlace VARCHAR,
                    ImmediateCause VARCHAR,
                    Heroin CHAR,
                    Cocaine CHAR,
                    Fentanyl CHAR,
                    Oxycodone CHAR,
                    Oxymorphone CHAR,
                    EtOH CHAR,
                    Hydrocodone CHAR,
                    Benzodiazepine CHAR,
                    Methadone CHAR,
                    Amphet CHAR,
                    Tramad CHAR,
                    Morphine_not_heroin CHAR,
                    Other VARCHAR,
                    Any_Opioid CHAR,
                    MannerofDeath VARCHAR,
                    AmendedMannerofDeath VARCHAR,
                    DeathLoc VARCHAR
                    )"""
    with conn:
        cur.execute(table)

    #####
    ### Direct Insertion from csv
    #####
    with open(dataset_filename, 'r') as f:
        reader = csv.reader(f)
        data = next(reader)
        query = 'INSERT OR IGNORE INTO maindata values ({0})'
        query = query.format(','.join('?' * len(data)))
        #cur.execute(query, data)
        for data in reader:
            cur.execute(query, data)

    #####
    ### Demographic table
    #####
    with conn:
        drop2 = "DROP TABLE IF EXISTS Demographic"
        cur.execute(drop2)

    table2 = """CREATE TABLE Demographic(
                CaseNumber VARCHAR NOT NULL,
                Dat DATE,
                Sex CHAR,
                Race VARCHAR,
                Age INT
                )"""
    with conn:
        cur.execute(table2)

    ### Insertion
    with conn:
        query2 = "SELECT CaseNumber, Dat, Sex, Race, Age FROM maindata"
        cur.execute(query2)
        ls = cur.fetchall()

    ### Manipulating Sex column
    lis = []
    for i in ls:
        if i[2] == 'Male':
            temp = list(i)
            temp[2] = 'M'
            mod = tuple(temp)
            lis.append(mod)
        elif i[2] == 'Female':
            temp = list(i)
            temp[2] = 'F'
            mod = tuple(temp)
            lis.append(mod)
        ### Converting non-binaries to male
        else:
            temp = list(i)
            temp[2] = 'M'
            mod = tuple(temp)
            lis.append(mod)

    ### Manipulating Race column
    final = []
    for i in lis:
        if i[3] == None:
            app = (i[0],i[1],i[2],'White',i[4])
            final.append(app)
        else:
            llist = i[3].split(',')
            if len(llist) == 1:
                final.append(i)
            else:
                for j in range(0,len(llist)):
                    app = (i[0],i[1],i[2],llist[j],i[4])
                    final.append(app)

    ### Insertion into table
    with conn:
        for i in final:
            transfer = "INSERT INTO Demographic VALUES(?,?,?,?,?)"
            cur.execute(transfer,i)

        ### Saving table as csv
        sel = "SELECT * FROM Demographic"
        cur.execute(sel)
        with open('Demographic.csv','w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cur.fetchall())

    #####
    ### Drug Table
    #####
    with conn:
        drop3 = "DROP TABLE IF EXISTS Drugdata"
        cur.execute(drop3)

    table3 = """CREATE TABLE Drugdata(
                CaseNumber VARCHAR NOT NULL,
                Drugset VARCHAR(13),
                Other VARCHAR,
                FOREIGN KEY (CaseNumber) REFERENCES maindata(CaseNumber))"""

    with conn:
        cur.execute(table3)

    ### Insertion
    query3 = """SELECT CaseNumber, Heroin, Cocaine, Fentanyl, Oxycodone,
                Oxymorphone, EtOH, Hydrocodone, Benzodiazepine,
                Methadone, Amphet, Tramad, Morphine_not_heroin,
                Any_Opioid, Other FROM maindata"""
    cur.execute(query3)
    rs = cur.fetchall()

    final = []

    ### Populating bitsets
    for i in rs:
        bits = ""
        for j in range(1,(len(i)-1)):
            if i[j] == 'Y':
                bits = bits+"1"
            else:
                bits = bits+"0"
        final.append((i[0],bits,i[len(i)-1]))

    ### Insertion into table
    with conn:
        for i in final:
            transfer = "INSERT INTO Drugdata VALUES (?,?,?)"
            cur.execute(transfer, i)

        ### Saving table as csv
        sel = "SELECT * FROM Drugdata"
        cur.execute(sel)
        with open('Drugdata.csv','w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cur.fetchall())


    #####
    ### Geographic table
    #####
    drop4 = "DROP TABLE IF EXISTS GeographicData"
    with conn:
        cur.execute(drop4)

    table4 = """CREATE TABLE GeographicData (
                CaseNumber VARCHAR NOT NULL,
                Dat Date,
                Residence_City VARCHAR,
                Residence_County VARCHAR,
                Residence_State VARCHAR,
                Death_City VARCHAR,
                Death_County VARCHAR,
                Death_State VARCHAR,
                DeathCoordinates VARCHAR,
                FOREIGN KEY (CaseNumber) REFERENCES maindata(CaseNumber))"""
    with conn:
        cur.execute(table4)

    ### Insertion
    query4 = """SELECT CaseNumber, Dat, Residence_City, Residence_County,
                Residence_State, Death_City, Death_County, Death_State,
                DeathLoc FROM maindata"""
    cur.execute(query4)
    rs = cur.fetchall()

    ### Cleaning Data
    final = []
    for i in rs:
        ls = list(i)

        ### If Residence_State missing, ignore observation
        if ls[4] != "":
            state = ls[4]
        else:
            state = "CT"

        ### Isolating death city, state and coordinates from data
        loc = ls[8]
        stcoor = ""
        coor = ""
        city = ""
        for j in range(0,len(loc)):
            if loc[j] == ',':
                stcoor = loc[j+2:len(loc)]
                break
            else:
                city = city + loc[j]

        ### Isolating coordinates from stcoor
        for k in range(0,len(stcoor)):
            if stcoor[k] == '(':
                coor = stcoor[k:len(stcoor)]
                break

        city = city.strip()

        final.append((ls[0], ls[1], ls[2], ls[3], state, city, ls[6], 'CT', coor))

    ### Insertion into table
    with conn:
        for i in final:
            transfer = "INSERT INTO GeographicData VALUES (?,?,?,?,?,?,?,?,?)"
            cur.execute(transfer, i)

        ### Saving table as csv
        sel = "SELECT * FROM GeographicData"
        cur.execute(sel)
        with open('Geographicdata.csv','w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cur.fetchall())

create_database('test.csv')



def graphs_demographic(db_name):
    conn = create_connection(db_name)
    cur = conn.cursor()

    ### Accessing table
    tab = "SELECT * FROM Demographic"
    cur.execute(tab)
    rs = cur.fetchall()

    ### Converting to a data frame
    df = pd.DataFrame(rs, columns = ['CaseNumber', 'Date', 'Sex', 'Race', 'Age'])

graphs_demographic('database.db')




def graphs_drugdata(db_name):
    conn = create_connection(db_name)
    cur = conn.cursor()

    ### Accessing table
    tab = "SELECT * FROM Drugdata"
    cur.execute(tab)
    rs = cur.fetchall()

    ### Converting to a data frame
    df = pd.DataFrame(rs, columns = ['CaseNumber', 'Drugset', 'Other'])

graphs_drugdata('database.db')




def graphs_geographic(db_name):
    conn = create_connection(db_name)
    cur = conn.cursor()

    ### Accessing table
    tab = "SELECT * FROM GeographicData"
    cur.execute(tab)
    rs = cur.fetchall()

    ### Converting to a data frame
    df = pd.DataFrame(rs, columns = ['CaseNumber', 'Date', 'Residence_City', 'Residence_County', 'Residence_State', 'Death_City', 'Death_County', 'Death_State', 'DeathCoordinates'])

graphs_geographic('database.db')
