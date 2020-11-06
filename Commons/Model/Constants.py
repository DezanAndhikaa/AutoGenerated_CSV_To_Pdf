from sqlalchemy.ext.declarative import declarative_base


class Constants(object):
    # DB Region
    ConnectionString = "postgresql://postgres:AdminPassword123@localhost:5432/reviewDatabase"
    EnableAutoMigration = False
    Base = declarative_base()
    # End of DB Region

    # Relationship Hash Table
    Relationship = {
        1: ' I am reviewing myself',
        2: ' He/She reports to me',
        3: ' I report to him/her',
        4: ' Direct team mate',
        5: ' Team mate in another team'
    }

    # End of Relationship Hash Table

    # PDF Report
    FilePath = "Files/Output/PDF Report"
    FileTitle = "PDF Report"
