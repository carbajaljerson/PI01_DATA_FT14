

# 1. Library imports
import uvicorn
from fastapi import FastAPI
import numpy as np
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

# Creacion del objecto FastAPI
app = FastAPI()

#pickle_in = open("classifier.pkl","rb")
#classifier=pickle.load(pickle_in)

with open("data/dataUser.pkl", "rb") as file1:
    dataUser= pickle.load(file1)



@app.get('/')
def index():
    return {'message': 'Proyecto Individual de Jerson Carbajal Ramirez'}


@app.get('/{name}')
def get_name(name: str):
    return {'Desarrollado por Jerson Carbajal Ramirez': f'{name}'}


@app.get('/userId/')
def userdata(userId:str):
    #Se ingresa el userId, retornando el monto gastado por el usuario, porcentaje de recomendación y cantidad de Items'''
    
    cantidad= dataUser[dataUser['user_id']==userId].groupby('user_id')['item_id'].nunique().iloc[0]
    porcentaje = round(((dataUser.loc[dataUser["user_id"] == userId].recommend.sum())/(len(dataUser.loc[dataUser["user_id"] == userId]))),2)*100
    #cantidad = (dataUser['items_count'].loc[dataUser["user_id"] == userId]).max()
    gastoTotal = round(dataUser['price'].loc[dataUser["user_id"] == userId].sum(),2)
    
   
    return {'Usuario':userId, 'Gasto Total':gastoTotal, 'Porcentaje de recomendación (%)':porcentaje, 'Cantidad de Items':int(cantidad)}

@app.get('/rangeDate/')
def countreviews(fechaInicio:str, fechaFin:str):
    
    pass


@app.get('/genre/')
def genre(genreRanking:str):
    
    pass
    

@app.get('/userforgenre/')
def userforgenre(genre:str):
    
    pass

@app.get('/developer/')
def developer(developer:str):
    
    pass

@app.get('/sentiment/')
def sentiment_analysis(year:int):
    
    pass



@app.get('/recomendacion/')
def recomendacion(idItem:str):
    
    pass

#uvicorn main:app
