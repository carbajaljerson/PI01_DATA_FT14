# PI01_DATA_FT14



## **DESARROLLO DEL PROYECO INDIVIDUAL ** :white_circle:

### **1. Etapa del proceso ETL** :arrow_right:

- Cargamos el archivos csv con la libereria pandas.
- Luego hacemos todo el trabajo ETL(Extract,Transform,Load)
- Pasamos los valores nulos o vacios de 'revenue' con 0 y igualmente lo hacemos con la columna 'budget'.
- Reordenamos el orden de fecha como nos piden al formato '%Y-%m-%d'.
- Separamos el año a una nueva columna que la llamaremos release_year.
- Desanidamos por el valor que queremos necesarios de las columnas 'genres', 'belongs_to_collection', 'production_companies' 'production_countries', 'spoken_languages'
- En una nueva columna que la llamaremos return sacar el resultado de la division entre las columnas revenue y budget.
- Eliminamos las columnas que no serán utilizadas, video,imdb_id,adult,original_title,vote_count,poster_path y homepage.
- En una nueva columna tengo que sacar el nombre del mes que tengo en la columna release_date, que lo pondremos en la columna month y igualmente hacemos con los dias de la semana que la pondremos en la columna que llamaremos day.
- En la columna 'day' tengo miércoles y sábado con tildes, le quitaremos las tildes para que nos pueda funcionar.
- En la columna de belongs_to_collection lo pasaremos a todo con minusculas con lower.
- Y por ultimo lo exportamos para hacer las APIS.






**Este repositorio incluye:**

+ Un análisis exploratorio de datos (EDA)<br/>
+ El proceso de ETL paso a paso<br/>
+ Notebooks para su visualización<br/>
+ Desarrollo de una API cons FastApi<br/>
+ Implementación<br/>



## Detalles adicionales del proyecto

Aquí se muestra información adicional y recursos relacionados con el proyecto:

1. `Video explicativo:` Se ha creado un [video explicativo](https://...)  donde te muestro algunas funciones de mi proyecto con el uso de la API.

2. `Acceso a la API:` En el siguiente [enlace de la API](https://...) podras encontrar las funciones de este proyecto.

3. `Obtención de datos originales:` Los datos utilizados para este proyecto de análisis, estan en el siguiente [enlace de descarga](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) 