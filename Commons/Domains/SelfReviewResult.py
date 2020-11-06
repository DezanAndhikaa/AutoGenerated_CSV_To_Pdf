from sqlalchemy import Column, Integer, String
from Commons.Model.Constants import Constants


class SelfReviewResult(Constants.Base):
    __tablename__ = "SelfReviewResults"

    idSelfReviewResult = Column('idSelfReviewResult', Integer, primary_key=True)
    idReview = Column('idReview', Integer)
    answerWorkScore = Column('answerWorkScore', Integer)
    answerExplainWorkScore = Column('answerExplainWorkScore', String)
    answerDriveScore = Column('answerDriveScore', Integer)
    answerExplainDriveScore = Column('answerExplainDriveScore', String)



