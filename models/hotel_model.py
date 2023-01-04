from typing import Optional
from core.configs import settings
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

class HotelModel(settings.DBBaseModel):
    __tablename__='hoteis'
    id=Column(Integer, primary_key=True, autoincrement=True)
    nome=Column(String(100))
    estrelas=Column(Float(precision=1))
    diaria=Column(Float(precision=2))
    cidade = Column(String(80))
    site_id = Column(Integer, ForeignKey('sites.id'))
    sites = relationship("SiteModel", back_populates='hoteis', lazy="joined")
    


