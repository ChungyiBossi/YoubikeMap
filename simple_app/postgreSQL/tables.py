from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
Base = declarative_base()
Base.metadata.clear()


class LineUser(Base):
    __tablename__ = 'lineUser'

    lineUserId = Column(String, primary_key=True)
    fullname = Column(String)

    def __init__(self, lineUserId, fullname):
        self.lineUserId = lineUserId
        self.fullname = fullname

    def __repr__(self):
        return "< User:('%s','%s') >" % (self.lineUserId, self.fullname)

