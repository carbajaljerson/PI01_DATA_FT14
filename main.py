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
    
with open("data/dataUserGenre.pkl", "rb") as file3:
    dataUserGenre= pickle.load(file3)
    
with open("data/dataDevYear.pkl", "rb") as file4:
    dataDevYear= pickle.load(file4)
    
with open("data/dataDevItem.pkl", "rb") as file5:
    dataDevItem= pickle.load(file5)
    
with open("data/dataFreeYear.pkl", "rb") as file6:
    dataFreeYear= pickle.load(file6)


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
    
    sumUserGenres = dataUserGenre[dataUserGenre['genres'] == genre]
    result = pd.DataFrame(sumUserGenres).reset_index()
    result = result.sort_values('playtime_forever')
    result=result.tail(5).reset_index()
    
    top5Users =[]
    cont =  len(result)-1
    while cont>=0:       
        #top5Users.append(result.user_id[cont])
        top5Users.append({'User': result.user_id[cont],'Url': result.user_url[cont]})
        cont=cont-1
    
    return {'Top 5 Usuarios':top5Users}

@app.get('/developer/')
def developer(developer:str):
    
    
    
    #dataDeveloper = data[data['developer']== developer]
    
    #itemsPearYear = dataDeveloper.groupby('release_year')['item_id'].nunique()
    itemsPearYear =  dataDevYear[dataDevYear['developer']== developer]
    
    #cantidadItems = dataDeveloper.groupby('developer')['item_id'].nunique()
    cantidadItems =  dataDevItem[dataDevItem['developer']== developer]
    
    
    #itemsFreePearYear = dataDeveloper[dataDeveloper['price']==0].groupby('release_year')['item_id'].nunique()
    itemsFreePearYear = dataFreeYear[dataFreeYear['developer']== developer]
    
    porcentaje= (itemsFreePearYear/itemsPearYear)*100
    
    rowPercent = []
    for anio in itemsPearYear.index:
        
        percentFree = porcentaje.get(anio)
        
        if np.isnan(percentFree):        
            rowPercent.append({'Año': anio,'Contenido Free':'0.00%'})
        
        else:
            rowPercent.append({'Año': anio,'Contenido Free':f"{percentFree:.2f}%"})

    return {'Cantidad Items': str(cantidadItems.iloc[0]),'Porcentaje Contenido Free': rowPercent}

@app.get('/sentiment/')
def sentiment_analysis(year:int):
    
    pass



@app.get('/recomendacion/')
def recomendacion(idItem:str):
    
    pass

#uvicorn main:app
