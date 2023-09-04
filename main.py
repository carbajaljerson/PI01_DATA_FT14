# Library imports

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



with open("data/dataUser.pkl", "rb") as file1:
    dataUser= pickle.load(file1)

with open("data/dataGenres.pkl", "rb") as file2:
    dataGenres= pickle.load(file2)
    

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
    
    #Se ingresa el rango de Fechas, retornando el cantidad de Usuarios y el porcentaje de recomendación
    
    mask = (dataUser['posted'] >= fechaInicio) & (dataUser['posted'] <= fechaFin)
    cantidad =  len(pd.DataFrame(dataUser.loc[mask])['user_id'].unique())
    porcentaje = round(((dataUser.loc[mask].recommend.sum())/(cantidad)),2)*100
    
    return {'Cantidad de usuarios':cantidad, 'Porcentaje de recomendación (%)':porcentaje}


@app.get('/genre/')
def genre(genreRanking:str):
    
    #sumGenres = dataGenres
    sumGenres = dataGenres.sort_values(ascending=False)
    result = pd.DataFrame(sumGenres).reset_index()
    
    index=None
    for i in range(len(result)):
        if (result.genres[i]==genreRanking):
            index=i
            break   
    
    puesto = str(index+1)
    return {'Puesto del Género':puesto}
    

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
