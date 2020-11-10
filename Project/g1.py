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

for line in r1:
    flag=0
    lsofdrugs=[]
    for ele in line:
        if ele[4]== TRUE:   #Did they die from heroin
            HeroinAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Heroin")
        elif ele[5]== TRUE:
            CocainAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Cocain")
        elif ele[6]== TRUE:
            FentanylAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Fentanyl")
        elif ele[7]== TRUE:
            OxycodoneAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Oxycodone")
        elif ele[8]== TRUE:
            OxymorphoneAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Oxymorphone")
        elif ele[9]== TRUE:
            EtOHAges.append(ele[1])
            flag=+1
            lsofdrugs.append("EtOH")
        elif ele[10]== TRUE:
            HydrocodoneAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Hydrocodone")
        elif ele[12]== TRUE:
            BenzodiazepineAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Benzodiazepine")
        elif ele[12]== TRUE:
            MethadoneAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Methadone")
        elif ele[13]== TRUE:
            AmphetAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Amphet")
        elif ele[14]== TRUE:
            TramadAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Tramad")
        elif ele[15]== 'MORPHINE' or 'MORPH':
            MorphineAges.append(ele[1])
            flag=+1
            lsofdrugs.append("Morphine")
        if flag>= 2:
            Mixed.append('ele[0]':{ele[1],ele[2],flag})

agelist=(HeroinAges,CocainAges,FentanylAges,OxycodoneAges,OxymorphoneAges,EtOHAges,HydrocodoneAges,BenzodiazepineAges,MethadoneAges,AmphetAges, TramadAges, MorphineAges)

for i in agelist:
    df = pd.DataFrame({'freq': i })
    df.groupby('freq', as_index=False).size().plot(kind='bar')
    plt.show()

import matplotlib.pyplot as plt

colors = list("rgbcmyk")

for data_dict in Mixed.values():
   x = data_dict.keys()
   y = data_dict.values()
   plt.scatter(x,y,color=colors.pop())

plt.show()
