from mapper.object_mapper import ObjectMapper
from reportlab.pdfgen import canvas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle

from Commons.Domains.ReviewQuery import ReviewQuery
from Commons.Model.Constants import Constants


class ExportNewPdf:
    def __init__(self, engine: create_engine):
        self.engine = engine
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()
        self.pdf = canvas.Canvas(Constants.FilePath)
        self.document = []

        users = self.session.query(ReviewQuery).filter(ReviewQuery.ReviewedMembers == "Selvie").all()
        counter = 0
        for user_data in users:
            self.add_cover()
            self.add_first_page(user_data.ReviewedMembers)
            self.add_second_page("Desember")
            self.add_third_page()
            self_review = self.session.query(ReviewQuery)\
                .filter(ReviewQuery.ReviewedMembers == user_data.ReviewedMembers,
                        ReviewQuery.Relationship.like('%reviewing myself%')).first()
            if self_review is not None:
                self.add_self_report(self_review)

            reviews = self.session.query(ReviewQuery).filter(ReviewQuery.ReviewedMembers == user_data.ReviewedMembers,
                                                             ReviewQuery.Relationship.notlike('%reviewing myself%')).all()

            if not reviews is None:
                for data_review in reviews:
                    self.add_report_review(data_review)

            SimpleDocTemplate(Constants.FilePath + " " + user_data.ReviewedMembers + ".pdf", pagesize=letter,
                              topMargin=6, bottomMargin=6). \
                build(self.document)
            self.document = []


    def add_cover(self):
        self.document.append(Image("Files/Images/cover.png", 8 * inch, 10 * inch))
        self.document.append(PageBreak())

    def add_first_page(self, name):
        self.document.append(Spacer(1, 300))
        self.document.append(Paragraph(name + " Report", ParagraphStyle(name='Name',
                                                                        alignment=TA_CENTER,
                                                                        leading=40,
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
        work = Paragraph('1. Work: ' + self_review.MyProjectScore, ParagraphStyle(name='styleWork',
                                                                                        fontSize=16))
        explain = Paragraph('Explanation: ' + self_review.MyExamplesToBeBetter, ParagraphStyle(name='styleWork',
                                                                                               leading=20,
                                                                                               fontSize=16))
        self.document.append(work)
        self.document.append(Spacer(20, 10))
        self.document.append(explain)
        self.document.append(Spacer(20, 30))
        drive = Paragraph('2. Drive & Fit: ' + self_review.MyDriveFit, ParagraphStyle(name='styleWork',
                                                                                      fontSize=16))
        drive_explain = Paragraph('Explanation: ' + self_review.MyExamplesToBe, ParagraphStyle(name='styleWork',
                                                                                               leading=20,
                                                                                               fontSize=16))
        self.document.append(drive)
        self.document.append(Spacer(20, 10))
        self.document.append(drive_explain)

        combination = Paragraph('3. Combination Score: ' + str(self_review.MyProjectScore) +' , '+ str(self_review.MyDriveFit),
                          ParagraphStyle(name='styleWork', fontSize=16))
        self.document.append(Spacer(20, 30))
        self.document.append(combination)

        self.document.append(PageBreak())

    def add_report_review(self, result_review):
        self.document.append(Spacer(20, 60))
        reviewer = Paragraph("Reviewers: " + result_review.ReviewerName, ParagraphStyle(name='SelfReviews',
                                                                                        leading=25,
                                                                                        fontSize=20))
        relation = Paragraph("Relationship: " + result_review.Relationship, ParagraphStyle(name='SelfReviews',
                                                                                           leading=25,
                                                                                           fontSize=20))
        self.document.append(reviewer)
        self.document.append(Spacer(20, 10))
        self.document.append(relation)

        self.document.append(Spacer(20, 40))
        work = Paragraph('1. Work: ' + result_review.ProjectScore, ParagraphStyle(name='styleWork',
                                                                                  fontSize=16))
        explain = Paragraph('Explanation: ' + result_review.ExamplesToBeBetter, ParagraphStyle(name='styleWork',
                                                                                               leading=25,
                                                                                               fontSize=16))
        self.document.append(work)
        self.document.append(Spacer(20, 10))
        self.document.append(explain)
        self.document.append(Spacer(20, 30))
        drive = Paragraph('2. Drive & Fit: ' + result_review.DriveFit, ParagraphStyle(name='styleWork', leading=25,
                                                                                      fontSize=16))
        drive_explain = Paragraph('Explanation: ' + result_review.ExamplesToBe,
                                  ParagraphStyle(name='styleWork',
                                                 leading=25,
                                                 fontSize=16))
        self.document.append(drive)
        self.document.append(Spacer(20, 10))
        self.document.append(drive_explain)

        combination = Paragraph(
            '3. Combination Score: ' + result_review.ProjectScore + ' , ' + result_review.DriveFit,
            ParagraphStyle(name='styleWork', fontSize=16))
        self.document.append(Spacer(20, 30))
        self.document.append(combination)

        additional = Paragraph(
            'Additional Comments for Improvement: ',
            ParagraphStyle(name='styleWork', leading=25, fontSize=16))
        answer_additional = Paragraph(result_review.StartAndStop, ParagraphStyle(name='styleWork', leading=25, fontSize=16))
        self.document.append(Spacer(20, 30))
        self.document.append(additional)
        self.document.append(Spacer(20,10))
        self.document.append(answer_additional)
        self.document.append(PageBreak())