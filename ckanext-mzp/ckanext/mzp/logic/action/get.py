import sqlalchemy

import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import validate
from ckan.logic import NotAuthorized

from ckanext.mzp.logic.schema import package_sources_list_schema
from ckanext.mzp.model import DatasetSourceModel
import logging
log = logging.getLogger(__name__)

_select = sqlalchemy.sql.select
_and_ = sqlalchemy.and_


def package_source_list(context, data_dict):
    '''List sources associated with a package.

    :param package_id: id or name of the package
    :type package_id: string

    :rtype: list of dictionaries
    '''
    if 'id' not in data_dict:
        data_dict['id'] = data_dict['package_id']

    toolkit.check_access('package_show', context, data_dict)

    # validate the incoming data_dict
    validated_data_dict, errors = validate(data_dict,
                                           package_sources_list_schema(),
                                           context)

    if errors:
        raise toolkit.ValidationError(errors)

    # get a list of showcase ids associated with the package id
    source_list = DatasetSourceModel.get_package_sources(
        validated_data_dict['package_id'])
    print('package sources')
    print(source_list)
    source_results = []
    for source_ in source_list:
        if source_.source_link.startswith('http'):
            source_results.append({'id': source_.id, 'title': source_.source_title, 'link': source_.source_link,
                                   'source_id': source_.id, 'is_external': True})
            continue

        try:
            source = toolkit.get_action('package_show')(
                context,
                {'name_or_id': source_.source_link}
            )
            source['source_id'] = source_.id
            source_results.append(source)
        except NotAuthorized:
            log.debug('Not authorized to access Package with ID: '
                      + str(source.source_link))
    return source_results


def package_reference_list(context, data_dict):
    '''List sources associated with a package.

    :param package_id: id or name of the package
    :type package_id: string

    :rtype: list of dictionaries
    '''

    if 'id' not in data_dict:
        data_dict['id'] = data_dict['package_id']

    toolkit.check_access('package_show', context, data_dict)

    # validate the incoming data_dict
    validated_data_dict, errors = validate(data_dict,
                                           package_sources_list_schema(),
                                           context)

    if errors:
        raise toolkit.ValidationError(errors)

    # get a list of showcase ids associated with the package id
    reference_list = DatasetSourceModel.get_package_references(
        validated_data_dict['package_id'])

    referencer_results = []
    for reference in reference_list:
        try:
            referencer = toolkit.get_action('package_show')(
                context,
                {'name_or_id': reference.package_id}
            )
            referencer_results.append(referencer)
        except NotAuthorized:
            log.debug('Not authorized to access Package with ID: '
                      + str(reference.package_id))
    return referencer_results

