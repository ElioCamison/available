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


@app.get("/api/v1/providers/", response_model=List[schemas.Provider])
def fetch_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    providers = crud.get_providers(db, skip=skip, limit=limit)
    if len(providers) == 0:
        data = json.load(open('./resource/providers.json', 'r'))
        for provider in data:
            crud.create_provider(db, json.loads(json.dumps(provider), object_hook=lambda d: SimpleNamespace(**d))) 
        
        providers = crud.get_providers(db, skip=skip, limit=limit)

    return providers

@app.get("/api/v1/avails/")
async def fetch_avails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
        Primero se obtienen los proveedores. Con las urls de estos se instancian los objetos de rates y options
        Una vez instanciados estos se crean los hoteles y al final se instancian los avails

    """
    providers = crud.get_providers(db, skip=skip, limit=limit)
    # rs = request
    # Con qrequests se preparan todas las peticiones que tengan los proveedores, en caso de fallar una no impedira
    # que el resto se lance, simplemente esa tenga el status correspondiente al fallo
    rs = (grequests.get(provider.url) for provider in providers)
    # En este punto se lanzan todas las peticiones en paralelo.
    response = grequests.map(rs)
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
