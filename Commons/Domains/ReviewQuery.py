from sqlalchemy import Column, String, Integer

from Commons.Model.Constants import Constants


class ReviewQuery(Constants.Base):
    __tablename__ = "STG_RawMonthlyPerformance"

    IdReview = Column('IdReview', Integer, primary_key=True)
    ReviewerName = Column('ReviewerName', String)
    ReviewedMembers = Column('ReviewedMembers', String)
    Relationship = Column('Relationship', String)
    ProjectScore = Column('ProjectScore', String)
    MyProjectScore = Column('MyProjectScore', String)
    MyLeaderScore = Column('MyLeaderScore', String)
    ExamplesToBeBetter = Column('ExamplesToBeBetter', String)
    ExamplesToMyLead = Column('ExamplesToMyLead', String)
    MyExamplesToBeBetter = Column('MyExamplesToBeBetter', String)
    DriveFit = Column('DriveFit', String)
    MyDriveFit = Column('MyDriveFit', String)
    ExamplesToBe = Column('ExamplesToBe', String)
    MyExamplesToBe = Column('MyExamplesToBe', String)
    StartAndStop = Column('StartandStop', String)
    feedbackHC = Column('feedbackHC', String)
    feedbackHC2 = Column('feedbackHC2', String)
    ReviewDate = Column('ReviewDate', String)
