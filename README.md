# PI01_DATA_FT14



## **DESARROLLO DEL PROYECO INDIVIDUAL ** :white_circle:

### **1. Etapa del proceso ETL** :

- Cargamos los archivos con extensión .json con las libererias de json y pandas.
- Luego se realizó el trabajo ETL(Extracción, Transformación y Carga)
- Se verificó que algunas columnas presentan valores de tipo arreglo como lo presentó la columna 'genres' y se desanidaron. 
- Se realizaron transformaciones como por ejemplo se dio formato de fechas '%Y-%m-%d' a la columna 'posted'.
- Se Eliminaron las columnas que no eran explicativas para el proyecto.
- Luego de las transformaciones y normalización de los datos se exportaron los archivos serializados para el consumo de la API.


### **2. Etapa de Desarrollo API** :

Se utilizó el framework FastAPI para la implementación de la API, y se crearon las siguientes funciones:

* **userdata**: Esta función recibe el 'user_id' y retorna la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a la columna recommend y la cantidad de items asociadas al usuario.

* **countreviews**: Esta función recibe un rango de fechas para consultar la cantidad de usuarios que realizaron reviews en ese periodo, y el porcentaje de las recomendaciones en base a la columna recommend.

* **genre**: Esta función recibe el género del videojuego y devuelve el puesto del género de acuerdo al ranking que está basado en la cantidad de horas jugadas (columna PlayTimeForever).

* **userforgenre**: Esta función recibe como parámetro el género de un videojuego y devuelve el top 5 de los usuarios con más horas de juego en el género ingresado, indicando el id del usuario y el url de su perfil.

* **developer**: Esta función recibe como parámetro 'developer', que es la empresa desarrolladora del juego, y devuelve la cantidad de items que desarrolla dicha empresa y el porcentaje de contenido Free por año por sobre el total que desarrolla.

* **sentiment_analysis**: Esta función recibe como parámetro el año de lanzamiento de un juego y según ese año devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento, como Negativo, Neutral y Positivo.

* **recomendacion_juego**: Esta función recibe como parámetro el nombre de un juego y devuelve una lista con 5 juegos recomendados similares al ingresado.

* **recomendacion_usuario**: Esta función recibe como parámetro el id de un usuario y devuelve una lista con 5 juegos recomendados para dicho usuario teniendo en cuenta las similitudes entre los usuarios.




**Este repositorio incluye:**

+ Un análisis exploratorio de datos (EDA)<br/>
+ El proceso de ETL paso a paso<br/>
+ Notebooks para su visualización<br/>
+ Desarrollo de una API cons FastApi<br/>
+ Implementación<br/>



## Detalles adicionales del proyecto

Aquí se muestra información adicional y recursos relacionados con el proyecto:

1. `Video explicativo:` Se ha creado un [video explicativo](https://...)  donde te muestro algunas funciones de mi proyecto con el uso de la API.

2. `Acceso a la API:` En el siguiente [enlace de la API](https://pi01-data-ft14-jcr.onrender.com/) podras encontrar las funciones de este proyecto.

3. `Obtención de datos originales:` Los datos utilizados para este proyecto de análisis, estan en el siguiente [enlace de descarga](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) 