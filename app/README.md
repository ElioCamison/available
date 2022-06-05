# <h1>Challenge</h1>

El objetivo es integrar dos proveedores de servicios hoteleros y crear una API que devuelva los datos agrupados.
Para ello, se han creado 2 rutas públicas que devolverán un JSON estático cada vez que reciban una petición GET

# <h2>Como usar el proyecto</h2>

<ul>
    <li>Descargar/clonar el proyecto de GitHub <a href="https://github.com/ElioCamison/available.git">Acceso al proyecto</a></li>
    <li>pip install -r requirements.txt</li>
    <li>poetry shell</li>
    <li>uvicorn app.main:app</li>
    <li>uvicorn app.main:app --reload <i>Opcional, evitará que tenga que parar la ejecución en cada cambio que se realiza</i></li>
</ul>

# <h2>Endpoints disponibles</h2>

<ul>
    <li><a href="http://127.0.0.1:8000/api/v1/providers/">Providers</a></li>
    <li><a href="http://127.0.0.1:8000/api/v1/provider/">Crea un nuevo proveedor</a></li>
    <li><a href="http://127.0.0.1:8000/api/v1/avails/">Avails</a></li>    
</ul>
<a href="http://127.0.0.1:8000/docs">Documentación API</a>

# <h2>Aspectos a tener en cuenta</h2>
Para poder consultar el endpoint de avails, y que muestre resultados, primero se debe de consultar el endpoints de providers, donde se instanciaran los objects que se disponen en un fichero estático. Una vez estén instanciados se podrá consultar el endpoint de avails.

# <h2>Resource</h2>
El directorio resource contiene un json estático de los proveedores dados, a partir de estos se desarrolla el proyecto.

# <h2>Collections</h2>
Contiene un json, el cual se podrá importar y contiene los endpoints que permite la API. En el se podrá ver ejemplos de las diferentes peticiones.

# <h2>Testing</h2>
python -m pytest tests/ o\
pytest 

# <h2>Enlaces de interés para llevar a cabo la prueba</h2>
<ul>
    <li><a href="https://fastapi.tiangolo.com/tutorial/">Documentación FastAPI</a></li>
    <li><a href="https://python-poetry.org/docs/">Documentación poetry</a></li>
    <li><a href="https://openbase.com/python/grequests">Librería peticiones asincronas</a></li>        
</ul>
