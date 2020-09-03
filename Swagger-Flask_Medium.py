#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries

# In[ ]:


#--Step--1
###################################################################################################
import numpy as np
import pandas as pd
# from flask import Flask, render_template
# from flask_restplus import Api, Resource
import os
import re
# from difflib import SequenceMatcher
import nltk
# nltk.download()
import string
from fuzzywuzzy import fuzz
from nltk import word_tokenize
import string
###################################################################################################


# ### Read Dataset (Knowledge base)

# In[ ]:


#--Step--2
###################################################################################################
os.chdir("D:/Soliton/Soliton Work/previous work/Problems/")
data=pd.read_excel('ECQ_Meditech/Dictionary (eCQM).xlsx')
df=pd.DataFrame(data)
###################################################################################################


# ### Work -- Text Processing 

# In[ ]:


#--Step--3
###################################################################################################
exclude = set(string.punctuation)
#----------------------------------remove punctuation---------------

def remove_punctuation(x):
    """
    Helper function to remove punctuation from a string
    x: any string
    """
    try:
        x = ''.join(ch for ch in x if ch not in exclude)
    except:
        pass
    return x
prob_data= df['ProblemDisplayName'].apply(remove_punctuation)

prob_data=prob_data.astype(str).str.lower()
#----------------------------------remove punctuation END---------------
stopwords=['-on-','-','in','at','on','and','with','of','to','diabetic','other','unspecified','disorder','procedure',
           'finding','uti','views','view','vw','mri','mr','nm',
          'ip','note','ir','ext','vas','(',')','ap','y','[',']','pa','v',
#           ] 
           'due','arf','r','ckd',
           'alc','chf','cva','esrd','dvt','paf','h/o','bmi',
           's/p','hx','pe','sebsequent','very','hrt','rvr','tia','situation','severe',]

#-------Text normalization--------

problem_data = []
for a in prob_data:
    text1 = a.split()
    ################---text1 Processing----------
    text1 = " ".join(text1)
    text1=text1.replace('1','one')
    text1=text1.replace('2','two')
    text1=text1.replace('3','three')
    text1=text1.replace('4','four')
    text1=text1.replace('5','five')
    text1=text1.replace('6','six')
    text1=text1.replace('7','seven')
    text1=text1.replace('8','eight')
    text1=text1.replace('9','nine')
    text1=text1.replace('0','zero')
    text1=text1.replace('15','fifteen')
#     text1=text1.replace('%2F','/')
    text_tokens = word_tokenize(str(text1))
    tokens_without_sw = [word for word in text_tokens if not word in stopwords]
    text1 = (" ").join(tokens_without_sw)
    problem_data.append(text1)
###################################################################################################
print("---Run---")


# ### Work -- String Matching with Fuzzy Logics using Client (testing) Problem and return the final output

# In[ ]:


#--step--4
def get_data(ProblemDisplayName):
    import time
    t0=time.time()
    lis=[]
    result={}
    problem=[]
    Client_problem= remove_punctuation(ProblemDisplayName)
    Client_problem=Client_problem.lower()
    data = Client_problem.split()
    ################---text1 Processing----------
    data = " ".join(data)
    data=data.replace('1','one')
    data=data.replace('2','two')
    data=data.replace('3','three')
    data=data.replace('4','four')
    data=data.replace('5','five')
    data=data.replace('6','six')
    data=data.replace('7','seven')
    data=data.replace('8','eight')
    data=data.replace('9','nine')
    data=data.replace('0','zero')
    data=data.replace('15','fifteen')
    data=data.replace('single','one')
    data=data.replace('sinus','Sinuses')
    data=data.replace('arteries','artery')        
    data=data.replace('venous','vein')        
    data=data.replace('arches','arch')
    data=data.replace('bilat','bilateral')    
    data=data.replace('arterial','artery')  
    data=data.replace('bones','bone')
    data=data.replace('feet','foot')
    data=data.replace('2f','-')
    data=data.replace('/','')
    text_tokens1 = word_tokenize(str(data))
    tokens_without_sw1 = [word for word in text_tokens1 if not word in stopwords]
    data = (" ").join(tokens_without_sw1)
    problem.append(data)
#     print(problem)
    count=0 
    for cp in problem:
        data=cp.split()
        data.sort()   
        client_prob=" ".join(data)
    for data1 in problem_data:
        data1=data1.split(" ")
        data1.sort()
        data1=" ".join(data1)
        count=count+1
        res=fuzz.ratio(client_prob,data1)
#         len_res=len(str(res))
        if res>=100:
#              result[res]=count
# #         print(result1)
# #         print("length:",res_len)
#     if len(result)>0:  
#         max_key1=max(result)
#         for key, val in result.items():
#             if key==max_key1:
            index2=(count-1)
            Code=df['ProblemCode'][index2]
            CodeSystem=df['ProblemCodeSystemName'][index2]
            EnterProblem=Client_problem
            FindingProblem= df['ProblemDisplayName'][index2]
            Result=res
            t1=time.time()
            lis.append(Code)
            lis.append(CodeSystem)
            lis.append(EnterProblem)
            lis.append(FindingProblem)
            lis.append(t1-t0)
    return lis


# ### Import Swagger API store and Display the Resutls with Swagger Documentation

# In[ ]:


#--Step--5    ----Problem----
from flask import Flask
from flask_restplus import Api, Resource
flask_app = Flask(__name__)
api = Api(app = flask_app)
###################################################################################################
name_space = api.namespace('Persivia-APP', description='Web Service to Codified Non Codify Data')
@name_space.route("/Problem/v1/<string:ProblemDisplayName>")
class MainClass1(Resource):
    def get(self, ProblemDisplayName):
        data=get_data(ProblemDisplayName)
        if data:
            return{
    #         "Status": "Got the Problem results..!",
            'ProvidedDisplayName':data[2],'DisplayName':data[3],'code':data[0],'CodeSystem':data[1],'Response TIme':data[4] }
        else:
            return "null"
              
if __name__ == '__main__':
    flask_app.run(port=7000)


# In[ ]:




