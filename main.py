

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



with open("data/steamGames.pkl", "rb") as file:
    dataGames = pickle.load(file)
    
with open("data/steamItems.pkl", "rb") as file:
    dataItems = pickle.load(file)
    
with open("data/steamReviews.pkl", "rb") as file:
    dataReviews = pickle.load(file)
    
dataUser = pd.merge(dataItems,dataReviews,on=['user_id','item_id','user_url'],how='outer')    
    
    
##DataFrame UserData
dfGames=dataGames[['item_id','price','items_count']]
dfUser =dataUser[['item_id','user_id','recommend']]
dfUserData = pd.merge(dfUser,dfGames,on='item_id',how='outer')

dfUserData = dfUserData.dropna(subset=['user_id'])
dfUserData = dfUserData.reset_index(drop=True)
dfUserData = dfUserData.drop_duplicates()
dfUserData.reset_index(drop=True,inplace=True)
dfUserData['price'] = dfUserData['price'].replace(np.nan, 0)
###DataFrame UserData


data = pd.merge(dataUser,dataGames,on='item_id',how='outer')



##DataFrame Sentiment
dfGamesSentiment=dataGames[['item_id','release_year']]
dfUserSentiment =dataUser[['item_id','user_id','sentiment_analysis']]
dataSentiment = pd.merge(dfUserSentiment,dfGamesSentiment,on='item_id',how='outer')

dataSentiment = dataSentiment.dropna(subset=['user_id'])
dataSentiment = dataSentiment.reset_index(drop=True)

dataSentiment = dataSentiment.dropna(subset=['release_year'])
dataSentiment = dataSentiment.reset_index(drop=True)
dataSentiment['sentiment_analysis'].fillna(1, inplace=True)
##DataFrame Sentiment



##DataFrame Recomendación
dataRec =data[['item_id','item_name','genres']]
#dataRec['item_id']=dataRec['item_id'].astype(str)
dataRec =dataRec.drop_duplicates()
dataRec=dataRec.dropna()
dataRec=dataRec.reset_index(drop=True)
##DataFrame Recomendación

@app.get('/')
def index():
    return {'message': 'Proyecto Individual de Jerson Carbajal Ramirez'}


@app.get('/{name}')
def get_name(name: str):
    return {'Desarrollado por Jerson Carbajal Ramirez': f'{name}'}


@app.get('/userId/')
def userdata(userId:str):
    #Se ingresa el userId, retornando el monto gastado por el usuario, porcentaje de recomendación y cantidad de Items'''
    
    cantidad= dfUserData[dfUserData['user_id']==userId].groupby('user_id')['item_id'].nunique().iloc[0]
    porcentaje = round(((dfUserData.loc[dfUserData["user_id"] == userId].recommend.sum())/(len(dfUserData.loc[dfUserData["user_id"] == userId]))),2)*100
    #cantidad = (dfUserData['items_count'].loc[dfUserData["user_id"] == userId]).max()
    gastoTotal = round(dfUserData['price'].loc[dfUserData["user_id"] == userId].sum(),2)
    
   
    return {'Usuario':userId, 'Gasto Total':gastoTotal, 'Porcentaje de recomendación (%)':porcentaje, 'Cantidad de Items':int(cantidad)}

@app.get('/rangeDate/')
def countreviews(fechaInicio:str, fechaFin:str):
    
    #Se ingresa el rango de Fechas, retornando el cantidad de Usuarios y el porcentaje de recomendación
    
    mask = (data['posted'] >= fechaInicio) & (data['posted'] <= fechaFin)
    cantidad =  len(pd.DataFrame(data.loc[mask])['user_id'].unique())
    porcentaje = round(((data.loc[mask].recommend.sum())/(cantidad)),2)*100
    

    return {'Cantidad de usuarios':cantidad, 'Porcentaje de recomendación (%)':porcentaje}


@app.get('/genre/')
def genre(genreRanking:str):
    
    sumGenres = data.groupby('genres').playtime_forever.agg('sum')
    sumGenres = sumGenres.sort_values(ascending=False)
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
    
    sumUserGenres = data[data['genres'] == genre].groupby(['user_id']).playtime_forever.agg('sum')
    result = pd.DataFrame(sumUserGenres).reset_index()
    result = result.sort_values('playtime_forever')
    result=result.tail(5).reset_index()
    
    top5Users =[]
    cont =  len(result)-1
    while cont>=0:
        top5Users.append(result.user_id[cont])
        cont=cont-1
    
    return {'Top 5 Usuarios':top5Users}

@app.get('/developer/')
def developer(developer:str):
    
    data['release_year']=data['release_year'].astype(str)
    
    dataDeveloper = data[data['developer']== developer]
    itemsPearYear = dataDeveloper.groupby('release_year')['item_id'].nunique()
    
    cantidadItems = dataDeveloper.groupby('developer')['item_id'].nunique()
    
    itemsFreePearYear = dataDeveloper[dataDeveloper['price']==0].groupby('release_year')['item_id'].nunique()
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
    tfidf_matriz = vectorizar.fit_transform(dataRec['genres'])
  
    #Tanto el linear_kernel como la cosine_similarity produjeron el mismo resultado
    #Sin embargo, linear_kernel tardó menos en ejecutarse
    
    cosineSim = linear_kernel(tfidf_matriz,tfidf_matriz)
        
    #Asignar vectores de características a item_id   
    indices = pd.Series(dataRec.index, index=dataRec['item_id']).drop_duplicates()
    
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
    result=dataRec['item_name'].iloc[itemIndices].values
    
    return dict(enumerate(result.flatten(), 1))

#uvicorn main:app