Challenge

La prueba consiste en unificar los dos resultados de las diferentes llamadas a las api, obteniendo un único resultado.

# Puesta en marcha del proyecto, lanzar los siguientes comandos
poetry shell # en caso de no tener instalado poetry https://python-poetry.org/docs/#installation
uvicorn app.main:app
uvicorn app.main:app --reload # En caso de querer modificar algo

Este api está construido con FastAPI, por tanto se ha creado un swagger con documentación de los endpoints, al cual se puede acceder desde.
http://127.0.0.1:8000/docs

# A tener en cuenta
Para poder consultar el endpoint de avails, y que muestre resultados, primero se debe de consultar el endpoints de providers, donde se instanciaran los objects que se disponen en un fichero estático. Una vez estén instanciados se podrá consultar el endpoint de avails.

# Enlaces de interés para llevar a cabo la prueba
Documentación FastAPI --> https://fastapi.tiangolo.com/tutorial/
Poetry --> https://python-poetry.org/docs/#installation
Peticiones asincronas --> https://openbase.com/python/grequests