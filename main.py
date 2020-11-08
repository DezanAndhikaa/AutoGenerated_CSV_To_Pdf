from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Application.ConvertCsv import ConvertCsv
from Application.ExportNewPdf import ExportNewPdf
from Application.ExportPdf import ExportPdf
from Commons.Model.Constants import Constants
from Persistences.DbContext import DbContext


def main():
    engine = create_engine(Constants.ConnectionString, echo=True)
    DbContext(engine)
    # ConvertCsv("Files/Input/actual.csv", engine)
    # ExportPdf(engine)
    ExportNewPdf(engine)


try:
    from Commons.Domains.ReviewQuery import ReviewQuery
    print('INFO : Domains imported')
except ImportError as e:
    print(e)

if __name__ == '__main__':
    main()
