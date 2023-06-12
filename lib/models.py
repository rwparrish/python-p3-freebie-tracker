from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    freebies = relationship('Freebie', back_populates='company', cascade='all, delete-orphan')
    
    # not sure I can explain this:
    devs = association_proxy('freebies', 'dev',
        creator=lambda dv: Freebie(dev=dv))

    def __repr__(self):
        return f'<Company {self.name}>'
    

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    freebies = relationship('Freebie', back_populates='dev', cascade='all, delete-orphan')
    # not sure I can explain this:
    companies = association_proxy('freebies', 'company',
        creator=lambda cpy: Freebie(company=cpy))

    def __repr__(self):
        return f'<Dev {self.name}>'


class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    
    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')
    
    def __repr__(self):
        return f'<Freebie {self.name}>'
    
    
    