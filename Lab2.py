#!/usr/bin/env python
# coding: utf-8

# Before you turn this problem in, make sure everything runs as expected. First, **restart the kernel** (in the menubar, select Kernel$\rightarrow$Restart) and then **run all cells** (in the menubar, select Cell$\rightarrow$Run All).
# 
# Make sure you fill in any place that says `YOUR CODE HERE` or "YOUR ANSWER HERE", as well as your name and collaborators below:

# In[95]:


NAME = "Kunal Mehta"
COLLABORATORS = ""


# ---

# # Lab 2 Introduction
# 
# 
# In this lab you will use parse a vcf file to extracts parts of it and load it into a database. 
# The fields you will be parsing from the vcf file are: 
# ```
# CHROM
# POS	
# ID	
# REF	
# ALT	
# QUAL	
# FILTER
# ```
# and from the INFO column, the following fields:
# ```
# 1000g2015aug_all
# ExAC_ALL
# FATHMM_pred
# LRT_pred
# MetaLR_pred
# MetaSVM_pred
# MutationAssessor_pred
# MutationTaster_pred
# PROVEAN_pred
# Polyphen2_HDIV_pred
# Polyphen2_HVAR_pred
# SIFT_pred
# fathmm-MKL_coding_pred.
# ```
# The fields:
# ```
# FATHMM_pred
# LRT_pred
# MetaLR_pred
# MetaSVM_pred
# MutationAssessor_pred
# MutationTaster_pred
# PROVEAN_pred
# Polyphen2_HDIV_pred
# Polyphen2_HVAR_pred
# SIFT_pred
# fathmm-MKL_coding_pred
# ```
# are predictor fields. They use a letter to indicate whether a given variation is harmful or not.
# 
# NOTE: use the helper functions in cell2. To use them, you have to run CELL 2! 
# 

# In[96]:


## Helper functions

import os
import sqlite3
from sqlite3 import Error
import gzip

def create_connection(db_file, delete_db=False):
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


# # Part 1 (10 pts)
# 
# In part1 you will open the gzipped vcf file using the python gzip module and figure out all the possible values for the predictor fields. 
# 
# You do not have to unzip the file. Use `with gzip.open(filename,'rt') as fp:` to read one line at a time. 
# 
# 

# In[97]:


