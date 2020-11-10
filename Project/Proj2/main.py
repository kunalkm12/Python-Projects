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

    #Plotting the drug overdose cases among the top 5 races.
    tab = "Select race, count(*) as count from Demographic where Race != "" group by race order by count desc Limit 5;"
    cur.execute(tab)
    rs = cur.fetchall()

    ### Converting to a data frame
    import matplotlib.pyplot as plt
    lst_race=[]
    lst_count=[]

    for ele in rs:
        lst_race.append(ele[0])
        lst_count.append(ele[1])

    # showing plot
    plt.figure(figsize=(12, 6))
    plt.barh(lst_race, lst_count, 0.45, color='black')
    plt.grid()
    plt.show()

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

###Plotting the data












def graphs_demographic(db_name):
    conn = create_connection(db_name)
    cur = conn.cursor()

    print('\n')
    print('Plot 1:')
    print('\n')

    ### Plotting the drug overdose cases among the top 5 races.
    tab = "SELECT RACE, COUNT(*) AS Count FROM Demographic GROUP BY Race ORDER BY count DESC Limit 5;"
    cur.execute(tab)
    rs = cur.fetchall()

    ### Converting to a data frame and lists of race and count
    df = pd.DataFrame(rs, columns = ['Race', 'Count'])
    lst_race=[]
    lst_count=[]

    for ele in rs:
        lst_race.append(ele[0])
        lst_count.append(ele[1])

    ### Showing plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set(xlabel='Count of Cases', ylabel='Race', title='Accidental Drug related Deaths by Race')
    plt.barh(lst_race, lst_count, 0.45, color='black')
    plt.grid()
    plt.show()


    print('\n')
    print('Plot 2:')
    print('\n')


    ### Plotting total overdose cases against time in years
    tab = "select Dat from Demographic"
    cur.execute(tab)
    rs = cur.fetchall()
    years = ['2012', '2013', '2014', '2015', '2016', '2017']
    years_count = []
    lst=[]

    for i in rs:
        date = i[0].split('/')
        if len(date) == 3:
            lst.append(date[2])

    for j in years:
        years_count.append(lst.count(str(j)))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(years, years_count, color='red')
    ax.set(xlabel='Time', ylabel='Count', title='Overdose cases over Years')
    ax.grid()
    plt.show()


    print('\n')
    print('Plot 3:')
    print('\n')


    ### Scatter plot for total number of deaths between different age groups
    sql_statement = "SELECT AGE, COUNT(*) AS Count FROM Demographic WHERE Age != '' GROUP BY Age"
    df = pd.read_sql_query(sql_statement, conn)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set(xlabel='Count of Cases', ylabel='Age', title='Accidental Drug related Deaths for different age groups')
    plt.scatter(df['Age'], df['Count'], 20, color='blue')
    plt.grid()
    plt.show()
















#Plotting total overdose cases against time in years




##scatter plot for total number of deaths between different age groups
##Observe that most of the cases are in the age group range of 25-55





##Plot to show the geographical distribution of cases in few cities
##
import chart_studio.plotly as py
import plotly.graph_objects as go
import pandas as pd

db_name = 'drug_deaths.db'
conn = create_connection(db_name)

sql_statement = "select Residence_State, count(*) as count, DeathLoc from maindata where Residence_State != '' group by Residence_State;"
df = pd.read_sql_query(sql_statement, conn)

lst=[]
for i,row in df.iterrows():
    loc = row.DeathLoc
    loc_lst = loc.split('(')
    loc_lst = loc_lst[1].split(',')
    lon = loc_lst[1].split(')')
    lst.append((row['Residence_State'], row['count'], loc_lst[0], lon[0].strip(), row['Residence_State']+' State Data'))

df = pd.DataFrame(lst, columns=['Residence_State', 'count', 'lat', 'lon', 'text'])

df['text'] = df['Residence_State'] + '<br> ' + (df['count']).astype(str)+' case(s)'
limits = [(0,2),(3,10),(11,50),(21,50),(50,2000)]
colors = ["royalblue","crimson","lightseagreen","orange","green"]
cities = []
scale = 5000

fig = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['count']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))

fig.update_layout(
        title_text = 'US city drug overdose',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)',
        )
    )

fig.show()

## To find out the top 10 drugsets responsible for overdose deaths
## Drugset Order --> Heroin, Cocaine, Fentanyl, Oxycodone,Oxymorphone, EtOH, Hydrocodone, Benzodiazepine, Methadone, Amphet,
## Tramad, Morphine_not_heroin, Any_Opioid

db_name = 'drug_deaths.db'
conn = create_connection(db_name)

