from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

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
    
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name,  value)
        freebie.dev = dev
        freebie.company = self
        
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()
    # the code below was my best try - I think this has something to do with
    # fine tuning the query object before execution VS grabbing all the records
    # and then doing iteration...
        # companies = session.query(cls)
        # comp = min(companies, key=lambda x: x["founding_year"])
        # return comp
    


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
    
    def received_one(self, item_name):
        dev_freebie = session.query(Freebie).filter(Freebie.dev_id == self.id, Freebie.item_name == item_name).all()
        if dev_freebie:
            return True
        else:
            return False
        
    def give_away(self, dev, freebie):
        if self.id == freebie.dev_id:
            freebie.dev_id = dev.id
    
    


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
        return f'<Freebie {self.item_name}>'
    
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
    
    
    