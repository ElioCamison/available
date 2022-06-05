from typing import List, Union

from pydantic import BaseModel, HttpUrl


# -- Model Provider
class ProviderBase(BaseModel):
    name: str
    code: str
    url: HttpUrl


class ProviderCreate(ProviderBase):
    """
        Extiende del modelo base dado que no va a incrementar de atributos por el momento
    """
    pass

class Provider(ProviderBase):
    id: int

    class Config:
        orm_mode = True


# -- Model Options
class OptionsBase(BaseModel):
    hotel_id: int
    nights: int
    night_price: int
    provider: int


class OptionsCreate(OptionsBase):
    pass


class Options(OptionsBase):
    hotel_id: int
    nights: int
    night_price: int
    provider: int

    class Config:
        orm_mode = True


# -- Model Rates
class RatesBase(BaseModel):
    id: int
    hotel_id: int 
    nights: int
    final_price: int


class RatesCreate(OptionsBase):
    pass


class Rates(OptionsBase):
    id: int
    hotel_id: int 
    nights: int
    final_price: int

    class Config:
        orm_mode = True


# -- Model Hotel
class HotelBase(BaseModel):
    id: int
    options: List[Options] = []


class HotelCreate(OptionsBase):
    pass


class Hotel(OptionsBase):
    id: int
    options: List[Options] = []

    class Config:
        orm_mode = True
        