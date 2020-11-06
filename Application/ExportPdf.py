from reportlab.pdfgen import canvas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle

from Commons.Domains.Review import Review
from Commons.Domains.ReviewResult import ReviewResult
from Commons.Domains.SelfReviewResult import SelfReviewResult
from Commons.Domains.User import User
from Commons.Model.Constants import Constants


class ExportPdf:
    def __init__(self, engine: create_engine):

        self.engine = engine
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()
        self.pdf = canvas.Canvas(Constants.FilePath)
        self.document = []

        # Query from db
        users = self.session.query(User).all()

        for data in users:
            self.document = []
            self.add_cover()
            self.add_first_page(data.userCredentialName)
            self.add_second_page("Desember")
            self.add_third_page()

            single_self_review = self.session.query(Review).filter(Review.idUserReviewed == data.idUser, Review.relationship == 1).first()
            if not single_self_review is None:
                self_answer = self.session.query(SelfReviewResult).filter(SelfReviewResult.idReview == single_self_review.idReview).first()
                self.add_self_report(self_answer)

            review = self.session.query(Review).filter(Review.idUserReviewed == data.idUser).all()
            for entity_review in review:
                if entity_review.relationship != 1:
                    single_review = self.session.query(ReviewResult)\
                        .filter(ReviewResult.idReview == entity_review.idReview).all()
                    for data_review in single_review:
                        self.add_report_review(data_review, entity_review)

            SimpleDocTemplate(Constants.FilePath + " " + data.userCredentialName + ".pdf", pagesize=letter,
                              topMargin=6, bottomMargin=6). \
                build(self.document)

    def add_cover(self):
        self.document.append(Image("Files/Images/cover.png", 8 * inch, 10 * inch))
        self.document.append(PageBreak())

    def add_first_page(self, name):
        self.document.append(Spacer(1, 300))
        self.document.append(Paragraph(name + " Report", ParagraphStyle(name='Name',
                                                                        alignment=TA_CENTER,
                                                                        fontSize=32)))
        self.document.append(PageBreak())

    def add_second_page(self, date):
        self.document.append(Spacer(1, 300))
        self.document.append(Paragraph(date + " Report", ParagraphStyle(name='Name',
                                                                        alignment=TA_CENTER,
                                                                        fontSize=32)))
        self.document.append(PageBreak())

    def add_third_page(self):
        self.document.append(Spacer(90, 20))
        self.document.append(Image("Files/Images/score.png", 8.2 * inch, 10 * inch))
        self.document.append(PageBreak())

    def add_self_report(self, self_review):
        self.document.append(Spacer(20, 80))
        paragraph = Paragraph("Self Reviews", ParagraphStyle(name='SelfReviews',
                                                             fontSize=20))
        self.document.append(paragraph)

        self.document.append(Spacer(20, 30))
        work = Paragraph('1. Work: ' + str(self_review.answerWorkScore), ParagraphStyle(name='styleWork',
                                                                                        fontSize=16))
        explain = Paragraph('Explanation: ' + str(self_review.answerExplainWorkScore), ParagraphStyle(name='styleWork',
                                                                                        fontSize=16))
        self.document.append(work)
        self.document.append(Spacer(20, 10))
        self.document.append(explain)
        self.document.append(Spacer(20, 30))
        drive = Paragraph('2. Drive & Fit: ' + str(self_review.answerDriveScore), ParagraphStyle(name='styleWork',
                                                                                        fontSize=16))
        drive_explain = Paragraph('Explanation: ' + self_review.answerExplainDriveScore, ParagraphStyle(name='styleWork',
                                                                                        fontSize=16))
        self.document.append(drive)
        self.document.append(Spacer(20, 10))
        self.document.append(drive_explain)

        combination = Paragraph('3. Combination Score: '+ str(self_review.answerWorkScore) +' , '+ str(self_review.answerDriveScore),
                          ParagraphStyle(name='styleWork',fontSize=16))
        self.document.append(Spacer(20, 30))
        self.document.append(combination)

        self.document.append(PageBreak())

    def add_report_review(self, result_review, entity_review):
        self.document.append(Spacer(20, 60))
        reviewer = Paragraph("Reviewers: "+ str(self.get_user_name_by_id(entity_review.idUserReviewer)), ParagraphStyle(name='SelfReviews',
                                                             fontSize=20))
        relation = Paragraph("Relationship: "+ Constants.Relationship[int(entity_review.relationship)], ParagraphStyle(name='SelfReviews',
                                                             fontSize=20))
        self.document.append(reviewer)
        self.document.append(Spacer(20, 10))
        self.document.append(relation)

        self.document.append(Spacer(20, 40))
        work = Paragraph('1. Work: ' + str(result_review.answerWorkScore), ParagraphStyle(name='styleWork',
                                                                                        fontSize=16))
        explain = Paragraph('Explanation: ' + str(result_review.answerExplainWorkScore), ParagraphStyle(name='styleWork',
                                                                                                      fontSize=16))
        self.document.append(work)
        self.document.append(Spacer(20, 10))
        self.document.append(explain)
        self.document.append(Spacer(20, 30))
        drive = Paragraph('2. Drive & Fit: ' + str(result_review.answerDriveScore), ParagraphStyle(name='styleWork',
                                                                                                 fontSize=16))
        drive_explain = Paragraph('Explanation: ' + result_review.answerExplainDriveScore,
                                  ParagraphStyle(name='styleWork',
                                                 fontSize=16))
        self.document.append(drive)
        self.document.append(Spacer(20, 10))
        self.document.append(drive_explain)

        combination = Paragraph(
            '3. Combination Score: ' + str(result_review.answerWorkScore) + ' , ' + str(result_review.answerDriveScore),
            ParagraphStyle(name='styleWork', fontSize=16))
        self.document.append(Spacer(20, 30))
        self.document.append(combination)

        additional = Paragraph(
            'Additional Comments for Improvement: ',
            ParagraphStyle(name='styleWork', fontSize=16))
        answer_additional = Paragraph(result_review.answerTips, ParagraphStyle(name='styleWork', fontSize=16))
        self.document.append(Spacer(20, 30))
        self.document.append(additional)
        self.document.append(Spacer(20,10))
        self.document.append(answer_additional)
        self.document.append(PageBreak())

    def get_user_name_by_id(self, id_user):
        result = self.session.query(User).filter(User.idUser == id_user).first()
        return result.userCredentialName
