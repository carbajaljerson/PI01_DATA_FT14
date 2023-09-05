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
    
with open("data/dataSentiment.pkl", "rb") as file7:
    dataSentiment= pickle.load(file7)
    
with open("data/dataRecomend.pkl", "rb") as file8:
    dataRecomend= pickle.load(file8)


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
        
        top5Users.append({'User': result.user_id[cont],'Url': result.user_url[cont]})
        cont=cont-1
    
    return {'Top 5 Usuarios':top5Users}

@app.get('/developer/')
def developer(developer:str):
    
    itemsPearYear =  dataDevYear[dataDevYear['developer']== developer]
    itemsPearYear = itemsPearYear.set_index('release_year')['item_id']
        
    cantidadItems =  dataDevItem[dataDevItem['developer']== developer]
    cantidadItems =  cantidadItems.set_index('developer')['item_id']
       
    itemsFreePearYear = dataFreeYear[dataFreeYear['developer']== developer]
    itemsFreePearYear = itemsFreePearYear.set_index('release_year')['item_id']
    
    porcentaje= (itemsFreePearYear/itemsPearYear)*100
    
    rowPercent = []
    
    for anio in itemsPearYear.index:
        
        percentFree = porcentaje.get(anio)
        
        if np.isnan(percentFree):        
            rowPercent.append({'Año': anio,'Contenido Free':'0.00%'})
        
        else:
            rowPercent.append({'Año': anio,'Contenido Free':f"{percentFree:.2f}%"})

    return {'Cantidad Items': str(cantidadItems.sum()),'Porcentaje Contenido Free': rowPercent}

@app.get('/sentiment/')
def sentiment_analysis(year:int):
    
    dfSentiment = dataSentiment[dataSentiment['release_year']== year]
    resultado=dfSentiment['sentiment_analysis'].value_counts()

    for i, valor in resultado.items():
        if(i==2):
            positivo = valor
        elif (i==1):
            neutral = valor
        elif (i==0):
            negativo = valor

    return {'Negativo': int(negativo) ,'Neutral': int(neutral), 'Positve':int(positivo)}


@app.get('/recomendacion/')
def recomendacion(idItem:str):
    
    #Min_df requiere que un término aparezca para que se considere parte del vocabulario.
    #Max_df excluye términos que son demasiado frecuentes y que es poco probable que ayuden a predecir la etiqueta
    #ngram_range=(1,2) Donde un bigrama es un par de palabras adyacentes en un texto
    
    vectorizar = TfidfVectorizer(min_df=10, max_df=0.5, ngram_range=(1,2))
    tfidf_matriz = vectorizar.fit_transform(dataRecomend['genres'])
  
    #Tanto el linear_kernel como la cosine_similarity produjeron el mismo resultado
    #Sin embargo, linear_kernel tardó menos en ejecutarse
    
    cosineSim = linear_kernel(tfidf_matriz[:1000,:])
        
    #Asignar vectores de características a item_id   
    indices = pd.Series(dataRecomend.index, index=dataRecomend['item_id']).drop_duplicates()
    
    if (indices[idItem].size > 1):
        idx =indices[idItem].iloc[0]
    else:
        idx = indices[idItem]
    
    # Obtener las puntuaciones de similitud por pares
    simScores = list(enumerate(cosineSim[idx]))
    
    # Ordena los juegos según las puntuaciones de similitud.
    simScores = sorted(simScores, key=lambda x: x[1], reverse=True)
    
    # Obtener las puntuaciones de los 10 juegos más similares
    simScores = simScores[1:11]
    
    # Obtener los  indices de los juegos
    itemIndices = [i[0] for i in simScores]
    
    # Retornar el top 10 de los juegos con similitud
    result=dataRecomend['app_name'].iloc[itemIndices].values
    
    return dict(enumerate(result.flatten(), 1))


#uvicorn main:app
