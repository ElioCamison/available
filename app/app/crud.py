from sqlalchemy.orm import Session

from . import models, schemas

def get_provider(db: Session, provider_id: int):
    return db.query(models.Provider).filter(models.Provider.id == provider_id).first()


def get_provider_by_url(db: Session, url: str):
    return db.query(models.Provider).filter(models.Provider.url == url).first()


def get_providers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Provider).offset(skip).limit(limit).all()


def create_provider(db: Session, provider: schemas.ProviderCreate):
    db_provider = models.Provider(name=provider.name, 
                              code=provider.code,
                              url=provider.url)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider



# -- CREATE RATES
def create_rate(db: Session, rate: schemas.ProviderCreate):
    db_rate = models.Rates(hotel_id = rate.hotel_id,
                           nights = rate.nights,
                           final_price=rate.final_price)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate


#def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#    db_item = models.Item(**item.dict(), owner_id=user_id)
#    db.add(db_item)
#    db.commit()
#    db.refresh(db_item)
#    return db_item