### Accessing table
sql_statement = "select Drugset,count(*) as TotalCases from Drugdata group by Drugset order by TotalCases desc limit 11;"
df = pd.read_sql_query(sql_statement, conn)
display(df)

labels = ['Heroin', 'Cocaine', 'Heroin and Fentanyl', 'Heroin and Cocaine', 'Fentanyl', 'Heroin and Any_Opioid', 'Heroin and EtOH', 'Heroin, Cocaine and Fentanyl', 'Heroin and Benzodiazepine', 'Oxycodone']
sizes = [414, 192, 177, 169, 160, 125, 108, 92, 72, 67]
explode = (0.15, 0.15, 0, 0, 0.15, 0, 0, 0, 0, 0)

fig1, ax1 = plt.subplots(figsize=(12, 7))
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
ax1.axis('equal')

plt.show()


#Linear Regression analysis

    # dump = "SELECT * FROM Drugdata"
    # cur.execute(dump)
    # table1_rows = cur.fetchall()

import pandas as pd
rawdata = pd.read_csv("https://eas503.ccr.buffalo.edu/user/elyselev/edit/Drug_Deaths_Analysis/test.csv")
rawdata

#Relationships: Age freq per drug, Mixed drug relationships

r1=rawdata[['CaseNumber,''Age','Sex','Race','Heroin','Cocaine','Fentanyl','Oxycodone','Oxymorphone','EtOH','Hydrocodone','Benzodiazepine','Methadone','Amphet','Tramad','Morphine (not heroin)']]

HeroinAges=[]
CocainAges=[]
FentanylAges=[]
OxycodoneAges=[]
OxymorphoneAges=[]
EtOHAges=[]
HydrocodoneAges=[]
BenzodiazepineAges=[]
MethadoneAges=[]
AmphetAges=[]
TramadAges=[]
MorphineAges=[]

Mixed=[]
Mixed2=[]

        for line in r1:
        num_of_drugs=0
        lsofdrugs=[]
        for ele in line:
            if ele[4]= TRUE:   #Did they die from heroin
                HeroinAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Heroin")
            elif ele[5]= TRUE:
                CocainAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Cocain")
            elif ele[6]= TRUE:
                FentanylAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Fentanyl")
            elif ele[7]= TRUE:
                OxycodoneAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Oxycodone")
            elif ele[8]= TRUE:
                OxymorphoneAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Oxymorphone")
            elif ele[9]= TRUE:
                EtOHAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("EtOH")
            elif ele[10]= TRUE:
                HydrocodoneAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Hydrocodone")
            elif ele[12]= TRUE:
                BenzodiazepineAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Benzodiazepine")
            elif ele[12]= TRUE:
                MethadoneAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Methadone")
            elif ele[13]= TRUE:
                AmphetAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Amphet")
            elif ele[14]= TRUE:
                TramadAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Tramad")
            elif ele[15]= 'MORPHINE' or 'MORPH':
                MorphineAges.append(ele[1])
                num_of_drugs=+1
                lsofdrugs.append("Morphine")

            if num_of_drugs>= 2:
                Mixed.append('ele[0]':{ele[1],num_of_drugs})

    agelist=(HeroinAges,CocainAges,FentanylAges,OxycodoneAges,OxymorphoneAges,EtOHAges,HydrocodoneAges,BenzodiazepineAges,MethadoneAges,AmphetAges, TramadAges, MorphineAges)

for i in agelist:
    df = pd.DataFrame({'freq': i })
    df.groupby('freq', as_index=False).size().plot(kind='bar')
    plt.show()

#scatter plot of number of drugs taken and age of the person

import matplotlib.pyplot as plt

colors = list("rgbcmyk")

for data_dict in Mixed.values():
   x = data_dict.keys()
   y = data_dict.values()
   plt.scatter(x,y,color=colors.pop())

plt.show()


#Most common cities of Residence Death


#Associate rule mining/Apriori
#1: Association between drugs
#2: Association between race, age, gender, and drug

#MAKE 2 TABLES:
#.  -One of JUST drugs, with the binary "Y" (Just_Drugs_from_original.csv)
#.  -One of Age(binned),race(white is 1, 0 is other?),Gender(binary), and drugs (other)   (Age_race_gend_bi.csv)


#JUST DRUG RELATIONS ASSOCIATED
conn = create_connection('TestDrug.db')
sql_statement="SELECT Heroin,Cocaine,Fentanyl,Oxycodone,Oxymorphone,EtOH,Hydrocodone,Benzodiazepine,Methadone,Amphet,Tramad,Morphine_not_heroin FROM maindata"
df = pd.read_sql_query(sql_statement, conn)
display(df)

records = []
for i in range(0, 3583):
    records.append([str(df.values[i,j]) for j in range(0, 11)])

