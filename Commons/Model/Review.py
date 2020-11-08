from sqlalchemy import Column, String, Integer


class Review:

    ReviewerName = Column('ReviewerName', String)
    Relationship = Column('Relationship', String)
    ProjectScore = Column('ProjectScore', String)
    ExamplesToBeBetter = Column('ExamplesToBeBetter', String)
    DriveFit = Column('DriveFit', String)
    ExamplesToBe = Column('ExamplesToBe', String)
    StartAndStop = Column('StartandStop', String)
    feedbackHC = Column('feedbackHC', String)
    feedbackHC2 = Column('feedbackHC2', String)
    ReviewDate = Column('ReviewDate', String)
