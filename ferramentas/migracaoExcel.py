import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, DateTime, Float
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class RegisterNF(Base):
    __tablename__ = 'register_NF'
    id = Column(Integer, primary_key=True)
    NFId = Column(BigInteger, nullable=True, unique=True)
    NFDate = Column(DateTime, nullable=True)
    NFValue = Column(Float, nullable=True)

def read_excel_and_write_to_db(columns, excel_file, db_file):
    df = pd.read_excel(excel_file)
    engine = create_engine(f'sqlite:///{db_file}')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():
        register = RegisterNF(
            NFId=row[columns[0]],
            NFDate=row[columns[1]],
            NFValue=row[columns[2]]
        )
        session.add(register)

    session.commit()
    session.close()

if __name__ == "__main__":
    # a lista deverá conter os nomes dos campos no excel ['numero da nota', 'data', 'valor da nota']
    columns = ['NFId', 'NFDate', 'NFValue'] 
    read_excel_and_write_to_db(columns, '/Users/verissimo/Projeto_Integrador_IV/ferramentas/3 - BASE DADOS 2024_AGO.xlsx', '/Users/verissimo/Projeto_Integrador_IV/var/app-instance/database.db')