def get_predictor_values(filename):
    """
    See part 1 description 
    """
    import gzip
    ls = []
    dct = {}
    x1=[]
    x2=[]
    x3=[]
    x4=[]
    x5=[]
    x6=[]
    x7=[]
    x8=[]
    x9=[]
    x10=[]
    x11=[]
    with gzip.open(filename,'rt') as fp:
        for line in fp:
            line.strip()
            if line.startswith("#CHR"):
                head = line.split('\t')
            elif line.startswith("##") == False:
                llist = line.split('\t')
                ls.append(llist[7])
        
    for i in range(0,len(ls)):
        vals = ls[i].split(';')
        for j in vals:
            if j.startswith('FATHMM_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x1:
                    x1.append(m)
                    
            elif j.startswith('LRT_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x2:
                    x2.append(m)
                    
            elif j.startswith('MetaLR_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x3:
                    x3.append(m)
                    
            elif j.startswith('MetaSVM_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x4:
                    x4.append(m)
                    
            elif j.startswith('MutationAssessor_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x5:
                    x5.append(m)
                    
            elif j.startswith('MutationTaster_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x6:
                    x6.append(m)
                    
            elif j.startswith('PROVEAN_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x7:
                    x7.append(m)
                    
            elif j.startswith('Polyphen2_HDIV_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x8:
                    x8.append(m)
                    
            elif j.startswith('Polyphen2_HVAR_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x9:
                    x9.append(m)
                    
            elif j.startswith('SIFT_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x10:
                    x10.append(m)
                    
            elif j.startswith('fathmm-MKL_coding_pred'):
                m = j.split('=')[1]
                if m!='.' and m not in x11:
                    x11.append(m)
                
    dct.update({'FATHMM_pred':x1})
    dct.update({'LRT_pred':x2})
    dct.update({'MetaLR_pred':x3})
    dct.update({'MetaSVM_pred':x4})
    dct.update({'MutationAssessor_pred':x5})
    dct.update({'MutationTaster_pred':x6})
    dct.update({'PROVEAN_pred':x7})
    dct.update({'Polyphen2_HDIV_pred':x8})
    dct.update({'Polyphen2_HVAR_pred':x9})
    dct.update({'SIFT_pred':x10})
    dct.update({'fathmm-MKL_coding_pred':x11})
    return dct


# In[98]:



## Can take 30 seconds to run!
expected_solution = {'SIFT_pred': ['D', 'T'], 'Polyphen2_HDIV_pred': ['D', 'B', 'P'], 'Polyphen2_HVAR_pred': ['D', 'B', 'P'], 'LRT_pred': ['D', 'N', 'U'], 'MutationTaster_pred': ['D', 'P', 'N', 'A'], 'MutationAssessor_pred': ['H', 'N', 'L', 'M'], 'FATHMM_pred': ['T', 'D'], 'PROVEAN_pred': ['D', 'N'], 'MetaSVM_pred': ['D', 'T'], 'MetaLR_pred': ['D', 'T'], 'fathmm-MKL_coding_pred': ['D', 'N']}
filename = 'test_4families_annovar.vcf.gz'
predictor_values = get_predictor_values(filename)
assert predictor_values == expected_solution


# # Part 2 (No points)
# 
# You will now create 13 tables
# Tables 1-11 will be for :
# 
# FATHMM_pred
# LRT_pred 
# MetaLR_pred
# MetaSVM_pred
# MutationAssessor_pred
# MutationTaster_pred
# PROVEAN_pred
# Polyphen2_HDIV_pred
# Polyphen2_HVAR_pred
# SIFT_pred
# fathmm_MKL_coding_pred ## NOTE: I have replaced the dash with an underscore. 
# 
# The first column for each of these tables will be the name of the field + ID, e.g., FATHMM_predID. This
# column will be of type not null primary key. The second column will be called `prediction` and will be of
# type TEXT not null. The prediction values will be values you extracted for each of the fields in the previous step. 
# For example, 'FATHMM_pred' has two prediction values 'T' and 'D'. Name the tables after their field name, e.g.,  
# call table that will contains values of FATHMM_pred `FATHMM_pred`.  Make sure to sort the values, meaning, D should 
# be inserted before T. 
# 
# 
# Table 12 will be the Variants table. 
# The first column will be VariantID. 
# 
# The other columns will be:
# CHROM   
# POS 
# ID  
# REF 
# ALT 
# QUAL    
# FILTER
# thousandg2015aug_all ##NOTE: a column name cannot start with a number, so you have to rename!
# ExAC_ALL
# 
# 
# Table 12 will have 11 more columns that relate to each of prediction table. Consider writing a utility function
# to fetch the primary key for a given prediction from each of the prediction table. Name each of the 
# column should be the name of predictor + ID, e.g., FATHMM_predID. 
# 
# 
# You have already deteremined their data type, so use that to set their data type. 
# For integer use INTEGER. 
# For float use REAL. 
# For string use TEXT. 
# 
# Table 13  will be called PredictionStats. The first column will be PredictorStatsID INTEGER NOT NULL PRIMARY KEY. 
# The second column will be VariantID. The third column will be PredictorName. The fourth column will be PredictorValue. 
# This is not a normalized table!
# 
# The prediction value will be a float value mapped from the prediction text.  Use the following information to 
# assign values: 
# REF: https://brb.nci.nih.gov/seqtools/colexpanno.html#dbnsfp
# 
# FATHMM_pred
# - T = 0
# - D = 1
# 
# LRT_pred 
# - D = 1
# - N = 0
# - U = 0
# 
# MetaLR_pred
# - T = 0
# - D = 1
# 
# MetaSVM_pred
# - T = 0
# - D = 1
# 
# MutationAssessor_pred
# - H = 1
# - N = 0
# - L = 0.25
# - M = 0.5
# 
# MutationTaster_pred
# - D = 1
# - P = 0
# - N = 0
# - A = 1
# 
# PROVEAN_pred
# - D = 1
# - N = 0
# 
# Polyphen2_HDIV_pred
# - D = 1
# - B = 0
# - P = 0.5
# 
# Polyphen2_HVAR_pred
# - D = 1
# - B = 0
# - P = 0.5
# 
# SIFT_pred
# - D = 1
# - T = 0
# 
# fathmm-MKL_coding_pred
# - D = 1
# - N = 0
# 
# 
# ```
# 
# prediction_mapping = {
#     'FATHMM_pred': {'T': 0, 'D': 1},
#     'MetaLR_pred': {'T': 0, 'D': 1},
#     'MetaSVM_pred': {'T': 0, 'D': 1},
#     'SIFT_pred': {'T': 0, 'D': 1},
#     'fathmm_MKL_coding_pred': {'D': 1, 'N': 0},
#     'LRT_pred': {'U': 0, 'N': 0, 'D': 1},
#     'MutationAssessor_pred': {'H': 1, 'N': 0, 'L': 0.25, 'M': 0.5},  
#     'MutationTaster_pred': {'D': 1, 'P': 0, 'N': 0, 'A': 1},
#     'PROVEAN_pred': {'D': 1, 'N': 0},
#     'Polyphen2_HDIV_pred': {'D': 1, 'B': 0, 'P': 0.5},
#     'Polyphen2_HVAR_pred': {'D': 1, 'B': 0, 'P': 0.5},
# }
# 
# 
# ```
# 
# 
# The idea is that 11 predictors have been used to annotate all the variants in the file. This table combines all that information in one table. 
# By grouping the table based on variantid and summing the prediction values mapped from the prediction text, you can find which variants have a consensus on their being deterimental. 
# 
# IMPORTANT: instead of fathmm-MKL_coding_pred use fathmm_MKL_coding_pred everywhere. 
# HINT: You have to commit the changes you make to the table, otherwise your changes will not be saved. Consider wrapping all changes inside `with conn:`
# 
# 
# 

# In[99]:


# Creating lab2.db 
db_file = 'lab2.db'
conn = create_connection(db_file, delete_db=True)
conn.close()


# In[100]:


import pandas as pd
def create_tables_1_11(db_file):
    import sqlite3
    import pandas as pd
    """
    Create tables 1 to 11.
    INPUT: db_file -- Name of database file -- eg. lab2.db
    
    """
    # YOUR CODE HERE
    conn = create_connection(db_file)
    cur = conn.cursor()

    drop1 = "DROP TABLE IF EXISTS FATHMM_pred"
    drop2 = "DROP TABLE IF EXISTS LRT_pred"
    drop3 = "DROP TABLE IF EXISTS MetaLR_pred"
    drop4 = "DROP TABLE IF EXISTS MetaSVM_pred"
    drop5 = "DROP TABLE IF EXISTS MutationAssessor_pred"
    drop6 = "DROP TABLE IF EXISTS MutationTaster_pred"
    drop7 = "DROP TABLE IF EXISTS PROVEAN_pred"
    drop8 = "DROP TABLE IF EXISTS Polyphen2_HDIV_pred"
    drop9 = "DROP TABLE IF EXISTS Polyphen2_HVAR_pred"
    drop10 = "DROP TABLE IF EXISTS SIFT_pred"
    drop11 = "DROP TABLE IF EXISTS fathmm_MKL_coding_pred"
    cur.execute(drop1)
    cur.execute(drop2)
    cur.execute(drop3)
    cur.execute(drop4)
    cur.execute(drop5)
    cur.execute(drop6)
    cur.execute(drop7)
    cur.execute(drop8)
    cur.execute(drop9)
    cur.execute(drop10)
    cur.execute(drop11)
    
    table1 = "CREATE TABLE FATHMM_pred (FATHMM_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table2 = "CREATE TABLE LRT_pred (LRT_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table3 = "CREATE TABLE MetaLR_pred (MetaLR_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table4 = "CREATE TABLE MetaSVM_pred (MetaSVM_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table5 = "CREATE TABLE MutationAssessor_pred (MutationAssessor_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table6 = "CREATE TABLE MutationTaster_pred (MutationTaster_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table7 = "CREATE TABLE PROVEAN_pred (PROVEAN_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table8 = "CREATE TABLE Polyphen2_HDIV_pred (Polyphen2_HDIV_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table9 = "CREATE TABLE Polyphen2_HVAR_pred (Polyphen2_HVAR_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table10 = "CREATE TABLE SIFT_pred (SIFT_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    table11 = "CREATE TABLE fathmm_MKL_coding_pred (fathmm_MKL_coding_predID INT NOT NULL PRIMARY KEY, prediction TEXT NOT NULL)"
    
    create_table(conn,table1)
    create_table(conn,table2)
    create_table(conn,table3)
    create_table(conn,table4)
    create_table(conn,table5)
    create_table(conn,table6)
    create_table(conn,table7)
    create_table(conn,table8)
    create_table(conn,table9)
    create_table(conn,table10)
    create_table(conn,table11)
    
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    x6 = []
    x7 = []
    x8 = []
    x9 = []
    x10 = []
    x11 = []
    dct = get_predictor_values(filename)
    
    for i,j in dct.items():
        if i == 'FATHMM_pred':
            x1 = sorted(j)
        elif i == 'LRT_pred':
            x2 = sorted(j)
        elif i == 'MetaLR_pred':
            x3 = sorted(j)
        elif i == 'MetaSVM_pred':
            x4 = sorted(j)
        elif i == 'MutationAssessor_pred':
            x5 = sorted(j)
        elif i == 'MutationTaster_pred':
            x6 = sorted(j)
        elif i == 'PROVEAN_pred':
            x7 = sorted(j)
        elif i == 'Polyphen2_HDIV_pred':
            x8 = sorted(j)
        elif i == 'Polyphen2_HVAR_pred':
            x9 = sorted(j)
        elif i == 'SIFT_pred':
            x10 = sorted(j)
        elif i == 'fathmm-MKL_coding_pred':
            x11 = sorted(j)
    d1 = []
    d2 = []
    d3 = []
    d4 = []
    d5 = []
    d6 = []
    d7 = []
    d8 = []
    d9 = []
    d10 = []
    d11 = []
    for i in range(0,4):
        if i < len(x1):
            d1.append((i+1,x1[i]))
        if i < len(x2):
            d2.append((i+1,x2[i]))
        if i < len(x3):
            d3.append((i+1,x3[i]))
        if i < len(x4):
            d4.append((i+1,x4[i]))
        if i < len(x5):
            d5.append((i+1,x5[i]))
        if i < len(x6):
            d6.append((i+1,x6[i]))
        if i < len(x7):
            d7.append((i+1,x7[i]))
        if i < len(x8):
            d8.append((i+1,x8[i]))
        if i < len(x9):
            d9.append((i+1,x9[i]))
        if i < len(x10):
            d10.append((i+1,x10[i]))
        if i < len(x11):
            d11.append((i+1,x11[i]))
    
    with conn:
        for i in d1:
            transfer = "INSERT INTO FATHMM_pred VALUES(?,?)"
            cur.execute(transfer,i)
            
        for i in d2:
            transfer = "INSERT INTO LRT_pred VALUES(?,?)"
            cur.execute(transfer,i)
            
        for i in d3:
            transfer = "INSERT INTO MetaLR_pred VALUES(?,?)"
            cur.execute(transfer,i)
            
        for i in d4:
            transfer = "INSERT INTO MetaSVM_pred VALUES(?,?)"
            cur.execute(transfer,i)
            
        for i in d5:
            transfer = "INSERT INTO MutationAssessor_pred VALUES(?,?)"
            cur.execute(transfer,i)
        
        for i in d6:
            transfer = "INSERT INTO MutationTaster_pred VALUES(?,?)"
            cur.execute(transfer,i)
        
        for i in d7:
            transfer = "INSERT INTO PROVEAN_pred VALUES(?,?)"
            cur.execute(transfer,i)
        
        for i in d8:
            transfer = "INSERT INTO Polyphen2_HDIV_pred VALUES(?,?)"
            cur.execute(transfer,i)
        
        for i in d9:
            transfer = "INSERT INTO Polyphen2_HVAR_pred VALUES(?,?)"
            cur.execute(transfer,i)
        
        for i in d10:
            transfer = "INSERT INTO SIFT_pred VALUES(?,?)"
            cur.execute(transfer,i)
            
        for i in d11:
            transfer = "INSERT INTO fathmm_MKL_coding_pred VALUES(?,?)"
            cur.execute(transfer,i)

db_file = 'lab2.db'    
create_tables_1_11(db_file)


# # Part 3 (10 pts)
# 
# Write a function that returns a dictionary that maps for a given predictor its letter prediction to foreign key value. 
# Conver the dash in 'fathmm-MKL_coding_pred' to an underscore. 
# 

# In[101]:


def get_predictor_value_to_fk_map(db_file):
    """
    See part 3 description 
    
    INPUT: db_file -- Name of database file -- eg. lab2.db
    
    """
    # YOUR CODE HERE
    conn = create_connection(db_file)
    cur = conn.cursor()
    
    dct = get_predictor_values(filename)
    dct['fathmm_MKL_coding_pred'] = dct['fathmm-MKL_coding_pred']
    del dct['fathmm-MKL_coding_pred']
    final = {}
    for i,j in dct.items():
        dic = {}
        acc = "SELECT * FROM " + i
        cur.execute(acc)
        rs = cur.fetchall()
        for k in j:
            for l in rs:
                if l[1] == k:
                    dic[k] = l[0]
        final[i] = dic
    return final


# In[102]:


expected_solution = {
    'FATHMM_pred': {'D': 1, 'T': 2}, 
    'LRT_pred': {'D': 1, 'N': 2, 'U': 3}, 
    'MetaLR_pred': {'D': 1, 'T': 2}, 
    'MetaSVM_pred': {'D': 1, 'T': 2}, 
    'MutationAssessor_pred': {'H': 1, 'L': 2, 'M': 3, 'N': 4}, 
    'MutationTaster_pred': {'A': 1, 'D': 2, 'N': 3, 'P': 4}, 
    'PROVEAN_pred': {'D': 1, 'N': 2}, 
    'Polyphen2_HDIV_pred': {'B': 1, 'D': 2, 'P': 3}, 
    'Polyphen2_HVAR_pred': {'B': 1, 'D': 2, 'P': 3}, 
    'SIFT_pred': {'D': 1, 'T': 2}, 
    'fathmm_MKL_coding_pred': {'D': 1, 'N': 2}}

db_file = 'lab2.db'
predictor_fk_map = get_predictor_value_to_fk_map(db_file)
assert predictor_fk_map == expected_solution


# # Part 4 (No Points)
# Create table 12 or the variants table. See description above
# 

# In[112]:


def create_variants_table(db_file):
    """
    Part 4
    """
    import pandas as pd
    conn = create_connection(db_file)
    cus = conn.cursor()
    drop12 = "DROP TABLE IF EXISTS Variants"
    cus.execute(drop12)
    
    # YOUR CODE HERE
    table12 = """CREATE TABLE Variants (
                VariantID INTEGER NOT NULL PRIMARY KEY,
                CHROM TEXT,
                POS INT,
                ID TEXT,
                REF TEXT,
                ALT TEXT,
                QUAL REAL,
                FILTER TEXT,
                thousandg2015aug_all REAL,
                ExAC_ALL REAL,
                FATHMM_predID INT,
                LRT_predID INT,
                MetaLR_predID INT,
                MetaSVM_predID INT,
                MutationAssessor_predID INT,
                MutationTaster_predID INT,
                PROVEAN_predID INT,
                Polyphen2_HDIV_predID INT,
                Polyphen2_HVAR_predID INT,
                SIFT_predID INT,
                fathmm_MKL_coding_predID INT,
                FOREIGN KEY (FATHMM_predID) REFERENCES FATHMM_pred(FATHMM_predID),
                FOREIGN KEY (LRT_predID) REFERENCES LRT_pred(LRT_predID),
                FOREIGN KEY (MetaLR_predID) REFERENCES MetaLR_pred(MetaLR_predID),
                FOREIGN KEY (MetaSVM_predID) REFERENCES MetaSVM_pred(MetaSVM_predID),
                FOREIGN KEY (MutationAssessor_predID) REFERENCES MutationAssessor_pred(MutationAssessor_predID),
                FOREIGN KEY (MutationTaster_predID) REFERENCES MutationTaster_pred(MutationTaster_predID),
                FOREIGN KEY (PROVEAN_predID) REFERENCES PROVEAN_pred(PROVEAN_predID),
                FOREIGN KEY (Polyphen2_HDIV_predID) REFERENCES Polyphen2_HDIV_pred(Polyphen2_HDIV_predID),
                FOREIGN KEY (Polyphen2_HVAR_predID) REFERENCES Polyphen2_HVAR_pred(Polyphen2_HVAR_predID),
                FOREIGN KEY (SIFT_predID) REFERENCES SIFT_pred(SIFT_predID),
                FOREIGN KEY (fathmm_MKL_coding_predID) REFERENCES fathmm_MKL_coding_pred(fathmm_MKL_coding_predID)
                );"""
    create_table(conn, table12)
    sel = "SELECT * FROM Variants"
    df = pd.read_sql_query(sel, conn)
    display(df)
    
# create table
db_file = 'lab2.db'
create_variants_table(db_file)


# # Part 5 (No Points)
# 
# Create table 13 -- or the prediction stats table. See description above. 
# 

# In[104]:


def create_predictionstats_table(db_file):
    import pandas as pd
    """
    Part 5   
    """
    # YOUR CODE HERE
    conn = create_connection(db_file)
    cur = conn.cursor()
    drop13 = "DROP TABLE IF EXISTS PredictionStats"
    cur.execute(drop13)
    
    table13 = """CREATE TABLE PredictionStats(
                   PredictorStatsId INTEGER NOT NULL PRIMARY KEY,
                   VariantID INTEGER,
                   PredictorName TEXT,
                   PredictorValue REAL
                    )"""
    create_table(conn, table13)
    sel = "SELECT * FROM PredictionStats"
    df = pd.read_sql_query(sel, conn)
    display(df)
    
db_file = 'lab2.db'
create_predictionstats_table(db_file)


# # Part 6 (10 Points)
# 
# Write a function to pull the following info fields given the whole info field. 
# ```
# values_to_pull = [
#         '1000g2015aug_all',
#         'ExAC_ALL',
#         'FATHMM_pred',
#         'LRT_pred',
#         'MetaLR_pred',
#         'MetaSVM_pred',
#         'MutationAssessor_pred',
#         'MutationTaster_pred',
#         'PROVEAN_pred',
#         'Polyphen2_HDIV_pred',
#         'Polyphen2_HVAR_pred',
#         'SIFT_pred',
#         'fathmm-MKL_coding_pred',
#     ]
# ```
# 

# In[105]:


def pull_info_values(info):
    """
    See part 6 description
    """

    values_to_pull = [
        '1000g2015aug_all',
        'ExAC_ALL',
        'FATHMM_pred',
        'LRT_pred',
        'MetaLR_pred',
        'MetaSVM_pred',
        'MutationAssessor_pred',
        'MutationTaster_pred',
        'PROVEAN_pred',
        'Polyphen2_HDIV_pred',
        'Polyphen2_HVAR_pred',
        'SIFT_pred',
        'fathmm-MKL_coding_pred',
    ]
    ls = info.split(';')
    fin = []
    for i in ls:
        m = i.split('=')
        if len(m) == 1 or m[1] == '.':
            fin.append((m[0],''))
        else:
            fin.append((m[0],m[1]))    
    dic = {}
    for i in fin:
        if i[0] in values_to_pull:
            if i[0] == 'fathmm-MKL_coding_pred':
                dic['fathmm_MKL_coding_pred'] = i[1]
            elif i[0] == '1000g2015aug_all':
                dic['thousandg2015aug_all'] = i[1]
            else:
                dic[i[0]] = i[1]
    return dic
    


# In[106]:


sample_info_input = "AC=2;AF=0.333;AN=6;BaseQRankSum=2.23;ClippingRankSum=0;DP=131;ExcessHet=3.9794;FS=2.831;MLEAC=2;MLEAF=0.333;MQ=60;MQRankSum=0;QD=12.06;ReadPosRankSum=-0.293;SOR=0.592;VQSLOD=21.79;culprit=MQ;DB;POSITIVE_TRAIN_SITE;ANNOVAR_DATE=2018-04-16;Func.refGene=exonic;Gene.refGene=MAST2;GeneDetail.refGene=.;ExonicFunc.refGene=nonsynonymous_SNV;AAChange.refGene=MAST2:NM_015112:exon29:c.G3910A:p.V1304M;Func.ensGene=exonic;Gene.ensGene=ENSG00000086015;GeneDetail.ensGene=.;ExonicFunc.ensGene=nonsynonymous_SNV;AAChange.ensGene=ENSG00000086015:ENST00000361297:exon29:c.G3910A:p.V1304M;cytoBand=1p34.1;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=0.034;SIFT_converted_rankscore=0.440;SIFT_pred=D;Polyphen2_HDIV_score=0.951;Polyphen2_HDIV_rankscore=0.520;Polyphen2_HDIV_pred=P;Polyphen2_HVAR_score=0.514;Polyphen2_HVAR_rankscore=0.462;Polyphen2_HVAR_pred=P;LRT_score=0.002;LRT_converted_rankscore=0.368;LRT_pred=N;MutationTaster_score=1.000;MutationTaster_converted_rankscore=0.810;MutationTaster_pred=D;MutationAssessor_score=1.67;MutationAssessor_score_rankscore=0.430;MutationAssessor_pred=L;FATHMM_score=1.36;FATHMM_converted_rankscore=0.344;FATHMM_pred=T;PROVEAN_score=-1.4;PROVEAN_converted_rankscore=0.346;PROVEAN_pred=N;VEST3_score=0.158;VEST3_rankscore=0.189;MetaSVM_score=-1.142;MetaSVM_rankscore=0.013;MetaSVM_pred=T;MetaLR_score=0.008;MetaLR_rankscore=0.029;MetaLR_pred=T;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=4.716;CADD_raw_rankscore=0.632;CADD_phred=24.6;DANN_score=0.998;DANN_rankscore=0.927;fathmm-MKL_coding_score=0.900;fathmm-MKL_coding_rankscore=0.506;fathmm-MKL_coding_pred=D;Eigen_coding_or_noncoding=c;Eigen-raw=0.461;Eigen-PC-raw=0.469;GenoCanyon_score=1.000;GenoCanyon_score_rankscore=0.747;integrated_fitCons_score=0.672;integrated_fitCons_score_rankscore=0.522;integrated_confidence_value=0;GERP++_RS=4.22;GERP++_RS_rankscore=0.490;phyloP100way_vertebrate=4.989;phyloP100way_vertebrate_rankscore=0.634;phyloP20way_mammalian=1.047;phyloP20way_mammalian_rankscore=0.674;phastCons100way_vertebrate=1.000;phastCons100way_vertebrate_rankscore=0.715;phastCons20way_mammalian=0.999;phastCons20way_mammalian_rankscore=0.750;SiPhy_29way_logOdds=17.151;SiPhy_29way_logOdds_rankscore=0.866;Interpro_domain=.;GTEx_V6_gene=ENSG00000162415.6;GTEx_V6_tissue=Nerve_Tibial;esp6500siv2_all=0.0560;esp6500siv2_aa=0.0160;esp6500siv2_ea=0.0761;ExAC_ALL=0.0553;ExAC_AFR=0.0140;ExAC_AMR=0.0386;ExAC_EAS=0.0005;ExAC_FIN=0.0798;ExAC_NFE=0.0788;ExAC_OTH=0.0669;ExAC_SAS=0.0145;ExAC_nontcga_ALL=0.0541;ExAC_nontcga_AFR=0.0129;ExAC_nontcga_AMR=0.0379;ExAC_nontcga_EAS=0.0004;ExAC_nontcga_FIN=0.0798;ExAC_nontcga_NFE=0.0802;ExAC_nontcga_OTH=0.0716;ExAC_nontcga_SAS=0.0144;ExAC_nonpsych_ALL=0.0496;ExAC_nonpsych_AFR=0.0140;ExAC_nonpsych_AMR=0.0386;ExAC_nonpsych_EAS=0.0005;ExAC_nonpsych_FIN=0.0763;ExAC_nonpsych_NFE=0.0785;ExAC_nonpsych_OTH=0.0638;ExAC_nonpsych_SAS=0.0145;1000g2015aug_all=0.024361;1000g2015aug_afr=0.0038;1000g2015aug_amr=0.0461;1000g2015aug_eur=0.0795;1000g2015aug_sas=0.0041;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=rs33931638;avsnp150=rs33931638;CADD13_RawScore=4.716301;CADD13_PHRED=24.6;Eigen=0.4614;REVEL=0.098;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0507;gnomAD_genome_AFR=0.0114;gnomAD_genome_AMR=0.0430;gnomAD_genome_ASJ=0.1159;gnomAD_genome_EAS=0;gnomAD_genome_FIN=0.0802;gnomAD_genome_NFE=0.0702;gnomAD_genome_OTH=0.0695;gerp++gt2=4.22;cosmic70=.;InterVar_automated=Benign;PVS1=0;PS1=0;PS2=0;PS3=0;PS4=0;PM1=0;PM2=0;PM3=0;PM4=0;PM5=0;PM6=0;PP1=0;PP2=0;PP3=0;PP4=0;PP5=0;BA1=1;BS1=1;BS2=0;BS3=0;BS4=0;BP1=0;BP2=0;BP3=0;BP4=0;BP5=0;BP6=0;BP7=0;Kaviar_AF=0.0552127;Kaviar_AC=8536;Kaviar_AN=154602;ALLELE_END"

expected_solution = {
    'thousandg2015aug_all': '0.024361', 
    'ExAC_ALL': '0.0553', 
    'SIFT_pred': 'D', 
    'Polyphen2_HDIV_pred': 'P', 
    'Polyphen2_HVAR_pred': 'P', 
    'LRT_pred': 'N',
    'MutationTaster_pred': 'D', 
    'MutationAssessor_pred': 'L', 
    'FATHMM_pred': 'T', 
    'PROVEAN_pred': 'N', 
    'MetaSVM_pred': 'T', 
    'MetaLR_pred': 'T', 
    'fathmm_MKL_coding_pred': 'D'
}


solution  = pull_info_values(sample_info_input)
assert solution == expected_solution


# # Part 7 (10 points)
# 
# Remember that to insert a record in SQLite, you have to use `cur.execute(sql, values)`, where `sql` is the insert statement and `values` is a list/tuple of values that will be substituted into the `sql` string wherever there is a question mark. 
# 
# Write a function that takes in as input: CHROM, POS, ID, REF, ALT, QUAL, FILTER, info_values and returns a list with the values in the following order:
# ```
# CHROM 
# POS
# ID
# REF
# ALT
# QUAL
# FILTER
# thousandg2015aug_all # 1000 has been replaced by the text thousand
# ExAC_ALL
# FATHMM_pred
# LRT_pred
# MetaLR_pred
# MetaSVM_pred
# MutationAssessor_pred
# MutationTaster_pred
# PROVEAN_pred
# Polyphen2_HDIV_pred
# Polyphen2_HVAR_pred
# SIFT_pred
# fathmm_MKL_coding_pred # note that the dash has been replaced by underscore
# ```
# 
# The info_values dictionary contains the predictor values. Use `None` for any empty/missing value for info fields, thousandg2015aug_all, and ExAC_ALL. 
# 
# 

# In[107]:


def build_values_list(CHROM, POS, ID, REF, ALT, QUAL, FILTER, info_values):
    """
    See part 7 description 
    
    """
#    YOUR CODE HERE
    tables = [
        'FATHMM_pred',
        'LRT_pred',
        'MetaLR_pred',
        'MetaSVM_pred',
        'MutationAssessor_pred',
        'MutationTaster_pred',
        'PROVEAN_pred',
        'Polyphen2_HDIV_pred',
        'Polyphen2_HVAR_pred',
        'SIFT_pred',
        'fathmm_MKL_coding_pred',
    ]
    ls = []
    ls.append(CHROM)
    ls.append(POS)
    ls.append(ID)
    ls.append(REF)
    ls.append(ALT)
    ls.append(QUAL)
    ls.append(FILTER)
    val = info_values.get('thousandg2015aug_all')
    if val:
        ls.append(val)
    else:
        ls.append(None)
    val = info_values.get('ExAC_ALL')
    if val:
        ls.append(val)
    else:
        ls.append(None)
    
    for table in tables:
        val = info_values.get(table)
        if val:
            ls.append(predictor_fk_map[table][val])
        else:
            ls.append(None)
            
    return ls


# In[108]:


CHROM, POS, ID, REF, ALT, QUAL, FILTER = (7, 87837848, '.', 'C', 'A', 418.25, 'PASS') 
info_values = {'SIFT_pred': 'D', 'Polyphen2_HDIV_pred': 'D', 'Polyphen2_HVAR_pred': 'D', 'LRT_pred': 'D', 'MutationTaster_pred': 'D', 'MutationAssessor_pred': 'H', 'FATHMM_pred': 'T', 'PROVEAN_pred': 'D', 'MetaSVM_pred': 'D', 'MetaLR_pred': 'D', 'fathmm_MKL_coding_pred': 'D'}

results = build_values_list(CHROM, POS, ID, REF, ALT, QUAL, FILTER, info_values)
expected_results = [7, 87837848, '.', 'C', 'A', 418.25, 'PASS', None, None, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1]
assert results == expected_results


# # Part 8 (No Points)
# 
# Create a function that takes the database `conn` and `values` from the `build_values_list` function to insert a variant record. 
# 
# IMPORTANT: Function should return the id of the row inserted, which will be VariantId
# 

# In[109]:


def insert_variant(conn, values):
    """
    See description Part 8
    """
    cur = conn.cursor()
    sel = """INSERT INTO Variants (CHROM, POS, ID, REF, ALT, QUAL, FILTER, thousandg2015aug_all,
                ExAC_ALL,
                FATHMM_predID,
                LRT_predID,
                MetaLR_predID,
                MetaSVM_predID,
                MutationAssessor_predID,
                MutationTaster_predID,
                PROVEAN_predID,
                Polyphen2_HDIV_predID,
                Polyphen2_HVAR_predID,
                SIFT_predID,
                fathmm_MKL_coding_predID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    with conn:
        cur.execute(sel,values)
        
    sel = "SELECT COUNT(*) FROM Variants"
    cur.execute(sel)
    rs = cur.fetchall()
    if rs[0][0]%1000==0:
        print(rs[0][0])
    return rs[0][0]
    
#     ls = []
#     cur = conn.cursor()
#     sel = "SELECT VariantID FROM Variants ORDER BY VariantID DESC LIMIT 1"
#     cur.execute(sel)
#     m = cur.fetchall()
#     if m == []:
#         m = 0
#     else:
#         m = m[0][0]
#     m = m+1
#     ls.append(m)
#     for i in values:
#         ls.append(i)
#     ls = tuple(ls)
#     with conn:
#         transfer = "INSERT INTO Variants VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
#         cur.execute(transfer, ls)
#     if m%1000==0:
#         print(m)
#     return m


# In[ ]:





# # Part 9 (No Points)
# 
# Create a function that takes the database `conn` and `values` which is the tuple `(VariantId, PredictorName, PredictorValue)` Where `VariantId` will be the return value from the `insert_variant` function,  `PredictorName` is the name of the predictor, and `PredictorValue` is the mapping of the text value to a numeric value. 
# 

# In[110]:


def insert_predictionstat(conn, values):
    """
    See description in part 9
    """
    cur = conn.cursor()
    sel = "INSERT INTO PredictionStats (VariantID, PredictorName, PredictorValue) VALUES (?, ?, ?)"
    cur.execute(sel,values)
    
#     ls = []
#     cur = conn.cursor()
#     sel = "SELECT PredictorStatsID FROM PredictionStats ORDER BY PredictorStatsID DESC LIMIT 1"
#     cur.execute(sel)
#     m = cur.fetchall()
#     if m == []:
#         m = 0
#     else:
#         m = m[0][0]
#     m = m+1
#     ls.append(m)
#     for i in values:
#         ls.append(i)
#     ls = tuple(ls)
#     with conn:
#         transfer = "INSERT INTO PredictionStats VALUES(?,?,?,?)"
#         cur.execute(transfer, ls)
    


# # Part 10 (No Points)
# 
# Write a function to insert records into both the variants and predictor_stats table. 
# Hint:
# 1) Open connection to database  
# 2) Read file one line at a time using gzip read
# 3) Extract CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO
# 4) Use the pull_info_values function
# 5) Use build_values_list 
# 6) Use insert_variant -- save variant_id
# 7) Use insert_predictionstat -- insert each predictor at a time and remember to use `prediction_mapping` mapping. 
# 
# 
# 
# 
# ```
# 
# prediction_mapping = {
#     'FATHMM_pred': {'T': 0, 'D': 1},
#     'MetaLR_pred': {'T': 0, 'D': 1},
#     'MetaSVM_pred': {'T': 0, 'D': 1},
#     'SIFT_pred': {'T': 0, 'D': 1},
#     'fathmm_MKL_coding_pred': {'D': 1, 'N': 0},
#     'LRT_pred': {'U': 0, 'N': 0, 'D': 1},
#     'MutationAssessor_pred': {'H': 1, 'N': 0, 'L': 0.25, 'M': 0.5},  
#     'MutationTaster_pred': {'D': 1, 'P': 0, 'N': 0, 'A': 1},
#     'PROVEAN_pred': {'D': 1, 'N': 0},
#     'Polyphen2_HDIV_pred': {'D': 1, 'B': 0, 'P': 0.5},
#     'Polyphen2_HVAR_pred': {'D': 1, 'B': 0, 'P': 0.5},
# }
# 
# 
# ```
# 

# In[113]:


prediction_mapping = {
    'FATHMM_pred': {'T': 0, 'D': 1},
    'MetaLR_pred': {'T': 0, 'D': 1},
    'MetaSVM_pred': {'T': 0, 'D': 1},
    'SIFT_pred': {'T': 0, 'D': 1},
    'fathmm_MKL_coding_pred': {'D': 1, 'N': 0},
    'LRT_pred': {'U': 0, 'N': 0, 'D': 1},
    'MutationAssessor_pred': {'H': 1, 'N': 0, 'L': 0.25, 'M': 0.5},  
    'MutationTaster_pred': {'D': 1, 'P': 0, 'N': 0, 'A': 1},
    'PROVEAN_pred': {'D': 1, 'N': 0},
    'Polyphen2_HDIV_pred': {'D': 1, 'B': 0, 'P': 0.5},
    'Polyphen2_HVAR_pred': {'D': 1, 'B': 0, 'P': 0.5},
}
values_to_pull = [
        'FATHMM_pred',
        'LRT_pred',
        'MetaLR_pred',
        'MetaSVM_pred',
        'MutationAssessor_pred',
        'MutationTaster_pred',
        'PROVEAN_pred',
        'Polyphen2_HDIV_pred',
        'Polyphen2_HVAR_pred',
        'SIFT_pred',
        'fathmm_MKL_coding_pred',
]
tables = values_to_pull

"PULL"
"""expected_solution = {
    'thousandg2015aug_all': '0.024361', 
    'ExAC_ALL': '0.0553', 
    'SIFT_pred': 'D', 
    'Polyphen2_HDIV_pred': 'P', 
    'Polyphen2_HVAR_pred': 'P', 
    'LRT_pred': 'N',
    'MutationTaster_pred': 'D', 
    'MutationAssessor_pred': 'L', 
    'FATHMM_pred': 'T', 
    'PROVEAN_pred': 'N', 
    'MetaSVM_pred': 'T', 
    'MetaLR_pred': 'T', 
    'fathmm_MKL_coding_pred': 'D'
}
"""

"BUILD"
"""CHROM, POS, ID, REF, ALT, QUAL, FILTER = (7, 87837848, '.', 'C', 'A', 418.25, 'PASS') 
info_values = {'SIFT_pred': 'D', 'Polyphen2_HDIV_pred': 'D', 'Polyphen2_HVAR_pred': 'D', 'LRT_pred': 'D', 'MutationTaster_pred': 'D', 'MutationAssessor_pred': 'H', 'FATHMM_pred': 'T', 'PROVEAN_pred': 'D', 'MetaSVM_pred': 'D', 'MetaLR_pred': 'D', 'fathmm_MKL_coding_pred': 'D'}
expected_results = [7, 87837848, '.', 'C', 'A', 418.25, 'PASS', None, None, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1]
"""

def populate_variants_predictorstats_tables(db_file, filename):
    """
    See description in part 10
    """    
    import gzip
    conn = create_connection(db_file)
    cur = conn.cursor()
    with gzip.open(filename,'rt') as fp:
        for line in fp:
            if line.startswith('#') == False:
                llist = line.split('\t')
                infodic = pull_info_values(llist[7])
                ls = build_values_list(llist[0], llist[1], llist[2], llist[3], llist[4], llist[5], llist[6], infodic)
                vid = insert_variant(conn, ls)
                
                for table in tables:
                    value = infodic.get(table)
                    if value:
                        m = prediction_mapping[table][value]
                        app = (vid, table, m)
                        print(app)
                        insert_predictionstat(conn,app)
                

db_file = 'lab2.db'
filename = 'test_4families_annovar.vcf.gz'
populate_variants_predictorstats_tables(db_file, filename)


# In[114]:


import pandas as pd
sel = "SELECT * FROM PredictionStats"
conn = create_connection('lab2.db')
cur = conn.cursor()
df = pd.read_sql_query(sel,conn)
display(df)


# # Part 11 (10 Points)
# 
# Write a function that returns the total number of variants
# 
# 

# In[115]:


def num_of_total_variants(conn):
    # YOUR CODE HERE
    cur = conn.cursor()
    sel = "SELECT COUNT(*) FROM Variants"
    cur.execute(sel)
    rs = cur.fetchall()
    print(rs[0][0])
    return rs[0][0]


# In[116]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert num_of_total_variants(conn) == 50001
conn.close()


# # Part 12 (10 Points)
# Write a function returns the total number of variant predictions -- the count of the predictiostats table. 

# In[117]:


def num_of_total_variant_predictions(conn):
    """
    Part 12
    """
    cur = conn.cursor()
    sel = "SELECT COUNT(*) FROM PredictionStats"
    cur.execute(sel)
    rs = cur.fetchall()
    print(rs[0][0])
    return rs[0][0]
    
db_file = 'lab2.db'
con = create_connection(db_file)
num_of_total_variant_predictions(con)


# In[118]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert num_of_total_variant_predictions(conn) == 1324
conn.close()


# # Part 13 (10 Points)
# Return the total number of variant predictions that have value greater than zero. Number of values from the predictionstats table that are greater than 0. 

# In[119]:


def num_of_total_variant_predictions_with_value_gt_zero(conn):
    """
    See part 13 description
    """
    # YOUR CODE HERE
    sel = "SELECT COUNT(*) FROM PredictionStats WHERE PredictorValue > 0"
    cur = conn.cursor()
    cur.execute(sel)
    rs = cur.fetchall()
    print(rs[0][0])
    return rs[0][0]
    raise NotImplementedError()


# In[120]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert num_of_total_variant_predictions_with_value_gt_zero(conn) == 219
conn.close()


# # Part 14 (10 Points)
# 
# Write a function that given `CHROM, POS, ID, REF, ALT` returns a variant's info with the following columns (column order is important) :
# ```
# Variants.CHROM,
# Variants.POS,
# Variants.ID,
# Variants.REF,
# Variants.ALT,
# Variants.QUAL,
# Variants.FILTER,
# Variants.thousandg2015aug_all,
# Variants.ExAC_ALL,
# FATHMM_pred.prediction,
# LRT_pred.prediction,
# MetaLR_pred.prediction,
# MetaSVM_pred.prediction,
# MutationAssessor_pred.prediction,
# MutationTaster_pred.prediction,
# PROVEAN_pred.prediction,
# Polyphen2_HDIV_pred.prediction,
# Polyphen2_HVAR_pred.prediction,
# SIFT_pred.prediction,
# fathmm_MKL_coding_pred.prediction,
# sum(PredictionStats.PredictorValue)
# ```
# 
# For the predictions, return the actual text value. And the last column is the sum of all the mapped prediction scores for a given variant!
# 
# 

# In[122]:


def fetch_variant(conn, CHROM, POS, ID, REF, ALT):
    """
    See Part 14 description
    """
    # YOUR CODE HERE
    cur = conn.cursor()
    sel = """SELECT Variants.CHROM,
                    Variants.POS,
                    Variants.ID,
                    Variants.REF,
                    Variants.ALT,
                    Variants.QUAL,
                    Variants.FILTER,
                    Variants.thousANDg2015aug_all,
                    Variants.ExAC_ALL,
                    FATHMM_pred.prediction,
                    LRT_pred.prediction,
                    MetaLR_pred.prediction,
                    MetaSVM_pred.prediction,
                    MutationAssessor_pred.prediction,
                    MutationTaster_pred.prediction,
                    PROVEAN_pred.prediction,
                    Polyphen2_HDIV_pred.prediction,
                    Polyphen2_HVAR_pred.prediction,
                    SIFT_pred.prediction,
                    fathmm_MKL_coding_pred.prediction,
                    sum(PredictionStats.PredictorValue)
                    from Variants LEFT JOIN FATHMM_pred USING (FATHMM_predId)
                    LEFT JOIN LRT_pred USING (LRT_predId)
                    LEFT JOIN MetaLR_pred USING (MetaLR_predId)
                    LEFT JOIN MetaSVM_pred USING (MetaSVM_predId)
                    LEFT JOIN MutationAssessor_pred USING (MutationAssessor_predId)
                    LEFT JOIN MutationTaster_pred USING (MutationTaster_predId)
                    LEFT JOIN PROVEAN_pred USING (PROVEAN_predId)
                    LEFT JOIN Polyphen2_HDIV_pred USING (Polyphen2_HDIV_predId)
                    LEFT JOIN Polyphen2_HVAR_pred USING (Polyphen2_HVAR_predId)
                    LEFT JOIN SIFT_pred USING (SIFT_predId)
                    LEFT JOIN fathmm_MKL_coding_pred USING (fathmm_MKL_coding_predId)
                    LEFT JOIN PredictionStats USING (VariantID)
                    WHERE Variants.CHROM=? AND Variants.POS=? AND Variants.ID=? AND Variants.REF=? AND Variants.ALT=?"""
    cur.execute(sel,(CHROM,POS,ID,REF,ALT))
    rs = cur.fetchall()
    if len(rs)==1:
        print(rs[0])
        return rs[0]
#     else:
#         sel = """SELECT Variants.CHROM,
#                     Variants.POS,
#                     Variants.ID,
#                     Variants.REF,
#                     Variants.ALT,
#                     Variants.QUAL,
#                     Variants.FILTER,
#                     Variants.thousANDg2015aug_all,
#                     Variants.ExAC_ALL,
#                     FATHMM_pred.prediction,
#                     LRT_pred.prediction,
#                     MetaLR_pred.prediction,
#                     MetaSVM_pred.prediction,
#                     MutationAssessor_pred.prediction,
#                     MutationTaster_pred.prediction,
#                     PROVEAN_pred.prediction,
#                     Polyphen2_HDIV_pred.prediction,
#                     Polyphen2_HVAR_pred.prediction,
#                     SIFT_pred.prediction,
#                     fathmm_MKL_coding_pred.prediction,
#                     NULL
#                     from Variants LEFT JOIN FATHMM_pred USING (FATHMM_predId)
#                     LEFT JOIN LRT_pred USING (LRT_predId)
#                     LEFT JOIN MetaLR_pred USING (MetaLR_predId)
#                     LEFT JOIN MetaSVM_pred USING (MetaSVM_predId)
#                     LEFT JOIN MutationAssessor_pred USING (MutationAssessor_predId)
#                     LEFT JOIN MutationTaster_pred USING (MutationTaster_predId)
#                     LEFT JOIN PROVEAN_pred USING (PROVEAN_predId)
#                     LEFT JOIN Polyphen2_HDIV_pred USING (Polyphen2_HDIV_predId)
#                     LEFT JOIN Polyphen2_HVAR_pred USING (Polyphen2_HVAR_predId)
#                     LEFT JOIN SIFT_pred USING (SIFT_predId)
#                     LEFT JOIN fathmm_MKL_coding_pred USING (fathmm_MKL_coding_predId)
#                     LEFT JOIN PredictionStats USING (VariantID)
#                     WHERE Variants.CHROM=? AND Variants.POS=? AND Variants.ID=? AND Variants.REF=? AND Variants.ALT=?"""
#         cur.execute(sel,(CHROM,POS,ID,REF,ALT))
#         rs = cur.fetchall()
#         if len(rs)==1:
#             print(rs[0])
#             return rs[0]


# In[124]:


import pandas as pd
conn = create_connection('lab2.db')
cur = conn.cursor()
sel = """SELECT * FROM Variants WHERE VariantID = 614"""
df = pd.read_sql_query(sel,conn)
display(df)


# In[125]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert fetch_variant(conn, '22', 25599849, 'rs17670506', 'G', 'A') == ('22', 25599849, 'rs17670506', 'G', 'A', 3124.91, 'PASS', 0.0251597, 0.0425, 'D', 'D', 'T', 'T', 'M', 'D', 'D', 'D', 'D', 'D', 'D', 8.5)
conn.close()


# In[ ]:





# In[126]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert fetch_variant(conn, 'X', 2836184, 'rs73632976', 'C', 'T') == ('X', 2836184, 'rs73632976', 'C', 'T', 1892.12, 'PASS', None, 0.0427, 'D', 'U', 'D', 'T', 'M', 'P', 'D', 'P', 'P', 'D', 'D', 6.5)
conn.close()


# In[127]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert fetch_variant(conn, '5', 155935708, 'rs45559835', 'G', 'A') == ('5', 155935708, 'rs45559835', 'G', 'A', 1577.12, 'PASS', 0.0189696, 0.0451, 'D', 'D', 'T', 'T', 'L', 'D', 'D', 'P', 'B', 'T', 'D', 5.75)
conn.close()


# In[128]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert fetch_variant(conn, '4', 123416186, '.', 'A', 'G') == ('4', 123416186, '.', 'A', 'G', 23.25, 'PASS', None, None, None, None, None, None, None, None, None, None, None, None, None, None)
conn.close()


# # Part 15 (10 Points)
# Write a function that returns the variant with the highest predictor score sum. 
# 
# Return the variant info the following order:
# ```
# Variants.CHROM,
# Variants.POS,
# Variants.ID,
# Variants.REF,
# Variants.ALT,
# Variants.QUAL,
# Variants.FILTER,
# Variants.thousandg2015aug_all,
# Variants.ExAC_ALL,
# FATHMM_pred.prediction,
# LRT_pred.prediction,
# MetaLR_pred.prediction,
# MetaSVM_pred.prediction,
# MutationAssessor_pred.prediction,
# MutationTaster_pred.prediction,
# PROVEAN_pred.prediction,
# Polyphen2_HDIV_pred.prediction,
# Polyphen2_HVAR_pred.prediction,
# SIFT_pred.prediction,
# fathmm_MKL_coding_pred.prediction,
# sum(PredictionStats.PredictorValue)
#         
# ```
# 
# Again, return the predictor text values and the last column is the sum of the prediction values. 

# In[134]:


def variant_with_highest_sum_of_predictor_value(conn):
    """
    See part 15 description 
    """
    # YOUR CODE HERE
    sel = """SELECT Variants.CHROM,Variants.POS,Variants.ID,Variants.REF,Variants.ALT,Variants.QUAL,Variants.FILTER,Variants.thousandg2015aug_all,Variants.ExAC_ALL,FATHMM_pred.prediction,LRT_pred.prediction,MetaLR_pred.prediction,MetaSVM_pred.prediction,MutationAssessor_pred.prediction,MutationTaster_pred.prediction,PROVEAN_pred.prediction,Polyphen2_HDIV_pred.prediction,Polyphen2_HVAR_pred.prediction,SIFT_pred.prediction,fathmm_MKL_coding_pred.prediction,sum(PredictionStats.PredictorValue) from Variants,FATHMM_pred,LRT_pred,MetaLR_pred,MetaSVM_pred,MutationAssessor_pred,MutationTaster_pred,ProVEAN_pred,polyphen2_HDIV_pred,polyphen2_HVAR_pred,sift_pred,fathmm_MKL_coding_pred, PredictionStats where  FATHMM_pred.FATHMM_predID=Variants.FATHMM_predID and LRT_pred.LRT_predID=Variants.LRT_predID and MetaLR_pred.MetaLR_predID=Variants.MetaLR_predID and MetaSVM_pred.MetaSVM_predID=Variants.MetaSVM_predID and MutationAssessor_pred.MutationAssessor_predID = Variants.MutationAssessor_predID and MutationTaster_pred.MutationTaster_predID= Variants.MutationTaster_predID and PROVEAN_pred.PROVEAN_predID= Variants.PROVEAN_predID and Polyphen2_HDIV_pred.Polyphen2_HDIV_predID=Variants.Polyphen2_HDIV_predID and Polyphen2_HVAR_pred.Polyphen2_HVAR_predID = Variants.Polyphen2_HVAR_predID and SIFT_pred.SIFT_predID= Variants.SIFT_predID and fathmm_MKL_coding_pred.fathmm_MKL_coding_predID = Variants.fathmm_MKL_coding_predID and Variants.VariantID=PredictionStats.VariantID group by PredictionStats.VariantID order by sum(PredictionStats.PredictorValue) desc limit 1"""
    cur = conn.cursor()
    cur.execute(sel)
    rs = cur.fetchall()
    ls = []
    ls.append(rs[0][0])
    ls.append(rs[0][1])
    ls.append(rs[0][2])
    for i in range(3,len(rs[0])):
        if rs[0][i] != '.':
            ls.append(rs[0][i])
        else:
            ls.append(None)
    print(tuple(ls))
    return tuple(ls)


# In[135]:


db_file = 'lab2.db'
conn = create_connection(db_file)
assert variant_with_highest_sum_of_predictor_value(conn) == ('7', 87837848, '.', 'C', 'A', 418.25, 'PASS', None, None, 'T', 'D', 'D', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 10.0)
conn.close()


# In[ ]:




