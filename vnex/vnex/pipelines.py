# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    MetaData,
    Integer,
    Text,
    select
)
from scrapy.exceptions import DropItem

class VnexPipeline(object):
    pass
    """ def __init__(self):
        _engine = create_engine("sqlite:///data.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _vnex_items = Table("news", _metadata,
                             Column("id", Integer, primary_key=True),
                             Column("url", Text),
                             Column("title", Text),
                             Column("description",Text))
        _metadata.create_all(_engine)
        self.connection = _connection
        self.vnex_items = _vnex_items
    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            q = select([self.vnex_items]).where(self.vnex_items.c.title ==
                                                 item['title'])
            existence = list(self.connection.execute(q))
            if existence:
                raise DropItem("Item existed")
            else:
                ins_query = [self.vnex_items].insert().values(
                    url=item["url"],
                    title=item["title"],
                    description=item["discription"]
                )
                self.connection.execute(ins_query)
        return item
 """