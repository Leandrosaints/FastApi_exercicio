from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

class AddressesModel(BaseModel):
    __tablename__='addresses'
    id:int =Column(Integer, primary_key=True, autoincrement=True)
    #hotel_id = Column(Integer, ForeignKey('hoites.id'))
    site_id = Column(Integer, ForeignKey('sites.id'))
    
    #hotel = relationship('HotelModel', back_populates='addresses')
    site = relationship("SiteModel", back_populates='addresses')
