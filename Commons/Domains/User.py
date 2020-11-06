from sqlalchemy import Column, String, Integer

from Commons.Model.Constants import Constants


class User(Constants.Base):
    __tablename__ = "Users"
    idUser = Column('idUser', Integer, primary_key=True)
    userCredentialName = Column('userCredentialName', String)
    userDivision = Column('userDivision', String)
