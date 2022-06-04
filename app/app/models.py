from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base

class Provider(Base):
    __tablename__ = "provider"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    url = Column(String)


class Rates(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))
    nights = Column(Integer)
    final_price = Column(Integer)


class Options(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    nights = Column(Integer)
    night_price = Column(Integer)
    rates_id = Column(Integer, ForeignKey("rates.id"))
    
    hotels = relationship("Hotel", back_populates="options")
    #rates = relationship("Rates", back_populates="rates")


class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True, index=True)
    options_id = Column(Integer, ForeignKey("options.id"))

    options = relationship("Options", back_populates="hotels")