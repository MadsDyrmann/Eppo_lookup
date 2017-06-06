# -*- coding: utf-8 -*-
"""
@author: Mads Dyrmann

Version 0.1

Build hierarchy of EPPO codes.


"""

import pandas as pd
import sqlite3 as lite



class eppoplant():
    def __init__(self):
        self.children=[]
        self.codeid=''
        self.eppocode=''


def buildParentHierarchy(eppocode, t_links_df, t_codes_df):
    
    plant=eppoplant()
    plant.eppocode=eppocode
    
        
    newParant=True
    
    while newParant:
        #Get id of current top-most plant       
        codeid = t_codes_df.loc[t_codes_df.eppocode==plant.eppocode].codeid
        
        if len(codeid)>0:
            codeid=codeid.iloc[0]
        
            plant.codeid=codeid
            
            #Look-up codeid in order to find parent
            parent_codeid =  t_links_df.loc[t_links_df.codeid==codeid].codeid_parent
            if len(parent_codeid)>0:
                parent_codeid=parent_codeid.iloc[0]
                newParant=True
                
                newparentplant=eppoplant()
                newparentplant.children.append(plant)
                newparentplant.codeid = parent_codeid               
                newparentplant.eppocode = t_codes_df.loc[t_codes_df.codeid==parent_codeid].eppocode.iloc[0]
                
                plant = newparentplant
            else:
                newParant=False

    return plant
    



with lite.connect("eppocodes.sqlite") as con:
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    sql = "SELECT * FROM t_codes"
    t_codes_df = pd.read_sql(sql, con)

    sql = "SELECT * FROM t_links"
    t_links_df = pd.read_sql(sql, con)    
 


##################################
##################################

#code is the eppo code. planthierarchy is a plant object instance, containing the parents for the code in question
code='BRSNN' #Raps  
planthierarchy = buildParentHierarchy(eppocode=code, t_links_df=t_links_df, t_codes_df=t_codes_df)
    
    
