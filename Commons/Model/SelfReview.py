from sqlalchemy import Column, String, Integer


class SelfReview:

    ReviewerName = Column('ReviewerName', String)
    MyProjectScore = Column('MyProjectScore', String)
    MyExamplesToBeBetter = Column('MyExamplesToBeBetter', String)
    MyDriveFit = Column('MyDriveFit', String)
    MyExamplesToBe = Column('MyExamplesToBe', String)
    ReviewDate = Column('ReviewDate', String)
