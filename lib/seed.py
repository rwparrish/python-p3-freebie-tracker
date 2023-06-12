#!/usr/bin/env python3
import Faker
from random import choice as rc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Freebie, Dev

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def delete_records():
    session.query(Company).delete()
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.commit()
    
def create_records():
    companies = [Company(fake.name(), fake.random_int(min=1930, max=2023)) for i in range(20)]
    freebies = [Freebie(fake.name(), fake.random_int(min=1, max=117)) for i in range(100)]
    devs = [Dev(fake.name()) for i in range(50)]
    session.add_all(companies + freebies + devs)
    session.commit()
    return companies, freebies, devs

def relate_records(companies, freebies, devs):
    for freebie in freebies:
        freebie.dev = rc(devs)
        freebie.company = rc(companies)

    session.add_all(freebies)
    session.commit()
    
if __name__ == '__main__':
    delete_records()
    companies, freebies, devs = create_records()
    relate_records(companies, freebies, devs)


