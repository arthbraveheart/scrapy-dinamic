# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from scrapy.exceptions import DropItem
from datetime import datetime
import logging

Base = declarative_base()


class M_Model(Base):
    __tablename__ = 'magalu'
    #__table_args__ = {'schema': 'public'}  # Remove if not using schemas

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    url = Column(Text, nullable=False)
    ean = Column(BigInteger, nullable=False)  # Matches BIGINT in SQL
    date_now = Column(DateTime, server_default=func.now())  # Database handles default

class ML_Model(Base):
    __tablename__ = 'mercado_livre'
    #__table_args__ = {'schema': 'public'}  # Remove if not using schemas

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    url = Column(Text, nullable=False)
    ean = Column(BigInteger, nullable=False)  # Matches BIGINT in SQL
    date_now = Column(DateTime, server_default=func.now())  # Database handles default


class MagaluPipeline(object):
    """
    Modified version using SQLAlchemy ORM for PostgreSQL connection
    """

    # Update with your credentials
    DATABASE_URI = "postgresql://postgres:1728@localhost:5432/dular"

    def __init__(self):
        self.engine = create_engine(self.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)

    def open_spider(self, spider):
        """ Called when the spider is opened """
        self.session = self.Session()

    def close_spider(self, spider):
        """ Called when the spider is closed """
        if self.session:
            self.session.close()

    def process_item(self, item, spider):
        try:
            #item_date = datetime.strptime(item['date_now'], "%d-%m-%Y")
            record = M_Model(
                name=item['name'],
                price=float(item['price']),
                url=item['url'],
                ean=int(item['ean']),
                #date_now=item['date_now']
            )
            self.session.add(record)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error saving item: {str(e)}", exc_info=True)
            raise DropItem(f"Failed to insert item: {str(e)}")
        return item

class MLivrePipeline(object):
    """
    Modified version using SQLAlchemy ORM for PostgreSQL connection
    """

    # Update with your credentials
    DATABASE_URI = "postgresql://postgres:1728@localhost:5432/dular"

    def __init__(self):
        self.engine = create_engine(self.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)

    def open_spider(self, spider):
        """ Called when the spider is opened """
        self.session = self.Session()

    def close_spider(self, spider):
        """ Called when the spider is closed """
        if self.session:
            self.session.close()

    def process_item(self, item, spider):
        try:
            #item_date = datetime.strptime(item['date_now'], "%d-%m-%Y")
            record = ML_Model(
                name=item['name'],
                price=float(item['price']),
                url=item['url'],
                ean=int(item['ean']),
                #date_now=item['date_now']
            )
            self.session.add(record)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error saving item: {str(e)}", exc_info=True)
            raise DropItem(f"Failed to insert item: {str(e)}")
        return item


class MPipeline:
    def process_item(self, item, spider):
        return item
