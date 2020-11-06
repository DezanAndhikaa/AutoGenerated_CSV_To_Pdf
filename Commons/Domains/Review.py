from sqlalchemy import Column, Integer, String

from Commons.Model.Constants import Constants


class Review(Constants.Base):
    __tablename__ = "Reviews"

    idReview = Column('idReview', Integer, primary_key=True)
    idUserReviewer = Column('idUserReviewer', Integer)
    idUserReviewed = Column('idUserReviewed', Integer)
    relationship = Column('relationship', Integer)
    reviewDate = Column('reviewDate', String)
