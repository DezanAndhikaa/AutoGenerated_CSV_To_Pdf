from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Application.ConvertCsv import ConvertCsv
from Application.ExportPdf import ExportPdf
from Commons.Model.Constants import Constants
from Persistences.DbContext import DbContext


def main():
    engine = create_engine(Constants.ConnectionString, echo=True)
    DbContext(engine)
    ConvertCsv("Files/Input/DataCSV.csv", engine)
    ExportPdf(engine)


try:
    from Commons.Domains.User import User
    from Commons.Domains.Review import Review
    from Commons.Domains.SelfReviewResult import SelfReviewResult
    from Commons.Domains.ReviewResult import ReviewResult
    print('INFO : Domains imported')
except ImportError as e:
    print(e)

if __name__ == '__main__':
    main()
