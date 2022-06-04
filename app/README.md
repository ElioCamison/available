# <h1>Challenge</h1>

El objetivo es integrar dos proveedores de servicios hoteleros y crear una API que devuelva los datos agrupados.
Para ello, se han creado 2 rutas públicas que devolverán un JSON estático cada vez que reciban una petición GET

# <h2>Puesta en marcha del proyecto, lanzar los siguientes comandos</h2>
poetry shell # en caso de no tener instalado poetry https://python-poetry.org/docs/#installation \
uvicorn app.main:app \
uvicorn app.main:app --reload # En caso de querer modificar algo

Este api está construido con FastAPI, por tanto se ha creado un swagger con documentación de los endpoints, al cual se puede acceder desde. http://127.0.0.1:8000/docs

# <h2>A tener en cuenta</h2>
Para poder consultar el endpoint de avails, y que muestre resultados, primero se debe de consultar el endpoints de providers, donde se instanciaran los objects que se disponen en un fichero estático. Una vez estén instanciados se podrá consultar el endpoint de avails.

# <h2>Enlaces de interés para llevar a cabo la prueba</h2>
Documentación FastAPI --> https://fastapi.tiangolo.com/tutorial/ \
Poetry --> https://python-poetry.org/docs/#installation \
Peticiones asincronas --> https://openbase.com/python/grequests