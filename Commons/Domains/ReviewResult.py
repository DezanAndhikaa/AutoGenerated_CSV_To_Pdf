from sqlalchemy import Column, Integer, String

from Commons.Model.Constants import Constants


class ReviewResult(Constants.Base):
    __tablename__ = "ReviewResults"

    idReviewResult = Column('idReviewResult', Integer, primary_key=True)
    idReview = Column('idReview', Integer)
    answerWorkScore = Column('answerWorkScore', Integer)
    answerExplainWorkScore = Column('answerExplainWorkScore', String)
    answerDriveScore = Column('answerDriveScore', Integer)
    answerExplainDriveScore = Column('answerExplainDriveScore', String)
    answerTips = Column('answerTips', String)
    answerLeaderFeeling = Column('answerLeaderFeeling', Integer)