association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=1.5, min_length=1)
association_results = list(association_rules)
print(len(association_rules))


for item in association_rules:

    # first index of the inner list
    # Contains base item and add item
    pair = item[0]
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("===============================")



#Age,race,gender, and drug association



conn = create_connection('TestDrug.db')

white = []
black =[]
hispanic=[]

races = ['White', 'Black', 'Hispanic']
for ele in races:
    sql_statement="SELECT * FROM Demographic where race == '"+ ele +"';"
    df = pd.read_sql_query(sql_statement, conn)
    #display(df)

    for i, row in df.iterrows():
        if ele == 'White':
            white.append(row['CaseNumber'])
        elif ele == 'Black':
            black.append(row['CaseNumber'])
        elif ele == 'Hispanic':
            hispanic.append(row['CaseNumber'])

age_groups = ['10 and 20', '20 and 30', '30 and 40', '40 and 50', '50 and 60']
grp1 = []
grp2 =[]
grp3=[]
grp4=[]
grp5 =[]
for ele in age_groups:
    sql_statement="SELECT * FROM Demographic where Age Between "+ele+";"
    df = pd.read_sql_query(sql_statement, conn)
#     display(df)

    for i, row in df.iterrows():
        if ele == '10 and 20':
            grp1.append(row['CaseNumber'])
        elif ele == '20 and 30':
            grp1.append(row['CaseNumber'])
        elif ele == '30 and 40':
            grp1.append(row['CaseNumber'])
        elif ele == '40 and 50':
            grp1.append(row['CaseNumber'])
        elif ele == '50 and 60':
            grp1.append(row['CaseNumber'])
mainlstt=[]
sql_statement="SELECT * FROM Demographic;"
df = pd.read_sql_query(sql_statement, conn)
# display(df)

for i, row in df.iterrows():
    if row['CaseNumber'] in white and row['CaseNumber'] in grp1 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,1,0,0,0,0,1,0))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp1 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,1,0,0,0,0,0,1))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp2 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,1,0,0,0,1,0))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp2 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,1,0,0,0,0,1))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp3 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,1,0,0,1,0))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp3 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,1,0,0,0,1))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp4 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,0,1,0,1,0))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp4 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,0,1,0,0,1))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp5 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,0,0,1,1,0))
    elif row['CaseNumber'] in white and row['CaseNumber'] in grp5 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,0,0,1,0,1))

    elif row['CaseNumber'] in black and row['CaseNumber'] in grp1 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,1,0,0,0,0,1,0))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp1 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,1,0,0,0,0,0,1))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp2 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,1,0,0,0,1,0))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp2 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,1,0,0,0,0,1))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp3 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,1,0,0,1,0))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp3 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,1,0,0,0,1))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp4 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,0,1,0,1,0))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp4 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,0,1,0,0,1))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp5 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,0,0,1,1,0))
    elif row['CaseNumber'] in black and row['CaseNumber'] in grp5 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,0,0,1,0,1))

    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp1 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,1,0,0,0,0,1,0))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp1 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,1,0,0,0,0,0,1))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp2 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,1,0,0,0,1,0))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp2 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,1,0,0,0,0,1))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp3 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,1,0,0,1,0))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp3 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,1,0,0,0,1))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp4 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,0,1,0,1,0))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp4 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,0,1,0,0,1))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp5 and row['Sex'] == 'M':
        mainlstt.append((1,0,0,0,0,0,0,1,1,0))
    elif row['CaseNumber'] in hispanic and row['CaseNumber'] in grp5 and row['Sex'] == 'F':
        mainlstt.append((1,0,0,0,0,0,0,1,0,1))

df1 = pd.DataFrame(mainlstt, columns=['White', 'Black', 'Hispanic', 'AgeGroup_10-20','AgeGroup_20-30', 'AgeGroup_30-40', 'AgeGroup_40-50', 'AgeGroup_50-60', 'Male', 'Female'])
#display(df)

conn = create_connection('TestDrug.db')
sql_statement="""SELECT Heroin,Cocaine,Fentanyl,Oxycodone,Oxymorphone,EtOH,Hydrocodone,Benzodiazepine,Methadone,Amphet,Tramad,Morphine_not_heroin
FROM maindata JOIN df1 WHERE RACE IN ('White','Black','Hispanic, White')"""
df2 = pd.read_sql_query(sql_statement, conn)
display(df2)

records = []
for i in range(0, 3583):
    records.append([str(df2.values[i,j]) for j in range(0, 25)])

association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=1.5, min_length=1)
association_results = list(association_rules)
print(len(association_rules))

for item in association_rules:

    # first index of the inner list
    # Contains base item and add item
    pair = item[0]
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("===============================")
