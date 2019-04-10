from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import types

from ckan.model.domain_object import DomainObject
from ckan.model.meta import metadata, mapper, Session
from ckan import model

import logging
log = logging.getLogger(__name__)


dataset_source_table = None

def define_dataset_source_table():
    global dataset_source_table

    dataset_source_table = Table('mzp_dataset_source', metadata,
                                 Column('id', types.Integer, primary_key=True, nullable=False),
                                 Column('package_id', types.UnicodeText, ForeignKey('package.id',
                                                                                    ondelete='CASCADE',
                                                                                    onupdate='CASCADE')),
                                 Column('source_title', types.UnicodeText, nullable=False),
                                 Column('source_link', types.UnicodeText, nullable=False))
    mapper(DatasetSourceModel, dataset_source_table)


def setup():
    if dataset_source_table is None:
        define_dataset_source_table()

    if model.package_table.exists():
        if not dataset_source_table.exists():
            dataset_source_table.create()


class DatasetSourceModel(DomainObject):
    @classmethod
    def filter(cls, **kwargs):
        return Session.query(cls).filter_by(**kwargs)

    @classmethod
    def exists(cls, **kwargs):
        if cls.filter(**kwargs).first():
            return True
        else:
            return False

    @classmethod
    def get(cls, **kwargs):
        instance = cls.filter(**kwargs).first()
        return instance

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        Session.add(instance)
        Session.commit()
        return instance.as_dict()

    @classmethod
    def get_package_sources(cls, package_id):
        '''
        Return a list of sources associated with the passed package id.
        '''
        package_sources = cls.filter(package_id=package_id).all()
        return package_sources

    @classmethod
    def delete_package_source(cls, source_id):
        source_to_delete = cls.get(id=source_id)
        Session.delete(source_to_delete)
        Session.commit()

    @classmethod
    def get_package_references(cls, package_id):
        references = cls.filter(source_link=package_id).all()
        return references