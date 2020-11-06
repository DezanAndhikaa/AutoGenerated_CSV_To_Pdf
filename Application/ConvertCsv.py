import csv

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from Commons.Domains.Review import Review
from Commons.Domains.ReviewResult import ReviewResult
from Commons.Domains.SelfReviewResult import SelfReviewResult
from Commons.Domains.User import User
from Commons.Model.Constants import Constants
from random import randint

# Index info from csv
# 0 = User credential
# 1 = Who is reviewed by this user
# 2 = User division
# 3 = User relationship
# 4 = Reviewed work score
# 5 = Self work score
# 6 = Leader feeling score
# 7 = Explain work
# 8 = Self explain work
# 9 = Drive score
# 10 = Self drive score
# 11 = Explain drive
# 12 = Explain tips (stop & start)
# 15 = Date


def translate_relationship(relation: str):
    keys = list(Constants.Relationship.keys())
    value = list(Constants.Relationship.values())
    return keys[value.index(relation.replace('.', '').rstrip())]


class ConvertCsv:
    def __init__(self, path: str, db: create_engine):
        self.path_file = path
        self.engine = db
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

        first_line = True
        first_line_data = True
        with open(self.path_file, newline='') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=';', quotechar='|')

            for row in spam_reader:
                if first_line:
                    first_line = False
                    continue

                if not first_line:
                    data = '; '.join(row)
                    row_split = data.split(';')
                    self.insert_user(row_split, randint(0, 1000))

        with open(self.path_file, newline='') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=';', quotechar='|')
            for rows in spam_reader:
                if first_line_data:
                    first_line_data = False
                    continue

                if not first_line_data:
                    data = '; '.join(rows)
                    id_review = randint(0, 99999999)

                    self.import_to_db(data, id_review)

    def import_to_db(self, row: str, id_review):
        split_row = row.split(';')
        cleansing_relationship = split_row[3].replace('.', '')

        if cleansing_relationship == Constants.Relationship[1]:
            self.insert_self_review(split_row, id_review)
        else:
            self.insert_user_review(split_row, id_review)

    def is_user_exist(self, user_name):
        result = self.session.query(User.userCredentialName).filter(User.userCredentialName == user_name).first()
        if result is None:
            return False
        return True

    def get_id_user_by_name(self, username):
        result = self.session.query(User.idUser).filter(User.userCredentialName == username).first()
        return result

    def insert_user_review(self, split_row, id_review):
        self.insert_review(split_row, id_review)
        if len(split_row[6].replace(' ', '')) == 0:
            split_row[6] = 0

        if len(split_row[4].replace(' ', '')) == 0:
            split_row[4] = 0

        if len(split_row[9].replace(' ', '')) == 0:
            split_row[9] = 0

        user_review = ReviewResult(
            idReview=id_review,
            idReviewResult=randint(0, 1000),
            answerWorkScore=int(split_row[4]),
            answerExplainWorkScore=split_row[7],
            answerDriveScore=int(split_row[9]),
            answerExplainDriveScore=split_row[11],
            answerTips=split_row[12],
            answerLeaderFeeling=int(split_row[6])
        )
        self.session.add(user_review)
        self.session.commit()

    def insert_user(self, split_row, id_user: int):
        if len(split_row[0]) > 2:
            user = User(
                idUser=id_user,
                userDivision=split_row[2],
                userCredentialName=split_row[0].strip()
            )
            if not self.is_user_exist(user.userCredentialName):
                self.session.add(user)
                self.session.commit()

    def insert_review(self, split_row, id_review):
        relation = split_row[3]
        relation.rstrip()
        review = Review(
            idReview=id_review,
            idUserReviewer=self.get_id_user_by_name(split_row[0].strip()),
            idUserReviewed=self.get_id_user_by_name(split_row[1].strip()),
            relationship=translate_relationship(relation),
            reviewDate=split_row[16]
        )
        self.session.add(review)
        self.session.commit()

    def insert_self_review(self,split_row, id_review):
        self.insert_review(split_row, id_review)
        if len(split_row[5].replace(' ', '')) == 0:
            split_row[5] = 0
        if len(split_row[10].replace(' ', '')) == 0:
            split_row[10] = 0

        self_review = SelfReviewResult(
            idSelfReviewResult=randint(0, 1000),
            idReview=id_review,
            answerWorkScore=int(split_row[5]),
            answerExplainWorkScore=split_row[7],
            answerDriveScore=int(split_row[10]),
            answerExplainDriveScore=split_row[11]
        )
        self.session.add(self_review)
        self.session.commit()