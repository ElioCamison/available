from sqlalchemy.orm import Session

from . import models, schemas


# -- ****************************************
# -- Providers
# -- ****************************************

def get_provider(db: Session, provider_id: int):
    """
        Devuelve un proveedor en base a su atributo id
    """
    return db.query(models.Provider).filter(models.Provider.id == provider_id).first()


def get_provider_by_url(db: Session, url: str):
    """
        Devuelve un proveedor en base a su atributo URL
    """
    return db.query(models.Provider).filter(models.Provider.url == url).first()


def get_providers(db: Session, skip: int = 0, limit: int = 100):
    """
        Devuelve todos los proveedores
    """
    return db.query(models.Provider).offset(skip).limit(limit).all()


def delete_provider(db: Session, provider_id: int):
    """
        Borra un proveedor en base a su atributo id
    """
    
    db.query(models.Provider).filter(models.Provider.id == provider_id).delete()
    db.commit()
    return {"ok": True}


def create_provider(db: Session, provider: schemas.ProviderCreate):
    """
        Crea un proveedor
    """
    db_provider = models.Provider(name=provider.name, 
                                  code=provider.code,
                                  url=provider.url)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

# -- ****************************************
# -- Options
# -- ****************************************

def get_options(db: Session, skip: int = 0, limit: int = 100):
    """
        Devuelve todos las opciones(paquetes) que tiene un proveedor en concreto
    """
    return db.query(models.Options).offset(skip).limit(limit).all()

def create_options(db: Session, options: schemas.OptionsCreate):
    """
        Crea un paquete de opciones
    """
    print(options)
    db_options = models.Options(hotel_id=options['hotel_id'], 
                                nights=options['nights'],
                                night_price=options['night_price'],
                                provider=options['provider'])
    db.add(db_options)
    db.commit()
    db.refresh(db_options)
    return db_options


# -- CREATE RATES
def create_rate(db: Session, rate: schemas.ProviderCreate):
    db_rate = models.Rates(hotel_id = rate.hotel_id,
                           nights = rate.nights,
                           final_price=rate.final_price)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate
