from sqlalchemy import create_engine

from Commons.Model.Constants import Constants

Base = Constants.Base()


class DbContext(object):
    def __init__(self, engine_db: create_engine):
        self.engine = engine_db

        if Constants.EnableAutoMigration:
            print('Creating table...')
            Base.metadata.create_all(bind=self.engine)

    def return_engine(self):
        return self.engine
