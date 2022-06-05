#import sys
#import os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + './')
import json
import grequests
import requests
import ast
from types import SimpleNamespace

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -- Crea un nuevo proveedor
@app.post("/api/v1/provider/", response_model=schemas.Provider)
def create_provider(provider: schemas.ProviderCreate, db: Session = Depends(get_db)):
    """
        Ejemplo de la peticion en el collections.
    """
    # Si existe algun proveedor con la url del nuevo proveedor, este no se creara y devolvera un error
    db_provider = crud.get_provider_by_url(db,provider.url)
    if db_provider:
        raise HTTPException(status_code=400, detail="Ya existe un proveedor con la url indicada.")
    # Crea el nuevo proveedor
    return crud.create_provider(db, provider=provider)

# -- Obtiene todos los proveedores
@app.get("/api/v1/providers/", response_model=List[schemas.Provider])
def fetch_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
        Obtiene todos los proveedores, en caso de no disponerlos todavía se crearan los proveedores estaticos
        de la carpeta resource
    """
    providers = crud.get_providers(db, skip=skip, limit=limit)
    if len(providers) == 0:
        # Se crean los proveedores de la carpeta resource
        data = json.load(open('./resource/providers.json', 'r'))
        for provider in data:
            crud.create_provider(db, json.loads(json.dumps(provider), object_hook=lambda d: SimpleNamespace(**d))) 
        
        providers = crud.get_providers(db, skip=skip, limit=limit)

    return providers

# -- Obtiene un unico proveedor
@app.get("/api/v1/providers/{provider_id}", response_model=schemas.Provider)
def fetch_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = crud.get_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_provider


@app.delete("/api/v1/providers/{provider_id}", status_code=204)
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = crud.delete_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return {'borrado':True}



# -- Obtiene el listado de disponibilidades
@app.get("/api/v1/avails/")
async def fetch_avails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
        Primero se obtienen los proveedores. Con las urls de estos se instancian los objetos de rates y options
        Una vez instanciados estos se crean los hoteles y al final se instancian los avails

        se debería de guardar cada objecto correspondiente
    """
    providers = crud.get_providers(db, skip=skip, limit=limit)
    # Con qrequests se preparan todas las peticiones que tengan los proveedores, en caso de fallar una no impedira
    # que el resto se lance, simplemente esa tenga el status correspondiente al fallo
    # rs = request
    rs = (grequests.get(provider.url) for provider in providers)
    # En este punto se lanzan todas las peticiones en paralelo.
    response = grequests.map(rs)
    # TODO - No tiene la estructura correcta
    result = []
    for r in response:
        # El contenido de la respuesta es de tipo byte por tanto hay que parsearlo
        parse = ast.literal_eval(r.content.decode("UTF-8"))
        if 'rates' in parse:
            provider = crud.get_provider_by_url(db,str(r.url))
            for rate in parse['rates']:
                result.append(
                    {
                        'hotel':rate['hotel'],
                        'options':[
                            {
                                'hotel':rate['hotel'],
                                'nights': rate['nights'],
                                'final_price':rate['final_price'],
                                'provider': provider.code
                            }
                        ]
                    }
                )
        elif 'options' in parse:
            provider = crud.get_provider_by_url(db,str(r.url))
            for options in parse['options']:
                result.append(
                    {
                        'hotel':int(options['hotel']),
                        'options':[
                            {
                                'hotel':int(options['hotel']),
                                'nights': options['nights'],
                                'final_price':options['night_price'] * int(options['nights']),
                                'provider': provider.code
                            }
                        ]
                    }
                )

    return result
