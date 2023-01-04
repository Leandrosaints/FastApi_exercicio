from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class SiteModel(settings.DBBaseModel):
    __tablename__='sites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(256))
    hoteis = relationship(
        "HotelModel",
        cascade="all, delete-orphan",
        back_populates='sites',
        uselist= True,
        lazy="joined"
    )

    


